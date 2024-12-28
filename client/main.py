import requests

url = "http://127.0.0.1:5000/login"
login_info = {"username": "username", "password": "password"}
response = requests.post(url, json=login_info)

print(response.json()["token"])
