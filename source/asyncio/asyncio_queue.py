#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Using a queue
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


async def consumer(n, q, future):
    LOG.debug('in consumer {}'.format(n))
    while True:
        LOG.debug('consumer {} waiting for item'.format(n))
        item = await q.get()
        LOG.debug('consumer {} has item {}'.format(n, item))
        q.task_done()
        if item is None:
            break
        else:
            await asyncio.sleep(0.01 * item)
    future.set_result(True)


async def producer(q, num_workers):
    LOG.debug('starting producer')
    # Add some numbers to the queue to simulate jobs
    LOG.debug('adding task values to the queue')
    for i in range(num_workers * 3):
        await q.put(i)
    # Add None entries in the queue to signal the consumers to exit
    LOG.debug('adding stop signals to the queue')
    for i in range(num_workers):
        await q.put(None)
    LOG.debug('producer waiting for queue to empty')
    await q.join()
    LOG.debug('ending producer')


event_loop = asyncio.get_event_loop()

q = asyncio.Queue(loop=event_loop)

num_consumers = 2

# Create some futures to let us know when both coroutines are done.
futures = [
    asyncio.Future(loop=event_loop)
    for i in range(num_consumers)
]

try:
    # Set up tasks watching the condition
    tasks = [
        event_loop.create_task(
            consumer(i, q, futures[i])
        )
        for i in range(num_consumers)
    ]

    # Schedule the task to manipulate the condition variable
    event_loop.create_task(
        producer(q, num_consumers)
    )

    LOG.debug('entering event loop')
    result = event_loop.run_until_complete(
        asyncio.wait(futures, loop=event_loop),
    )
    LOG.debug('exited event loop')
finally:
    LOG.debug('closing event loop')
    event_loop.close()
