#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""
#end_pymotw_header

import bz2
import os

data = open('lorem.txt', 'r').read() * 1024
print('Input contains {} bytes'.format(len(data)))

for i in range(1, 10):
    filename = 'compress-level-{}.bz2'.format(i)
    with bz2.BZ2File(filename, 'wb', compresslevel=i) as output:
        output.write(data)
    os.system('cksum {}'.format(filename))
