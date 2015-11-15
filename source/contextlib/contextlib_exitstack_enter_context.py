#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2015 Doug Hellmann.  All rights reserved.
"""
"""
#end_pymotw_header

import contextlib


@contextlib.contextmanager
def make_context(i):
    print('%s entering' % i)
    yield {}
    print('%s exiting' % i)


def variable_stack(n, msg):
    with contextlib.ExitStack() as stack:
        for i in range(n):
            stack.enter_context(make_context(i))
        print(msg)


variable_stack(2, 'inside context')
