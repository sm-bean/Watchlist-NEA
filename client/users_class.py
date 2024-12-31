import requests
import token_handling
import datetime
import films_class
import recommendation
from math import sqrt


class User:
    def __init__(self, username, token):
        self.url = "http://127.0.0.1:5000/"
        self.username = username
        self.films = []
        self.ratings_dates = []
        self.set_films(token)

    def get_watchlists(self):
        pass

    def check_username_available(self, username):
        username_info = {"username": username}
        response = requests.post(self.url, json=username_info)

        return response.json()["available"]

    def get_films(self, token):
        auth_header = {"Authorization": f"Bearer {token}"}

        response = requests.post(self.url + "getfilms", headers=auth_header)

        if response.status_code == 401:
            token_handling.expired_token()

        return response

    def set_films(self, token):
        db_films = self.get_films(token)
        films = []
        ratings_dates = []
        for db_film in db_films:
            films.append(
                films_class.Film(
                    db_film[0],
                    db_film[1],
                    db_film[2],
                    db_film[3],
                    db_film[4],
                    db_film[5],
                )
            )
            ratings_dates.append(db_film[6], db_film[7])
        self.films = films
        self.ratings_dates = ratings_dates

    def get_common_films(self, friend):
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
        films_dupe = self.films[:]

        iterations = 5

        if len(films_dupe) < 5:
            if len(films_dupe) == 0:
                return []
            iterations = len(films_dupe)

        recents = []
        for i in range(iterations):
            most_recent_date = datetime.date(0, 0, 0)
            most_recent_film = None
            for film in films_dupe:
                if self.get_date(film) > most_recent_date:
                    most_recent_date = self.get_date(film)
                    most_recent_film = film

            recents.append(most_recent_film)
            films_dupe.remove(most_recent_film)

        return recents

    def get_correlation_coefficient(self, friend):
        pass

    def get_rating(self, film):
        index = None
        for i in range(len(self.films)):
            if self.films[i][0] == film.film_id:
                index = i

        if index is None:
            return "not seen"

        return self.ratings_dates[index][0]

    def get_date(self, film):
        index = None
        for i in range(len(self.films)):
            if self.films[i][0] == film.film_id:
                index = i

        if index is None:
            return "not seen"

        return self.ratings_dates[index][1]


class ClientUser(User):
    def __init__(self):
        self.token = ""
        self.url = "http://127.0.0.1:5000/"
        self.auth_header

    def log_film(self, film, rating):
        rating_info = {"film_id": film.film_id, "rating": rating}

        response = requests.post(
            self.url + "logfilm", json=rating_info, headers=self.auth_header
        )

        if response.status_code == 401:
            token_handling.expired_token()

    def login(self, username, password):
        login_info = {"username": username, "password": password}

        response = requests.post(self.url + "login", json=login_info)

        if response.status_code == 200:
            self.set_auth(response.json().get("token"))
            self.username = username
            return True
        return False

    # CHECK THAT USER EXISTS BEFORE CREATING FRIEND OBJECT CLIENT SIDE
    def add_friend(self, friend):
        username_info = {"username": friend.username}
        available_response = requests.post(
            self.url + "checkusername", json=username_info
        )

        if available_response.json()["available"]:
            return "user does not exist"

        users_info = {
            "friend_username": friend.username,
            "correlation coefficient": recommendation.correlation_coefficient(
                self, friend
            ),
        }

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
        users_info = {"friend_username": friend_username}

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
