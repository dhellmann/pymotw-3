#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Expand tilde in filenames.
"""

#end_pymotw_header

import os.path

for user in [ '', 'dhellmann', 'postgresql' ]:
    lookup = '~' + user
    print '%12s : %s' % (lookup, os.path.expanduser(lookup))
