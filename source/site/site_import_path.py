#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""The default import path from site
"""
#end_pymotw_header

import sys
import os
import platform
import site

if 'Windows' in platform.platform():
    SUFFIXES = [
        '',
        'lib/site-packages',
        ]
else:
    SUFFIXES = [
        'lib/python%s/site-packages' % sys.version[:3],
        'lib/site-python',
        ]

print 'Path prefixes:'
for p in site.PREFIXES:
    print '  ', p

for prefix in sorted(set(site.PREFIXES)):
    print
    print prefix
    for suffix in SUFFIXES:
        print
        print ' ', suffix
        path = os.path.join(prefix, suffix).rstrip(os.sep)
        print '   exists :', os.path.exists(path)
        print '   in path:', path in sys.path
