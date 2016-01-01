#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Using an event primitive
"""
#end_pymotw_header

import asyncio
import functools


def set_event(event):
    print('setting event in callback')
    event.set()


async def coro1(event):
    print('coro1 waiting for event')
    await event.wait()
    print('coro1 triggered')


async def coro2(event):
    print('coro2 waiting for event')
    await event.wait()
    print('coro2 triggered')


event_loop = asyncio.get_event_loop()
try:
    # Create a shared event
    event = asyncio.Event(loop=event_loop)
    print('event state: {}'.format(event.is_set()))

    event_loop.call_later(
        0.1, functools.partial(set_event, event)
    )

    print('entering event loop')
    result = event_loop.run_until_complete(
        asyncio.wait([coro1(event),
                      coro2(event)]),
    )
    print('exited event loop')

    print('event state: {}'.format(event.is_set()))
finally:
    event_loop.close()
