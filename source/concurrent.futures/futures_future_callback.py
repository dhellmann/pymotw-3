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
    print('{}: sleeping {}'.format(
        threading.current_thread().name,
        n)
    )
    time.sleep(n / 10)
    print('{}: done with {}'.format(
        threading.current_thread().name,
        n)
    )
    return n / 10


def done(fn):
    print('callback checking status of {}'.format(fn))
    if fn.running():
        print('still running')
    elif fn.cancelled():
        print('cancelled')
    elif fn.done():
        print('done')
        error = fn.exception()
        if error:
            print('error returned: {}'.format(error))
        else:
            result = fn.result()
            print('value returned: {}'.format(result))


if __name__ == '__main__':
    ex = futures.ThreadPoolExecutor(max_workers=2)
    print('main: starting')
    f = ex.submit(task, 5)
    f.add_done_callback(done)
    result = f.result()
