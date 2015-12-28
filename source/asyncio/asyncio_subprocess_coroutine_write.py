#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Communicating with a subprocess using coroutines
"""
#end_pymotw_header

import asyncio
import asyncio.subprocess
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(message)s',
    stream=sys.stderr,
)
LOG = logging.getLogger('')


async def run_tr(loop, input):
    LOG.debug('in run_tr')

    create = asyncio.create_subprocess_exec(
        'tr', '[:lower:]', '[:upper:]',
        stdout=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE,
        loop=loop,
    )
    LOG.debug('launching process')
    proc = await create
    LOG.debug('pid {}'.format(proc.pid))

    LOG.debug('communicating with process')
    stdout, stderr = await proc.communicate(input.encode())

    LOG.debug('waiting for process to complete')
    await proc.wait()

    return_code = proc.returncode
    LOG.debug('return code {}'.format(return_code))
    if not return_code:
        results = bytes(stdout).decode()
    else:
        results = ''

    return (return_code, results)


event_loop = asyncio.get_event_loop()

MESSAGE = """
This message will be converted
to all caps.
"""

try:
    LOG.debug('entering event loop')
    return_code, results = event_loop.run_until_complete(run_tr(event_loop, MESSAGE))
finally:
    LOG.debug('closing event loop')
    event_loop.close()

if return_code:
    LOG.debug('error exit {}'.format(return_code))
else:
    print('Original: {!r}'.format(MESSAGE))
    print('Changed: {!r}'.format(results))
