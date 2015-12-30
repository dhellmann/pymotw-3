#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Starting one coroutine from within another
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


async def outer(loop):
    LOG.info('in outer')
    result1 = await phase1()
    result2 = await phase2(result1)
    return (result1, result2)


async def phase1():
    LOG.info('in phase1')
    return 'result1'


async def phase2(arg):
    LOG.info('in phase2')
    return 'result2 derived from {}'.format(arg)


event_loop = asyncio.get_event_loop()

LOG.info('creating task')
task = event_loop.create_task(outer(event_loop))
LOG.info('task: %r' % (task,))

try:
    LOG.info('entering event loop')
    event_loop.run_until_complete(task)
finally:
    LOG.info('closing event loop')
    event_loop.close()

LOG.info('task result: {!r}'.format(task.result()))
