#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

#end_pymotw_header

import imp
import sys

for i in range(2):
    print(i, end=' ')
    try:
        m = sys.modules['example']
    except KeyError:
        print('(not in sys.modules)', end=' ')
    else:
        print('(have in sys.modules)', end=' ')
    f, filename, description = imp.find_module('example')
    example_package = imp.load_module('example', f, filename,
                                      description)
