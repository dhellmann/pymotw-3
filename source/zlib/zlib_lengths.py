#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""
#end_pymotw_header

import zlib

original_data = b'This is the original text.'

fmt = '%15s  %15s'
print(fmt % ('len(data)', 'len(compressed)'))
print(fmt % ('-' * 15, '-' * 15))

for i in range(5):
    data = original_data * i
    compressed = zlib.compress(data)
    highlight = '*' if len(data) < len(compressed) else ''
    print(fmt % (len(data), len(compressed)), highlight)
