#!/usr/bin/env python3
"""Grouping sequential values with groupby().
"""
#end_pymotw_header

from itertools import *
import operator
import pprint


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '(%s, %s)' % (self.x, self.y)

    def __cmp__(self, other):
        return cmp((self.x, self.y), (other.x, other.y))


# Create a dataset of Point instances
data = list(imap(Point,
                 cycle(islice(count(), 3)),
                 islice(count(), 7),
                 )
            )
print('Data:')
pprint.pprint(data, width=69)
print()

# Try to group the unsorted data based on X values
print 'Grouped, unsorted:'
for k, g in groupby(data, operator.attrgetter('x')):
    print(k, list(g))
print()

# Sort the data
data.sort()
print('Sorted:')
pprint.pprint(data, width=69)
print()

# Group the sorted data based on X values
print('Grouped, sorted:')
for k, g in groupby(data, operator.attrgetter('x')):
    print(k, list(g))
print()
