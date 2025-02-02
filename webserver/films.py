import mysql.connector
import dotenv
import os
import datetime


def get_films_watched(username):
    dotenv.load_dotenv()
    db_password = os.getenv("db_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="serverconnection",
        password=db_password,
        database="watchlists",
    )

    mycursor = mydb.cursor()
    film_query = "SELECT films.FilmID, Title, AverageRating, ReleaseDate, Runtime, Genre, Rating, DateWatched FROM films, userwatchedratings WHERE Username = %s AND films.FilmID = userwatchedratings.FilmID"
    val = (username,)
    mycursor.execute(film_query, val)
    myresult = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    return myresult


def log_film_watched(username, data):
    dotenv.load_dotenv()
    db_password = os.getenv("db_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="serverconnection",
        password=db_password,
        database="watchlists",
    )

    film_id = data["film_id"]
    rating = data["rating"]

    mycursor = mydb.cursor()
    film_query = (
        "SELECT Username FROM userwatchedratings WHERE FilmID = %s AND Username = %s"
    )
    val = (film_id, username)
    mycursor.execute(film_query, val)
    myresult = mycursor.fetchone()

    if myresult is None:
        film_query = "INSERT INTO userwatchedratings (FilmID, Username, Rating, DateWatched) VALUES (%s, %s, %s, %s)"
        val = (film_id, username, rating, datetime.date.today())
        mycursor.execute(film_query, val)
        mydb.commit()

        mycursor.close()
        mydb.close()

        return True

    mycursor.close()
    mydb.close()

    return False


def find_film(film_title):
    dotenv.load_dotenv()
    db_password = os.getenv("db_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="serverconnection",
        password=db_password,
        database="watchlists",
    )

    mycursor = mydb.cursor()
    film_query = "SELECT FilmID, Title, AverageRating, ReleaseDate, Runtime, Genre FROM films WHERE Title = %s"
    val = (film_title,)
    mycursor.execute(film_query, val)
    myresult = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    return myresult
