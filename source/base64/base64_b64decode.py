#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""
#end_pymotw_header

import base64

original_string = 'This is the data, in the clear.'
binary_string = original_string.encode('utf-8')

print('Original:', binary_string)

encoded_string = base64.b64encode(binary_string)
print('Encoded :', encoded_string)

decoded_string = base64.b64decode(encoded_string)
print('Decoded :', decoded_string)
