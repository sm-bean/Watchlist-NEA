import mysql.connector
import dotenv
import os
import datetime

# Does a join query between films and userwatched ratings to get films watched by a user


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


# Checks that the user hasn't logged the film before, and then inserts record into userwatchedrating with current date if not


def log_film_watched(data):
    dotenv.load_dotenv()
    db_password = os.getenv("db_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="serverconnection",
        password=db_password,
        database="watchlists",
    )

    username = data["username"]
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
        val = (film_id, username, rating, datetime.datetime.now(datetime.timezone.utc))
        mycursor.execute(film_query, val)
        mydb.commit()

        mycursor.close()
        mydb.close()

        return True

    mycursor.close()
    mydb.close()

    return False


# Queries for the film by title and returns all results


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
