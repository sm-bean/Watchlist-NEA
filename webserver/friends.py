import mysql.connector
import dotenv
import os


def request_friend(data):
    dotenv.load_dotenv()
    db_password = os.getenv("db_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="serverconnection",
        password=db_password,
        database="watchlists",
    )

    username1 = data["username"]
    username2 = data["friend_username"]
    cor_coeff = data["correlation coefficient"]
    friendship_status = "Request"

    mycursor = mydb.cursor()
    friendship_query = (
        "SELECT Status FROM friendships WHERE Username1 = %s AND Username2 = %s"
    )

    val = (username1, username2)
    mycursor.execute(friendship_query, val)
    myresult1 = mycursor.fetchone()
    val = (username2, username1)
    mycursor.execute(friendship_query, val)
    myresult2 = mycursor.fetchone()

    if myresult1 is None and myresult2 is None:
        friendship_query = "INSERT INTO friendships (Username1, Username2, Status, CorrelationCoefficient) VALUES (%s, %s, %s, %s)"
        val = (username1, username2, friendship_status, cor_coeff)
        mycursor.execute(friendship_query, val)
        mydb.commit()

        mycursor.close()
        mydb.close()

        return True

    mycursor.close()
    mydb.close()

    return False


def accept_friendship(username1, username2):
    dotenv.load_dotenv()
    db_password = os.getenv("db_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="serverconnection",
        password=db_password,
        database="watchlists",
    )

    mycursor = mydb.cursor()
    friendship_query = (
        "SELECT Status FROM friendships WHERE Username1 = %s AND Username2 = %s"
    )

    val = (username2, username1)
    mycursor.execute(friendship_query, val)
    myresult = mycursor.fetchone()

    if myresult is None:
        mycursor.close()
        mydb.close()

        return "no request"

    if myresult[0] == "Accepted":
        mycursor.close()
        mydb.close()

        return "already accepted"

    friendship_query = (
        "UPDATE friendships SET Status = %s WHERE Username1 = %s AND Username2 = %s"
    )
    val = ("Accepted", username2, username1)
    mycursor.execute(friendship_query, val)
    mydb.commit()

    mycursor.close()
    mydb.close()

    return "friend added"


def get_friendships(username):
    dotenv.load_dotenv()
    db_password = os.getenv("db_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="serverconnection",
        password=db_password,
        database="watchlists",
    )

    mycursor = mydb.cursor()
    friendship_query = "SELECT Username2, Status, CorrelationCoefficient FROM friendships WHERE Username1 = %s"
    val = (username,)
    mycursor.execute(friendship_query, val)
    myresult1 = mycursor.fetchall()
    friendship_query = "SELECT Username1, Status, CorrelationCoefficient FROM friendships WHERE Username2 = %s"
    mycursor.execute(friendship_query, val)
    myresult2 = mycursor.fetchall()
    if myresult1 is None:
        myresult = myresult2
    elif myresult2 is None:
        myresult = myresult1
    else:
        myresult = myresult1 + myresult2

    mycursor.close()
    mydb.close()

    return myresult


def get_friendship_requests(username):
    dotenv.load_dotenv()
    db_password = os.getenv("db_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="serverconnection",
        password=db_password,
        database="watchlists",
    )

    mycursor = mydb.cursor()
    friendship_query = (
        "SELECT Username1 FROM friendships WHERE Username2 = %s AND Status = %s"
    )
    val = (username, "Request")
    mycursor.execute(friendship_query, val)
    myresult = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    return myresult


def update_coefficient(data):
    dotenv.load_dotenv()
    db_password = os.getenv("db_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="serverconnection",
        password=db_password,
        database="watchlists",
    )

    username = data["username"]
    friend_username = data["friend_username"]
    correlation_coefficient = data["correlation_coefficient"]

    mycursor = mydb.cursor()
    friendship_query = (
        "SELECT Status FROM friendships WHERE Username1 = %s AND Username2 = %s"
    )

    val = (username, friend_username)
    mycursor.execute(friendship_query, val)
    myresult = mycursor.fetchone()

    user_pos = 1

    if myresult is None:
        val = (friend_username, username)
        mycursor.execute(friendship_query, val)
        myresult = mycursor.fetchone()
        user_pos = 2

        if myresult is None:
            mycursor.close()
            mydb.close()

            return False

    friendship_query = "UPDATE friendships SET CorrelationCoefficient = %s WHERE Username1 = %s AND Username2 = %s"

    if user_pos == 1:
        val = (correlation_coefficient, username, friend_username)
    else:
        val = (correlation_coefficient, friend_username, username)

    mycursor.execute(friendship_query, val)
    mydb.commit()

    mycursor.close()
    mydb.close()

    return True
