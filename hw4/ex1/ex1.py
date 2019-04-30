#!/usr/bin/env python3

import sys
import random
import datetime
import csv

from random import randrange, randint
import numpy as np
import scipy as sp

date_start = datetime.date(2000, 1, 1)
date_period = 365 * 17

# Reads in emails.txt and movies.txt and creates 'num_movies' entries for each
# email.
# Returns the database for testing purposes, the emails and the movies
def create_db(num_movies):
    with open("emails.txt") as f:
        emails = f.read().split("\n")
    while "" in emails:
        emails.remove("")

    with open("movies.txt") as f:
        movies = f.read().split("\n")
    while "" in movies:
        movies.remove("")

    db = []

    for email in emails[:3]:
        movies_index = list(range(0, len(movies)))
        random.shuffle(movies_index)
        for i, f in enumerate(movies_index[0:num_movies]):
            dat = date_start + datetime.timedelta(randint(1, date_period))
            db.append([email, movies[f], dat, randint(1, 5)])

    return db, emails, movies


def count_ratings(db, movies, rating_levels):
    k = len(movies)
    assert len(movies) == len(rating_levels) == k


    epsilon = 0.69314718056 / k     # composition of queries, sum of epsilon ofr each query must be equal to the level of privacy requested 
    sensitivity = 1                 # for counting queries
    
    # save queries result in order to prevent averaging attacks 
    saved_queries = {}

    result = []

    # iterate over all queries
    for m, r in zip(movies, rating_levels):
        count = 0
        key = m + str(r)

        # get saved query result, if there's one 
        saved = saved_queries.get(key)
        # if there's a saved result, just use that in order to not give any other value of the distribution
        if saved is not None:
            result.append(saved)
        else:
            # iterate over all database rows and compute count query
            for row in db:
                if row[1] == m and row[3] >= r:
                    count = count + 1
            # add laplacian noise to the result
            res = count + np.random.laplace(0, sensitivity/epsilon)
            # save result for next queries
            saved_queries[key] = res
            result.append(res)

    return result


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # You can change this part to test the queries as you like.
        print("Testing mode")
        db, emails, movies = create_db(1000)
        print("------------")
        queried_movies = ['The Godfather', 'Seven Samurai', 'The Godfather', 'Seven Samurai'] #movies[:5]
        queried_rating_levels = [2,3,2,3] #np.random.randint(1, high=5, size=5)
        results = count_ratings(db, queried_movies, queried_rating_levels)
        print("Queried movies:", queried_movies)
        print("Queried rating levels:", queried_rating_levels)
        print("Response:", results)

    else:
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !! Do not modify this part !!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        db_file = sys.argv[1]
        with open(db_file) as f:
            db = list(csv.reader(f, skipinitialspace=True))

        # Get nice ints for comparisons
        for i, line in enumerate(db):
            db[i][3] = int(line[3])

        movies, rating_levels = sys.argv[2:4]
        movies = movies.split('|')
        rating_levels = [int(x) for x in rating_levels.split(',')]
        result = count_ratings(db, movies, rating_levels)

        with open("/tmp/student.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows([result])
