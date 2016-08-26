#!/usr/bin/env python
"""Example use of linecache module.
"""
#end_pymotw_header

import linecache
from linecache_data import *

filename = make_tempfile()

# The cache always returns a string, and uses
# an empty string to indicate a line which does
# not exist.
not_there = linecache.getline(filename, 500)
print 'NOT THERE: %r includes %d characters' % \
    (not_there, len(not_there))

cleanup(filename)
