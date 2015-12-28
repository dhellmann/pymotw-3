#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Scheduling a callback with call_soon
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


def callback():
    LOG.debug('callback invoked')


def stopper(loop):
    LOG.debug('stopper invoked')
    loop.stop()


event_loop = asyncio.get_event_loop()

LOG.debug('registering callbacks')
event_loop.call_soon(callback)
event_loop.call_soon(functools.partial(stopper, event_loop))

try:
    LOG.debug('entering event loop')
    event_loop.run_forever()
finally:
    LOG.debug('closing event loop')
    event_loop.close()
