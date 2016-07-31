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

namespace_types = sorted(n
                         for n in dir(uuid)
                         if n.startswith('NAMESPACE_')
                         )
name = 'www.doughellmann.com'

for namespace_type in namespace_types:
    print namespace_type
    namespace_uuid = getattr(uuid, namespace_type)
    print ' ', uuid.uuid3(namespace_uuid, name)
    print ' ', uuid.uuid3(namespace_uuid, name)
    print
