from flask import Flask, request, jsonify
import login
import friends
import films
import watchlists
import inspect
from functools import wraps
import jwt
import dotenv
import os

app = Flask(__name__)


def check_jwt(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        token = ""

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        else:
            return jsonify({"message": "missing token"}), 401

        try:
            dotenv.load_dotenv()
            jwt_secret = os.getenv("jwt_secret")
            algorithm = os.getenv("algorithm")

            username = jwt.decode(token, jwt_secret, algorithm)["username"]

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "token expired"}), 401
        except jwt.InvalidSignatureError:
            return jsonify({"message": "token invalid"}), 401

        if "username" in inspect.getfullargspec(func).args:
            kwargs["username"] = username

        return func(*args, **kwargs)

    return decorated_func


@app.route("/login", methods=["POST"])
def login_server():
    data = request.json
    result = login.login(data)
    if result != "":
        return jsonify({"token": result})
    return jsonify({"message": "Incorrect details"}), 401


@app.route("/checkusername", methods=["POST"])
def check_username():
    data = request.json
    username = data["username"]
    if login.check_username_availability(username):
        return jsonify({"available": True})
    return jsonify({"available": False})


@app.route("/createaccount", methods=["POST"])
def create_account_server():
    data = request.json
    token = login.create_account(data)
    return jsonify({"token": token})


@app.route("/addfriend", methods=["POST"])
@check_jwt
def add_friend(username):
    if friends.request_friend(username, request.json):
        return jsonify({"message": "friend added"})
    return jsonify({"message": "already friends/requested"}), 400


@app.route("/acceptfriend", methods=["POST"])
@check_jwt
def accept_friend(username):
    result = friends.accept_friendship(username, request.json["friend_username"])
    if result == "friend added":
        return jsonify({"message": result})
    return jsonify({"message": result}), 400


@app.route("/getfilms", methods=["GET"])
@check_jwt
def get_films(username):
    result = films.get_films_watched(username)
    return jsonify({"films": result})


@app.route("/getwatchlistfilms", methods=["POST"])
@check_jwt
def get_watchlist_films():
    data = request.json
    result = watchlists.get_films_in_watchlist(data["watchlist_id"])
    return jsonify({"films": result})


@app.route("/logfilm", methods=["POST"])
@check_jwt
def log_film(username):
    if films.log_film_watched(username, request.json):
        return jsonify({"message": "film logged"})
    return jsonify({"message": "already logged"}), 400


@app.route("/getwatchlistsin", methods=["GET"])
@check_jwt
def get_watchlists_in(username):
    result = watchlists.get_watchlists_user_in(username)
    return jsonify({"watchlists": result})


@app.route("/getfriends", methods=["GET"])
@check_jwt
def get_friends(username):
    result = friends.get_friendships(username)
    return jsonify({"friendships": result})


@app.route("/getwatchlistmembers", methods=["POST"])
@check_jwt
def get_watchlist_members():
    data = request.json
    result = watchlists.get_members(data["watchlist_id"])
    return jsonify({"members": result})


if __name__ == "__main__":
    app.run(debug=True)
