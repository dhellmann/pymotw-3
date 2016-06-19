#!/usr/bin/env python
"""Modifying an existing shelf opened with write-back enabled.
"""
#end_pymotw_header

import shelve
import pprint
from contextlib import closing

with closing(shelve.open('test_shelf.db', writeback=True)) as s:
    print 'Initial data:'
    pprint.pprint(s['key1'])
    
    s['key1']['new_value'] = 'this was not here before'
    print '\nModified:'
    pprint.pprint(s['key1'])

with closing(shelve.open('test_shelf.db', writeback=True)) as s:
    print '\nPreserved:'
    pprint.pprint(s['key1'])
