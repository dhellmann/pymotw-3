#!/usr/bin/env python3
"""Using cycle().
"""
#end_pymotw_header

from itertools import *

for i, item in izip(xrange(7), cycle(['a', 'b', 'c'])):
    print(i, item)
