#!/usr/bin/env python3
"""Using repeat() with izip().
"""
#end_pymotw_header

from itertools import *

for i, s in izip(count(), repeat('over-and-over', 5)):
    print(i, s)
