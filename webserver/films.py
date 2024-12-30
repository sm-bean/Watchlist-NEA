import mysql.connector
import dotenv
import os


def get_films_watched(data):
    dotenv.load_dotenv()
    db_password = os.getenv("db_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="serverconnection",
        password=db_password,
        database="watchlists",
    )

    username = data["username"]

    mycursor = mydb.cursor()
    film_query = "SELECT films.FilmID, Title, AverageRating, ReleaseDate, Runtime, Genre FROM films, userwatchedratings WHERE Username = %s AND films.FilmID = userwatchedratings.FilmID"
    val = (username,)
    mycursor.execute(film_query, val)
    myresult = mycursor.fetchall()

    return myresult
