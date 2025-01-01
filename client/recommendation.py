from math import sqrt


def correlation_coefficient(x, y, common_films):

    common_films = x.get_common_films(y)

    co_total = 0
    x_sigma = 0
    y_sigma = 0
    for film in common_films:
        co_total += (x.get_rating(film) - x.avg_rating) * (
            y.get_rating(film) - y.avg_rating
        )
        x_sigma += (x.get_rating(film) - x.avg_rating) ** 2
        y_sigma += (y.get_rating(film) - y.avg_rating) ** 2

    x_sigma = sqrt(x_sigma)
    y_sigma = sqrt(y_sigma)

    return co_total / (x_sigma * y_sigma)


def predict_value(user, film, friends):
    raters_diff = 0
    raters_correlation = 0

    for friend in friends:
        raters_diff += (
            friend.get_rating(film) - friend.avg_rating
        ) * user.get_correlation_coefficient(friend)
        raters_correlation += abs(user.get_correlation_coefficient(friend))

    return user.avg_rating + raters_diff / raters_correlation
