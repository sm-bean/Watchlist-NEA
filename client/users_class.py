import requests
import token_handling
import datetime
import films_class
import watchlist_class
import recommendation
from math import sqrt


class User:
    def __init__(self, username, token):
        self.url = "http://127.0.0.1:5000/"
        self.token = token
        self.auth_header = {"Authorization": f"Bearer {token}"}
        self.username = username
        self.films = []
        self.ratings_dates = []
        self.watchlists = []
        self.watchlist_invites = []
        self.friends = []
        self.friend_statuses = []
        self.avg_rating = 0
        self.neighbours = []
        self.neighbours_correlation_coefficients = []
        self.set_films()
        self.set_avg_rating()

    def get_films(self):
        response = requests.get(self.url + "getfilms", headers=self.auth_header)

        if response.status_code == 401:
            token_handling.expired_token()

        return response.json()["films"]

    def set_films(self):
        db_films = self.get_films()
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
            ratings_dates.append([db_film[6], db_film[7]])
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

    def get_recently_watched_films(self):
        films_dupe = self.films[:]

        iterations = 5

        if len(films_dupe) < iterations:
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
        index = None
        for i in range(len(self.friends)):
            if self.friends[i].username == friend.username:
                index = i

        if index is None:
            return "not friends"

        return self.friend_statuses[index][1]

    def get_friendship_status(self, friend):
        index = None
        for i in range(len(self.friends)):
            if self.friends[i].username == friend.username:
                index = i

        if index is None:
            return "not friends"

        return self.friend_statuses[index][0]

    def get_watchlist_invites(self, watchlist):
        index = None
        for i in range(len(self.watchlists)):
            if self.watchlists[i].watchlist_id == watchlist.watchlist_id:
                index = i

        if index is None:
            return "not in watchlist"

        return self.watchlist_invites[index]

    def get_rating(self, film):
        index = None
        for i in range(len(self.films)):
            if self.films[i].film_id == film.film_id:
                index = i

        if index is None:
            return "not seen"

        return self.ratings_dates[index][0]

    def get_date(self, film):
        index = None
        for i in range(len(self.films)):
            if self.films[i].film_id == film.film_id:
                index = i

        if index is None:
            return "not seen"

        return self.ratings_dates[index][1]

    def get_watchlists_in(self):
        response = requests.get(self.url + "getwatchlistsin", headers=self.auth_header)

        if response.status_code == 401:
            token_handling.expired_token()

        return response.json()["watchlists"]

    def set_watchlists_in(self):
        db_watchlists = self.get_watchlists_in()
        watchlists = []
        watchlist_invites = []
        for db_watchlist in db_watchlists:
            watchlists.append(
                watchlist_class.Watchlist(db_watchlist[0], db_watchlist[1], self.token)
            )
            if db_watchlist[2] == "True":
                watchlist_invites.append(True)
            else:
                watchlist_invites.append(False)

        self.watchlists = watchlists
        self.watchlist_invites = watchlist_invites

    def get_friends(self):
        response = requests.get(self.url + "getfriends", headers=self.auth_header)

        if response.status_code == 401:
            token_handling.expired_token()

        return response.json()["friendships"]

    def set_friends(self):
        db_friends = self.get_friends()
        friends = []
        friend_statuses = []
        for db_friend in db_friends:
            friends.append(User(db_friend[0], self.token))
            friend_statuses.append([db_friend[1], db_friend[2]])

    def set_avg_rating(self):
        pass  # DO THIS


class ClientUser(User):
    def __init__(self, username, token):
        User.__init__(self, username, token)
        self.set_friends()
        self.set_watchlists_in()
        self.set_neighbours()

    def log_film(self, film, rating):
        rating_info = {"film_id": film.film_id, "rating": rating}

        response = requests.post(
            self.url + "logfilm", json=rating_info, headers=self.auth_header
        )

        if response.status_code == 401:
            token_handling.expired_token()
        if response.status_code == 400:
            return response.json()["message"]

        self.films.append(film)
        self.ratings_dates.append(rating, datetime.date.today())

        return "film logged"

    def add_friend(self, friend):
        if token_handling.check_username_available(friend.username):
            return "user does not exist"

        cc = recommendation.correlation_coefficient(self, friend)

        users_info = {
            "friend_username": friend.username,
            "correlation coefficient": cc,
        }

        friend_response = requests.post(
            self.url + "addfriend", json=users_info, headers=self.auth_header
        )

        if friend_response.status_code == 401:
            token_handling.expired_token()
            return friend_response.json()["message"]
        if friend_response.status_code == 400:
            return friend_response.json()["message"]

        self.friends.append(friend)
        self.friend_statuses.append(["Request", cc])
        return "friend added"

    def accept_friend(self, friend):
        users_info = {"friend_username": friend.username}

        response = requests.post(
            self.url + "acceptfriend", json=users_info, headers=self.auth_header
        )

        if response.status_code == 401:
            token_handling.expired_token()
            return response.json()["message"]
        if response.status_code == 400:
            return response.json()["message"]

        # UPDATE FRIENDSHIP STATUS IN THE OBJECT HERE
        index = None
        for i in range(len(self.friends)):
            if self.friends[i].username == friend.username:
                index = i

        self.friend_statuses[index][0] = "Accepted"

        return "friend added"

    def update_correlation_coefficient(self, friend, corr_coeff):
        users_info = {
            "friend_username": friend.username,
            "correlation_coefficient": corr_coeff,
        }

        response = requests.post(
            self.url + "updatecorrelationcoefficient",
            json=users_info,
            headers=self.auth_header,
        )

        if response.status_code == 401:
            token_handling.expired_token()

        return response.json()["message"]

    # UPDATE WATCHLIST LIST IN OBJECT AFTER CREATING
    def create_watchlist(self, watchlist_name):
        watchlist_info = {"watchlist name": watchlist_name}

        response = requests.post(
            self.url + "createwatchlist", json=watchlist_info, headers=self.auth_header
        )

        if response.status_code == 401:
            token_handling.expired_token()

        watchlist_id = response.json()["watchlist_id"]

        return watchlist_class.Watchlist(watchlist_id, watchlist_name, self.token)

    def join_watchlist(self, watchlist):
        watchlist_info = {"watchlist_id": watchlist.watchlist_id}

        response = requests.post(
            self.url + "joinwatchlist", json=watchlist_info, headers=self.auth_header
        )

        if response.status_code == 401:
            token_handling.expired_token()

        return response.json()["message"]

    def invite_user_to_watchlist(self, invited_user, watchlist):
        if self.get_watchlist_invites(watchlist):
            return "you are only invited to the watchlist"

        watchlist_info = {
            "watchlist_id": watchlist.watchlist_id,
            "invited_username": invited_user.username,
        }

        response = requests.post(
            self.url + "watchlistinvite", json=watchlist_info, headers=self.auth_header
        )

        if response.status_code == 401:
            token_handling.expired_token()

        return response.json()["message"]

    def get_neighbours(self, num_neighbours, threshold):
        friend_correlation_coefficients = []
        neighbours_correlation_coefficients = []

        for status in self.friend_statuses:
            friend_correlation_coefficients.append(status[1])

        neighbours = []
        for i in range(len(self.friends)):
            if friend_correlation_coefficients[i] >= threshold:
                neighbours.append(self.friends[i])
                neighbours_correlation_coefficients.append(
                    friend_correlation_coefficients[i]
                )
                if len(neighbours) >= num_neighbours:
                    return neighbours

        temp_friends = self.friends[:]

        while len(neighbours) < num_neighbours:
            max_friend_index = friend_correlation_coefficients.index(
                max(friend_correlation_coefficients)
            )
            max_friend = temp_friends[max_friend_index]
            del temp_friends[max_friend_index]
            del friend_correlation_coefficients[max_friend_index]

            max_friend.set_friends()

            for friend in max_friend.friends:
                correlation_coefficient = recommendation.correlation_coefficient(
                    self, friend
                )
                if correlation_coefficient >= threshold:
                    neighbours.append(friend)
                    neighbours_correlation_coefficients.append(correlation_coefficient)
                    if len(neighbours) >= num_neighbours:
                        return neighbours

        return neighbours, neighbours_correlation_coefficients

    def set_neighbours(self, num_neighbours, threshold):
        neighbours, neighbours_correlation_coefficients = self.get_neighbours(
            num_neighbours, threshold
        )

        self.neighbours = neighbours
        self.neighbours_correlation_coefficients = neighbours_correlation_coefficients
