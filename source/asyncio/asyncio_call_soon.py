#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Scheduling a callback with call_soon
"""

#end_pymotw_header
import asyncio


def callback():
    print('callback invoked')


def stopper(loop):
    print('stopper invoked')
    loop.stop()


event_loop = asyncio.get_event_loop()
try:
    print('registering callbacks')
    event_loop.call_soon(callback)
    event_loop.call_soon(stopper, event_loop)

    print('entering event loop')
    event_loop.run_forever()
finally:
    print('closing event loop')
    event_loop.close()
