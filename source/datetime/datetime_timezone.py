#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Datetime with timezone
"""
#end_pymotw_header

import datetime

min5 = datetime.timezone(datetime.timedelta(hours=-5))
plus5 = datetime.timezone(datetime.timedelta(hours=5))
d = datetime.datetime.now(min5)
print('-5 zone    :', min5)
print('UTC zone   :', datetime.timezone.utc)
print('+5 zone    :', plus5)
print('UTC-5 time :', d)
print('UTC time   :', d.astimezone(datetime.timezone.utc))
print('UTC+5 time :', d.astimezone(plus5))
