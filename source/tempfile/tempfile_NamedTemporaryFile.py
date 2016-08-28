#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id$"
#end_pymotw_header

import os
import tempfile

with tempfile.NamedTemporaryFile() as temp:
    print 'temp:'
    print '  ', temp
    print 'temp.name:'
    print '  ', temp.name

print 'Exists after close:', os.path.exists(temp.name)
