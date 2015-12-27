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

LOG.debug('setting up gatherer')
gatherer = asyncio.gather(
    phase1(),
    phase2(),
    loop=event_loop,
)

try:
    LOG.debug('entering event loop')
    results = event_loop.run_until_complete(gatherer)
finally:
    LOG.debug('closing event loop')
    event_loop.close()

LOG.debug('results: %r' % (results,))
