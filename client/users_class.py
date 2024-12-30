import requests
import token_handling
import datetime
import films_class


class User:
    def __init__(self, username, token):
        self.url = "http://127.0.0.1:5000/"
        self.username = username
        self.films = self.get_films(token)

    def get_watchlists(self):
        pass

    def get_films(self, token):
        username_info = {"username": self.username}
        auth_header = {"Authorization": f"Bearer {token}"}

        response = requests.post(
            self.url + "getfilms", json=username_info, headers=auth_header
        )

        if response.status_code == 401:
            token_handling.expired_token()

        return response

    def set_films(self, token):
        db_films = self.get_films(token)
        films = []
        for db_film in db_films:
            films.append(films_class.Film(db_film[0], db_film[1], db_film[2]))

    def get_common_films(self, friend, token):
        self_films_list = []
        for film in self.films:
            self_films_list.append(film[0])

        friend_films_list = []
        for film in friend.films:
            friend_films_list.append(film[0])

        common_ids = list(set(self_films_list).intersection(friend_films_list))

        common_films = []
        for id in common_ids:
            for film in self.films:
                if id == film[0]:
                    common_films.append(film)

        return common_films

    def get_info(self):
        pass

    def get_recently_watched_films(self):
        # POTENTIAL REFERENCING ERROR HERE!!!!!!!
        films_dupe = self.films[:]
        # right there ^
        recents = []
        for i in range(5):
            most_recent_film = (None, None, datetime.date(0, 0, 0))
            for film in films_dupe:
                if film[2] > most_recent_film[2]:
                    most_recent_film = film

            recents.append(film)
            films_dupe.remove(film)

        return recents

    def get_correlation_coefficient(self, friend):
        pass


class ClientUser(User):
    def __init__(self):
        self.token = ""
        self.url = "http://127.0.0.1:5000/"
        self.auth_header

    def log_film(self, film, rating):
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
            token_handling.expired_token()
            return friend_response.json()["message"]
        if friend_response.status_code == 400:
            return friend_response.json()["message"]
        return "friend added"

    def accept_friend(self, friend_username):
        users_info = {"username1": self.username, "username2": friend_username}

        response = requests.post(
            self.url + "acceptfriend", json=users_info, headers=self.auth_header
        )

        if response.status_code == 401:
            token_handling.expired_token()
            return response.json()["message"]
        if response.status_code == 400:
            return response.json()["message"]

        return "friend added"

    def set_info(self):
        pass

    def set_auth(self, token):
        self.token = token
        self.auth_header = {"Authorization": f"Bearer {token}"}
