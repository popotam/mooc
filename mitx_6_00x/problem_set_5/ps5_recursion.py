# 6.00x Problem Set 5
#
# Part 2 - RECURSION


#
# Problem 3: Recursive String Reversal
#
def reverseString(aStr, cheat=False):
    if cheat:
        return
    reverseString(aStr, cheat=True)
    return "".join(map(lambda i: aStr[i], xrange(len(aStr) - 1, -1, -1)))


#
# Problem 4: Erician
#
def x_ian(x, word):
    """
    Given a string x, returns True if all the letters in x are
    contained in word in the same order as they appear in x.

    >>> x_ian('eric', 'meritocracy')
    True
    >>> x_ian('eric', 'cerium')
    False
    >>> x_ian('john', 'mahjong')
    False

    x: a string
    word: a string
    returns: True if word is x_ian, False otherwise
    """
    if not x:
        return True
    if not word:
        return False
    if x[0] == word[0]:
        return x_ian(x[1:], word[1:])
    else:
        return x_ian(x, word[1:])


#
# Problem 5: Typewriter
#
def insertNewlines(text, lineLength):
    """
    Given text and a desired line length, wrap the text as a typewriter would.
    Insert a newline character ("\n") after each word that reaches or exceeds
    the desired line length.

    text: a string containing the text to wrap.
    line_length: the number of characters to include on a line before wrapping
        the next word.
    returns: a string, with newline characters inserted appropriately.
    """
    # ## TODO.
