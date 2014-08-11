import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

matrix_size = 5


def mapper(record):
    matrix, row, column, value = record
    if matrix == 'a':
        for i in xrange(matrix_size):
            mr.emit_intermediate((row, i), record)
    elif matrix == 'b':
        for i in xrange(matrix_size):
            mr.emit_intermediate((i, column), record)


def reducer(key, list_of_values):
    row, column = key
    a_values = {(r, c): value for matrix, r, c, value in list_of_values
                if matrix == 'a'}
    b_values = {(r, c): value for matrix, r, c, value in list_of_values
                if matrix == 'b'}
    value = sum(
        a_values.get((row, i), 0) * b_values.get((i, column), 0)
        for i in xrange(matrix_size)
    )
    mr.emit((row, column, value))

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
