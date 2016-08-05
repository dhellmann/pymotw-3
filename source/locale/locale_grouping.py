#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""
"""
#end_pymotw_header

import locale

sample_locales = [
    ('USA', 'en_US'),
    ('France', 'fr_FR'),
    ('Spain', 'es_ES'),
    ('Portugal', 'pt_PT'),
    ('Poland', 'pl_PL'),
]

print('%10s %15s %20s' % ('Locale', 'Integer', 'Float'))
for name, loc in sample_locales:
    locale.setlocale(locale.LC_ALL, loc)

    print('%10s' % name, end=' ')
    print(locale.format('%15d', 123456, grouping=True), end=' ')
    print(locale.format('%20.2f', 123456.78, grouping=True))
