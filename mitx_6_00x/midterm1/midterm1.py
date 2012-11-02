import itertools


def laceStrings(s1, s2):
    """
    s1 and s2 are strings.

    Returns a new str with elements of s1 and s2 interlaced,
    beginning with s1. If strings are not of same length,
    then the extra elements should appear at the end.
    """
    return "".join([
        element for element in itertools.chain.from_iterable(
                itertools.izip_longest(s1, s2, fillvalue=None))
        if element
    ])


def laceStringsRecur(s1, s2):
    """
    s1 and s2 are strings.

    Returns a new str with elements of s1 and s2 interlaced,
    beginning with s1. If strings are not of same length,
    then the extra elements should appear at the end.
    """
    def helpLaceStrings(s1, s2, out):
        if s1 == '':
            return out + s2
        if s2 == '':
            return out + s1
        else:
            return helpLaceStrings(s1[1:], s2[1:], out + s1[0] + s2[0])
    return helpLaceStrings(s1, s2, '')


def fixedPoint(f, epsilon):
    """
    f: a function of one argument that returns a float
    epsilon: a small float

    returns the best guess when that guess is less than epsilon
    away from f(guess) or after 100 trials, whichever comes first.
    """
    guess = 1.0
    for i in range(100):
        if abs(f(guess) - guess) <= epsilon:
            return guess
        else:
            guess = f(guess)
    return guess


def sqrt_ver1(a):
    def tryit(x):
        return 0.5 * (a / x + x)
    return fixedPoint(tryit(a), 0.0001)


def babylon(a):
    def test(x):
        return 0.5 * ((a / x) + x)
    return test


def sqrt_ver2(a):
    return fixedPoint(babylon(a), 0.0001)


def myLog(x, b):
    '''
    x: a positive integer
    b: a positive integer

    returns: log_b(x), or, the logarithm of x relative to a base b.
    '''
    guess = 0
    while b ** (guess + 1) <= x:
        guess += 1
    return guess
