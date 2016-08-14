#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""OverflowError
"""
#end_pymotw_header

x = 10.0 ** 200

print 'x    =', x
print 'x*x  =', x*x
try:
    print 'x**2 =', x**2
except OverflowError, err:
    print err
