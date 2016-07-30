#!/usr/bin/env python3
"""Using repeat() and imap()
"""
#end_pymotw_header

from itertools import *

for i in imap(lambda x,y: (x, y, x*y), repeat(2), xrange(5)):
    print('%d * %d = %d' % i)
