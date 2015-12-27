#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Starting a task
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


async def task_func(loop):
    LOG.debug('in task_func')
    LOG.debug('scheduling second task without waiting')
    loop.create_task(second_task())
    LOG.debug('scheduled')
    return 'the result'


async def second_task():
    LOG.debug('in second_task')
    await asyncio.sleep(1)
    LOG.debug('done with second_task')


event_loop = asyncio.get_event_loop()

LOG.debug('creating task')
task = event_loop.create_task(task_func(event_loop))
LOG.debug('task: %r' % (task,))

try:
    LOG.debug('entering event loop')
    event_loop.run_until_complete(task)
    LOG.debug('task: %r' % (task,))
finally:
    LOG.debug('closing event loop')
    event_loop.close()

LOG.debug('task result: %r' % (task.result(),))
