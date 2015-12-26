==========================================
 SocketServer -- Creating Network Servers
==========================================

.. module:: SocketServer
    :synopsis: Creating network servers.

:Purpose: Creating network servers.
:Python Version: 1.4 and later

The :mod:`SocketServer` module is a framework for creating network
servers. It defines classes for handling synchronous network requests
(the server request handler blocks until the request is completed)
over TCP, UDP, Unix streams, and Unix datagrams. It also provides
mix-in classes for easily converting servers to use a separate thread
or process for each request.

Responsibility for processing a request is split between a server
class and a request handler class. The server deals with the
communication issues such as listening on a socket and accepting
connections, and the request handler deals with the "protocol"
issues like interpreting incoming data, processing it, and sending
data back to the client. This division of responsibility means that
many applications can use one of the existing server classes without
any modifications, and provide a request handler class for it to work
with the custom protocol.

Server Types
============

There are five different server classes defined in
:mod:`SocketServer`.  :class:`BaseServer` defines the API, and is not
intended to be instantiated and used directly. :class:`TCPServer` uses
TCP/IP sockets to communicate. :class:`UDPServer` uses datagram
sockets. :class:`UnixStreamServer` and :class:`UnixDatagramServer` use
Unix-domain sockets and are only available on Unix platforms.

Server Objects
==============

To construct a server, pass it an address on which to listen for
requests and a request handler *class* (not instance). The address
format depends on the server type and the socket family used. Refer to
the :mod:`socket` module documentation for details.

Once the server object is instantiated, use either
:func:`handle_request()` or :func:`serve_forever()` to process
requests. The :func:`serve_forever()` method calls
:func:`handle_request()` in an infinite loop, but if an application
needs to integrate the server with another event loop or use
:func:`select()` to monitor several sockets for different servers, it
can call :func:`handle_request()` directly.

Implementing a Server
=====================

When creating a server, it is usually sufficient to re-use one of the
existing classes and provide a custom request handler class.  For
other cases, :class:`BaseServer` includes several methods that can be
overridden in a subclass.

* ``verify_request(request, client_address)``: Return True to process
  the request or False to ignore it. For example, a server could
  refuse requests from an IP range or if it is overloaded.

* ``process_request(request, client_address)``: Calls
  :func:`finish_request()` to actually do the work of handling the
  request.  It can also create a separate thread or process, as the
  mix-in classes do.

* ``finish_request(request, client_address)``: Creates a request
  handler instance using the class given to the server's
  constructor. Calls :func:`handle()` on the request handler to
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
  :class:`StreamRequestHandler` the :func:`setup()` method creates
  file-like objects for reading from and writing to the socket.

* ``handle()``: Does the real work for the request. Parse the incoming
  request, process the data, and send a response.

* ``finish()``: Cleans up anything created during :func:`setup()`.

Many handlers can be implemented with only a :func:`handle()` method.

Echo Example
============

This example implements a simple server/request handler pair that
accepts TCP connections and echos back any data sent by the
client. It starts with the request handler.

.. literalinclude:: SocketServer_echo.py
   :lines: 6-39

The only method that actually needs to be implemented is
:func:`EchoRequestHandler.handle()`, but versions of all of the
methods described earlier are included to illustrate the sequence of
calls made.  The :class:`EchoServer` class does nothing
different from :class:`TCPServer`, except log when each method is
called.

.. literalinclude:: SocketServer_echo.py
   :lines: 41-96

The last step is to add a main program that sets up the server to run in
a thread, and sends it data to illustrate which methods are called as
the data is echoed back.

.. literalinclude:: SocketServer_echo.py
   :lines: 99-

Running the program produces:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'SocketServer_echo.py', break_lines_at=68))
.. }}}

::

	$ python SocketServer_echo.py

	EchoServer: __init__
	EchoServer: server_activate
	EchoServer: waiting for request
	EchoServer: Handling requests, press <Ctrl-C> to quit
	client: Server on 127.0.0.1:62859
	client: creating socket
	client: connecting to server
	EchoServer: verify_request(<socket._socketobject object at 0x100e1b8
	a0>, ('127.0.0.1', 62860))
	EchoServer: process_request(<socket._socketobject object at 0x100e1b
	8a0>, ('127.0.0.1', 62860))
	EchoServer: finish_request(<socket._socketobject object at 0x100e1b8
	a0>, ('127.0.0.1', 62860))
	EchoRequestHandler: __init__
	EchoRequestHandler: setup
	EchoRequestHandler: handle
	client: sending data: "Hello, world"
	EchoRequestHandler: recv()->"Hello, world"
	EchoRequestHandler: finish
	EchoServer: close_request(<socket._socketobject object at 0x100e1b8a
	0>)
	client: waiting for response
	client: response from server: "Hello, world"
	EchoServer: shutdown()
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

.. include:: SocketServer_echo_simple.py
    :literal:
    :start-after: #end_pymotw_header

In this case, no special server class is required since the
:mod:`TCPServer` handles all of the server requirements.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'SocketServer_echo_simple.py'))
.. }}}

::

	$ python SocketServer_echo_simple.py

	Sending : "Hello, world"
	Received: "Hello, world"

.. {{{end}}}

Threading and Forking
=====================

To add threading or forking support to a server, include the
appropriate mix-in in the class hierarchy for the server. The mix-in
classes override :func:`process_request()` to start a new thread or
process when a request is ready to be handled, and the work is done in
the new child.

For threads, use :class:`ThreadingMixIn`.

.. include:: SocketServer_threaded.py
    :literal:
    :start-after: #end_pymotw_header

The response from this threaded server includes the identifier of the
thread where the request is handled:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'SocketServer_threaded.py'))
.. }}}

::

	$ python SocketServer_threaded.py

	Server loop running in thread: Thread-1
	Sending : "Hello, world"
	Received: "Thread-2: Hello, world"

.. {{{end}}}

For separate processes, use the :class:`ForkingMixIn`.

.. include:: SocketServer_forking.py
    :literal:
    :start-after: #end_pymotw_header

In this case, the process ID of the child is included in the response
from the server:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'SocketServer_forking.py'))
.. }}}

::

	$ python SocketServer_forking.py

	Server loop running in process: 12797
	Sending : "Hello, world"
	Received: "12798: Hello, world"

.. {{{end}}}


.. seealso::

    `SocketServer <http://docs.python.org/lib/module-SocketServer.html>`_
        Standard library documentation for this module.

    :mod:`asyncore`
        Use ``asyncore`` to create asynchronous servers that do not
        block while processing a request.

    :mod:`SimpleXMLRPCServer`
        XML-RPC server built using :mod:`SocketServer`.
