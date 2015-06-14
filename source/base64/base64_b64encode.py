#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""
#end_pymotw_header

import base64
import textwrap

# Load this source file and strip the header.
with open(__file__, 'r', encoding='utf-8') as input:
    raw = input.read()
    initial_data = raw.split('#end_pymotw_header')[1]

binary_data = initial_data.encode('utf-8')
encoded_data = base64.b64encode(binary_data)

num_initial = len(binary_data)

# There will never be more than 2 padding bytes.
padding = 3 - (num_initial % 3)

print('%d bytes before encoding' % num_initial)
print('Expect %d padding bytes' % padding)
print('%d bytes after encoding\n' % len(encoded_data))
print(encoded_data)
