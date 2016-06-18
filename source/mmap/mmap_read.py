#!/usr/bin/env python
#
# Copyright 2007 Doug Hellmann.
#
"""Reading from a memory mapped file.

"""

#end_pymotw_header

import mmap
import contextlib

with open('lorem.txt', 'r') as f:
    with contextlib.closing(mmap.mmap(f.fileno(), 0,
                                      access=mmap.ACCESS_READ)
                            ) as m:
        print 'First 10 bytes via read :', m.read(10)
        print 'First 10 bytes via slice:', m[:10]
        print '2nd   10 bytes via read :', m.read(10)
