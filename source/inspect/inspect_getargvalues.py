#!/usr/bin/env python3
"""Inspecting the call stack.
"""
#end_pymotw_header

import inspect


def recurse(limit):
    local_variable = '.' * limit
    print(limit, inspect.getargvalues(inspect.currentframe()))
    if limit <= 0:
        return
    recurse(limit - 1)
    return local_variable

if __name__ == '__main__':
    recurse(2)
