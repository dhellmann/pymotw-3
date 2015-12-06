#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""The range of valid datetime values.
"""

__version__ = "$Id$"
#end_pymotw_header

import datetime

print 'Earliest  :', datetime.datetime.min
print 'Latest    :', datetime.datetime.max
print 'Resolution:', datetime.datetime.resolution
