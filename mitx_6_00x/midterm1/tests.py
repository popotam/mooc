

def test_lace_strings():
    from midterm1 import laceStrings
    result = laceStrings('abcd', 'efghi')
    expected = 'aebfcgdhi'
    print result
    print expected
    assert result == expected


def test_lace_strings_recur():
    from midterm1 import laceStringsRecur
    result = laceStringsRecur('abcd', 'efghi')
    expected = 'aebfcgdhi'
    print result
    print expected
    assert result == expected


def test_fixed_point():
    from midterm1 import fixedPoint, sqrt_ver2
    epsilon = 0.0001
    r1 = fixedPoint(lambda x: (-1) * (x ** 2), epsilon)
    r2 = sqrt_ver2(64)
    print "r1", r1
    print "r2", r2
    assert r1 == -1.0
    assert r2 - 8 < epsilon


def test_myLog():
    from midterm1 import myLog
    r1 = myLog(16, 2)
    r2 = myLog(15, 3)
    print "r1", r1
    print "r2", r2
    assert r1 == 4
    assert r2 == 2
