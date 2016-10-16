#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Future callbacks
"""
#end_pymotw_header

import asyncio
import functools


def callback(future, n):
    print('{}: future done: {}'.format(n, future.result()))


event_loop = asyncio.get_event_loop()
try:
    print('registering callbacks on future')
    all_done = asyncio.Future()
    all_done.add_done_callback(functools.partial(callback, n=1))
    all_done.add_done_callback(functools.partial(callback, n=2))

    print('setting result of future')
    all_done.set_result('the result')

    print('entering event loop')
    event_loop.run_until_complete(all_done)
finally:
    event_loop.close()
