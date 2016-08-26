#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Separate a filename into the base and extension.
"""

__version__ = "$Id$"
#end_pymotw_header

import os.path

for path in [ 'filename.txt',
              'filename',
              '/path/to/filename.txt',
              '/',
              '',
              'my-archive.tar.gz',
              'no-extension.',
              ]:
    print '%21s :' % path, os.path.splitext(path)
