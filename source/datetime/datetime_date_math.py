#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Calculations with dates.
"""

__version__ = "$Id$"
#end_pymotw_header

import datetime

today = datetime.date.today()
print 'Today    :', today

one_day = datetime.timedelta(days=1)
print 'One day  :', one_day

yesterday = today - one_day
print 'Yesterday:', yesterday

tomorrow = today + one_day
print 'Tomorrow :', tomorrow

print
print 'tomorrow - yesterday:', tomorrow - yesterday
print 'yesterday - tomorrow:', yesterday - tomorrow
