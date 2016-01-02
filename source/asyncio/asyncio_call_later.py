#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Scheduling a callback with call_later
"""
#end_pymotw_header

import asyncio


def callback(n):
    print('callback {} invoked'.format(n))


def stopper(loop):
    print('stopper invoked')
    loop.stop()


event_loop = asyncio.get_event_loop()
try:
    print('registering callbacks')
    event_loop.call_later(0.2, callback, 1)
    event_loop.call_later(0.1, callback, 2)
    event_loop.call_later(0.3, stopper, event_loop)
    event_loop.call_soon(callback, 3)

    print('entering event loop')
    event_loop.run_forever()
finally:
    print('closing event loop')
    event_loop.close()
