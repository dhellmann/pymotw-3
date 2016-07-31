#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id$"
#end_pymotw_header

import uuid

hostnames = ['www.doughellmann.com', 'blog.doughellmann.com']

for name in hostnames:
    print name
    print '  MD5   :', uuid.uuid3(uuid.NAMESPACE_DNS, name)
    print '  SHA-1 :', uuid.uuid5(uuid.NAMESPACE_DNS, name)
    print
