#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id$"
#end_pymotw_header

import string

for name in (s
             for s in dir(string)
             if not s.startswith('_')):
    value = getattr(string, name)
    # Look for byte string and unicode values
    if isinstance(value, basestring):
        print '%s=%r\n' % (name, value)
