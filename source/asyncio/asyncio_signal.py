#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Handling UNIX signals
"""
#end_pymotw_header

import asyncio
import functools
import logging
import os
import signal
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(message)s',
    stream=sys.stderr,
)
LOG = logging.getLogger('main')


def signal_handler(name):
    LOG.debug('signal_handler({!r})'.format(name))


event_loop = asyncio.get_event_loop()

event_loop.add_signal_handler(
    signal.SIGHUP,
    functools.partial(signal_handler, 'SIGHUP'),
)
event_loop.add_signal_handler(
    signal.SIGUSR1,
    functools.partial(signal_handler, 'SIGUSR1'),
)
event_loop.add_signal_handler(
    signal.SIGINT,
    functools.partial(signal_handler, 'SIGINT'),
)


async def send_signals():
    pid = os.getpid()

    for name in ['SIGHUP', 'SIGHUP', 'SIGUSR1', 'SIGINT']:
        LOG.debug('sending {}'.format(name))
        os.kill(pid, getattr(signal, name))
        # Yield control to allow the signal handler to run,
        # since the signal does not interrupt the program
        # flow otherwise.
        LOG.debug('yielding control')
        await asyncio.sleep(0.01)
    return

try:
    LOG.debug('starting send_signals task')
    event_loop.run_until_complete(send_signals())
finally:
    LOG.debug('closing event loop')
    event_loop.close()
