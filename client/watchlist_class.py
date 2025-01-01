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

        return response["films"]

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

    def add_film(self):
        pass

    def remove_film(self):
        pass

    def get_members(self):
        id_info = {"watchlist_id": self.watchlist_id}

        response = requests.post(
            self.url + "getwatchlistmembers", json=id_info, headers=self.auth_header
        )

        if response.status_code == 401:
            token_handling.expire_token()

        return response["members"]

    def get_random_film(self):
        return random.choice(self.films)

    def invite_user(self, user):
        pass
