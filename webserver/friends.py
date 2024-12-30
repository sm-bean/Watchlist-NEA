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

    username1 = data["username1"]
    username2 = data["username2"]
    cor_coeff = data["correlation coefficient"]
    friendship_status = "Request"

    mycursor = mydb.cursor()
    friendship_query = (
        "SELECT Username1 FROM friendships WHERE Username1 = %s AND Username2 = %s"
    )
    val = (username1, username2)
    mycursor.execute(friendship_query, val)
    myresult = mycursor.fetchone()

    if myresult is None:
        friendship_query = "INSERT INTO friendships (Username1, Username2, Status, CorrelationCoefficient) VALUES (%s, %s, %s, %s)"
        val = (username1, username2, friendship_status, cor_coeff)
        mycursor.execute(friendship_query, val)
        mydb.commit()
        return True
    return False


def accept_friendship(data):
    dotenv.load_dotenv()
    db_password = os.getenv("db_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="serverconnection",
        password=db_password,
        database="watchlists",
    )

    username1 = data["username1"]
    username2 = data["username2"]

    mycursor = mydb.cursor()
    friendship_query = (
        "SELECT Status FROM friendships WHERE Username1 = %s AND Username2 = %s"
    )

    val = (username1, username2)
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
