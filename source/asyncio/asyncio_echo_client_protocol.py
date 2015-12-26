#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""
"""
#end_pymotw_header

import asyncio
import functools
import sys


class EchoClient(asyncio.Protocol):

    def __init__(self, messages, loop):
        self.messages = messages
        self.loop = loop

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        print('connecting to {} port {}'.format(*self.address),
              file=sys.stderr)
        # This could be transport.writelines() except that
        # would make it harder to show each part of the message
        # being sent.
        for msg in self.messages:
            transport.write(msg)
            print('{}: sending {!r}'.format(self.address, msg),
                  file=sys.stderr)
        if transport.can_write_eof():
            transport.write_eof()

    def data_received(self, data):
        print('{}: received {!r}'.format(self.address, data),
              file=sys.stderr)

    def eof_received(self):
        print('{}: received EOF'.format(self.address),
              file=sys.stderr)
        self.transport.close()

    def connection_lost(self, exc):
        print('{}: server closed connection'.format(
            self.address), file=sys.stderr)
        self.transport.close()


messages = [
    b'This is the message. ',
    b'It will be sent ',
    b'in parts.',
]
server_address = ('localhost', 10000)

event_loop = asyncio.get_event_loop()

client_factory = functools.partial(EchoClient,
                                   messages,
                                   event_loop)
connection_factory = functools.partial(
    event_loop.create_connection,
    client_factory,
    *server_address,
)
event_loop.run_until_complete(
    asyncio.wait(
        [connection_factory(),
         connection_factory()],
        loop=event_loop,
    )
)

event_loop.close()
