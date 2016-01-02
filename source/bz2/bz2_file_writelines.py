#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""
#end_pymotw_header

import bz2
import itertools
import os

data = 'The same line, over and over.\n'.encode('utf-8')

with bz2.BZ2File('lines.bz2', 'wb') as output:
    output.writelines(
        itertools.repeat(data, 10),
    )

os.system('bzcat lines.bz2')
