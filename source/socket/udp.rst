=================================
 User Datagram Client and Server
=================================

The user datagram protocol (UDP) works differently from TCP/IP.  Where
TCP is a *stream oriented* protocol, ensuring that all of the data is
transmitted in the right order, UDP is a *message oriented* protocol.
UDP does not require a long-lived connection, so setting up a UDP
socket is a little simpler.  On the other hand, UDP messages must fit
within a single packet (for IPv4, that means they can only hold 65,507
bytes because the 65,535 byte packet also includes header information)
and delivery is not guaranteed as it is with TCP.

Echo Server
===========

Since there is no connection, per se, the server does not need to
listen for and accept connections.  It only needs to use ``bind()``
to associate its socket with a port, and then wait for individual
messages.

.. literalinclude:: socket_echo_server_dgram.py
   :caption:
   :start-after: #end_pymotw_header

Messages are read from the socket using ``recvfrom()``, which
returns the data as well as the address of the client from which it
was sent.

Echo Client
===========

The UDP echo client is similar the server, but does not use
``bind()`` to attach its socket to an address.  It uses
``sendto()`` to deliver its message directly to the server, and
``recvfrom()`` to receive the response.

.. literalinclude:: socket_echo_client_dgram.py
   :caption:
   :start-after: #end_pymotw_header

Client and Server Together
==========================

Running the server produces:

.. code-block:: none

   $ python3 socket_echo_server_dgram.py
   starting up on localhost port 10000
   
   waiting to receive message
   received 42 bytes from ('127.0.0.1', 57870)
   b'This is the message.  It will be repeated.'
   sent 42 bytes back to ('127.0.0.1', 57870)
   
   waiting to receive message
    
The client output is:

.. code-block:: none

   $ python3 socket_echo_client_dgram.py
   sending b'This is the message.  It will be repeated.'
   waiting to receive
   received b'This is the message.  It will be repeated.'
   closing socket
