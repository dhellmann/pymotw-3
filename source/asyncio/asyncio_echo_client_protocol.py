#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Echo client using a Protocol class
"""
#end_pymotw_header

import asyncio
import functools
import logging
import sys


class EchoClient(asyncio.Protocol):

    def __init__(self, messages, loop, num):
        self.messages = messages
        self.loop = loop
        self.num = num
        self.log = logging.getLogger('EchoClient%s' % num)

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.log.debug(
            'connecting to {} port {}'.format(*self.address)
        )
        # This could be transport.writelines() except that
        # would make it harder to show each part of the message
        # being sent.
        for msg in self.messages:
            transport.write(msg)
            self.log.debug('sending {!r}'.format(msg))
        if transport.can_write_eof():
            transport.write_eof()

    def data_received(self, data):
        self.log.debug('received {!r}'.format(data))

    def eof_received(self):
        self.log.debug('received EOF')
        self.transport.close()

    def connection_lost(self, exc):
        self.log.debug('server closed connection')
        self.transport.close()


logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)
log = logging.getLogger('main')

messages = [
    b'This is the message. ',
    b'It will be sent ',
    b'in parts.',
]
server_address = ('localhost', 10000)

event_loop = asyncio.get_event_loop()

# Build multiple clients
connections = []
for i in range(1, 3):
    client_factory = functools.partial(
        EchoClient,
        messages,
        event_loop,
        i,
    )
    connection_factory = functools.partial(
        event_loop.create_connection,
        client_factory,
        *server_address,
    )
    connections.append(connection_factory())

# Wait until the work for all of the clients is done.
log.debug('waiting for clients to complete')
try:
    event_loop.run_until_complete(
        asyncio.wait(connections, loop=event_loop),
    )
finally:
    log.debug('closing event loop')
    event_loop.close()
