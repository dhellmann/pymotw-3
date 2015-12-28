#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Starting a subprocess using coroutines
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


def _parse_results(output):
    LOG.debug('parsing results')
    # Output has one row of headers, all single words.  The
    # remaining rows are one per filesystem, with columns more or
    # less matching the headers (assuming that none of the mount
    # points have whitespace in the names).
    if not output:
        return []
    lines = output.splitlines()
    headers = lines[0].split()
    devices = lines[1:]
    results = [
        dict(zip(headers, line.split()))
        for line in devices
    ]
    return results


async def run_df(loop):
    LOG.debug('in run_df')

    buffer = bytearray()

    create = asyncio.create_subprocess_exec(
        'df', '-hl',
        stdout=asyncio.subprocess.PIPE,
        loop=loop,
    )
    LOG.debug('launching process')
    proc = await create
    LOG.debug('pid {}'.format(proc.pid))

    while True:
        line = await proc.stdout.readline()
        LOG.debug('read {!r}'.format(line))
        if not line:
            LOG.debug('no more output from command')
            break
        buffer.extend(line)

    LOG.debug('waiting for process to complete')
    await proc.wait()

    return_code = proc.returncode
    LOG.debug('return code {}'.format(return_code))
    if not return_code:
        cmd_output = bytes(buffer).decode()
        results = _parse_results(cmd_output)
    else:
        results = []

    return (return_code, results)


event_loop = asyncio.get_event_loop()

try:
    LOG.debug('entering event loop')
    return_code, results = event_loop.run_until_complete(run_df(event_loop))
finally:
    LOG.debug('closing event loop')
    event_loop.close()

if return_code:
    LOG.debug('error exit {}'.format(return_code))
else:
    print('\nFree space:')
    for r in results:
        print('{Mounted:25}: {Avail}'.format(**r))
