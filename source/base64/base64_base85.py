#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Demonstrates base85 and ascii85 encodings.

http://bugs.python.org/17618
"""
#end_pymotw_header

import base64

original_data = b'This is the data, in the clear.'
print('Original    : %s bytes %r' %
      (len(original_data), original_data))

b64_data = base64.b64encode(original_data)
print('b64 Encoded : %s bytes %r' %
      (len(b64_data), b64_data))

b85_data = base64.b85encode(original_data)
print('b85 Encoded : %s bytes %r' %
      (len(b85_data), b85_data))

a85_data = base64.a85encode(original_data)
print('a85 Encoded : %s bytes %r' %
      (len(a85_data), a85_data))
