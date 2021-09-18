=====================
 Sending Binary Data
=====================

Sockets transmit streams of bytes.  Those bytes can contain text
messages, as in the previous examples, or they can be made up of
binary data that has been encoded for transmission.  To prepare binary
data values for transmission, pack them into a buffer with
:mod:`struct`.

This client program encodes an integer, a string of two characters,
and a floating point value into a sequence of bytes that can be passed
to the socket for transmission.

.. include:: socket_binary_client.py
   :literal:
   :start-after: #end_pymotw_header

The server program uses the same :class:`Struct` specifier to unpack
the bytes it receives.

.. include:: socket_binary_server.py
   :literal:
   :start-after: #end_pymotw_header

Running the client produces:

::

    $ python ./socket_binary_client.py 
    
    sending "0100000061620000cdcc2c40" (1, 'ab', 2.7)
    closing socket

And the server shows the values it receives:

::

    $ python ./socket_binary_server.py 
    
    waiting for a connection
    received "0100000061620000cdcc2c40"
    unpacked: (1, 'ab', 2.700000047683716)
    
    waiting for a connection

The floating point value loses some precision as it is packed and
unpacked, but otherwise the data is transmitted as expected.  One
thing to keep in mind is that depending on the value of the integer,
it may be more efficient to convert it to text and then transmit,
instead of using :mod:`struct`.  The integer ``1`` uses one byte when
represented as a string, but four when packed into the structure.

.. seealso::

    :mod:`struct`
        Converting between strings and other data types.
