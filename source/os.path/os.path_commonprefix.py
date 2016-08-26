#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Find the prefix string common to a group of paths.
"""

__version__ = "$Id$"
#end_pymotw_header

import os.path

paths = ['/one/two/three/four',
         '/one/two/threefold',
         '/one/two/three/',
         ]
for path in paths:
    print 'PATH:', path

print
print 'PREFIX:', os.path.commonprefix(paths)
