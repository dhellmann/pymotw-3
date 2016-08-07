#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Simple pattern examples.
"""
#end_pymotw_header

import re

patterns = [ 'this', 'that' ]
text = 'Does this text match the pattern?'

print 'Text: %r\n' % text

for pattern in patterns:
    print 'Seeking "%s" ->' % pattern, 

    if re.search(pattern,  text) is None:
        print 'no match'
    else:
        print 'match!'
