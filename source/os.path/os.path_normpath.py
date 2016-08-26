#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Compute a "normalized" path.
"""

__version__ = "$Id$"
#end_pymotw_header

import os.path

for path in [ 'one//two//three', 
              'one/./two/./three', 
              'one/../alt/two/three',
              ]:
    print '%20s : %s' % (path, os.path.normpath(path))
