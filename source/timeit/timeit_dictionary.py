#!/usr/bin/env python3

"""Example of using timeit programatically.

Time various ways to populate and check a dictionary using a long list
of strings and integers.
"""
#end_pymotw_header

import timeit
import sys

# A few constants
range_size=1000
count=1000
setup_statement = "l = [ (str(x), x) for x in range(1000) ]; d = {}"

def show_results(result):
    "Print results in terms of microseconds per pass and per item."
    global count, range_size
    per_pass = 1000000 * (result / count)
    print('%.2f usec/pass' % per_pass, end=' ')
    per_item = per_pass / range_size
    print('%.2f usec/item' % per_item)

print("%d items" % range_size)
print("%d iterations" % count)
print()

# Using __setitem__ without checking for existing values first
print('__setitem__:', end=' ')
t = timeit.Timer("""
for s, i in l:
    d[s] = i
""", 
setup_statement)
show_results(t.timeit(number=count))

# Using setdefault
print('setdefault :', end=' ')
t = timeit.Timer("""
for s, i in l:
    d.setdefault(s, i)
""",
setup_statement)
show_results(t.timeit(number=count))

# Using has_key
print('has_key    :', end=' ')
t = timeit.Timer("""
for s, i in l:
    if not d.has_key(s):
        d[s] = i
""", 
setup_statement)
show_results(t.timeit(number=count))

# Using exceptions
print('KeyError   :', end=' ')
t = timeit.Timer("""
for s, i in l:
    try:
        existing = d[s]
    except KeyError:
        d[s] = i
""", 
setup_statement)
show_results(t.timeit(number=count))

# Using "in"
print('"not in"   :', end=' ')
t = timeit.Timer("""
for s, i in l:
    if s not in d:
        d[s] = i
""", 
setup_statement)
show_results(t.timeit(number=count))

