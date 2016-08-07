#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""
#end_pymotw_header

import zlib

data = open('lorem.txt', 'rb').read()

cksum = zlib.adler32(data)
print('Adler32: %12d' % cksum)
print('       : %12d' % zlib.adler32(data, cksum))

cksum = zlib.crc32(data)
print('CRC-32 : %12d' % cksum)
print('       : %12d' % zlib.crc32(data, cksum))
