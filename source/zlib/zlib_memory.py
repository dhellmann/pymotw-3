#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id$"
#end_pymotw_header

import zlib
import binascii

original_data = 'This is the original text.'
print 'Original     :', len(original_data), original_data

compressed = zlib.compress(original_data)
print 'Compressed   :', len(compressed), binascii.hexlify(compressed)

decompressed = zlib.decompress(compressed)
print 'Decompressed :', len(decompressed), decompressed
