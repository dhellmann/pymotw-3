#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Comparing floating point values
"""
# abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
#end_pymotw_header

import math

print('NaN, NaN:', math.isclose(math.nan, math.nan))
print('NaN, 1.0:', math.isclose(math.nan, 1.0))
print('Inf, Inf:', math.isclose(math.inf, math.inf))
print('Inf, 1.0:', math.isclose(math.inf, 1.0))
