#!/usr/bin/env python3
# encoding: utf-8
#
"""
"""
#end_pymotw_header

from statistics import *

data = [1, 2, 3, 4]

print('1: {:0.2f}'.format(median_grouped(data, interval=1)))
print('2: {:0.2f}'.format(median_grouped(data, interval=2)))
print('3: {:0.2f}'.format(median_grouped(data, interval=3)))
