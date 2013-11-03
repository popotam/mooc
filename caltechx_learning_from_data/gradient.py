#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import math

INITIAL = (1.0, 1.0)
LEARNING_RATE = 0.1
MAX_ITERATIONS = 1000


def func(u, v):
    return (u * math.e ** v - 2 * v * math.e ** -u) ** 2


def u_derivative(u, v):
    return (
        2 * (math.e ** v + 2 * v * math.e ** -u)
        * (u * math.e ** v - 2 * v * math.e ** -u)
    )


def v_derivative(u, v):
    return (
        2 * (u * math.e ** v - 2 * math.e ** -u)
        * (u * math.e ** v - 2 * v * math.e ** -u)
    )


def simple_descent(theta=INITIAL):
    print("simple_descent")
    iteration = 0
    u, v = theta
    error = func(u, v)
    print("%i : (%.14f, %.14f) : %.14f" % (iteration, u, v, error))
    while (error > 10 ** -14) and iteration < MAX_ITERATIONS:
        delta_u = u_derivative(u, v)
        delta_v = v_derivative(u, v)
        u = u - LEARNING_RATE * delta_u
        v = v - LEARNING_RATE * delta_v
        error = func(u, v)
        iteration += 1
        print("%i : (%.14f, %.14f) : %.14f" % (iteration, u, v, error))
    return u, v, iteration, error



def twostep_descent(theta=INITIAL):
    print("twostep_descent")
    iteration = 0
    u, v = theta
    error = func(u, v)
    print("%i : (%.14f, %.14f) : %.14f" % (iteration, u, v, error))
    while iteration < 15:
        delta_u = u_derivative(u, v)
        u = u - LEARNING_RATE * delta_u
        delta_v = v_derivative(u, v)
        v = v - LEARNING_RATE * delta_v
        error = func(u, v)
        iteration += 1
        print("%i : (%.14f, %.14f) : %.14f" % (iteration, u, v, error))
    return u, v, iteration, error


if __name__ == "__main__":
    simple_descent()
    twostep_descent()
