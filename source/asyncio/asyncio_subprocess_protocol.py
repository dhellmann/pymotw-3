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

    def pipe_data_received(self, fd, data):
        LOG.debug('read {} bytes'.format(len(data)))
        self.output.extend(data)

    def _parse_results(self, output):
        # Output has one row of headers, all single words.  The
        # remaining rows are one per filesystem, with columns more or
        # less matching the headers (assuming that none of the mount
        # points have whitespace in the names).
        lines = output.splitlines()
        headers = lines[0].split()
        devices = lines[1:]
        results = []
        for line in devices:
            results.append(dict(zip(headers, line.split())))
        return results

    def process_exited(self):
        LOG.debug('process exited, parsing output')
        cmd_output = bytes(self.output).decode('ascii')
        results = self._parse_results(cmd_output)
        self.done.set_result(results)


async def run_df(loop):
    LOG.debug('in run_df')

    cmd_done = asyncio.Future(loop=loop)
    factory = functools.partial(DFProtocol, cmd_done)
    create = loop.subprocess_exec(
        factory,
        'df', '-hl',
        stdin=None, stderr=None)
    transport, protocol = await create
    await cmd_done
    transport.close()

    return cmd_done.result()


event_loop = asyncio.get_event_loop()

try:
    LOG.debug('entering event loop')
    result = event_loop.run_until_complete(run_df(event_loop))
finally:
    LOG.debug('closing event loop')
    event_loop.close()

LOG.debug('Free space:')
for r in result:
    LOG.debug('{Mounted:25}: {Avail}'.format(**r))
