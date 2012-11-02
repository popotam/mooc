import itertools


def laceStrings(s1, s2):
    """
    s1 and s2 are strings.

    Returns a new str with elements of s1 and s2 interlaced,
    beginning with s1. If strings are not of same length,
    then the extra elements should appear at the end.
    """
    # Your Code Here
    return "".join([
        element for element in itertools.chain.from_iterable(
                itertools.izip_longest(s1, s2, fillvalue=None))
        if element
    ])
