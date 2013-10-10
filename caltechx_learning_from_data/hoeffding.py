#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import random

NUM_FLIPS = 10
NUM_COINS = 1000
NUM_EXPERIMENTS = 10000


def single_coin(n=NUM_FLIPS):
    return sum(random.choice((0, 1)) for i in xrange(n)) / n


def experiment(n=NUM_COINS):
    coins = [single_coin() for i in xrange(n)]
    return coins[0], random.choice(coins), min(coins)

if __name__ == "__main__":
    c1, crand, cmin = zip(*[experiment() for i in xrange(NUM_EXPERIMENTS)])
    print sum(x for x in c1) / float(NUM_EXPERIMENTS)
    print sum(x for x in crand) / float(NUM_EXPERIMENTS)
    print sum(x for x in cmin) / float(NUM_EXPERIMENTS)
