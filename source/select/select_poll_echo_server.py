#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Server half of echo example.
"""
#end_pymotw_header

import select
import socket
import sys
import Queue

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

# Bind the socket to the port
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
server.bind(server_address)

# Listen for incoming connections
server.listen(5)

# Keep up with the queues of outgoing messages
message_queues = {}

# Do not block forever (milliseconds)
TIMEOUT = 1000

# Commonly used flag sets
READ_ONLY = ( select.POLLIN |
              select.POLLPRI |
              select.POLLHUP |
              select.POLLERR )
READ_WRITE = READ_ONLY | select.POLLOUT

# Set up the poller
poller = select.poll()
poller.register(server, READ_ONLY)

# Map file descriptors to socket objects
fd_to_socket = { server.fileno(): server,
               }

while True:

    # Wait for at least one of the sockets to be ready for processing
    print >>sys.stderr, 'waiting for the next event'
    events = poller.poll(TIMEOUT)

    for fd, flag in events:

        # Retrieve the actual socket from its file descriptor
        s = fd_to_socket[fd]

        # Handle inputs
        if flag & (select.POLLIN | select.POLLPRI):

            if s is server:
                # A readable socket is ready to accept a connection
                connection, client_address = s.accept()
                print >>sys.stderr, '  connection', client_address
                connection.setblocking(0)
                fd_to_socket[ connection.fileno() ] = connection
                poller.register(connection, READ_ONLY)

                # Give the connection a queue for data to send
                message_queues[connection] = Queue.Queue()

            else:
                data = s.recv(1024)
                if data:
                    # A readable client socket has data
                    print >>sys.stderr, '  received "%s" from %s' % \
                        (data, s.getpeername())
                    message_queues[s].put(data)
                    # Add output channel for response
                    poller.modify(s, READ_WRITE)

                else:
                    # Interpret empty result as closed connection
                    print >>sys.stderr, '  closing', client_address
                    # Stop listening for input on the connection
                    poller.unregister(s)
                    s.close()

                    # Remove message queue
                    del message_queues[s]

        elif flag & select.POLLHUP:
            # Client hung up
            print >>sys.stderr, '  closing', client_address, '(HUP)'
            # Stop listening for input on the connection
            poller.unregister(s)
            s.close()

        elif flag & select.POLLOUT:
            # Socket is ready to send data, if there is any to send.
            try:
                next_msg = message_queues[s].get_nowait()
            except Queue.Empty:
                # No messages waiting so stop checking
                print >>sys.stderr, s.getpeername(), 'queue empty'
                poller.modify(s, READ_ONLY)
            else:
                print >>sys.stderr, '  sending "%s" to %s' % \
                    (next_msg, s.getpeername())
                s.send(next_msg)

        elif flag & select.POLLERR:
            print >>sys.stderr, '  exception on', s.getpeername()
            # Stop listening for input on the connection
            poller.unregister(s)
            s.close()

            # Remove message queue
            del message_queues[s]
