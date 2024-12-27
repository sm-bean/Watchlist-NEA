import mysql.connector
import bcrypt
import jwt
import datetime
import dotenv
import os


def login(data):
    dotenv.load_dotenv()
    db_password = os.getenv("db_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="serverconnection",
        password=db_password,
        database="watchlists",
    )

    username = data.get("username")
    password = data.get("password")

    mycursor = mydb.cursor()
    password_query = 'SELECT HashedPassword FROM userauthdetails WHERE Username = "%s"'
    adr = (username,)
    mycursor.execute(password_query, adr)
    myresult = mycursor.fetchone()

    if myresult is None:
        return [False, ""]

    bytes = password.encode("utf-8")
    result = bcrypt.checkpw(bytes, myresult[0])

    if result:
        return [True, create_jwt_token(username)]
    return [False, ""]


def create_jwt_token(username):
    dotenv.load_dotenv()
    secret = os.getenv("jwt_secret")
    algorithm = os.getenv("algorithm")

    token = jwt.encode(
        {
            "user": username,
            "exp": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(hours=1),
        },
        secret,
        algorithm,
    )


def check_username_availability(username):
    dotenv.load_dotenv()
    db_password = os.getenv("db_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="serverconnection",
        password=db_password,
        database="watchlists",
    )

    mycursor = mydb.cursor()
    username_query = 'SELECT Username FROM userauthdetails WHERE Username = "%s"'
    adr = (username,)
    mycursor.execute(username_query, adr)
    myresult = mycursor.fetchone()

    if myresult is None:
        return True
    return False
