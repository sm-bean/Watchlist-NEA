import users_class
import requests

# Quits session if token expires


def expired_token():
    print("token expired, restart program to log back in again")
    quit()


# Quits session if a server side error occurs


def server_side_error():
    print("A server side error occured, restart program to log back in again")
    quit()


# Sends login requests to server and returns client object if successful


def login(username, password):
    login_info = {"username": username, "password": password}

    response = requests.post("http://127.0.0.1:5000/" + "login", json=login_info)

    if response.status_code == 200:
        return users_class.ClientUser(username, response.json()["token"])
    return False


# Checks if username is already in DB


def check_username_available(username):
    username_info = {"username": username}
    response = requests.post(
        "http://127.0.0.1:5000/" + "checkusername", json=username_info
    )

    return response.json()["available"]


# Sends request to server to create account, returns client object if successful


def create_account(username, password):
    account_info = {"username": username, "password": password}

    response = requests.post(
        "http://127.0.0.1:5000/" + "createaccount", json=account_info
    )

    if response.status_code == 200:
        return users_class.ClientUser(username, response.json()["token"])
    return False
