#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Show the groups within the matches for a pattern.
"""
#end_pymotw_header

import re

def test_patterns(text, patterns=[]):
    """Given source text and a list of patterns, look for
    matches for each pattern within the text and print
    them to stdout.
    """
    # Look for each pattern in the text and print the results
    for pattern, desc in patterns:
        print 'Pattern %r (%s)\n' % (pattern, desc)
        print '  %r' % text
        for match in re.finditer(pattern, text):
            s = match.start()
            e = match.end()
            prefix = ' ' * (s)
            print '  %s%r%s ' % (prefix, text[s:e], ' '*(len(text)-e)),
            print match.groups()
            if match.groupdict():
                print '%s%s' % (' ' * (len(text)-s), match.groupdict())
        print
    return
