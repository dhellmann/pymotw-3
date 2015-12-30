#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Running a blocking function in a process pool
"""
#end_pymotw_header

import asyncio
import concurrent.futures
import logging
import sys
import time

logging.basicConfig(
    level=logging.DEBUG,
    format='PID %(process)5s %(name)18s: %(message)s',
    stream=sys.stderr,
)
LOG = logging.getLogger('main')


def blocks(n):
    log = logging.getLogger('blocks({})'.format(n))
    log.debug('running')
    time.sleep(1)
    log.debug('done')
    return n ** 2


async def run_blocking_tasks(loop, executor):
    log = logging.getLogger('run_blocking_tasks')
    log.debug('starting task')

    log.debug('creating executor tasks')
    blocking_tasks = [
        loop.run_in_executor(
            executor,
            blocks,
            i,
        )
        for i in range(6)
    ]
    log.debug('waiting for executor tasks')
    results = await asyncio.gather(*blocking_tasks, loop=loop)
    log.debug('results: {!r}'.format(results))

    log.debug('exiting')


executor = concurrent.futures.ProcessPoolExecutor(max_workers=3)

event_loop = asyncio.get_event_loop()
try:
    LOG.debug('entering event loop')
    event_loop.run_until_complete(run_blocking_tasks(event_loop, executor))
finally:
    LOG.debug('closing event loop')
    event_loop.close()
