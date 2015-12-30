#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Starting a subprocess using the Protocol API
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


class DFProtocol(asyncio.SubprocessProtocol):

    def __init__(self, done):
        self.done = done
        self.output = bytearray()

    def connection_made(self, transport):
        LOG.debug('process started {}'.format(
            transport.get_pid()))
        self.transport = transport

    def pipe_data_received(self, fd, data):
        LOG.debug('read {} bytes'.format(len(data)))
        self.output.extend(data)

    def process_exited(self):
        LOG.debug('process exited')
        return_code = self.transport.get_returncode()
        LOG.debug('return code {}'.format(return_code))
        if not return_code:
            cmd_output = bytes(self.output).decode()
            results = self._parse_results(cmd_output)
        else:
            results = []
        self.done.set_result((return_code, results))

    def _parse_results(self, output):
        LOG.debug('parsing results')
        # Output has one row of headers, all single words.  The
        # remaining rows are one per filesystem, with columns
        # more or less matching the headers (assuming that none
        # of the mount points have whitespace in the names).
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

    cmd_done = asyncio.Future(loop=loop)
    factory = functools.partial(DFProtocol, cmd_done)
    proc = loop.subprocess_exec(
        factory,
        'df', '-hl',
        stdin=None,
        stderr=None,
    )
    try:
        LOG.debug('launching process')
        transport, protocol = await proc
        LOG.debug('waiting for process to complete')
        await cmd_done
    finally:
        transport.close()

    return cmd_done.result()


event_loop = asyncio.get_event_loop()

try:
    LOG.debug('entering event loop')
    return_code, results = event_loop.run_until_complete(
        run_df(event_loop)
    )
finally:
    LOG.debug('closing event loop')
    event_loop.close()

if return_code:
    LOG.debug('error exit {}'.format(return_code))
else:
    print('\nFree space:')
    for r in results:
        print('{Mounted:25}: {Avail}'.format(**r))
