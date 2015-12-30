#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Waiting for a future to be done
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


def mark_done(future, result):
    LOG.debug('setting future result to {!r}'.format(result))
    future.set_result(result)


event_loop = asyncio.get_event_loop()

all_done = asyncio.Future(loop=event_loop)

LOG.debug('scheduling mark_done')
event_loop.call_soon(
    functools.partial(mark_done, all_done, 'the result'),
)

try:
    LOG.debug('entering event loop')
    result = event_loop.run_until_complete(all_done)
    LOG.debug('returned result: %r' % (result,))
finally:
    LOG.debug('closing event loop')
    event_loop.close()

LOG.debug('future result: %r' % (all_done.result(),))
