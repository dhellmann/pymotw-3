#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Determine the base filename from a path.
"""

#end_pymotw_header

import os.path

for path in [ '/one/two/three', 
              '/one/two/three/',
              '/',
              '.',
              '']:
    print('%15s : %s' % (path, os.path.basename(path)))
