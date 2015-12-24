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

# Sockets from which we expect to read
inputs = [ server ]

# Sockets to which we expect to write
outputs = [ ]

# Keep up with the queues of outgoing messages
message_queues = {}

while inputs:

    # Wait for at least one of the sockets to be ready for processing
    print >>sys.stderr, '\nwaiting for the next event'
    timeout = 1
    readable, writable, exceptional = select.select(inputs,
                                                    outputs,
                                                    inputs,
                                                    timeout)

    if not (readable or writable or exceptional):
        print >>sys.stderr, '  timed out, do some other work here'
        continue

    # Handle inputs
    for s in readable:

        if s is server:
            # A "readable" server socket is ready to accept a connection
            connection, client_address = s.accept()
            print >>sys.stderr, 'connection from', client_address
            connection.setblocking(0)
            inputs.append(connection)

            # Give the connection a queue for data we want to send
            message_queues[connection] = Queue.Queue()

        else:
            data = s.recv(1024)
            if data:
                # A readable client socket has data
                print >>sys.stderr, 'received "%s" from %s' % \
                    (data, s.getpeername())
                message_queues[s].put(data)
                # Add output channel for response
                if s not in outputs:
                    outputs.append(s)
                    
            else:
                # Interpret empty result as closed connection
                print >>sys.stderr, 'closing', client_address
                # Stop listening for input on the connection
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()

                # Remove message queue
                del message_queues[s]

    # Handle outputs
    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except Queue.Empty:
            # No messages waiting so stop checking for writability.
            print >>sys.stderr, s.getpeername(), 'queue empty'
            outputs.remove(s)
        else:
            print >>sys.stderr, 'sending "%s" to %s' % \
                (next_msg, s.getpeername())
            s.send(next_msg)

    # Handle "exceptional conditions"
    for s in exceptional:
        print >>sys.stderr, 'exception condition on', s.getpeername()
        # Stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

        # Remove message queue
        del message_queues[s]
