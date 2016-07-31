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

for node in [ 0x1ec200d9e0, 0x1e5274040e ]:
    print uuid.uuid1(node), hex(node)
