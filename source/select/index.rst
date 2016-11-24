===================================
select --- Wait for I/O Efficiently
===================================

.. module:: select
    :synopsis: Wait for I/O Efficiently

The :mod:`select` module provides access to platform-specific I/O
monitoring functions.  The most portable interface is the POSIX
function :func:`select`, which is available on UNIX and Windows.  The
module also includes :func:`poll`, a UNIX-only API, and several
options that only work with specific variants of UNIX.

.. note::

   The new :mod:`selectors` module provides a higher-level interface
   built on top of the APIs in :mod:`select`. It is easier to build
   portable code using :mod:`selectors`, so use that module unless the
   low-level APIs provided by :mod:`select` are somehow required.

Using select()
==============

Python's :func:`select` function is a direct interface to the
underlying operating system implementation.  It monitors sockets, open
files, and pipes (anything with a :func:`fileno` method that returns a
valid file descriptor) until they become readable or writable or a
communication error occurs.  :func:`select` makes it easier to monitor
multiple connections at the same time, and is more efficient than
writing a polling loop in Python using socket timeouts, because the
monitoring happens in the operating system network layer, instead of
the interpreter.

.. note::

   Using Python's file objects with :func:`select` works for UNIX, but
   is not supported under Windows.

The echo server example from the :mod:`socket` section can be extended
to watch for more than one connection at a time by using
:func:`select`.  The new version starts out by creating a non-blocking
TCP/IP socket and configuring it to listen on an address.

.. literalinclude:: select_echo_server.py
   :caption:
   :lines: 10-26

The arguments to :func:`select` are three lists containing
communication channels to monitor.  The first is a list of the objects
to be checked for incoming data to be read, the second contains
objects that will receive outgoing data when there is room in their
buffer, and the third those that may have an error (usually a
combination of the input and output channel objects).  The next step
in the server is to set up the lists containing input sources and
output destinations to be passed to :func:`select`.

.. literalinclude:: select_echo_server.py
   :lines: 28-32

Connections are added to and removed from these lists by the server
main loop.  Since this version of the server is going to wait for a
socket to become writable before sending any data (instead of
immediately sending the reply), each output connection needs a queue
to act as a buffer for the data to be sent through it.

.. literalinclude:: select_echo_server.py
   :lines: 34-35

The main portion of the server program loops, calling :func:`select` to
block and wait for network activity.

.. literalinclude:: select_echo_server.py
   :lines: 37-44

:func:`select` returns three new lists, containing subsets of the
contents of the lists passed in.  All of the sockets in the
:data:`readable` list have incoming data buffered and available to be
read.  All of the sockets in the :data:`writable` list have free space
in their buffer and can be written to.  The sockets returned in
:data:`exceptional` have had an error (the actual definition of
"exceptional condition" depends on the platform).

The "readable" sockets represent three possible cases.  If the socket
is the main "server" socket, the one being used to listen for
connections, then the "readable" condition means it is ready to accept
another incoming connection.  In addition to adding the new connection
to the list of inputs to monitor, this section sets the client socket
to not block.

.. literalinclude:: select_echo_server.py
   :lines: 46-59

The next case is an established connection with a client that has sent
data.  The data is read with :func:`recv`, then placed on the queue so
it can be sent through the socket and back to the client.

.. literalinclude:: select_echo_server.py
   :lines: 61-71

A readable socket *without* data available is from a client that has
disconnected, and the stream is ready to be closed.

.. literalinclude:: select_echo_server.py
   :lines: 73-84

There are fewer cases for the writable connections.  If there is data
in the queue for a connection, the next message is sent.  Otherwise,
the connection is removed from the list of output connections so that
the next time through the loop :func:`select` does not indicate that
the socket is ready to send data.

.. literalinclude:: select_echo_server.py
   :lines: 86-100

Finally, if there is an error with a socket, it is closed.

.. literalinclude:: select_echo_server.py
   :lines: 102-

The example client program uses two sockets to demonstrate how the
server with :func:`select` manages multiple connections at the same
time.  The client starts by connecting each TCP/IP socket to the
server.

.. literalinclude:: select_echo_multiclient.py
   :caption:
   :lines: 10-30

Then it sends one piece of the message at a time via each socket and
reads all responses available after writing new data.

.. literalinclude:: select_echo_multiclient.py
   :lines: 32-

Run the server in one window and the client in another.  The output
will look like this, with different port numbers.

.. code-block:: none

   $ python3 select_echo_server.py
   starting up on localhost port 10000
   waiting for the next event
     connection from ('127.0.0.1', 61003)
   waiting for the next event
     connection from ('127.0.0.1', 61004)
   waiting for the next event
     received b'This is the message. ' from ('127.0.0.1', 61003)
     received b'This is the message. ' from ('127.0.0.1', 61004)
   waiting for the next event
     sending b'This is the message. ' to ('127.0.0.1', 61003)
     sending b'This is the message. ' to ('127.0.0.1', 61004)
   waiting for the next event
      ('127.0.0.1', 61003) queue empty
      ('127.0.0.1', 61004) queue empty
   waiting for the next event
     received b'It will be sent ' from ('127.0.0.1', 61003)
     received b'It will be sent ' from ('127.0.0.1', 61004)
   waiting for the next event
     sending b'It will be sent ' to ('127.0.0.1', 61003)
     sending b'It will be sent ' to ('127.0.0.1', 61004)
   waiting for the next event
      ('127.0.0.1', 61003) queue empty
      ('127.0.0.1', 61004) queue empty
   waiting for the next event
     received b'in parts.' from ('127.0.0.1', 61003)
   waiting for the next event
     received b'in parts.' from ('127.0.0.1', 61004)
     sending b'in parts.' to ('127.0.0.1', 61003)
   waiting for the next event
      ('127.0.0.1', 61003) queue empty
     sending b'in parts.' to ('127.0.0.1', 61004)
   waiting for the next event
      ('127.0.0.1', 61004) queue empty
   waiting for the next event
     closing ('127.0.0.1', 61004)
     closing ('127.0.0.1', 61004)
   waiting for the next event

The client output shows the data being sent and received using both
sockets.

.. code-block:: none

   $ python3 select_echo_multiclient.py
   connecting to localhost port 10000
   ('127.0.0.1', 61003): sending b'This is the message. '
   ('127.0.0.1', 61004): sending b'This is the message. '
   ('127.0.0.1', 61003): received b'This is the message. '
   ('127.0.0.1', 61004): received b'This is the message. '
   ('127.0.0.1', 61003): sending b'It will be sent '
   ('127.0.0.1', 61004): sending b'It will be sent '
   ('127.0.0.1', 61003): received b'It will be sent '
   ('127.0.0.1', 61004): received b'It will be sent '
   ('127.0.0.1', 61003): sending b'in parts.'
   ('127.0.0.1', 61004): sending b'in parts.'
   ('127.0.0.1', 61003): received b'in parts.'
   ('127.0.0.1', 61004): received b'in parts.'

Non-blocking I/O With Timeouts
==============================

:func:`select` also takes an optional fourth parameter, which is the
number of seconds to wait before breaking off monitoring if no
channels have become active.  Using a timeout value lets a main
program call :func:`select` as part of a larger processing loop,
taking other actions in between checking for network input.

When the timeout expires, :func:`select` returns three empty lists.
Updating the server example to use a timeout requires adding the extra
argument to the :func:`select` call and handling the empty lists after
:func:`select` returns.

.. literalinclude:: select_echo_server_timeout.py
   :caption:
   :lines: 44-52

This "slow" version of the client program pauses after sending each
message, to simulate latency or other delay in transmission.

.. literalinclude:: select_echo_slow_client.py
   :caption:
   :start-after: #end_pymotw_header

Running the new server with the slow client produces:

.. code-block:: none

   $ python3 select_echo_server_timeout.py
   starting up on localhost port 10000
   waiting for the next event
     timed out, do some other work here
   waiting for the next event
     connection from ('127.0.0.1', 61144)
   waiting for the next event
     timed out, do some other work here
   waiting for the next event
     received b'Part one of the message.' from ('127.0.0.1', 61144)
   waiting for the next event
     sending b'Part one of the message.' to ('127.0.0.1', 61144)
   waiting for the next event
   ('127.0.0.1', 61144) queue empty
   waiting for the next event
     timed out, do some other work here
   waiting for the next event
     received b'Part two of the message.' from ('127.0.0.1', 61144)
   waiting for the next event
     sending b'Part two of the message.' to ('127.0.0.1', 61144)
   waiting for the next event
   ('127.0.0.1', 61144) queue empty
   waiting for the next event
     timed out, do some other work here
   waiting for the next event
   closing ('127.0.0.1', 61144)
   waiting for the next event
     timed out, do some other work here

And this is the client output:

.. code-block:: none

   $ python3 select_echo_slow_client.py
   connecting to localhost port 10000
   sending b'Part one of the message.'
   sending b'Part two of the message.'
   received b'Part one of the '
   received b'message.Part two'
   received b' of the message.'
   closing socket

Using poll()
============

The :func:`poll` function provides similar features to :func:`select`,
but the underlying implementation is more efficient.  The trade-off is
that :func:`poll` is not supported under Windows, so programs using
:func:`poll` are less portable.

An echo server built on :func:`poll` starts with the same socket
configuration code used in the other examples.

.. literalinclude:: select_poll_echo_server.py
   :caption:
   :lines: 10-29

The timeout value passed to :func:`poll` is represented in
milliseconds, instead of seconds, so in order to pause for a full
second the timeout must be set to ``1000``.

.. literalinclude:: select_poll_echo_server.py
   :lines: 31-32

Python implements :func:`poll` with a class that manages the
registered data channels being monitored.  Channels are added by
calling :func:`register` with flags indicating which events are
interesting for that channel.  The full set of flags is listed in
:table:`Event Flags for poll()`.

.. table:: Event Flags for poll()

   =================  ===========
   Event              Description
   =================  ===========
   :const:`POLLIN`    Input ready
   :const:`POLLPRI`   Priority input ready
   :const:`POLLOUT`   Able to receive output
   :const:`POLLERR`   Error
   :const:`POLLHUP`   Channel closed
   :const:`POLLNVAL`  Channel not open
   =================  ===========

The echo server will be setting up some sockets just for reading and
others to be read from or written to.  The appropriate combinations of
flags are saved to the local variables :data:`READ_ONLY` and
:data:`READ_WRITE`.

.. literalinclude:: select_poll_echo_server.py
   :lines: 34-41

The :data:`server` socket is registered so that any incoming
connections or data triggers an event.

.. literalinclude:: select_poll_echo_server.py
   :lines: 43-45

Since :func:`poll` returns a list of tuples containing the file
descriptor for the socket and the event flag, a mapping from file
descriptor numbers to objects is needed to retrieve the
:class:`socket` to read or write from it.

.. literalinclude:: select_poll_echo_server.py
   :lines: 47-50

The server's loop calls :func:`poll` and then processes the "events"
returned by looking up the socket and taking action based on the flag
in the event.

.. literalinclude:: select_poll_echo_server.py
   :lines: 52-62

As with :func:`select`, when the main server socket is "readable,"
that really means there is a pending connection from a client.  The
new connection is registered with the :data:`READ_ONLY` flags to watch
for new data to come through it.

.. literalinclude:: select_poll_echo_server.py
   :lines: 64-78

Sockets other than the server are existing clients and :func:`recv`
is used to access the data waiting to be read.

.. literalinclude:: select_poll_echo_server.py
   :lines: 80-81

If :func:`recv` returns any data, it is placed into the outgoing queue
for the socket, and the flags for that socket are changed using
:func:`modify` so :func:`poll` will watch for the socket to be ready
to receive data.

.. literalinclude:: select_poll_echo_server.py
   :lines: 82-89

An empty string returned by :func:`recv` means the client
disconnected, so :func:`unregister` is used to tell the :class:`poll`
object to ignore the socket.

.. literalinclude:: select_poll_echo_server.py
   :lines: 91-100

The :const:`POLLHUP` flag indicates a client that "hung up" the
connection without closing it cleanly.  The server stops polling
clients that disappear.

.. literalinclude:: select_poll_echo_server.py
   :lines: 102-108

The handling for writable sockets looks like the version used in the
example for :func:`select`, except that :func:`modify` is used to
change the flags for the socket in the poller, instead of removing it
from the output list.

.. literalinclude:: select_poll_echo_server.py
   :lines: 110-124

And, finally, any events with :const:`POLLERR` cause the server to
close the socket.

.. literalinclude:: select_poll_echo_server.py
   :lines: 126-

When the poll-based server is run together with
``select_echo_multiclient.py`` (the client program that uses multiple
sockets), this is the output.

.. code-block:: none

   $ python3 select_poll_echo_server.py
   starting up on localhost port 10000
   waiting for the next event
   waiting for the next event
   waiting for the next event
   waiting for the next event
     connection ('127.0.0.1', 61253)
   waiting for the next event
     connection ('127.0.0.1', 61254)
   waiting for the next event
     received b'This is the message. ' from ('127.0.0.1', 61253)
     received b'This is the message. ' from ('127.0.0.1', 61254)
   waiting for the next event
     sending b'This is the message. ' to ('127.0.0.1', 61253)
     sending b'This is the message. ' to ('127.0.0.1', 61254)
   waiting for the next event
   ('127.0.0.1', 61253) queue empty
   ('127.0.0.1', 61254) queue empty
   waiting for the next event
     received b'It will be sent ' from ('127.0.0.1', 61253)
     received b'It will be sent ' from ('127.0.0.1', 61254)
   waiting for the next event
     sending b'It will be sent ' to ('127.0.0.1', 61253)
     sending b'It will be sent ' to ('127.0.0.1', 61254)
   waiting for the next event
   ('127.0.0.1', 61253) queue empty
   ('127.0.0.1', 61254) queue empty
   waiting for the next event
     received b'in parts.' from ('127.0.0.1', 61253)
     received b'in parts.' from ('127.0.0.1', 61254)
   waiting for the next event
     sending b'in parts.' to ('127.0.0.1', 61253)
     sending b'in parts.' to ('127.0.0.1', 61254)
   waiting for the next event
   ('127.0.0.1', 61253) queue empty
   ('127.0.0.1', 61254) queue empty
   waiting for the next event
     closing ('127.0.0.1', 61254)
   waiting for the next event
     closing ('127.0.0.1', 61254)
   waiting for the next event

.. using PIPE_BUF to limit writes

Platform-specific Options
=========================

Less portable options provided by :mod:`select` are :class:`epoll`,
the *edge polling* API supported by Linux; :class:`kqueue`, which uses
BSD's *kernel queue*; and :class:`kevent`, BSD's *kernel event*
interface.  Refer to the operating system library documentation for
more detail about how they work.

.. seealso::

    * :pydoc:`select`

    * :mod:`selectors` -- Higher-level abstraction on top of
      :mod:`select`.

    * `Socket Programming HOWOTO
      <https://docs.python.org/howto/sockets.html>`__ -- An
      instructional guide by Gordon McMillan, included in the standard
      library documentation.

    * :mod:`socket` -- Low-level network communication.

    * :mod:`SocketServer` -- Framework for creating network server
      applications.

    * :mod:`asyncio` -- Asynchronous I/O framework

    * *Unix Network Programming, Volume 1: The Sockets Networking API, 3/E*
      By W. Richard Stevens, Bill Fenner, and Andrew
      M. Rudoff. Published by Addison-Wesley Professional, 2004.
      ISBN-10: 0131411551

    * *Foundations of Python Network Programminng, 3/E* By Brandon
      Rhodes and John Goerzen. Published by Apress, 2014. ISBN-10:
      1430258543
