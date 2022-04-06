### K8s:
``` shell
$ kubectl apply -f google-secret
$ kubectl apply -f deployment.yaml
$ kubectl port-forward flask-server-deployment-6d7684784-5fdrp 5000:5000
```
![image](https://user-images.githubusercontent.com/85695187/161314909-05e87361-3a4d-4870-9856-8e69964ffb69.png)
### Docker launch:
``` shell
$ docker build -t python-flask .

$ docker run -p 5000:5000 python-flask
```
### Login page:
![photo_2022-03-18_21-00-11](https://user-images.githubusercontent.com/85695187/159058746-fab11be1-ce83-4665-8eab-7fd04793e950.jpg)
### Starting page:
![photo_2022-03-18_21-00-13](https://user-images.githubusercontent.com/85695187/159058751-4f57201c-c174-489b-b5d4-4d6f18ce8028.jpg)
### About page:
![photo_2022-03-18_21-00-15](https://user-images.githubusercontent.com/85695187/159058754-6ccc5592-4e88-4e30-b874-cf210918bd44.jpg)
### User-Agent page:
![photo_2022-03-18_21-00-16](https://user-images.githubusercontent.com/85695187/159058755-0b8ee955-06e2-46ef-8e83-a0fda30bfa0c.jpg)
### Weather page:
![photo_2022-03-18_21-00-18](https://user-images.githubusercontent.com/85695187/159058757-4af1724d-2a8a-434f-a3f3-cd18d706e703.jpg)
- Weather for a week:
![photo_2022-03-18_21-00-20](https://user-images.githubusercontent.com/85695187/159058758-35d81ca0-6c8c-4480-9b86-a9a2f81b583d.jpg)
![photo_2022-03-18_21-00-22](https://user-images.githubusercontent.com/85695187/159058764-41838b8a-cda4-462f-8c11-12e9a22d3fcd.jpg)
- Weather for a specific day:
![photo_2022-03-18_21-00-24](https://user-images.githubusercontent.com/85695187/159058765-4e315392-39a9-4d95-97f6-c35332f76716.jpg)
![photo_2022-03-18_21-00-27](https://user-images.githubusercontent.com/85695187/159058767-96308a2b-aaf8-42ba-8a75-e5d890283b24.jpg)
