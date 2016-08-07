#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""
#end_pymotw_header

import zlib

input_data = 'Some repeated text.\n' * 1024

results = set()
for i in range(1, 10):
    data = zlib.compress(input_data, i)
    results.add(data)

print(len(results))
