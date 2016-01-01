#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Using a lock primitive
"""
#end_pymotw_header

import asyncio
import functools


def unlock(lock):
    print('callback releasing lock')
    lock.release()


async def coro1(lock):
    print('coro1 waiting for the lock')
    with await lock:
        print('coro1 acquired lock')
    print('coro1 released lock')


async def coro2(lock):
    print('coro2 waiting for the lock')
    await lock
    try:
        print('coro2 acquired lock')
    finally:
        print('coro2 released lock')
        lock.release()


event_loop = asyncio.get_event_loop()
try:
    # Create and acquire a shared lock.
    lock = asyncio.Lock()
    print('acquiring the lock before starting coroutines')
    event_loop.run_until_complete(lock.acquire())
    print('lock acquired: {}'.format(lock.locked()))

    # Schedule a callback to unlock the lock.
    event_loop.call_later(0.1, functools.partial(unlock, lock))

    # Run the coroutines that want to use the lock.
    print('entering event loop')
    event_loop.run_until_complete(
        asyncio.wait([coro1(lock),
                      coro2(lock)]),
    )
    print('exited event loop')

    print('lock status: {}'.format(lock.locked()))
finally:
    event_loop.close()
