=============================================
 selectors --- I/O Multiplexing Abstractions
=============================================

.. module:: selectors
   :synopsis: I/O Multiplexing Abstractions

:Purpose: Provide platform-independent abstractions for I/O
          multiplexing based on the ``select`` module.

The ``selectors`` module provides a platform-independent
abstraction layer on top of the platform-specific I/O monitoring
functions in :mod:`select`.

Operating Model
===============

The APIs in ``selectors`` are event-based, similar to :func:`poll`
from :mod:`select`. A selector object provides methods for specifying
what events to look for on a socket, and then lets the caller wait for
events in a platform-independent way.

Registering interest in an event creates a :class:`SelectorKey`, which
holds the socket, information about the events of interest, and
optional application data.  The owner of the selector calls its
``select()`` method to learn about events. The return value is a
sequence of key objects and a bitmask indicating what events have
occurred. A program using a selector should repeatedly call
``select()``, then handle the events appropriately.

Echo Server
===========

The echo server example below uses the application data in the
:class:`SelectorKey` to register a callback function to be invoked on
the new event. The main loop gets the callback from the key and passes
the socket and event mask to it. As the server starts, it registers
the :func:`accept` function to be called for read events on the main
server socket. Accepting the connection produces a new socket, which
is then registered with the :func:`read` function as a callback for
read events.

.. literalinclude:: selectors_echo_server.py
   :caption:
   :start-after: #end_pymotw_header

When :func:`read` receives no data from the socket, it interprets the
read event as the other side of the connection being closed instead of
sending data. It removes the socket from the selector and closes
it. In order to avoid an infinite loop, this server also shuts itself
down after it has finished communicating with a single client.

Echo Client
===========

The echo client example below processes all of the I/O events in the
main loop, instead of using callbacks. It sets up the selector to
report read events on the socket, and to report when the socket is
ready to send data. Because it is looking at two types of events, the
client must check which occurred by examining the mask value.  After
all of its outgoing data has been sent, it changes the selector
configuration to only report when there is data to read.

.. literalinclude:: selectors_echo_client.py
   :caption:
   :start-after: #end_pymotw_header

The client tracks the amount of data it has sent, and the amount it
has received. When those values match and are non-zero, the client
exits the processing loop and cleanly shuts down by removing the
socket from the selector and closing both the socket and the selector.

Server and Client Together
==========================

The client and server should be run in separate terminal windows, so
they can communicate with each other.  The server output shows the
incoming connection and data, as well as the response sent back to
the client.

.. NOT RUNNING

.. code-block:: none

   $ python3 source/selectors/selectors_echo_server.py
   starting up on localhost port 10000
   waiting for I/O
   waiting for I/O
   accept(('127.0.0.1', 59850))
   waiting for I/O
   read(('127.0.0.1', 59850))
     received b'This is the message.  It will be repeated.'
   waiting for I/O
   read(('127.0.0.1', 59850))
     closing
   shutting down

The client output shows the outgoing message and the response from the
server.

.. NOT RUNNING

.. code-block:: none

   $ python3 source/selectors/selectors_echo_client.py
   connecting to localhost port 10000
   waiting for I/O
   client(('127.0.0.1', 10000))
     ready to write
     sending b'This is the message.  '
   waiting for I/O
   client(('127.0.0.1', 10000))
     ready to write
     sending b'It will be repeated.'
   waiting for I/O
   client(('127.0.0.1', 10000))
     ready to write
     switching to read-only
   waiting for I/O
   client(('127.0.0.1', 10000))
     ready to read
     received b'This is the message.  It will be repeated.'
   shutting down

.. seealso::

   * :pydoc:`selectors`

   * :mod:`select` -- Lower-level APIs for handling I/O efficiently.
