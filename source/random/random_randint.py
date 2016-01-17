#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Generating random integers.
"""
#end_pymotw_header

import random

print '[1, 100]:',

for i in xrange(3):
    print random.randint(1, 100),

print '\n[-5, 5]:',
for i in xrange(3):
    print random.randint(-5, 5),
print

