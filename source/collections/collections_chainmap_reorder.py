#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2015 Doug Hellmann.  All rights reserved.
#
"""Reading values from a ChainMap after reordering it
"""
#end_pymotw_header

import collections

a = {'a': 'A', 'c': 'C'}
b = {'b': 'B', 'c': 'D'}

m = collections.ChainMap(a, b)

print(m.maps)
print('c = %s\n' % m['c'])

# reverse the list
m.maps = list(reversed(m.maps))

print(m.maps)
print('c = %s' % m['c'])
