#!/usr/bin/env python3
"""Using izip()
"""
#end_pymotw_header

from itertools import *

for i in izip([1, 2, 3], ['a', 'b', 'c']):
    print(i)
