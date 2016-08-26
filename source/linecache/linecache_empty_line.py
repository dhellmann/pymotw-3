#!/usr/bin/env python
"""Example use of linecache module.
"""
#end_pymotw_header

import linecache
from linecache_data import *

filename = make_tempfile()

# Blank lines include the newline
print 'BLANK : %r' % linecache.getline(filename, 8)

cleanup(filename)
