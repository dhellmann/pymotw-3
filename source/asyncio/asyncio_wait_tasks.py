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


async def start_tasks(loop):
    LOG.debug('in start_tasks')
    LOG.debug('waiting for sub-tasks')
    tasks = [
        loop.create_task(phase1()),
        loop.create_task(phase2()),
    ]
    completed, pending = await asyncio.wait(tasks, loop=loop)
    results =  [ t.result() for t in tasks ]
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

LOG.debug('creating task')
task = event_loop.create_task(start_tasks(event_loop))

try:
    LOG.debug('entering event loop')
    event_loop.run_until_complete(task)
finally:
    LOG.debug('closing event loop')
    event_loop.close()

LOG.debug('task result: %r' % (task.result(),))
