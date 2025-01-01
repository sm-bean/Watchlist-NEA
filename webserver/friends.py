import mysql.connector
import dotenv
import os


def request_friend(username1, data):
    dotenv.load_dotenv()
    db_password = os.getenv("db_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="serverconnection",
        password=db_password,
        database="watchlists",
    )

    username2 = data["friend_username"]
    cor_coeff = data["correlation coefficient"]
    friendship_status = "Request"

    mycursor = mydb.cursor()
    friendship_query = (
        "SELECT Status FROM friendships WHERE Username1 = %s AND Username2 = %s"
    )

    val = (username1, username2)
    mycursor.execute(friendship_query, val)
    val = (username2, username1)
    mycursor.execute(friendship_query, val)
    myresult = mycursor.fetchone()

    if myresult is None:
        friendship_query = "INSERT INTO friendships (Username1, Username2, Status, CorrelationCoefficient) VALUES (%s, %s, %s, %s)"
        val = (username1, username2, friendship_status, cor_coeff)
        mycursor.execute(friendship_query, val)
        mydb.commit()
        return True
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
        return "no request"
    if myresult[0] == "Accepted":
        return "already accepted"

    friendship_query = "UPDATE friendships SET Status = 'Accepted' WHERE Username1 = %s AND Username2 = %s"
    mycursor.execute(friendship_query, val)
    mydb.commit()

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
    friendship_query(
        "SELECT Username1, Status, CorrelationCoefficient FROM friendships WHERE Username2 = %s"
    )
    mycursor.execute(friendship_query, val)
    myresult = mycursor.fetchall()

    return myresult
