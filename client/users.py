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
        self.url = "http://127.0.0.1:5000/login"

    def log_film(self):
        pass

    def login(self, username, password):
        login_info = {"username": username, "password": password}

        response = requests.post(self.url, json=login_info)

        if response.status_code == 200:
            self.token = response.json().get("token")
            return True
        return False

    def check_username_available(self, username):
        username_payload = {"username": username}
        response = requests.post(self.url, json=username_payload)

        return response.json().get("available")

    def add_friend(self):
        pass

    def accept_friend(self):
        pass

    def set_info(self):
        pass