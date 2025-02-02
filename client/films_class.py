import datetime


class Film:
    def __init__(self, film_id, title, avg_rating, release_date, runtime, genre=""):
        self.film_id = film_id
        self.title = title
        self.avg_rating = avg_rating
        self.release_date = datetime.datetime.strptime(
            release_date, "%a, %d %b %Y %H:%M:%S %Z"
        ).date()
        self.runtime = runtime
        self.genre = genre
