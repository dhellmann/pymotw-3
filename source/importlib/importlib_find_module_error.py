#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

#end_pymotw_header

import imp

try:
    imp.find_module('no_such_module')
except ImportError, err:
    print('ImportError:', err)

