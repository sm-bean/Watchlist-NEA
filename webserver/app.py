from flask import Flask, request, jsonify
import login
import friends
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

        return func(username, *args, **kwargs)

    return decorated_func


@app.route("/login", methods=["POST"])
def login_server():
    data = request.json
    result = login.login(data)
    if result[0]:
        return jsonify({"token": result[1]})
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
    data = request.json
    if friends.request_friend(data):
        return jsonify({"message": "friend added"})
    return jsonify({"message": "already friends/requested"}), 401


@app.route("/acceptfriend", methods=["POST"])
@check_jwt
def accept_friend():
    result = friends.accept_friendship(request.json)
    if result == "friend added":
        return jsonify({"message": result})
    return jsonify({"message": result}), 401


if __name__ == "__main__":
    app.run(debug=True)
