import mysql.connector
import bcrypt
import jwt
import datetime
import dotenv
import os

# Retrieves the hashed password from the database for the username and checks it against the password submitted. If details are correct it returns a JWT


def login(data):
    dotenv.load_dotenv()
    db_password = os.getenv("db_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="serverconnection",
        password=db_password,
        database="watchlists",
    )

    username = data["username"]
    password = data["password"]

    mycursor = mydb.cursor()
    password_query = "SELECT HashedPassword FROM users WHERE Username = %s"
    val = (username,)
    mycursor.execute(password_query, val)
    myresult = mycursor.fetchone()

    mycursor.close()
    mydb.close()

    if myresult is None:
        return ""

    bytes_password = password.encode("utf-8")
    result = bcrypt.checkpw(bytes_password, myresult[0])

    if result:
        return create_jwt_token(username)
    return ""


# Encodes the username in a JWT and returns it


def create_jwt_token(username):
    dotenv.load_dotenv()
    jwt_secret = os.getenv("jwt_secret")
    algorithm = os.getenv("algorithm")

    token = jwt.encode(
        {
            "user": username,
            "exp": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(hours=1),
        },
        jwt_secret,
        algorithm,
    )

    return token


# Checks if the username is in the database, and returns True if not


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
    username_query = "SELECT Username FROM users WHERE Username = %s"
    val = (username,)
    mycursor.execute(username_query, val)
    myresult = mycursor.fetchone()

    mycursor.close()
    mydb.close()

    if myresult is None:
        return True
    return False


# Salts and hashes the given password and inserts the user into users table, then returns a JWT


def create_account(data):
    dotenv.load_dotenv()
    db_password = os.getenv("db_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="serverconnection",
        password=db_password,
        database="watchlists",
    )

    username = data["username"]
    password = data["password"]

    bytes_password = password.encode("utf-8")
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(bytes_password, salt)

    mycursor = mydb.cursor()
    create_account_query = (
        "INSERT INTO users (Username, DateJoined, HashedPassword) VALUES (%s, %s, %s)"
    )
    val = (username, datetime.date.today(), hashed_password)
    mycursor.execute(create_account_query, val)
    mydb.commit()

    mycursor.close()
    mydb.close()

    return create_jwt_token(username)
