#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import math
import random

NUM_EXPERIMENTS = 100
LEARNING_RATE = 0.01
MAX_ITERATIONS = 1000
MONTE_CARLO_THING = 1000


def random_x():
    return random.random() * 2 - 1


def generate_f():
    px, py = random_x(), random_x()
    qx, qy = random_x(), random_x()

    def predict_f((x0, x1, x2)):
        x = x1
        y = x2
        pred_y = py + ((qy - py) / (qx - px)) * (x - px)
        return +1 if y > pred_y else -1
    return predict_f


def generate_data_set(func, n=10):
    return [(x, func(x))
            for x in ((1.0, random_x(), random_x()) for i in xrange(n))]


def logistic(w, x):
    return sigmoid(sum(ww * xx for ww, xx in zip(w, x)))


def predict(w, x):
    return +1 if logistic(w, x) > 0.5 else -1


def sigmoid(x):
     return 1 / (1 + (math.e ** -x))


def cost_func_single(w, x, y):
    """
    function [J, grad] = costFunction(theta, X, y)

    m = length(y); % number of training examples

    J = 0;
    grad = zeros(size(theta));

    hth = sigmoid(X * theta);  % vector
    J = sum(-y .* log(hth) - (1 - y) .* log(1 - hth)) / m;

    for i = 1:size(theta),
        grad(i) = (1 / m) * sum((hth - y) .* X(:, i));
    end

    end
    """
    score = logistic(w, x)
    cost = (
        - int(y == 1) * math.log(score)
        - int(y == -1) * math.log(1.0 - score)
    )
    gradient = tuple((score - int(y == 1)) * xx for xx in x)
    return cost, gradient


def vector_change(old, new):
    diff = tuple(o - n for o, n in zip(old, new))
    return math.sqrt(sum(d ** 2 for d in diff))


def stochastic_gradient_descent(w, data_set, cost_func):
    epoch = 0
    old_w = tuple(ww + 1.0 for ww in w)
    while vector_change(old_w, w) >= 0.01 or epoch > MAX_ITERATIONS:
        old_w = w
        random.shuffle(data_set)
        sum_cost = 0
        for x, y in data_set:
            cost, gradient = cost_func(w, x, y)
            w = tuple(ww - LEARNING_RATE * gg for ww, gg in zip(w, gradient))
            sum_cost += cost
        epoch += 1
        #print("Epoch %i: %s %s" % (epoch, sum_cost, w))
    return w, epoch


def experiment(n=100):
    f = generate_f()
    data_set = generate_data_set(f, n)
    w = (0.0, 0.0, 0.0)
    w, epoch = stochastic_gradient_descent(w, data_set, cost_func_single)
    # Ein
    e_in = sum(
        cost_func_single(w, x, y)[0] for x, y in data_set
    ) / len(data_set)
    # Eout
    monte_carlo_set = generate_data_set(f, MONTE_CARLO_THING)
    e_out = sum(
        cost_func_single(w, x, y)[0] for x, y in monte_carlo_set
    ) / len(monte_carlo_set)
    return e_in, e_out, epoch


if __name__ == "__main__":
    print("N = 100")
    results = [experiment() for i in xrange(NUM_EXPERIMENTS)]
    for i in xrange(len(results[0])):
        print(sum(r[i] for r in results) / NUM_EXPERIMENTS)
