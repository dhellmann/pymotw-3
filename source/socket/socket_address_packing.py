#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Converting between string and binary representations of addresses.
"""
#end_pymotw_header

import binascii
import socket
import struct
import sys

for string_address in [ '192.168.1.1', '127.0.0.1' ]:
    packed = socket.inet_aton(string_address)
    print 'Original:', string_address
    print 'Packed  :', binascii.hexlify(packed)
    print 'Unpacked:', socket.inet_ntoa(packed)
    print
