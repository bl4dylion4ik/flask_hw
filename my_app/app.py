import json
import os
import sqlite3

from flask import Flask, redirect, request, url_for, render_template
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from oauthlib.oauth2 import WebApplicationClient
import requests

from db import init_db_command
from user import User
from weather import get_gp, get_weather_date, get_list_weather
from useragent import parse_useragent
from dotenv import load_dotenv

load_dotenv('my_app/setup_env.sh')

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

try:
    init_db_command()
except sqlite3.OperationalError:
    pass  # Assume it's already been created

client = WebApplicationClient(GOOGLE_CLIENT_ID)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("homepage_login.html")
    else:
        return render_template("homepage_logout.html")


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    login_user(user)

    return redirect(url_for("index"))


@app.route("/useragent")
def user_agent():
    header = dict(request.headers)
    parse_user = parse_useragent(header.get("User-Agent"))
    return render_template("useragent.html", os=parse_user[0], browser=parse_user[1])


@app.route("/weather")
def weather():
    return render_template("weather.html")


@app.route("/weather_day")
def weather_day():
    return render_template("form_weather_day.html")


@app.route("/weather_week")
def weather_week():
    return render_template("form_weather_week.html")


@app.route("/form_spec_day", methods=["POST"])
def form_spec_day():
    city = request.form.get("city").lower()
    date = request.form.get("date")
    return redirect(url_for("current_weather", city=city, date=date))


@app.route("/form_week", methods=["POST"])
def form_week():
    city = request.form.get("city").lower()
    return redirect(url_for("weather_list", city=city))


@app.route("/list/<string:city>")
def weather_list(city):
    weather = get_list_weather(get_gp(city)[0], get_gp(city)[1])
    return render_template("answer_weather_week.html", weather=weather)


@app.route("/<string:city>/<string:date>")
def current_weather(city, date):
    weather = get_weather_date(get_gp(city)[0], get_gp(city)[1], date)
    return render_template("answer_weather_day.html", date=date, weather=weather)


@app.route("/about")
def about():
    return render_template("about.html", name=current_user.name, email=current_user.email)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(ssl_context='adhoc', host="0.0.0.0", port=5000)
