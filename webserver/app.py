from flask import Flask, request, jsonify
import login

app = Flask(__name__)


@app.route("/login", methods=["POST"])
def loginserver():
    data = request.json
    result = login.login(data)
    if result[0]:
        return jsonify({"token": result[1]})
    return jsonify({"message": "Incorrect details"}), 401


@app.route("/checkusername", methods=["POST"])
def check_username():
    data = request.json
    username = data.get("username")
    if login.check_username_availability(username):
        return jsonify({"available": True})
    return jsonify({"available": False})


if __name__ == "__main__":
    app.run(debug=True)
