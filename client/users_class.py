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
        self.friend_requests = []
        self.avg_rating = 0
        self.neighbours = []
        self.neighbours_correlation_coefficients = []
        self.set_films()
        self.set_avg_rating()

    # Gets films seen by the user in their db format

    def get_films(self):
        username_info = {"username": self.username}

        response = requests.post(
            self.url + "getfilms", json=username_info, headers=self.auth_header
        )

        if response.status_code == 401:
            token_handling.expired_token()
        if response.status_code == 500:
            token_handling.server_side_error()

        return response.json()["films"]

    # Puts films into object format and stores in user object

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
            ratings_dates.append(
                [
                    db_film[6],
                    datetime.datetime.strptime(db_film[7], "%a, %d %b %Y %H:%M:%S %Z"),
                ]
            )
        self.films = films
        self.ratings_dates = ratings_dates

    # Gets common films between users by getting lists of ids of films seen by each user and finding their intersection

    def get_common_films(self, friend):
        self_films_list = []
        for film in self.films:
            self_films_list.append(film.film_id)

        friend_films_list = []
        for film in friend.films:
            friend_films_list.append(film.film_id)

        common_ids = list(set(self_films_list).intersection(friend_films_list))

        common_films = []
        for id in common_ids:
            for film in self.films:
                if id == film.film_id:
                    common_films.append(film)

        return common_films

    # Conducts a linear search for the most recent film 5 times

    def get_recently_watched_films(self):
        films_dupe = self.films[:]

        iterations = 5

        if len(films_dupe) < iterations:
            if len(films_dupe) == 0:
                return []
            iterations = len(films_dupe)

        recents = []
        for i in range(iterations):
            most_recent_date = datetime.datetime(1800, 1, 1)
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

    # Gets watchlists the user is in in db format

    def get_watchlists_in(self):
        username_info = {"username": self.username}

        response = requests.post(
            self.url + "getwatchlistsin", json=username_info, headers=self.auth_header
        )

        if response.status_code == 401:
            token_handling.expired_token()
        if response.status_code == 500:
            token_handling.server_side_error()

        return response.json()["watchlists"]

    # Creates objects for watchlists user in and stores them locally in the user

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

    # Gets friends of the user in their db format

    def get_friends(self):
        username_info = {"username": self.username}

        response = requests.post(
            self.url + "getfriends", json=username_info, headers=self.auth_header
        )

        if response.status_code == 401:
            token_handling.expired_token()
        if response.status_code == 500:
            token_handling.server_side_error()

        return response.json()["friendships"]

    # Creates objects for users friends and stores them locally

    def set_friends(self):
        db_friends = self.get_friends()
        friends = []
        friend_statuses = []
        if db_friends is None:
            self.friends = []
            self.friend_statuses = []
        else:
            for db_friend in db_friends:
                friends.append(User(db_friend[0], self.token))
                friend_statuses.append([db_friend[1], db_friend[2]])

            self.friends = friends
            self.friend_statuses = friend_statuses

    # Gets usernames of users who have sent friend requests to the client user, used separately to get_friends as get_friends does not say who sent the request

    def get_friend_requests(self):
        username_info = {"username": self.username}

        response = requests.post(
            self.url + "getfriendrequests", json=username_info, headers=self.auth_header
        )

        if response.status_code == 401:
            token_handling.expired_token()
        if response.status_code == 500:
            token_handling.server_side_error()

        return response.json()["friend requests"]

    # Sets usernames of friend requests in user object from db format

    def set_friend_requests(self):
        db_friend_requests = self.get_friend_requests()

        if db_friend_requests is None:
            self.friend_requests = []
        else:
            friend_requests = []

            for db_friend_request in db_friend_requests:
                friend_requests.append(db_friend_request[0])

            self.friend_requests = friend_requests

    # Calculates average rating of users logs and stores it

    def set_avg_rating(self):
        if len(self.ratings_dates) == 0:
            self.avg_rating = 0
        else:
            ratings_sum = 0
            for rating in self.ratings_dates:
                ratings_sum += rating[0]

            self.avg_rating = ratings_sum / len(self.ratings_dates)


# Object used for the client user which inherits from the general user

class ClientUser(User):
    def __init__(self, username, token):
        User.__init__(self, username, token)
        self.set_friends()
        self.set_friend_requests()
        self.set_watchlists_in()
        self.set_neighbours(10, 0)

    # Sends a request to the server to log the film in the db and stores the log locally if successful

    def log_film(self, film, rating):
        rating_info = {
            "username": self.username,
            "film_id": film.film_id,
            "rating": rating,
        }

        response = requests.post(
            self.url + "logfilm", json=rating_info, headers=self.auth_header
        )

        if response.status_code == 401:
            token_handling.expired_token()
        if response.status_code == 400:
            return response.json()["message"]

        self.films.append(film)
        self.ratings_dates.append(
            [rating, datetime.datetime.now(datetime.timezone.utc)]
        )

        for friend in self.friends:
            self.update_correlation_coefficient(
                friend, recommendation.correlation_coefficient(self, friend)
            )

        return "film logged"

    # Searches for all films with the title specified and creates objects for ones returned

    def search_film(self, film_title):
        film_info = {"film_title": film_title}

        response = requests.post(
            self.url + "searchfilm", json=film_info, headers=self.auth_header
        )

        if response.status_code == 401:
            token_handling.expired_token()
        if response.status_code == 500:
            token_handling.server_side_error()

        films = response.json()["films"]

        if films == []:
            return "not found"

        films_objects = []
        for film in films:
            films_objects.append(
                films_class.Film(film[0], film[1], film[2], film[3], film[4], film[5])
            )
        return films_objects

    def add_friend(self, friend):
        if token_handling.check_username_available(friend.username):
            return "user does not exist"

        cc = recommendation.correlation_coefficient(self, friend)

        users_info = {
            "username": self.username,
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
        if friend_response.status_code == 500:
            token_handling.server_side_error()

        self.friends.append(friend)
        self.friend_statuses.append(["Request", cc])
        return "friend added"

    def accept_friend(self, friend):
        users_info = {
            "username": self.username,
            "friend_username": friend.username,
        }

        response = requests.post(
            self.url + "acceptfriend", json=users_info, headers=self.auth_header
        )

        if response.status_code == 401:
            token_handling.expired_token()
            return response.json()["message"]
        if response.status_code == 400:
            return response.json()["message"]
        if response.status_code == 500:
            token_handling.server_side_error()

        index = None
        for i in range(len(self.friends)):
            if self.friends[i].username == friend.username:
                index = i

        self.friend_statuses[index][0] = "Accepted"
        self.friend_requests.remove(friend.username)

        return "friend added"

    def update_correlation_coefficient(self, friend, corr_coeff):
        users_info = {
            "username": self.username,
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
        if response.status_code == 500:
            token_handling.server_side_error()

        return response.json()["message"]

    def create_watchlist(self, watchlist_name):
        watchlist_info = {"username": self.username, "watchlist name": watchlist_name}

        response = requests.post(
            self.url + "createwatchlist", json=watchlist_info, headers=self.auth_header
        )

        if response.status_code == 401:
            token_handling.expired_token()
        if response.status_code == 500:
            token_handling.server_side_error()

        watchlist_id = response.json()["watchlist_id"]

        self.watchlists.append(
            watchlist_class.Watchlist(watchlist_id, watchlist_name, self.token)
        )
        self.watchlist_invites.append(False)

        return watchlist_class.Watchlist(watchlist_id, watchlist_name, self.token)

    def join_watchlist(self, watchlist):
        watchlist_info = {
            "username": self.username,
            "watchlist_id": watchlist.watchlist_id,
        }

        response = requests.post(
            self.url + "joinwatchlist", json=watchlist_info, headers=self.auth_header
        )

        if response.status_code == 401:
            token_handling.expired_token()
        if response.status_code == 500:
            token_handling.server_side_error()

        for i in range(len(self.watchlists)):
            if self.watchlists[i].watchlist_id == watchlist.watchlist_id:
                self.watchlist_invites[i] = False

        return response.json()["message"]

    def invite_user_to_watchlist(self, invited_user, watchlist):
        watchlist_info = {
            "watchlist_id": watchlist.watchlist_id,
            "invited_username": invited_user,
        }

        response = requests.post(
            self.url + "watchlistinvite", json=watchlist_info, headers=self.auth_header
        )

        if response.status_code == 401:
            token_handling.expired_token()

        return response.json()["message"]

    def get_neighbours(self, max_neighbours, threshold):
        neighbours_correlation_coefficients = []
        neighbours = []

        queue = []
        visited = []

        queue.append(self)
        visited.append(self)

        while queue != [] and len(neighbours) < max_neighbours:
            current_user = queue[0]
            queue = queue[1:]

            current_user.set_friends()
            for user in current_user.friends:
                in_visited = False
                for visited_user in visited:
                    if visited_user.username == user.username:
                        in_visited = True

                if in_visited == False and len(neighbours) < max_neighbours:
                    queue.append(user)
                    visited.append(user)
                    correlation_coefficient = recommendation.correlation_coefficient(
                        self, user
                    )
                    if correlation_coefficient >= threshold:
                        neighbours.append(user)
                        neighbours_correlation_coefficients.append(
                            correlation_coefficient
                        )

        return neighbours, neighbours_correlation_coefficients

    def set_neighbours(self, num_neighbours, threshold):
        neighbours, neighbours_correlation_coefficients = self.get_neighbours(
            num_neighbours, threshold
        )

        self.neighbours = neighbours
        self.neighbours_correlation_coefficients = neighbours_correlation_coefficients
