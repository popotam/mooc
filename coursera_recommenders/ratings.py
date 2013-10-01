#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
import csv

MY_MOVIES = [1637, 105, 238]  # 11, 121, 8587]


def stats(user_ratings, movie_ids, movie):
    x_and_y = {
        y: sum(1 for user in user_ratings
               if y in user_ratings[user] and movie in user_ratings[user])
        for y in movie_ids
        if y != movie
    }
    x = sum(1 for user in user_ratings
            if movie in user_ratings[user])
    not_x_and_y = {
        y: sum(1 for user in user_ratings
               if y in user_ratings[user] and movie not in user_ratings[user])
        for y in movie_ids
        if y != movie
    }
    not_x = sum(1 for user in user_ratings
                if movie not in user_ratings[user])
    simple = {
        y: x_and_y[y] / float(x)
        for y in movie_ids
        if y != movie
    }
    advanced = {
        y: (x_and_y[y] / float(x)) / (not_x_and_y[y] / float(not_x))
        for y in movie_ids
        if y != movie
    }
    return simple, advanced


def main():
    data = [
        (int(u), int(m), float(r))
        for u, m, r in
        csv.reader(open('data/recsys-data-ratings.csv'))
    ]
    user_ratings = defaultdict(dict)
    movie_ids = set()
    for user, movie, rating in data:
        user_ratings[user][movie] = rating
        movie_ids.add(movie)
    simple_output = open('simple.txt', 'w')
    advanced_output = open('advanced.txt', 'w')
    for movie in MY_MOVIES:
        simple, advanced = stats(user_ratings, movie_ids, movie)

        simple_output.write(str(movie))
        print "Simple", movie
        for score, movie_id in sorted(
                [
                    (value, key) for key, value in simple.iteritems()
                ], reverse=True)[:5]:
            simple_output.write(",%i,%f" % (movie_id, score))
            print movie_id, score
        simple_output.write("\n")
        print

        advanced_output.write(str(movie))
        print "Advanced", movie
        for score, movie_id in sorted(
                [
                    (value, key) for key, value in advanced.iteritems()
                ], reverse=True)[:5]:
            advanced_output.write(",%i,%f" % (movie_id, score))
            print movie_id, score
        advanced_output.write("\n")
        print
    simple_output.close()
    advanced_output.close()


if __name__ == "__main__":
    main()
