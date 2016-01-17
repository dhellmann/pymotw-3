#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Generate random numbers
"""
#end_pymotw_header

import random

for i in xrange(5):
    print '%04.3f' % random.random(),
print

