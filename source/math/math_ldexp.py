#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""From mantissa, exponent pair to floating point value.
"""
#end_pymotw_header

import math

print '{:^7}  {:^7}  {:^7}'.format('m', 'e', 'x')
print '{:-^7}  {:-^7}  {:-^7}'.format('', '', '')

for m, e in [ (0.8, -3),
              (0.5,  0),
              (0.5,  3),
              ]:
    x = math.ldexp(m, e)
    print '{:7.2f}  {:7d}  {:7.2f}'.format(m, e, x)
