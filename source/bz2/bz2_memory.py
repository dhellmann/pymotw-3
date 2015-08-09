#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id$"
#end_pymotw_header

import bz2
import binascii

original_data = 'This is the original text.'
print 'Original     : %d bytes' % len(original_data)
print original_data

print
compressed = bz2.compress(original_data)
print 'Compressed   : %d bytes' % len(compressed)
hex_version = binascii.hexlify(compressed)
for i in xrange(len(hex_version)/40 + 1):
    print hex_version[i*40:(i+1)*40]

print
decompressed = bz2.decompress(compressed)
print 'Decompressed : %d bytes' % len(decompressed)
print decompressed
