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
    print('{}: starting'.format(n))
    raise ValueError('the value {} is no good'.format(n))
    print('{}: done'.format(n))
    return n / 10


ex = futures.ThreadPoolExecutor(max_workers=2)
print('main: starting')
f = ex.submit(task, 5)

error = f.exception()
print('main: error: {}'.format(error))

try:
    result = f.result()
except ValueError as e:
    print('main: saw error "{}" when accessing result'.format(e))
else:
    print('main: result: {}'.format(result))
