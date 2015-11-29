#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2009 Doug Hellmann All rights reserved.
#
"""
"""
#end_pymotw_header

import decimal
import fractions

for v in [ decimal.Decimal('0.1'), 
           decimal.Decimal('0.5'), 
           decimal.Decimal('1.5'), 
           decimal.Decimal('2.0'),
           ]:
    print '%s = %s' % (v, fractions.Fraction.from_decimal(v))
