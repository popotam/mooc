#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import random

NUM_EXPERIMENTS = 1000
MAX_ITERATIONS = 1000
MONTE_CARLO_THING = 1000


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


def predict(w, x):
    return +1 if w[0] * x[0] + w[1] * x[1] + w[2] * x[2] > 0 else -1


def perceptron(data_set, w=(0.0, 0.0, 0.0)):
    iteration = 1
    while iteration < MAX_ITERATIONS:
        iteration += 1
        misclassified = [(x, y) for x, y in data_set
                         if predict(w, x) != y]
        if not misclassified:
            break
        x, y = random.choice(misclassified)
        w = (w[0] + y * x[0], w[1] + y * x[1], w[2] + y * x[2])
    return iteration, w


def sign(x):
    if x > 0:
        return 1
    else:
        return -1


def linear(data_set):
    from sklearn import linear_model
    clf = linear_model.LinearRegression(fit_intercept=False)
    X, Y = zip(*data_set)
    clf.fit(X, Y)
    #print sum(clf.predict(x) == y for x, y in data_set) / len(data_set)
    #for x, y in data_set:
    #    print y, clf.predict(x), sign(clf.predict(x)), predict(clf.coef_, x), \
    #        "***", clf.coef_[0] * x[0] + clf.coef_[1] * x[1] + clf.coef_[2] * x[2], \
    #        clf.coef_, x
    #e_in = sum(predict(clf.coef_, x) != y for x, y in data_set) / len(data_set)
    #e_in2 = sum(sign(clf.predict(x)) != y for x, y in data_set) / len(data_set)
    #print e_in, e_in2
    return (clf.coef_[0], clf.coef_[1], clf.coef_[2])


def experiment(n=100, use_perceptron=False):
    f = generate_f()
    data_set = generate_data_set(f, n)
    w = linear(data_set)
    # Ein
    e_in = sum(predict(w, x) != y for x, y in data_set) / len(data_set)
    # Eout
    e_out = sum(
        predict(w, x) != f(x)
        for x in ((1.0, random_x(), random_x())
                  for i in xrange(MONTE_CARLO_THING))
    ) / float(MONTE_CARLO_THING)
    if not use_perceptron:
        return e_in, e_out

    iterations, w = perceptron(data_set, w)
    # do the monte carlo
    e_perc = sum(
        predict(w, x) != f(x)
        for x in ((1.0, random_x(), random_x())
                  for i in xrange(MONTE_CARLO_THING))
    ) / float(MONTE_CARLO_THING)
    return e_in, e_out, iterations, e_perc

if __name__ == "__main__":
    print "N = 100"
    results = [experiment() for i in xrange(NUM_EXPERIMENTS)]
    print sum(e_in for e_in, _ in results) / NUM_EXPERIMENTS
    print sum(e_out for _, e_out in results) / NUM_EXPERIMENTS
    print "N = 10 (perceptron)"
    results = [experiment(10, True) for i in xrange(NUM_EXPERIMENTS)]
    print sum(e_in for e_in, _, _, _ in results) / NUM_EXPERIMENTS
    print sum(e_out for _, e_out, _, _ in results) / NUM_EXPERIMENTS
    print sum(i for _, _, i, _ in results) / NUM_EXPERIMENTS
    print sum(e_perc for _, _, _, e_perc in results) / NUM_EXPERIMENTS
