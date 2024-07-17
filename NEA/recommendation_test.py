from math import sqrt
from random import random

def predicted_value(user, item):
    p = user.avg_rating

def num_neighbours(network):
    sum = 0
    for user_correlation in network.neighbours_adjmat:
        for value in user_correlation:
            if value == 1:
                sum += 1

    return sum/2

def correlation_coefficient(x, y):
    co_total = 0
    xsigma = 0
    ysigma = 0
    for i in range(len(x.ratings)):
        co_total += (x.ratings[i] - x.avg_rating)*(y.ratings[i] - y.avg_rating)
        xsigma += (x.ratings[i] - x.avg_rating)**2
        ysigma += (y.ratings[i] - y.avg_rating)**2

    xsigma = sqrt(xsigma)
    ysigma = sqrt(ysigma)

    return (co_total/(xsigma * ysigma))

class Network:
    def __init__(self, users, threshold):
        self.users = users
        self.correlation_threshold = threshold
        self.correlation_matrix = []
        self.neighbours_adjmat = []
        

    def add_user(self, user):
        self.users.append(user)

    def generate_correlation_matrix(self):
        self.correlation_matrix = []
        user_correlations = []

        for user in self.users:
            user_correlations = []

            for other in self.users:
                if user == other:
                    user_correlations.append(-1)
                else:
                    user_correlations.append(correlation_coefficient(user, other))

            self.correlation_matrix.append(user_correlations)

    def generate_neighbour_adjmat(self):
        if self.correlation_matrix == []:
            print("please generate correlation matrix first")
        else:
            i = 0
            self.neighbours_adjmat = []
            for user_correlations in self.correlation_matrix:
                self.neighbours_adjmat.append([])
                for correlation in user_correlations:
                    if correlation >= self.correlation_threshold:
                        self.neighbours_adjmat[i].append(1)
                    else:
                        self.neighbours_adjmat[i].append(0)
                i += 1
                        


class User:
    def __init__(self, ID, ratings):
        self.ID = ID
        self.ratings = ratings
        self.avg_rating = sum(self.ratings)/len(self.ratings)
        self.neighbours = []

    def add_neighbours(self, network):
        for user in network.users:
            if user not in self.neighbours and correlation_coefficient(self, user) >= 0.9:
                self.neighbours.append(user)


class Item:
    def __init__(self, avg_rating):
        self.avg_rating = avg_rating


n = Network([], 0.3)
generated_ratings = []
for i in range(100):
    for i in range(100):
        generated_ratings.append(random() * 5)

    n.add_user(User(random(), generated_ratings))
    generated_ratings = []

n.generate_correlation_matrix()
n.generate_neighbour_adjmat()

print(num_neighbours(n))