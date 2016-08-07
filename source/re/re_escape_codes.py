#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Escape codes
"""
#end_pymotw_header

from re_test_patterns import test_patterns

test_patterns(
    'A prime #1 example!',
    [ (r'\d+', 'sequence of digits'),
      (r'\D+', 'sequence of nondigits'),
      (r'\s+', 'sequence of whitespace'),
      (r'\S+', 'sequence of nonwhitespace'),
      (r'\w+', 'alphanumeric characters'),
      (r'\W+', 'nonalphanumeric'),
      ])
