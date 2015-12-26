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
        self._received_len = 0
        self._sent_len = 0

    def connection_made(self, transport):
        self.address = transport.get_extra_info('peername')
        print('connecting to {} port {}'.format(*self.address),
              file=sys.stderr)
        for msg in self.messages:
            transport.write(msg)
            print('{}: sending {!r}'.format(self.address, msg),
                  file=sys.stderr)
            self._sent_len += len(msg)

    def data_received(self, data):
        print('{}: received {!r}'.format(self.address, data),
              file=sys.stderr)
        self._received_len += len(data)
        if self._received_len == self._sent_len:
            self.loop.stop()

    def connection_lost(self, exc):
        print('{}: server closed connection'.format(self.address),
              file=sys.stderr)
        self.loop.stop()


messages = [
    b'This is the message. ',
    b'It will be sent ',
    b'in parts.',
]
server_address = ('localhost', 10000)

event_loop = asyncio.get_event_loop()
client = functools.partial(EchoClient, messages, event_loop)
coroutine = event_loop.create_connection(client, *server_address)
event_loop.run_until_complete(coroutine)
event_loop.run_forever()
event_loop.close()
