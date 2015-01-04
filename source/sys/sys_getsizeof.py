#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2009 Doug Hellmann All rights reserved.
#
"""
"""
#end_pymotw_header

import sys

class OldStyle:
    pass

class NewStyle(object):
    pass

for obj in [ [], (), {}, 'c', 'string', 1, 2.3, 
             OldStyle, OldStyle(), NewStyle, NewStyle(),
             ]:
    print '%10s : %s' % (type(obj).__name__, sys.getsizeof(obj))
