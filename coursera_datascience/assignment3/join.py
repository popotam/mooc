import MapReduce
import sys
from itertools import product

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line


def mapper(record):
    order_id = record[1]
    mr.emit_intermediate(order_id, record)


def reducer(key, list_of_values):
    orders = (order for order in list_of_values
              if order[0] == 'order')
    line_items = (line_item for line_item in list_of_values
                  if line_item[0] == 'line_item')
    for order, line_item in product(orders, line_items):
        mr.emit(order + line_item)

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
