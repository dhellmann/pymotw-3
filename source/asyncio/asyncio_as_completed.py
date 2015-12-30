#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Dealing with individual background tasks as they finish
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


async def start_coroutines(loop):
    LOG.debug('in start_coroutines')
    LOG.debug('waiting for sub-tasks')
    coroutines = [
        phase1(),
        phase2(),
    ]
    results = []
    for task in asyncio.as_completed(coroutines, loop=loop):
        answer = await task
        results.append(answer)
    LOG.debug('completed, results: {!r}'.format(results))
    return results


async def phase1():
    LOG.debug('in phase1')
    await asyncio.sleep(2)
    LOG.debug('done with phase1')
    return 'phase1 result'


async def phase2():
    LOG.debug('in phase2')
    await asyncio.sleep(1)
    LOG.debug('done with phase2')
    return 'phase2 result'


event_loop = asyncio.get_event_loop()

try:
    LOG.debug('entering event loop')
    result = event_loop.run_until_complete(start_coroutines(event_loop))
finally:
    LOG.debug('closing event loop')
    event_loop.close()

LOG.debug('result: %r' % (result,))
