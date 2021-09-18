=========================================
SocketServer -- Creating network servers.
=========================================

.. module:: SocketServer
    :synopsis: Creating network servers.

:Purpose: Creating network servers.
:Available In: 1.4

The :mod:`SocketServer` module is a framework for creating network
servers. It defines classes for handling synchronous network requests
(the server request handler blocks until the request is completed)
over TCP, UDP, Unix streams, and Unix datagrams. It also provides
mix-in classes for easily converting servers to use a separate thread
or process for each request, depending on what is most appropriate for
your situation.

Responsibility for processing a request is split between a server
class and a request handler class. The server deals with the
communication issues (listing on a socket, accepting connections,
etc.) and the request handler deals with the "protocol" issues
(interpreting incoming data, processing it, sending data back to the
client). This division of responsibility means that in many cases you
can simply use one of the existing server classes without any
modifications, and provide a request handler class for it to work with
your protocol.

Server Types
============

There are five different server classes defined in
:mod:`SocketServer`.  :class:`BaseServer` defines the API, and is not
really intended to be instantiated and used
directly. :class:`TCPServer` uses TCP/IP sockets to
communicate. :class:`UDPServer` uses datagram
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
requests. The :func:`serve_forever()` method simply calls
:func:`handle_request()` in an infinite loop, so if you need to
integrate the server with another event loop or use :func:`select()`
to monitor several sockets for different servers, you could call
:func:`handle_request()` on your own. See the example below for more
detail.

Implementing a Server
=====================

If you are creating a server, it is usually possible to re-use one of
the existing classes and simply provide a custom request handler
class. If that does not meet your needs, there are several methods of
:class:`BaseServer` available to override in a subclass:

* ``verify_request(request, client_address)`` - Return True to process
  the request or False to ignore it. You could, for example, refuse
  requests from an IP range if you want to block certain clients from
  accessing the server.

* ``process_request(request, client_address)`` - Typically just calls
  :func:`finish_request()` to actually do the work. It can also create
  a separate thread or process, as the mix-in classes do (see below).

* ``finish_request(request, client_address)`` - Creates a request
  handler instance using the class given to the server's
  constructor. Calls :func:`handle()` on the request handler to
  process the request.

Request Handlers
================

Request handlers do most of the work of receiving incoming requests and
deciding what action to take. The handler is responsible for implementing the
"protocol" on top of the socket layer (for example, HTTP or XML-RPC). The
request handler reads the request from the incoming data channel, processes
it, and writes a response back out. There are 3 methods available to be
over-ridden.

* ``setup()`` - Prepare the request handler for the request. In the
  :class:`StreamRequestHandler`, for example, the :func:`setup()`
  method creates file-like objects for reading from and writing to the
  socket.

* ``handle()`` - Do the real work for the request. Parse the incoming
  request, process the data, and send a response.

* ``finish()`` - Clean up anything created during :func:`setup()`.

In many cases, you can simply provide a :func:`handle()` method.

Echo Example
============

Let's look at a simple server/request handler pair that accepts TCP
connectcions and echos back any data sent by the client. The only
method that actually needs to be provided in the sample code is
:func:`EchoRequestHandler.handle()`, but all of the methods described
above are overridden to insert :mod:`logging` calls so the output of
the sample program illustrates the sequence of calls made.

The only thing left is to have simple program that creates the
server, runs it in a thread, and connects to it to illustrate which
methods are called as the data is echoed back.

.. include:: SocketServer_echo.py
    :literal:
    :start-after: #end_pymotw_header

The output for the program should look something like this:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'SocketServer_echo.py'))
.. }}}

::

	$ python SocketServer_echo.py
	
	EchoServer: __init__
	EchoServer: server_activate
	EchoServer: waiting for request
	client: Server on 127.0.0.1:56210
	EchoServer: Handling requests, press <Ctrl-C> to quit
	client: creating socket
	EchoServer: handle_request
	client: connecting to server
	client: sending data: "Hello, world"
	EchoServer: verify_request(<socket._socketobject object at 0x1004cdfa0>, ('127.0.0.1', 56211))
	EchoServer: process_request(<socket._socketobject object at 0x1004cdfa0>, ('127.0.0.1', 56211))
	client: waiting for response
	EchoServer: finish_request(<socket._socketobject object at 0x1004cdfa0>, ('127.0.0.1', 56211))
	EchoRequestHandler: __init__
	EchoRequestHandler: setup
	EchoRequestHandler: handle
	EchoRequestHandler: recv()->"Hello, world"
	EchoRequestHandler: finish
	client: response from server: "Hello, world"
	EchoServer: close_request(<socket._socketobject object at 0x1004cdfa0>)
	client: closing socket
	EchoServer: handle_request
	client: done

.. {{{end}}}

The port number used will change each time you run it, as the kernel
allocates an available port automatically. If you want the server to
listen on a specific port each time you run it, provide that number in
the address tuple instead of the ``0``.

Here is a simpler version of the same thing, without the
:mod:`logging`:

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

Adding threading or forking support to a server is as simple as
including the appropriate mix-in in the class hierarchy for the
server. The mix-in classes override :func:`process_request()` to start
a new thread or process when a request is ready to be handled, and the
work is done in the new child.

For threads, use the :class:`ThreadingMixIn`:

.. include:: SocketServer_threaded.py
    :literal:
    :start-after: #end_pymotw_header

The response from the server includes the id of the thread where the
request is handled:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'SocketServer_threaded.py'))
.. }}}

::

	$ python SocketServer_threaded.py
	
	Server loop running in thread: Thread-1
	Sending : "Hello, world"
	Received: "Thread-2: Hello, world"

.. {{{end}}}

To use separate processes, use the :class:`ForkingMixIn`:

.. include:: SocketServer_forking.py
    :literal:
    :start-after: #end_pymotw_header

In this case, the process id of the child is included in the response
from the server:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'SocketServer_forking.py'))
.. }}}

::

	$ python SocketServer_forking.py
	
	Server loop running in process: 14610
	Sending : "Hello, world"
	Received: "14611: Hello, world"

.. {{{end}}}


.. seealso::

    `SocketServer <https://docs.python.org/2/library/socketserver.html>`_
        Standard library documentation for this module.

    :mod:`asyncore`
        Use asyncore to create asynchronous servers that do not block while processing a
        request.

    :mod:`SimpleXMLRPCServer`
        XML-RPC server built using :mod:`SocketServer`.
