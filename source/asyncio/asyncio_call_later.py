#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Scheduling a callback with call_later
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


def callback(n):
    LOG.debug('callback {} invoked'.format(n))


def stopper(loop):
    LOG.debug('stopper invoked')
    loop.stop()


event_loop = asyncio.get_event_loop()

LOG.debug('registering callbacks')
event_loop.call_later(0.2, functools.partial(callback, 1))
event_loop.call_later(0.1, functools.partial(callback, 2))
event_loop.call_later(0.3, functools.partial(stopper,
                                             event_loop))
event_loop.call_soon(functools.partial(callback, 3))

try:
    LOG.debug('entering event loop')
    event_loop.run_forever()
finally:
    LOG.debug('closing event loop')
    event_loop.close()
