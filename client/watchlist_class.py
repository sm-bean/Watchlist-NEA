import requests
import token_handling
import films_class
import random


class Watchlist:
    def __init__(self, watchlist_id, name, token):
        self.url = "http://127.0.0.1:5000/"
        self.name = name
        self.watchlist_id = watchlist_id
        self.token = token
        self.auth_header = {"Authorization": f"Bearer {token}"}
        self.films = []
        self.set_films()

    def get_films(self):
        id_info = {"watchlist_id": self.watchlist_id}

        response = requests.post(
            self.url + "getwatchlistfilms", json=id_info, headers=self.auth_header
        )

        if response.status_code == 401:
            token_handling.expire_token()

        return response.json()["films"]

    def set_films(self):
        db_films = self.get_films()
        films = []
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
        self.films = films

    def add_film(self, user, film):
        if user.get_watchlist_invites(self):
            return "user only invited to watchlist"

        id_info = {"watchlist_id": self.watchlist_id, "film_id": film.film_id}

        response = requests.post(
            self.url + "addwatchlistfilm", json=id_info, headers=self.auth_header
        )

        if response.status_code == 401:
            token_handling.expire_token()

        self.films.append(film)

        return response.json()["message"]

    def remove_film(self, user, film):
        if user.get_watchlist_invites(self):
            return "user only invited to watchlist"

        id_info = {"watchlist_id": self.watchlist_id, "film_id": film.film_id}

        response = requests.post(
            self.url + "removewatchlistfilm", json=id_info, headers=self.auth_header
        )

        if response.status_code == 401:
            token_handling.expire_token()

        for self_film in self.films:
            if self_film.film_id == film.film_id:
                self.films.remove(self_film)

        return response.json()["message"]

    def get_members(self):
        id_info = {"watchlist_id": self.watchlist_id}

        response = requests.post(
            self.url + "getwatchlistmembers", json=id_info, headers=self.auth_header
        )

        if response.status_code == 401:
            token_handling.expire_token()

        return response.json()["members"]

    def get_random_film(self):
        return random.choice(self.films)
