#!/usr/bin/env python3
"""Opening an existing shelf read-only.
"""
#end_pymotw_header

import shelve

with shelve.open('test_shelf.db', flag='r') as s:
    existing = s['key1']

print(existing)
