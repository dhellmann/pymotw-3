#!/usr/bin/env python
"""Creating a new shelf.
"""
#end_pymotw_header

import shelve
from contextlib import closing

with closing(shelve.open('test_shelf.db')) as s:
    s['key1'] = { 'int': 10, 'float':9.5, 'string':'Sample data' }
