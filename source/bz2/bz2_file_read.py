#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""
#end_pymotw_header

import bz2

with bz2.BZ2File('example.bz2', 'r') as input:
    print(input.read())
