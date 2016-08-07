#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Match objects.
"""
#end_pymotw_header

import re

pattern = 'this'
text = 'Does this text match the pattern?'

match = re.search(pattern, text)

s = match.start()
e = match.end()

print 'Found "%s"\nin "%s"\nfrom %d to %d ("%s")' % \
    (match.re.pattern, match.string, s, e, text[s:e])
