#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Basic trigonometric functions
"""
#end_pymotw_header

import math

print 'Degrees  Radians  Sine     Cosine    Tangent'
print '-------  -------  -------  --------  -------'

fmt = '  '.join(['%7.2f'] * 5)

for deg in range(0, 361, 30):
    rad = math.radians(deg)
    if deg in (90, 270):
        t = float('inf')
    else:
        t = math.tan(rad)
    print fmt % (deg, rad, math.sin(rad), math.cos(rad), t)
