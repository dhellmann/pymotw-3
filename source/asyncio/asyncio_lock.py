#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Using a lock primitive
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


def unlock(lock):
    LOG.debug('releasing lock')
    lock.release()


async def coro1(lock, future):
    LOG.debug('in coro1')
    with await lock:
        LOG.debug('coro1 acquired lock')
    LOG.debug('coro1 released lock')
    future.set_result(True)


async def coro2(lock, future):
    LOG.debug('in coro2')
    await lock
    try:
        LOG.debug('coro2 acquired lock')
    finally:
        LOG.debug('coro2 released lock')
        lock.release()
    future.set_result(True)


event_loop = asyncio.get_event_loop()

# Create a shared lock
lock = asyncio.Lock(loop=event_loop)

# Create some futures to let us know when
# both coroutines are done.
f1 = asyncio.Future(loop=event_loop)
f2 = asyncio.Future(loop=event_loop)

try:
    LOG.debug('acquiring the lock')
    event_loop.run_until_complete(lock.acquire())
    LOG.debug('lock acquired: {}'.format(lock.locked()))

    event_loop.call_later(1, functools.partial(unlock, lock))
    event_loop.create_task(coro1(lock, f1))
    event_loop.create_task(coro2(lock, f2))

    LOG.debug('entering event loop')
    result = event_loop.run_until_complete(
        asyncio.wait([f1, f2], loop=event_loop),
    )
    LOG.debug('exited event loop')

    LOG.debug('lock acquired: {}'.format(lock.locked()))
finally:
    LOG.debug('closing event loop')
    event_loop.close()
