import requests

url = "http://127.0.0.1:5000/checkusername"
username_payload = {"username": "username"}
response = requests.post(url, json=username_payload)

print(response.json().get("available"))
