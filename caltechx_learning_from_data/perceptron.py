#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

NUM_EXPERIMENTS = 1000
MAX_ITERATIONS = 1000
MONTE_CARLO_THING = 10000


def random_x():
    return random.random() * 2 - 1


def generate_f():
    px, py = random_x(), random_x()
    qx, qy = random_x(), random_x()

    def predict((x0, x1, x2)):
        x = x1
        y = x2
        pred_y = py + ((qy - py) / (qx - px)) * (x - px)
        return +1 if y > pred_y else -1
    return predict


def generate_data_set(func, n=10):
    return [(x, func(x))
            for x in ((1.0, random_x(), random_x()) for i in xrange(n))]


def perceptron_predict(w, x):
    return +1 if w[0] * x[0] + w[1] * x[1] + w[2] * x[2] > 0 else -1


def perceptron(data_set):
    w = (0.0, 0.0, 0.0)
    iteration = 1
    while iteration < MAX_ITERATIONS:
        iteration += 1
        misclassified = [(x, y) for x, y in data_set
                         if perceptron_predict(w, x) != y]
        if not misclassified:
            break
        x, y = random.choice(misclassified)
        w = (w[0] + y * x[0], w[1] + y * x[1], w[2] + y * x[2])
    return iteration, w


def experiment(n=10):
    f = generate_f()
    data_set = generate_data_set(f, n)
    iterations, w = perceptron(data_set)
    # do the monte carlo
    error = sum(
        perceptron_predict(w, x) != f(x)
        for x in ((1.0, random_x(), random_x())
                  for i in xrange(MONTE_CARLO_THING))
    ) / float(MONTE_CARLO_THING)
    return iterations, error

if __name__ == "__main__":
    print "N = 10"
    results = [experiment() for i in xrange(NUM_EXPERIMENTS)]
    print sum(iterations for iterations, _ in results) / float(NUM_EXPERIMENTS)
    print sum(error for _, error in results) / float(NUM_EXPERIMENTS)
    print
    print "N = 100"
    results = [experiment(100) for i in xrange(NUM_EXPERIMENTS)]
    print sum(iterations for iterations, _ in results) / float(NUM_EXPERIMENTS)
    print sum(error for _, error in results) / float(NUM_EXPERIMENTS)
