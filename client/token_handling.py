import users_class
import requests


def expired_token():
    print("token expired, restart program to log back in again")
    quit()


def login(username, password):
    login_info = {"username": username, "password": password}

    response = requests.post("http://127.0.0.1:5000/" + "login", json=login_info)

    if response.status_code == 200:
        return users_class.ClientUser(username, response.json()["token"])
    return False


def check_username_available(username):
    username_info = {"username": username}
    response = requests.post("http://127.0.0.1:5000/", json=username_info)

    return response.json()["available"]

def create_account(username, password):
    account_info = {"username": username, "password": password}

    response = requests.post("http://127.0.0.1:5000/" + "createaccount", json=username_info)

    if response.status_code == 200:
        return users_class.ClientUser(username, response.json()["token"])
    return False