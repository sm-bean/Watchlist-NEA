import mysql.connector
import dotenv
import os


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

    return myresult


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
    watchlist_query = "SELECT watchlists.WatchlistID, Name, Permissions FROM watchlists, watchlistmembers WHERE Username = %s AND watchlists.WatchlistID = watchlistmembers.WatchlistID"
    val = (username,)
    mycursor.execute(watchlist_query, val)
    myresult = mycursor.fetchall()

    return myresult


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
        "SELECT Username, Permissions FROM watchlists WHERE WatchlistID = %s"
    )
    val = (watchlist_id,)
    mycursor.execute(watchlist_query, val)
    myresult = mycursor.fetchall()

    return myresult
