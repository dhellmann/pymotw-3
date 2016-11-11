#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Using a condition primitive
"""

#end_pymotw_header
import asyncio
import functools


async def consumer(condition, n):
    with await condition:
        print('consumer {} is waiting'.format(n))
        await condition.wait()
        print('consumer {} triggered'.format(n))
    print('ending consumer {}'.format(n))


async def manipulate_condition(condition):
    print('starting manipulate_condition')

    # pause to let consumers start
    await asyncio.sleep(0.1)

    for i in range(1, 3):
        with await condition:
            print('notifying {}'.format(i))
            condition.notify(n=i)
        await asyncio.sleep(0.1)

    with await condition:
        print('notifying remaining')
        condition.notify_all()

    print('ending manipulate_condition')


event_loop = asyncio.get_event_loop()
try:
    # Create a condition
    condition = asyncio.Condition()

    # Set up tasks watching the condition
    consumers = [
        consumer(condition, i)
        for i in range(5)
    ]

    # Schedule a task to manipulate the condition variable
    event_loop.create_task(
        manipulate_condition(condition)
    )

    print('entering event loop')
    result = event_loop.run_until_complete(
        asyncio.wait(consumers),
    )
    print('exited event loop')
finally:
    print('closing event loop')
    event_loop.close()
