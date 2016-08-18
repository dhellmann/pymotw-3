#!/usr/bin/env python
"""Using getmembers()
"""
#end_pymotw_header

import inspect

import example

for name, data in inspect.getmembers(example):
    if name.startswith('__'):
        continue
    print '%s : %r' % (name, data)
