#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Multiline input
"""
#end_pymotw_header

import re

text = 'This is some text -- with punctuation.\nA second line.'
pattern = r'(^\w+)|(\w+\S*$)'
single_line = re.compile(pattern)
multiline = re.compile(pattern, re.MULTILINE)

print 'Text:\n  %r' % text
print 'Pattern:\n  %s' % pattern
print 'Single Line :'
for match in single_line.findall(text):
    print '  %r' % (match,)
print 'Multline    :'
for match in multiline.findall(text):
    print '  %r' % (match,)
