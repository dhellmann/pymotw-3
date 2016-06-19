#!/usr/bin/env python
"""Modifying an existing shelf opened with write-back enabled.
"""
#end_pymotw_header

import shelve
from contextlib import closing

with closing(shelve.open('test_shelf.db')) as s:
    print s['key1']
    s['key1']['new_value'] = 'this was not here before'

with closing(shelve.open('test_shelf.db', writeback=True)) as s:
    print s['key1']

