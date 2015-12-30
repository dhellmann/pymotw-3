#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Using an event primitive
"""
#end_pymotw_header

import asyncio
import functools
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(message)s',
    stream=sys.stderr,
)
LOG = logging.getLogger('')


def set_event(event):
    LOG.debug('setting event')
    event.set()


async def coro1(event, future):
    LOG.debug('in coro1')
    await event.wait()
    LOG.debug('coro1 triggered')
    future.set_result(True)


async def coro2(event, future):
    LOG.debug('in coro2')
    await event.wait()
    LOG.debug('coro2 triggered')
    future.set_result(True)


event_loop = asyncio.get_event_loop()

# Create an event
event = asyncio.Event(loop=event_loop)

# Create some futures to let us know when
# both coroutines are done.
f1 = asyncio.Future(loop=event_loop)
f2 = asyncio.Future(loop=event_loop)

try:
    event_loop.call_later(1, functools.partial(set_event, event))
    event_loop.create_task(coro1(event, f1))
    event_loop.create_task(coro2(event, f2))

    LOG.debug('entering event loop')
    result = event_loop.run_until_complete(
        asyncio.wait([f1, f2], loop=event_loop),
    )
    LOG.debug('exited event loop')

    LOG.debug('event set: {}'.format(event.is_set()))
finally:
    LOG.debug('closing event loop')
    event_loop.close()
