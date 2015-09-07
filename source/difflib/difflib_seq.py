#!/usr/bin/env python
#
# Copyright 2007 Doug Hellmann.
#
"""SequenceMatcher example
"""

#end_pymotw_header

import difflib
from difflib_data import *

s1 = [ 1, 2, 3, 5, 6, 4 ]
s2 = [ 2, 3, 5, 4, 6, 1 ]

print 'Initial data:'
print 's1 =', s1
print 's2 =', s2
print 's1 == s2:', s1==s2
print

matcher = difflib.SequenceMatcher(None, s1, s2)
for tag, i1, i2, j1, j2 in reversed(matcher.get_opcodes()):

    if tag == 'delete':
        print 'Remove %s from positions [%d:%d]' % \
            (s1[i1:i2], i1, i2)
        del s1[i1:i2]

    elif tag == 'equal':
        print 's1[%d:%d] and s2[%d:%d] are the same' % \
            (i1, i2, j1, j2)

    elif tag == 'insert':
        print 'Insert %s from s2[%d:%d] into s1 at %d' % \
            (s2[j1:j2], j1, j2, i1)
        s1[i1:i2] = s2[j1:j2]

    elif tag == 'replace':
        print 'Replace %s from s1[%d:%d] with %s from s2[%d:%d]' % (
            s1[i1:i2], i1, i2, s2[j1:j2], j1, j2)
        s1[i1:i2] = s2[j1:j2]

    print '  s1 =', s1

print 's1 == s2:', s1==s2
