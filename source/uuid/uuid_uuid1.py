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

u = uuid.uuid1()

print u
print type(u)
print 'bytes   :', repr(u.bytes)
print 'hex     :', u.hex
print 'int     :', u.int
print 'urn     :', u.urn
print 'variant :', u.variant
print 'version :', u.version
print 'fields  :', u.fields
print '\ttime_low            : ', u.time_low
print '\ttime_mid            : ', u.time_mid
print '\ttime_hi_version     : ', u.time_hi_version
print '\tclock_seq_hi_variant: ', u.clock_seq_hi_variant
print '\tclock_seq_low       : ', u.clock_seq_low
print '\tnode                : ', u.node
print '\ttime                : ', u.time
print '\tclock_seq           : ', u.clock_seq
