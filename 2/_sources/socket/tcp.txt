==========================
 TCP/IP Client and Server
==========================

Sockets can be configured to act as a *server* and listen for incoming
messages, or connect to other applications as a *client*.  After both
ends of a TCP/IP socket are connected, communication is
bi-directional.

Echo Server
===========

This sample program, based on the one in the standard library
documentation, receives incoming messages and echos them back to the
sender.  It starts by creating a TCP/IP socket.

.. literalinclude:: socket_echo_server.py
   :lines: 10-14

Then :func:`bind` is used to associate the socket with the server
address.  In this case, the address is ``localhost``, referring to the
current server, and the port number is 10000.

.. literalinclude:: socket_echo_server.py
   :lines: 16-19

Calling :func:`listen` puts the socket into server mode, and
:func:`accept` waits for an incoming connection.

.. literalinclude:: socket_echo_server.py
   :lines: 21-27

:func:`accept` returns an open connection between the server and
client, along with the address of the client.  The connection is
actually a different socket on another port (assigned by the kernel).
Data is read from the connection with :func:`recv` and transmitted
with :func:`sendall`.

.. literalinclude:: socket_echo_server.py
   :lines: 28-

When communication with a client is finished, the connection needs to
be cleaned up using :func:`close`.  This example uses a
``try:finally`` block to ensure that :func:`close` is always called,
even in the event of an error.

Echo Client
===========

The client program sets up its :class:`socket` differently from the
way a server does.  Instead of binding to a port and listening, it
uses :func:`connect` to attach the socket directly to the remote
address.

.. literalinclude:: socket_echo_client.py
   :lines: 10-19

After the connection is established, data can be sent through the
:class:`socket` with :func:`sendall` and received with :func:`recv`,
just as in the server.

.. literalinclude:: socket_echo_client.py
   :lines: 21-

When the entire message is sent and a copy received, the socket is
closed to free up the port.

Client and Server Together
==========================

The client and server should be run in separate terminal windows, so
they can communicate with each other.  The server output is:

::

    $ python ./socket_echo_server.py 

    starting up on localhost port 10000
    waiting for a connection
    connection from ('127.0.0.1', 52186)
    received "This is the mess"
    sending data back to the client
    received "age.  It will be"
    sending data back to the client
    received " repeated."
    sending data back to the client
    received ""
    no more data from ('127.0.0.1', 52186)
    waiting for a connection

The client output is:

::

    $ python socket_echo_client.py 

    connecting to localhost port 10000
    sending "This is the message.  It will be repeated."
    received "This is the mess"
    received "age.  It will be"
    received " repeated."
    closing socket

    $


Easy Client Connections
=======================

TCP/IP clients can save a few steps by using the convenience function
:func:`create_connection` to connect to a server.  The function takes
one argument, a two-value tuple containing the address of the server,
and derives the best address to use for the connection.

.. include:: socket_echo_client_easy.py
   :literal:
   :start-after: #end_pymotw_header

:func:`create_connection` uses :func:`getaddrinfo` to find candidate
connection parameters, and returns a :class:`socket` opened with the
first configuration that creates a successful connection.  The
:attr:`family`, :attr:`type`, and :attr:`proto` attributes can be
examined to determine the type of :class:`socket` being returned.

::

    $ python socket_echo_client_easy.py 
    
    Family  : AF_INET
    Type    : SOCK_STREAM
    Protocol: IPPROTO_TCP
    
    sending "This is the message.  It will be repeated."
    received "This is the mess"
    received "age.  It will be"
    received " repeated."
    closing socket

Choosing an Address for Listening
=================================

It is important to bind a server to the correct address, so that
clients can communicate with it.  The previous examples all used
``'localhost'`` as the IP address, which limits connections to clients
running on the same server.  Use a public address of the server, such
as the value returned by :func:`gethostname`, to allow other hosts to
connect.  This example modifies the echo server to listen on an
address specified via a command line argument.

.. include:: socket_echo_server_explicit.py
   :literal:
   :start-after: #end_pymotw_header

A similar modification to the client program is needed before the
server can be tested.

.. include:: socket_echo_client_explicit.py
   :literal:
   :start-after: #end_pymotw_header

After starting the server with the argument
``farnsworth.hellfly.net``, the :command:`netstat` command shows it
listening on the address for the named host.

::

    $ host farnsworth.hellfly.net

    farnsworth.hellfly.net has address 192.168.1.17
    
    $ netstat -an

    Active Internet connections (including servers)
    Proto Recv-Q Send-Q  Local Address          Foreign Address        (state)
    ...
    tcp4       0      0  192.168.1.17.10000     *.*                    LISTEN
    ...


Running the the client on another host, passing
``farnsworth.hellfly.net`` as the host where the server is running,
produces:

::

    $ hostname

    homer
    
    $ python socket_echo_client_explicit.py farnsworth.hellfly.net

    connecting to farnsworth.hellfly.net port 10000
    sending "This is the message.  It will be repeated."
    received "This is the mess"
    received "age.  It will be"
    received " repeated."

And the server output is:

::

    $ python ./socket_echo_server_explicit.py farnsworth.hellfly.net

    starting up on farnsworth.hellfly.net port 10000
    waiting for a connection
    client connected: ('192.168.1.8', 57471)
    received "This is the mess"
    received "age.  It will be"
    received " repeated."
    received ""
    waiting for a connection

Many servers have more than one network interface, and therefore more
than one IP address.  Rather than running separate copies of a service
bound to each IP address, use the special address :const:`INADDR_ANY`
to listen on all addresses at the same time.  Although :mod:`socket`
defines a constant for :const:`INADDR_ANY`, it is an integer value and
must be converted to a dotted-notation string address before it can be
passed to :func:`bind`.  As a shortcut, use the empty string ``''``
instead of doing the conversion.

.. include:: socket_echo_server_any.py
   :literal:
   :start-after: #end_pymotw_header

To see the actual address being used by a socket, call its
:func:`getsockname` method.  After starting the service, running
:command:`netstat` again shows it listening for incoming connections
on any address.

::

    $ netstat -an

    Active Internet connections (including servers)
    Proto Recv-Q Send-Q  Local Address          Foreign Address        (state)
    ...
    tcp4       0      0  *.10000                *.*                    LISTEN
    ...
