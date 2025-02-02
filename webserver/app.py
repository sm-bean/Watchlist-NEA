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

            username = jwt.decode(token, jwt_secret, algorithm)["user"]

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "token expired"}), 401
        except jwt.InvalidSignatureError:
            return jsonify({"message": "token invalid"}), 401

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
def add_friend():
    if friends.request_friend(request.json):
        return jsonify({"message": "friend added"})
    return jsonify({"message": "already friends/requested"}), 400


@app.route("/acceptfriend", methods=["POST"])
@check_jwt
def accept_friend():
    result = friends.accept_friendship(
        request.json["username"], request.json["friend_username"]
    )
    if result == "friend added":
        return jsonify({"message": result})
    return jsonify({"message": result}), 400


@app.route("/getfilms", methods=["POST"])
@check_jwt
def get_films():
    result = films.get_films_watched(request.json["username"])
    return jsonify({"films": result})


@app.route("/getwatchlistfilms", methods=["POST"])
@check_jwt
def get_watchlist_films():
    data = request.json
    result = watchlists.get_films_in_watchlist(data["watchlist_id"])
    return jsonify({"films": result})


@app.route("/logfilm", methods=["POST"])
@check_jwt
def log_film():
    if films.log_film_watched(request.json):
        return jsonify({"message": "film logged"})
    return jsonify({"message": "already logged"}), 400


@app.route("/getwatchlistsin", methods=["POST"])
@check_jwt
def get_watchlists_in():
    result = watchlists.get_watchlists_user_in(request.json["username"])
    return jsonify({"watchlists": result})


@app.route("/getfriends", methods=["POST"])
@check_jwt
def get_friends():
    result = friends.get_friendships(request.json["username"])
    return jsonify({"friendships": result})


@app.route("/getfriendrequests", methods=["POST"])
@check_jwt
def get_friend_requests():
    result = friends.get_friendship_requests(request.json["username"])
    return jsonify({"friend requests": result})


@app.route("/getwatchlistmembers", methods=["POST"])
@check_jwt
def get_watchlist_members():
    data = request.json
    result = watchlists.get_members(data["watchlist_id"])
    return jsonify({"members": result})


@app.route("/addwatchlistfilm", methods=["POST"])
@check_jwt
def add_watchlist_film():
    data = request.json
    result = watchlists.add_film(data["watchlist_id"], data["film_id"])
    if result:
        return jsonify({"message": "film added"})
    return jsonify({"message": "already in watchlist"}), 400


@app.route("/addwatchlistfilm", methods=["POST"])
@check_jwt
def remove_watchlist_film():
    data = request.json
    result = watchlists.remove_film(data["watchlist_id"], data["film_id"])
    if result:
        return jsonify({"message": "film removed"})
    return jsonify({"message": "film not in watchlist"}), 400


@app.route("/updatecorrelationcoefficient", methods=["POST"])
@check_jwt
def update_correlation_coefficient():
    result = friends.update_coefficient(request.json)
    if result:
        return jsonify({"message": "coefficient updated"})
    return jsonify({"message": "not friends"}), 400


@app.route("/joinwatchlist", methods=["POST"])
@check_jwt
def join_watchlist():
    result = watchlists.add_user(request.json["username"], request.json["watchlist_id"])
    if result == "watchlist joined":
        return jsonify({"message": result})
    return jsonify({"message": result}), 400


@app.route("/watchlistinvite", methods=["POST"])
@check_jwt
def watchlist_invite():
    data = request.json
    result = watchlists.invite_user(data)
    if result == "user invited":
        return jsonify({"message": result})
    return jsonify({"message": result}), 400


@app.route("/createwatchlist", methods=["POST"])
@check_jwt
def create_watchlist():
    result = watchlists.create_list(
        request.json["username"], request.json["watchlist name"]
    )
    return jsonify({"watchlist_id": result})


@app.route("/searchfilm", methods=["POST"])
@check_jwt
def search_film():
    data = request.json
    result = films.find_film(data["film_title"])
    return jsonify({"films": result})


if __name__ == "__main__":
    app.run(debug=True)
