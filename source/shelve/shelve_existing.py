#!/usr/bin/env python
"""Opening an existing shelf.
"""
#end_pymotw_header

import shelve
from contextlib import closing

with closing(shelve.open('test_shelf.db')) as s:
    existing = s['key1']

print existing
