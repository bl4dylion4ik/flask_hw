FROM python:3.9

WORKDIR /usr/flask-app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY my_app my_app
COPY sqlite_db .

CMD ["python", "./my_app/app.py"]
