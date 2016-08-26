#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Separate a path into its directory and base components.
"""

#end_pymotw_header

import os.path

for path in [ '/one/two/three', 
              '/one/two/three/',
              '/',
              '.',
              '']:
    print '%15s : %s' % (path, os.path.split(path))
