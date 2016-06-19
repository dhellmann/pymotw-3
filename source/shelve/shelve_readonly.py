#!/usr/bin/env python
"""Opening an existing shelf read-only.
"""
#end_pymotw_header

import shelve
from contextlib import closing

with closing(shelve.open('test_shelf.db', flag='r')) as s:
    existing = s['key1']

print existing
