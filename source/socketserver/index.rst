===========================================
 socketserver --- Creating Network Servers
===========================================

.. module:: socketserver
    :synopsis: Creating network servers.

:Purpose: Creating network servers.

The :mod:`socketserver` module is a framework for creating network
servers. It defines classes for handling synchronous network requests
(the server request handler blocks until the request is completed)
over TCP, UDP, UNIX streams, and UNIX datagrams. It also provides
mix-in classes for easily converting servers to use a separate thread
or process for each request.

Responsibility for processing a request is split between a server
class and a request handler class. The server deals with the
communication issues, such as listening on a socket and accepting
connections, and the request handler deals with the "protocol"
issues like interpreting incoming data, processing it, and sending
data back to the client. This division of responsibility means that
many applications can use one of the existing server classes without
any modifications, and provide a request handler class for it to work
with the custom protocol.

Server Types
============

There are five different server classes defined in
:mod:`socketserver`.  :class:`BaseServer` defines the API, and is not
intended to be instantiated and used directly. :class:`TCPServer` uses
TCP/IP sockets to communicate. :class:`UDPServer` uses datagram
sockets. :class:`UnixStreamServer` and :class:`UnixDatagramServer` use
UNIX-domain sockets and are only available on UNIX platforms.

Server Objects
==============

To construct a server, pass it an address on which to listen for
requests and a request handler *class* (not instance). The address
format depends on the server type and the socket family used. Refer to
the :mod:`socket` module documentation for details.

Once the server object is instantiated, use either
:func:`handle_request` or :func:`serve_forever` to process
requests. The :func:`serve_forever` method calls
:func:`handle_request` in an infinite loop, but if an application
needs to integrate the server with another event loop or use
:func:`select` to monitor several sockets for different servers, it
can call :func:`handle_request` directly.

Implementing a Server
=====================

When creating a server, it is usually sufficient to reuse one of the
existing classes and provide a custom request handler class.  For
other cases, :class:`BaseServer` includes several methods that can be
overridden in a subclass.

* ``verify_request(request, client_address)``: Return ``True`` to process
  the request or ``False`` to ignore it. For example, a server could
  refuse requests from an IP range or if it is overloaded.

* ``process_request(request, client_address)``: Calls
  :func:`finish_request` to actually do the work of handling the
  request.  It can also create a separate thread or process, as the
  mix-in classes do.

* ``finish_request(request, client_address)``: Creates a request
  handler instance using the class given to the server's
  constructor. Calls :func:`handle` on the request handler to
  process the request.

Request Handlers
================

Request handlers do most of the work of receiving incoming requests
and deciding what action to take. The handler is responsible for
implementing the protocol on top of the socket layer (i.e., HTTP,
XML-RPC, or AMQP). The request handler reads the request from the
incoming data channel, processes it, and writes a response back
out. There are three methods available to be over-ridden.

* ``setup()``: Prepares the request handler for the request. In the
  :class:`StreamRequestHandler` the :func:`setup` method creates
  file-like objects for reading from and writing to the socket.

* ``handle()``: Does the real work for the request. Parse the incoming
  request, process the data, and send a response.

* ``finish()``: Cleans up anything created during :func:`setup`.

Many handlers can be implemented with only a :func:`handle` method.

Echo Example
============

This example implements a simple server/request handler pair that
accepts TCP connections and echos back any data sent by the
client. It starts with the request handler.

.. literalinclude:: socketserver_echo.py
   :caption:
   :lines: 6-40

The only method that actually needs to be implemented is
:func:`EchoRequestHandler.handle`, but versions of all of the
methods described earlier are included to illustrate the sequence of
calls made.  The :class:`EchoServer` class does nothing
different from :class:`TCPServer`, except log when each method is
called.

.. literalinclude:: socketserver_echo.py
   :lines: 43-104

The last step is to add a main program that sets up the server to run in
a thread, and sends it data to illustrate which methods are called as
the data is echoed back.

.. literalinclude:: socketserver_echo.py
   :lines: 107-

Running the program produces the following output.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'socketserver_echo.py', break_lines_at=68))
.. }}}

::

	$ python3 socketserver_echo.py
	
	EchoServer: __init__
	EchoServer: server_activate
	EchoServer: waiting for request
	EchoServer: Handling requests, press <Ctrl-C> to quit
	client: Server on 127.0.0.1:53917
	client: creating socket
	client: connecting to server
	client: sending data: b'Hello, world'
	client: waiting for response
	EchoServer: verify_request(<socket.socket fd=7, family=AddressFamily
	.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 
	53917), raddr=('127.0.0.1', 53918)>, ('127.0.0.1', 53918))
	EchoServer: process_request(<socket.socket fd=7, family=AddressFamil
	y.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1',
	 53917), raddr=('127.0.0.1', 53918)>, ('127.0.0.1', 53918))
	EchoServer: finish_request(<socket.socket fd=7, family=AddressFamily
	.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 
	53917), raddr=('127.0.0.1', 53918)>, ('127.0.0.1', 53918))
	EchoRequestHandler: __init__
	EchoRequestHandler: setup
	EchoRequestHandler: handle
	EchoRequestHandler: recv()->"b'Hello, world'"
	EchoRequestHandler: finish
	client: response from server: b'Hello, world'
	EchoServer: shutdown()
	EchoServer: close_request(<socket.socket fd=7, family=AddressFamily.
	AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 5
	3917), raddr=('127.0.0.1', 53918)>)
	client: closing socket
	client: done

.. {{{end}}}

.. note::

  The port number used will change each time the program runs
  because the kernel allocates an available port automatically. To
  make the server listen on a specific port each time, provide that
  number in the address tuple instead of the ``0``.

Here is a condensed version of the same server, without the logging
calls.  Only the :func:`handle` method in the request handler class
needs to be provided.

.. literalinclude:: socketserver_echo_simple.py
    :caption:
    :start-after: #end_pymotw_header

In this case, no special server class is required since the
:mod:`TCPServer` handles all of the server requirements.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'socketserver_echo_simple.py'))
.. }}}

::

	$ python3 socketserver_echo_simple.py
	
	Sending : b'Hello, world'
	Received: b'Hello, world'

.. {{{end}}}

Threading and Forking
=====================

To add threading or forking support to a server, include the
appropriate mix-in in the class hierarchy for the server. The mix-in
classes override :func:`process_request` to start a new thread or
process when a request is ready to be handled, and the work is done in
the new child.

For threads, use :class:`ThreadingMixIn`.

.. literalinclude:: socketserver_threaded.py
    :caption:
    :start-after: #end_pymotw_header

The response from this threaded server includes the identifier of the
thread where the request is handled.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'socketserver_threaded.py'))
.. }}}

::

	$ python3 socketserver_threaded.py
	
	Server loop running in thread: Thread-1
	Sending : b'Hello, world'
	Received: b'Thread-2: Hello, world'

.. {{{end}}}

For separate processes, use the :class:`ForkingMixIn`.

.. literalinclude:: socketserver_forking.py
    :caption:
    :start-after: #end_pymotw_header

In this case, the process ID of the child is included in the response
from the server:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'socketserver_forking.py'))
.. }}}

::

	$ python3 socketserver_forking.py
	
	Server loop running in process: 69953
	Sending : b'Hello, world'
	Received: b'69954: Hello, world'

.. {{{end}}}


.. seealso::

    * :pydoc:`socketserver`

    * :mod:`socket` -- Low-level network communication

    * :mod:`select` -- Low-level asynchronous I/O tools

    * :mod:`asyncio` -- Asynchronous I/O, event loop, and concurrency tools

    * :mod:`SimpleXMLRPCServer` -- XML-RPC server built using
      :mod:`socketserver`.

    * *Unix Network Programming, Volume 1: The Sockets Networking API, 3/E*
      By W. Richard Stevens, Bill Fenner, and Andrew
      M. Rudoff. Published by Addison-Wesley Professional, 2004.
      ISBN-10: 0131411551

    * *Foundations of Python Network Programminng, 3/E* By Brandon
      Rhodes and John Goerzen. Published by Apress, 2014. ISBN-10:
      1430258543
