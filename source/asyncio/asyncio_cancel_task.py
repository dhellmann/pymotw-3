#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Starting a task, then canceling it
"""
#end_pymotw_header

import asyncio
import functools


async def task_func():
    print('in task_func')
    return 'the result'


event_loop = asyncio.get_event_loop()
try:
    print('creating task')
    task = event_loop.create_task(task_func())

    print('canceling task')
    task.cancel()

    print('entering event loop')
    event_loop.run_until_complete(task)
    print('task: {!r}'.format(task))
except asyncio.CancelledError:
    print('caught error from cancelled task')
else:
    print('task result: {!r}'.format(task.result()))
finally:
    event_loop.close()
