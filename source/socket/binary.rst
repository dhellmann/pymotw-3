=====================
 Sending Binary Data
=====================

Sockets transmit streams of bytes.  Those bytes can contain text
messages encoded to bytes, as in the previous examples, or they can be
made up of binary data that has been packed into a buffer with
:mod:`struct` to prepare it for transmission.

This client program encodes an integer, a string of two characters,
and a floating point value into a sequence of bytes that can be passed
to the socket for transmission.

.. literalinclude:: socket_binary_client.py
   :caption:
   :start-after: #end_pymotw_header

When sending multi-byte binary data between two systems, it is
important to ensure that both sides of the connection know what order
the bytes are in and how to assemble them back into the correct order
for the local architecture.  The server program uses the same
:class:`Struct` specifier to unpack the bytes it receives so they are
interpreted in the correct order.

.. literalinclude:: socket_binary_server.py
   :caption:
   :start-after: #end_pymotw_header

Running the client produces:

.. code-block:: none

   $ python3 source/socket/socket_binary_client.py
   values = (1, b'ab', 2.7)
   sending b'0100000061620000cdcc2c40'
   closing socket

And the server shows the values it receives:

.. code-block:: none

   $ python3 socket_binary_server.py
   
   waiting for a connection
   received b'0100000061620000cdcc2c40'
   unpacked: (1, b'ab', 2.700000047683716)
   
   waiting for a connection

The floating point value loses some precision as it is packed and
unpacked, but otherwise the data is transmitted as expected.  One
thing to keep in mind is that depending on the value of the integer,
it may be more efficient to convert it to text and then transmit,
instead of using :mod:`struct`.  The integer ``1`` uses one byte when
represented as a string, but four when packed into the structure.

.. seealso::

   * :mod:`struct` -- Converting between strings and other data types.
