#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Using a condition primitive
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


async def consumer(condition, n, future):
    LOG.debug('in consumer {}'.format(n))
    with await condition:
        LOG.debug('consumer {} acquired lock and is waiting'.format(n))
        await condition.wait()
        LOG.debug('consumer {} triggered'.format(n))
    future.set_result(True)


async def manipulate_condition(condition):
    LOG.debug('starting manipulate_condition')
    for i in range(2):
        with await condition:
            LOG.debug('notifying {}'.format(i))
            condition.notify(n=1)
        await asyncio.sleep(0.1)
    with await condition:
        LOG.debug('notifying remaining')
        condition.notify_all()
    LOG.debug('ending manipulate_condition')


event_loop = asyncio.get_event_loop()

# Create a condition
condition = asyncio.Condition(loop=event_loop)

num_consumers = 4

# Create some futures to let us know when both coroutines are done.
futures = [
    asyncio.Future(loop=event_loop)
    for i in range(num_consumers)
]

try:
    # Set up tasks watching the condition
    tasks = [
        event_loop.create_task(
            consumer(condition, i, futures[i])
        )
        for i in range(num_consumers)
    ]

    # Schedule the task to manipulate the condition variable
    event_loop.create_task(
        manipulate_condition(condition)
    )

    LOG.debug('entering event loop')
    result = event_loop.run_until_complete(
        asyncio.wait(futures, loop=event_loop),
    )
    LOG.debug('exited event loop')
finally:
    LOG.debug('closing event loop')
    event_loop.close()
