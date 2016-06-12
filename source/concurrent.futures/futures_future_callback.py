#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2016 Doug Hellmann.  All rights reserved.
# Written for https://pymotw.com
#
"""Done callbacks.
"""
#end_pymotw_header

import argparse
from concurrent import futures
import threading
import time


def task(n):
    print('{}: sleeping'.format(n))
    time.sleep(0.5)
    print('{}: done'.format(n))
    return n / 10


def get_state(fn):
    if fn.running():
        return 'running'
    elif fn.cancelled():
        return 'cancelled'
    elif fn.done():
        return 'no longer running'
    else:
        return 'unknown state'


def done(fn):
    print('{}: {}'.format(fn.arg, get_state(fn)))
    if not fn.done():
        return
    if fn.cancelled():
        return
    error = fn.exception()
    if error:
        print('{}: error returned: {}'.format(fn.arg, error))
    else:
        result = fn.result()
        print('{}: value returned: {}'.format(fn.arg, result))


if __name__ == '__main__':
    ex = futures.ThreadPoolExecutor(max_workers=2)
    print('main: starting')
    f = ex.submit(task, 5)
    f.arg = 5
    f.add_done_callback(done)
    result = f.result()
