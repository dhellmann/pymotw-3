#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""TCP echo server using asyncio with coroutines.
"""
#end_pymotw_header

import asyncio
import sys


@asyncio.coroutine
def echo(reader, writer):
    address = writer.get_extra_info('peername')
    print('connection from {}'.format(address),
          file=sys.stderr)
    while True:
        data = yield from reader.read(128)
        if data:
            print('received {!r} from {}'.format(data, address),
                  file=sys.stderr)
            writer.write(data)
            yield from writer.drain()
            print('sent {!r} to {}'.format(data, address),
                  file=sys.stderr)
        else:
            print('closing {}'.format(address),
                  file=sys.stderr)
            writer.close()
            return


server_address = ('localhost', 10000)
event_loop = asyncio.get_event_loop()

# Create and start the server once, to ensure we can listen on
# the desired port. If something goes wrong creating the server,
# this throws an exception.
coroutine = asyncio.start_server(echo, *server_address,
                                 loop=event_loop)
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
