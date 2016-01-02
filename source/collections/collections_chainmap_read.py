#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2015 Doug Hellmann.  All rights reserved.
#
"""Reading values from a ChainMap
"""
#end_pymotw_header

import collections

a = {'a': 'A', 'c': 'C'}
b = {'b': 'B', 'c': 'D'}

m = collections.ChainMap(a, b)

print('Individual Values')
print('a = %s' % m['a'])
print('b = %s' % m['b'])
print('c = %s' % m['c'])
print()

print('Keys = %s' % list(m.keys()))
print('Values = %s' % list(m.values()))
print()

print('Items:')
for k, v in m.items():
    print('%s = %s' % (k, v))
print()

print('"d" in m: %s' % ('d' in m))
