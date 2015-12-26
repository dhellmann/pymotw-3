#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Echo client using coroutines
"""
#end_pymotw_header

import asyncio
import functools
import sys


async def echo_client(server_address, messages, loop, num):

    def report(text):
        print('{}: {}'.format(num, text), file=sys.stderr)

    report('connecting to {} port {}'.format(*server_address))
    reader, writer = await asyncio.open_connection(
        *server_address, loop=loop)

    # This could be writer.writelines() except that
    # would make it harder to show each part of the message
    # being sent.
    for msg in messages:
        writer.write(msg)
        report('sending {!r}'.format(msg))
    writer.write_eof()
    await writer.drain()

    report('waiting for response')
    while True:
        data = await reader.read(128)
        if data:
            report('received {!r}'.format(data))
        else:
            report('closing')
            writer.close()
            return


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
    connections.append(
        echo_client(server_address, messages, event_loop, i)
    )
event_loop.run_until_complete(
    asyncio.wait(connections, loop=event_loop),
)

event_loop.close()
