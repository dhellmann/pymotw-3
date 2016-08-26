#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Compute an absolute path from a relative path.
"""

#end_pymotw_header

import os
import os.path

os.chdir('/tmp')

for path in [ '.',
              '..',
              './one/two/three',
              '../one/two/three',
              ]:
    print('%17s : "%s"' % (path, os.path.abspath(path)))
