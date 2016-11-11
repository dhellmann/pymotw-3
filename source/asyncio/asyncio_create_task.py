#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Starting a task
"""

#end_pymotw_header
import asyncio


async def task_func():
    print('in task_func')
    return 'the result'


event_loop = asyncio.get_event_loop()
try:
    print('creating task')
    task = event_loop.create_task(task_func())
    print('task: {!r}'.format(task))

    print('entering event loop')
    return_value = event_loop.run_until_complete(task)
    print('task: {!r}'.format(task))
    print('return value: {!r}'.format(return_value))
finally:
    event_loop.close()

print('task result: {!r}'.format(task.result()))
