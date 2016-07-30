#!/usr/bin/env python3
"""Using count()
"""
#end_pymotw_header

from itertools import *

for i in izip(count(1), ['a', 'b', 'c']):
    print(i)
