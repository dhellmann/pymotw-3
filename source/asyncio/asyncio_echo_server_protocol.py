#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""TCP echo server using asyncio with a Protocol class.
"""
#end_pymotw_header

import asyncio
import sys


class EchoServer(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        print('connection from {}'.format(self.address),
              file=sys.stderr)

    def data_received(self, data):
        print('received {!r} from {}'.format(data, self.address),
              file=sys.stderr)
        self.transport.write(data)
        print('sent {!r} to {}'.format(data, self.address),
              file=sys.stderr)

    def eof_received(self):
        print('received EOF from {}'.format(self.address),
              file=sys.stderr)
        if self.transport.can_write_eof():
            self.transport.write_eof()

    def connection_lost(self, error):
        if error:
            print('error from {}: {}'.format(self.address,
                                             error),
                  file=sys.stderr)
        else:
            print('closing {}'.format(self.address),
                  file=sys.stderr)


server_address = ('localhost', 10000)
event_loop = asyncio.get_event_loop()

# Create and start the server once, to ensure we can listen on
# the desired port. If something goes wrong creating the server,
# this throws an exception.
coroutine = event_loop.create_server(EchoServer, *server_address)
server = event_loop.run_until_complete(coroutine)
print('starting up on {} port {}'.format(*server_address),
      file=sys.stderr)

# Re-enter the event loop permanently to handle all connections.
try:
    event_loop.run_forever()
finally:
    server.close()
    event_loop.run_until_complete(server.wait_closed())
    event_loop.close()
