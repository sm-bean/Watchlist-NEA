from math import sqrt


def correlation_coefficient(x, y):

    common_films = x.get_common_films(y)

    if len(common_films) == 0:
        return 0

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

    if (x_sigma * y_sigma) == 0:
        return 0

    return round(co_total / (x_sigma * y_sigma), 2)


def predict_value(user, film, friends, friend_correlation_coefficients):
    raters_diff = 0
    raters_correlation = 0

    for i in range(len(friends)):
        friend_rating = friends[i].get_rating(film)
        if friend_rating != "not seen":
            raters_diff += (
                friends[i].get_rating(film) - friends[i].avg_rating
            ) * friend_correlation_coefficients[i]
            raters_correlation += abs(friend_correlation_coefficients[i])

    if raters_correlation == 0:
        return "no neighbours seen"

    return user.avg_rating + raters_diff / raters_correlation


def recommend_film(user, watchlist):
    neighbours = user.neighbours[:]
    neighbours_correlation_coefficients = user.neighbours_correlation_coefficients
    best_film = None
    best_predicted = 0

    for film in watchlist.films:
        predicted_value = predict_value(
            user, film, neighbours, neighbours_correlation_coefficients
        )
        if predicted_value != "no neighbours seen":
            if predicted_value > best_predicted:
                best_predicted = predicted_value
                best_film = film

    if best_film is None:
        return watchlist.get_random_film()

    return best_film
