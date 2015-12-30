#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Starting a task, then canceling it
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


async def task_func():
    LOG.info('in task_func, sleeping')
    try:
        await asyncio.sleep(1)
    except asyncio.CancelledError:
        LOG.info('task_func was cancelled')
        raise
    return 'the result'


async def task_canceller(t):
    LOG.info('in task_canceller')
    t.cancel()
    LOG.info('cancelled the task')


event_loop = asyncio.get_event_loop()

LOG.info('creating task')
task = event_loop.create_task(task_func())

try:
    LOG.info('entering event loop')
    event_loop.run_until_complete(task_canceller(task))
finally:
    LOG.info('closing event loop')
    event_loop.close()
