#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Echo client using coroutines
"""
#end_pymotw_header

import asyncio
import functools
import logging
import sys

MESSAGES = [
    b'This is the message. ',
    b'It will be sent ',
    b'in parts.',
]
SERVER_ADDRESS = ('localhost', 10000)


async def echo_client(server_address, messages, loop):

    log = logging.getLogger('echo_client')

    log.debug('connecting to {} port {}'.format(*server_address))
    reader, writer = await asyncio.open_connection(
        *server_address, loop=loop)

    # This could be writer.writelines() except that
    # would make it harder to show each part of the message
    # being sent.
    for msg in messages:
        writer.write(msg)
        log.debug('sending {!r}'.format(msg))
    writer.write_eof()
    await writer.drain()

    log.debug('waiting for response')
    while True:
        data = await reader.read(128)
        if data:
            log.debug('received {!r}'.format(data))
        else:
            log.debug('closing')
            writer.close()
            return


logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)
log = logging.getLogger('main')

event_loop = asyncio.get_event_loop()

try:
    event_loop.run_until_complete(
        echo_client(SERVER_ADDRESS, MESSAGES, event_loop)
    )
finally:
    log.debug('closing event loop')
    event_loop.close()
