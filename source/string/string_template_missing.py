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

values = { 'var':'foo' }

t = string.Template("$var is here but $missing is not provided")

try:
    print 'substitute()     :', t.substitute(values)
except KeyError, err:
    print 'ERROR:', str(err)
    
print 'safe_substitute():', t.safe_substitute(values)
