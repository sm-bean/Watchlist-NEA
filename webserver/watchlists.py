import mysql.connector
import dotenv
import os

# Joins the films and watchlistfilms tables to get the details about the films in the watchlist with watchlist_id given


def get_films_in_watchlist(watchlist_id):
    dotenv.load_dotenv()
    db_password = os.getenv("db_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="serverconnection",
        password=db_password,
        database="watchlists",
    )

    mycursor = mydb.cursor()
    watchlist_query = "SELECT films.FilmID, Title, AverageRating, ReleaseDate, Runtime, Genre FROM films, watchlistfilms WHERE WatchlistID = %s AND films.FilmID = watchlistfilms.FilmID"
    val = (watchlist_id,)
    mycursor.execute(watchlist_query, val)
    myresult = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    return myresult


# Joins watchlists and watchlistmembers to get the names of the watchlists the user is in


def get_watchlists_user_in(username):
    dotenv.load_dotenv()
    db_password = os.getenv("db_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="serverconnection",
        password=db_password,
        database="watchlists",
    )

    mycursor = mydb.cursor()
    watchlist_query = "SELECT watchlists.WatchlistID, Name, Invite FROM watchlists, watchlistmembers WHERE Username = %s AND watchlists.WatchlistID = watchlistmembers.WatchlistID"
    val = (username,)
    mycursor.execute(watchlist_query, val)
    myresult = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    return myresult


# Selects members by watchlistID


def get_members(watchlist_id):
    dotenv.load_dotenv()
    db_password = os.getenv("db_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="serverconnection",
        password=db_password,
        database="watchlists",
    )

    mycursor = mydb.cursor()
    watchlist_query = (
        "SELECT Username, Invite FROM watchlistmembers WHERE WatchlistID = %s"
    )
    val = (watchlist_id,)
    mycursor.execute(watchlist_query, val)
    myresult = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    return myresult


# Checks if film is already in watchlist, and if not, inserts record of film into watchlistfilms


def add_film(watchlist_id, film_id):
    dotenv.load_dotenv()
    db_password = os.getenv("db_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="serverconnection",
        password=db_password,
        database="watchlists",
    )

    mycursor = mydb.cursor()
    watchlist_query = (
        "SELECT WatchlistID FROM watchlistfilms WHERE WatchlistID = %s AND FilmID = %s"
    )
    val = (watchlist_id, film_id)
    mycursor.execute(watchlist_query, val)
    myresult = mycursor.fetchone()

    if myresult is None:
        watchlist_query = (
            "INSERT INTO watchlistfilms (WatchlistID, FilmID) VALUES (%s, %s)"
        )
        mycursor.execute(watchlist_query, val)
        mydb.commit()

        mycursor.close()
        mydb.close()

        return True

    mycursor.close()
    mydb.close()

    return False


# Checks if user is invited to watchlist, and if so, updates invite status to false


def add_user(username, watchlist_id):
    dotenv.load_dotenv()
    db_password = os.getenv("db_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="serverconnection",
        password=db_password,
        database="watchlists",
    )

    mycursor = mydb.cursor()
    watchlist_query = (
        "SELECT Invite FROM watchlistmembers WHERE WatchlistID = %s AND Username = %s"
    )
    val = (watchlist_id, username)
    mycursor.execute(watchlist_query, val)
    myresult = mycursor.fetchone()

    if myresult is None:
        mycursor.close()
        mydb.close()
        return "user not invited to watchlist"

    if myresult[0] == "False":
        mycursor.close()
        mydb.close()
        return "user already in watchlist"

    watchlist_query = "UPDATE watchlistmembers SET Invite = %s WHERE WatchlistID = %s and Username = %s"
    val = ("False", watchlist_id, username)
    mycursor.execute(watchlist_query, val)
    mydb.commit()

    mycursor.close()
    mydb.close()

    return "watchlist joined"


# Checks if the user is not yet invited to or in the watchlist, and then inserts the user into watchlistmembers


def invite_user(data):
    dotenv.load_dotenv()
    db_password = os.getenv("db_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="serverconnection",
        password=db_password,
        database="watchlists",
    )

    watchlist_id = data["watchlist_id"]
    username = data["invited_username"]

    mycursor = mydb.cursor()
    watchlist_query = (
        "SELECT Invite FROM watchlistmembers WHERE WatchlistID = %s AND Username = %s"
    )
    val = (watchlist_id, username)
    mycursor.execute(watchlist_query, val)
    myresult = mycursor.fetchone()

    if myresult is None:
        watchlist_query = "INSERT INTO watchlistmembers (WatchlistID, Username, Invite) VALUES (%s, %s, %s)"
        val = (watchlist_id, username, "True")
        mycursor.execute(watchlist_query, val)
        mydb.commit()

        mycursor.close()
        mydb.close()

        return "user invited"

    mycursor.close()
    mydb.close()
    return "user already invited/in watchlist"


# Creates watchlist in watchlists table, then gets id of watchlist created, and inserts user who created watchlist into watchlistmembers


def create_list(username, watchlist_name):
    dotenv.load_dotenv()
    db_password = os.getenv("db_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="serverconnection",
        password=db_password,
        database="watchlists",
    )

    mycursor = mydb.cursor()
    watchlist_query = "INSERT INTO watchlists (Name) VALUES (%s)"
    val = (watchlist_name,)
    mycursor.execute(watchlist_query, val)
    mydb.commit()

    watchlist_id = mycursor.lastrowid

    watchlist_query = "INSERT INTO watchlistmembers (WatchlistID, Username, Invite) VALUES (%s, %s, %s)"
    val = (watchlist_id, username, "False")
    mycursor.execute(watchlist_query, val)
    mydb.commit()

    mycursor.close()
    mydb.close()

    return watchlist_id
