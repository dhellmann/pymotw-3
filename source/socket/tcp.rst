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
sender.  It starts by creating a TCP/IP socket, then :func:`bind` is
used to associate the socket with the server address.  In this case,
the address is ``localhost``, referring to the current server, and the
port number is 10000.


.. literalinclude:: socket_echo_server.py
   :caption:
   :start-after: #end_pymotw_header

Calling :func:`listen` puts the socket into server mode, and
:func:`accept` waits for an incoming connection.  The integer argument
is the number of connections the system should queue up in the
background before rejecting new clients.  This example only expects to
work with one connection at a time.

:func:`accept` returns an open connection between the server and
client, along with the address of the client.  The connection is
actually a different socket on another port (assigned by the kernel).
Data is read from the connection with :func:`recv` and transmitted
with :func:`sendall`.

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
   :caption:
   :start-after: #end_pymotw_header

After the connection is established, data can be sent through the
:class:`socket` with :func:`sendall` and received with :func:`recv`,
just as in the server. When the entire message is sent and a copy
received, the socket is closed to free up the port.

Client and Server Together
==========================

The client and server should be run in separate terminal windows, so
they can communicate with each other.  The server output shows the
incoming connection and data, as well as the response sent back to
the client.

.. NOT RUNNING

.. code-block:: none

   $ python3 socket_echo_server.py
   starting up on localhost port 10000
   waiting for a connection
   connection from ('127.0.0.1', 65141)
   received b'This is the mess'
   sending data back to the client
   received b'age.  It will be'
   sending data back to the client
   received b' repeated.'
   sending data back to the client
   received b''
   no data from ('127.0.0.1', 65141)
   waiting for a connection

The client output shows the outgoing message and the response from the
server.

.. NOT RUNNING

.. code-block:: none

   $ python3 socket_echo_client.py
   connecting to localhost port 10000
   sending b'This is the message.  It will be repeated.'
   received b'This is the mess'
   received b'age.  It will be'
   received b' repeated.'
   closing socket

Easy Client Connections
=======================

TCP/IP clients can save a few steps by using the convenience function
:func:`create_connection` to connect to a server.  The function takes
one argument, a two-value tuple containing the address of the server,
and derives the best address to use for the connection.

.. literalinclude:: socket_echo_client_easy.py
   :caption:
   :start-after: #end_pymotw_header

:func:`create_connection` uses :func:`getaddrinfo` to find candidate
connection parameters, and returns a :class:`socket` opened with the
first configuration that creates a successful connection.  The
:attr:`family`, :attr:`type`, and :attr:`proto` attributes can be
examined to determine the type of :class:`socket` being returned.

.. NOT RUNNING

.. code-block:: none

   $ python3 socket_echo_client_easy.py
   Family  : AF_INET
   Type    : SOCK_STREAM
   Protocol: IPPROTO_TCP
   
   sending b'This is the message.  It will be repeated.'
   received b'This is the mess'
   received b'age.  It will be'
   received b' repeated.'
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

.. literalinclude:: socket_echo_server_explicit.py
   :caption:
   :start-after: #end_pymotw_header

A similar modification to the client program is needed before the
server can be tested.

.. literalinclude:: socket_echo_client_explicit.py
   :caption:
   :start-after: #end_pymotw_header

After starting the server with the argument ``hubert``, the
``netstat`` command shows it listening on the address for the
named host.

.. NOT RUNNING

.. code-block:: none

    $ host hubert.hellfly.net

    hubert.hellfly.net has address 10.9.0.6
    
    $ netstat -an | grep 10000

    Active Internet connections (including servers)
    Proto Recv-Q Send-Q  Local Address          Foreign Address        (state)
    ...
    tcp4       0      0  10.9.0.6.10000         *.*                    LISTEN
    ...

Running the client on another host, passing
``hubert.hellfly.net`` as the host where the server is running,
produces:

.. NOT RUNNING

.. code-block:: none

    $ hostname

    apu
    
    $ python3 ./socket_echo_client_explicit.py hubert.hellfly.net
    connecting to hubert.hellfly.net port 10000
    sending b'This is the message.  It will be repeated.'
    received b'This is the mess'
    received b'age.  It will be'
    received b' repeated.'

And the server output is:

.. NOT RUNNING

.. code-block:: none

   $ python3 socket_echo_server_explicit.py hubert.hellfly.net
   starting up on hubert.hellfly.net port 10000
   waiting for a connection
   client connected: ('10.9.0.10', 33139)
   received b''
   waiting for a connection
   client connected: ('10.9.0.10', 33140)
   received b'This is the mess'
   received b'age.  It will be'
   received b' repeated.'
   received b''
   waiting for a connection

Many servers have more than one network interface, and therefore more
than one IP address.  Rather than running separate copies of a service
bound to each IP address, use the special address :const:`INADDR_ANY`
to listen on all addresses at the same time.  Although ``socket``
defines a constant for :const:`INADDR_ANY`, it is an integer value and
must be converted to a dotted-notation string address before it can be
passed to :func:`bind`.  As a shortcut, use "``0.0.0.0``" or an empty
string (``''``) instead of doing the conversion.

.. literalinclude:: socket_echo_server_any.py
   :caption:
   :start-after: #end_pymotw_header

To see the actual address being used by a socket, call its
:func:`getsockname` method.  After starting the service, running
``netstat`` again shows it listening for incoming connections
on any address.

.. NOT RUNNING

.. code-block:: none

    $ netstat -an

    Active Internet connections (including servers)
    Proto Recv-Q Send-Q  Local Address    Foreign Address  (state)
    ...
    tcp4       0      0  *.10000          *.*              LISTEN
    ...
