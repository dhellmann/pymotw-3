#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""
#end_pymotw_header

import gzip

with gzip.open('example.txt.gz', 'rb') as input_file:
    print(input_file.read())
