#!/usr/bin/env python3
"""Using map()
"""
#end_pymotw_header

print('Doubles:')
for i in map(lambda x: 2 * x, range(5)):
    print(i)

print('Multiples:')
r1 = range(5)
r2 = range(5, 10)
for i in map(lambda x, y: (x, y, x * y), r1, r2):
    print('{:d} * {:d} = {:d}'.format(*i))
