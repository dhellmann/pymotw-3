#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Scheduling a callback with call_later
"""
#end_pymotw_header

import asyncio
import time


def callback(n, loop):
    print('callback {} invoked at {}'.format(n, loop.time()))


def stopper(loop):
    print('stopper invoked at    {}'.format(loop.time()))
    loop.stop()


event_loop = asyncio.get_event_loop()

now = event_loop.time()
print('clock time: {}'.format(time.time()))
print('loop  time: {}'.format(now))

print('registering callbacks')
event_loop.call_at(now + 0.2, callback, 1, event_loop)
event_loop.call_at(now + 0.1, callback, 2, event_loop)
event_loop.call_at(now + 0.3, stopper, event_loop)
event_loop.call_soon(callback, 3, event_loop)

try:
    print('entering event loop')
    event_loop.run_forever()
finally:
    print('closing event loop')
    event_loop.close()
