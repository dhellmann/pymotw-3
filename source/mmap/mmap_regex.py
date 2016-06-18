#!/usr/bin/env python
#
# Copyright 2007 Doug Hellmann.
#
"""Searching memory mapped files with regular expressions.
"""

__version__ = "$Id$"
#end_pymotw_header

import mmap
import re
import contextlib

pattern = re.compile(r'(\.\W+)?([^.]?nulla[^.]*?\.)',
                     re.DOTALL | re.IGNORECASE | re.MULTILINE)

with open('lorem.txt', 'r') as f:
    with contextlib.closing(mmap.mmap(f.fileno(), 0,
                                      access=mmap.ACCESS_READ)
                            ) as m:
        for match in pattern.findall(m):
            print match[1].replace('\n', ' ')
