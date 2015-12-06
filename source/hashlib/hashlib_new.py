#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Naming the hash type using a string.
"""
#end_pymotw_header

import hashlib
import sys


try:
    hash_name = sys.argv[1]
except IndexError:
    print('Specify the hash name as the first argument.')
else:
    try:
        data = sys.argv[2]
    except IndexError:
        from hashlib_data import lorem as data

    h = hashlib.new(hash_name)
    h.update(data.encode('utf-8'))
    print(h.hexdigest())
