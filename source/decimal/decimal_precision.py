#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2009 Doug Hellmann All rights reserved.
#
"""
"""
#end_pymotw_header

import decimal

d = decimal.Decimal('0.123456')

for i in range(4):
    decimal.getcontext().prec = i
    print i, ':', d, d * 1
