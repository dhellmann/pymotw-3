#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Future callbacks
"""
#end_pymotw_header

import asyncio
import functools
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)
LOG = logging.getLogger('main')


def callback(n, future):
    LOG.debug('{}: future done: {}'.format(n, future.result()))


event_loop = asyncio.get_event_loop()

LOG.debug('registering callbacks on future')
all_done = asyncio.Future(loop=event_loop)
all_done.add_done_callback(functools.partial(callback, 1))
all_done.add_done_callback(functools.partial(callback, 2))

LOG.debug('setting result of future')
all_done.set_result('the result')

try:
    LOG.debug('entering event loop')
    event_loop.run_until_complete(all_done)
finally:
    LOG.debug('closing event loop')
    event_loop.close()
