#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id$"
#end_pymotw_header

import zlib

input_data = 'Some repeated text.\n' * 1024

results = set()
for i in xrange(1, 10):
    data = zlib.compress(input_data, i)
    results.add(data)

print len(results)
