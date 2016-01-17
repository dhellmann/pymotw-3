#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Random values from a range
"""
#end_pymotw_header

import random

for i in xrange(3):
    print random.randrange(0, 101, 5),
print

