

def test_lace_strings():
    from midterm1 import laceStrings
    result = laceStrings('abcd', 'efghi')
    expected = 'aebfcgdhi'
    print result
    print expected
    assert result == expected
