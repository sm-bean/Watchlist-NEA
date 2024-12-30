import requests


class User:
    def __init__(self):
        return False

    def get_watchlists(self):
        pass

    def get_info(self):
        pass

    def get_recently_watched_films(self):
        pass

    def get_rating(self, film):
        pass

    def get_correlation_coefficient(self, friend):
        pass


class ClientUser(User):
    def __init__(self):
        self.token = ""
        self.url = "http://127.0.0.1:5000/"
        self.auth_header

    def log_film(self):
        pass

    def login(self, username, password):
        login_info = {"username": username, "password": password}

        response = requests.post(self.url + "login", json=login_info)

        if response.status_code == 200:
            self.set_auth(response.json().get("token"))
            return True
        return False

    def check_username_available(self, username):
        username_info = {"username": username}
        response = requests.post(self.url, json=username_info)

        return response.json()["available"]

    def add_friend(self, friend_username):
        users_info = {"username1": self.username, "username2": friend_username}

        username_info = {"username": friend_username}
        available_response = requests.post(
            self.url + "checkusername", json=username_info
        )

        if available_response.json()["available"]:
            return "user does not exist"

        friend_response = requests.post(
            self.url + "addfriend", json=users_info, headers=self.auth_header
        )

        if friend_response.status_code == 401:
            return friend_response.json()["message"]
        return "friend added"

    def accept_friend(self, friend_username):
        users_info = {"username1": self.username, "username2": friend_username}

        response = requests.post(
            self.url + "acceptfriend", json=users_info, headers=self.auth_header
        )

        if response.status_code == 401:
            return response.json()["message"]

        return "friend added"

    def set_info(self):
        pass

    def set_auth(self, token):
        self.token = token
        self.auth_header = {"Authorization": f"Bearer {token}"}
