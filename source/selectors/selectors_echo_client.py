#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2016 Doug Hellmann.  All rights reserved.
# Written for https://pymotw.com
#
"""Echo client using selectors instead of select directly.
"""
#end_pymotw_header

import selectors
import socket

mysel = selectors.DefaultSelector()
keep_running = True
outgoing = [
    b'It will be repeated.',
    b'This is the message.  ',
]
bytes_sent = 0
bytes_received = 0


def client(connection, mask):
    "Callback for socket events"
    global keep_running, bytes_sent, bytes_received

    client_address = connection.getpeername()
    print('client({})'.format(client_address))

    if mask & selectors.EVENT_READ:
        print('  ready to read')
        data = connection.recv(1024)
        if data:
            # A readable client socket has data
            print('  received {!r}'.format(data))
            bytes_received += len(data)
        if not data or bytes_received and bytes_received == bytes_sent:
            # Interpret empty result as closed connection,
            # and also close when we have received a copy
            # of all of the data sent.
            print('  closing')
            mysel.unregister(connection)
            connection.close()
            # Tell the main loop to stop
            keep_running = False

    elif mask & selectors.EVENT_WRITE:
        print('  ready to write')
        if not outgoing:
            # We are out of messages, so we no longer need to write
            # anything. Change our registration to let us keep reading
            # responses from the server.
            print('  switching to read-only')
            mysel.modify(sock, selectors.EVENT_READ, client)
        else:
            # Send the next message.
            next_msg = outgoing.pop()
            print('  sending {!r}'.format(next_msg))
            sock.sendall(next_msg)
            bytes_sent += len(next_msg)


# Connecting is a blocking operation, so call setblocking()
# after it returns.
server_address = ('localhost', 10000)
print('connecting to {} port {}'.format(*server_address))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_address)
sock.setblocking(False)

# Set up the callback so it is triggered when the socket
# is ready to receive data as well as when there is data
# to read.
mysel.register(
    sock,
    selectors.EVENT_READ | selectors.EVENT_WRITE,
    client,
)

while keep_running:
    print('waiting for I/O')
    for key, mask in mysel.select(timeout=1):
        callback = key.data
        callback(key.fileobj, mask)

print('shutting down')
mysel.close()
