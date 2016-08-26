#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Find the directory portion of a filename.
"""

#end_pymotw_header

import os.path

for path in [ '/one/two/three', 
              '/one/two/three/',
              '/',
              '.',
              '']:
    print('%15s : %s' % (path, os.path.dirname(path)))
