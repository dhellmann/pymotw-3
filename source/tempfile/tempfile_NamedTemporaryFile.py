#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

#end_pymotw_header

import os
import tempfile

with tempfile.NamedTemporaryFile() as temp:
    print 'temp:'
    print '  ', temp
    print 'temp.name:'
    print '  ', temp.name

print 'Exists after close:', os.path.exists(temp.name)
