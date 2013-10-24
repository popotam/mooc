#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import math
import random

NUM_EXPERIMENTS = 10000
MAX_ITERATIONS = 1000
MONTE_CARLO_THING = 1000


def random_x():
    return random.random() * 2 - 1


def sinus(x):
    return math.sin(math.pi * x[1])


def generate_data_set(func, n=2):
    return [(x, func(x))
            for x in ((1.0, random_x()) for i in xrange(n))]


def ax_regresion(data_set):
    ((_, x1), y1), ((_, x2), y2) = data_set
    a = (x1 * y1 + x2 * y2) / (x1 **2 + x2 ** 2)
    return (0.0, a)


def regression(w, x):
    return sum(ww * xx for ww, xx in zip(w, x))


def experiment(n=2):
    data_set = generate_data_set(sinus, n)
    w = ax_regresion(data_set)
    # Ein
    e_in = sum((regression(w, x) - y) ** 2
               for x, y in data_set) / len(data_set)
    # Eout
    e_out = sum(
        (regression(w, x) - sinus(x)) ** 2
        for x in ((1.0, random_x())
                  for i in xrange(MONTE_CARLO_THING))
    ) / MONTE_CARLO_THING
    return e_in, e_out, w[1], data_set


if __name__ == "__main__":
    print "N = 2"
    results = [experiment() for i in xrange(NUM_EXPERIMENTS)]
    print "Ein", sum(r[0] for r in results) / NUM_EXPERIMENTS
    print "Eout", sum(r[1] for r in results) / NUM_EXPERIMENTS
    a_average = sum(r[2] for r in results) / NUM_EXPERIMENTS
    print "a_average", a_average
    bias = sum(
        (regression((0.0, a_average), x) - sinus(x)) ** 2
        for x in ((1.0, random_x())
                  for i in xrange(MONTE_CARLO_THING))
    ) / MONTE_CARLO_THING
    print "bias", bias
    variance = sum(
        sum((regression((0.0, a), x) - regression((0.0, a_average), x)) ** 2
            for x, _ in data_set) / len(data_set)
        for _, _, a, data_set in results) / NUM_EXPERIMENTS
    print "variance", variance
