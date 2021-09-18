====================================
asyncore -- Asynchronous I/O handler
====================================

.. module:: asyncore
    :synopsis: Asynchronous I/O handler

:Purpose: Asynchronous I/O handler
:Available In: 1.5.2 and later

The asyncore module includes tools for working with I/O objects such as sockets so they can be managed asynchronously (instead of, for example, using threads).  The main class provided is :class:`dispatcher`, a wrapper around a socket that provides hooks for handling events like connecting, reading, and writing when invoked from the main loop function, :func:`loop`.

Clients
=======

To create an asyncore-based client, subclass :class:`dispatcher` and provide implementations for creating the socket, reading, and writing.  Let's examine this HTTP client, based on the one from the standard library documentation.

.. include:: asyncore_http_client.py
    :literal:
    :start-after: #end_pymotw_header

First, the socket is created in ``__init__()`` using the base class method ``create_socket()``.  Alternative implementations of the method may be provided, but in this case we want a TCP/IP socket so the base class version is sufficient.

The ``handle_connect()`` hook is present simply to illustrate when it is called.  Other types of clients that need to do some sort of hand-shaking or protocol negotiation should do the work in ``handle_connect()``.

``handle_close()`` is similarly presented for the purposes of showing when the method is called.  The base class version closes the socket correctly, so if you don't need to do extra cleanup on close you can leave the method out.

The asyncore loop uses ``writable()`` and its sibling method ``readable()`` to decide what actions to take with each dispatcher.  Actual use of poll() or select() on the sockets or file descriptors managed by each dispatcher is handled inside the :mod:`asyncore` code, so you don't need to do that yourself.  Simply indicate whether the dispatcher cares at all about reading or writing.  In the case of this HTTP client, ``writable()`` returns True as long as there is data from the request to send to the server.  ``readable()`` always returns True because we want to read all of the data.

Each time through the loop when ``writable()`` responds positively, ``handle_write()`` is invoked.  In this version, the HTTP request string that was built in ``__init__()`` is sent to the server and the write buffer is reduced by the amount successfully sent.

Similarly, when ``readable()`` responds positively and there is data to read, ``handle_read()`` is invoked.

The example below the ``__main__`` test configures logging for debugging then creates two clients to download two separate web pages.  Creating the clients registers them in a "map" kept internally by asyncore.  The downloading occurs as the loop iterates over the clients.  When the client reads 0 bytes from a socket that seems readable, the condition is interpreted as a closed connection and ``handle_close()`` is called.

One example of how this client app may run is:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncore_http_client.py'))
.. }}}

::

	$ python asyncore_http_client.py
	
	http://www.python.org/: connecting to ('www.python.org', 80)
	http://www.doughellmann.com/PyMOTW/contents.html: connecting to ('www.doughellmann.com', 80)
	root: LOOP STARTING
	http://www.python.org/: readable() -> True
	http://www.python.org/: writable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: writable() -> True
	http://www.python.org/: handle_connect()
	http://www.python.org/: handle_write() -> "GET http://www.python.org/ HTTP/1.0
	
	"
	http://www.python.org/: readable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: writable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: handle_connect()
	http://www.doughellmann.com/PyMOTW/contents.html: handle_write() -> "GET http://www.doughellmann.com/PyMOTW/contents.html HTTP/1.0
	
	"
	http://www.python.org/: readable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: handle_read() -> 2896 bytes
	http://www.python.org/: readable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	http://www.python.org/: readable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	http://www.python.org/: readable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	http://www.python.org/: readable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	http://www.python.org/: readable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	http://www.python.org/: readable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	http://www.python.org/: readable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	http://www.python.org/: readable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	http://www.python.org/: readable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	http://www.python.org/: readable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	http://www.python.org/: readable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	http://www.python.org/: readable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	http://www.python.org/: readable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: handle_read() -> 1432 bytes
	http://www.python.org/: readable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: handle_close()
	http://www.python.org/: handle_read() -> 0 bytes
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 481 bytes
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: handle_close()
	http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 0 bytes
	root: LOOP DONE
	http://www.python.org/ got 21704 bytes
	http://www.doughellmann.com/PyMOTW/contents.html got 481 bytes

.. {{{end}}}

Servers
=======

The example below illustrates using asyncore on the server by re-implementing the EchoServer from the :mod:`SocketServer` examples.  There are three classes: ``EchoServer`` receives incoming connections from clients and creates ``EchoHandler`` instances to deal with each.  The ``EchoClient`` is an asyncore dispatcher similar to the HttpClient defined above.

.. include:: asyncore_echo_server.py
    :literal:
    :start-after: #end_pymotw_header

The EchoServer and EchoHandler are defined in separate classes because they do different things.  When EchoServer accepts a connection, a new socket is established.  Rather than try to dispatch to individual clients within EchoServer, an EchoHandler is created to take advantage of the socket map maintained by asyncore.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncore_echo_server.py'))
.. }}}

::

	$ python asyncore_echo_server.py
	
	EchoServer: binding to ('127.0.0.1', 56199)
	EchoClient: connecting to ('127.0.0.1', 56199)
	EchoClient: writable() -> True
	EchoServer: handle_accept() -> ('127.0.0.1', 56200)
	EchoServer: handle_close()
	EchoClient: handle_connect()
	EchoClient: handle_write() -> (512) "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec
	egestas, enim et consectetuer ullamcorper, lectus ligula rutrum leo, a
	elementum elit tortor eu quam. Duis tincidunt nisi ut ante. Nulla
	facilisi. Sed tristique eros eu libero. Pellentesque vel arcu. Vivamus
	purus orci, iaculis ac, suscipit sit amet, pulvinar eu,
	lacus. Praesent placerat tortor sed nisl. Nunc blandit diam egestas
	dui. Pellentesque habitant morbi tristique senectus et netus et
	malesuada fames ac turpis egestas. Aliquam viverra f"
	EchoClient: writable() -> True
	EchoHandler('127.0.0.1', 56199): writable() -> False
	EchoHandler('127.0.0.1', 56199): handle_read() -> (256) "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec
	egestas, enim et consectetuer ullamcorper, lectus ligula rutrum leo, a
	elementum elit tortor eu quam. Duis tincidunt nisi ut ante. Nulla
	facilisi. Sed tristique eros eu libero. Pellentesque ve"
	EchoClient: handle_write() -> (225) "ringilla
	leo. Nulla feugiat augue eleifend nulla. Vivamus mauris. Vivamus sed
	mauris in nibh placerat egestas. Suspendisse potenti. Mauris massa. Ut
	eget velit auctor tortor blandit sollicitudin. Suspendisse imperdiet
	justo.
	"
	EchoClient: writable() -> False
	EchoHandler('127.0.0.1', 56199): writable() -> True
	EchoHandler('127.0.0.1', 56199): handle_read() -> (256) "l arcu. Vivamus
	purus orci, iaculis ac, suscipit sit amet, pulvinar eu,
	lacus. Praesent placerat tortor sed nisl. Nunc blandit diam egestas
	dui. Pellentesque habitant morbi tristique senectus et netus et
	malesuada fames ac turpis egestas. Aliquam viverra f"
	EchoHandler('127.0.0.1', 56199): handle_write() -> (256) "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec
	egestas, enim et consectetuer ullamcorper, lectus ligula rutrum leo, a
	elementum elit tortor eu quam. Duis tincidunt nisi ut ante. Nulla
	facilisi. Sed tristique eros eu libero. Pellentesque ve"
	EchoHandler('127.0.0.1', 56199): writable() -> True
	EchoClient: writable() -> False
	EchoHandler('127.0.0.1', 56199): writable() -> True
	EchoClient: handle_read() -> (256) "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec
	egestas, enim et consectetuer ullamcorper, lectus ligula rutrum leo, a
	elementum elit tortor eu quam. Duis tincidunt nisi ut ante. Nulla
	facilisi. Sed tristique eros eu libero. Pellentesque ve"
	EchoHandler('127.0.0.1', 56199): handle_read() -> (225) "ringilla
	leo. Nulla feugiat augue eleifend nulla. Vivamus mauris. Vivamus sed
	mauris in nibh placerat egestas. Suspendisse potenti. Mauris massa. Ut
	eget velit auctor tortor blandit sollicitudin. Suspendisse imperdiet
	justo.
	"
	EchoHandler('127.0.0.1', 56199): handle_write() -> (256) "l arcu. Vivamus
	purus orci, iaculis ac, suscipit sit amet, pulvinar eu,
	lacus. Praesent placerat tortor sed nisl. Nunc blandit diam egestas
	dui. Pellentesque habitant morbi tristique senectus et netus et
	malesuada fames ac turpis egestas. Aliquam viverra f"
	EchoHandler('127.0.0.1', 56199): writable() -> True
	EchoClient: writable() -> False
	EchoHandler('127.0.0.1', 56199): writable() -> True
	EchoClient: handle_read() -> (256) "l arcu. Vivamus
	purus orci, iaculis ac, suscipit sit amet, pulvinar eu,
	lacus. Praesent placerat tortor sed nisl. Nunc blandit diam egestas
	dui. Pellentesque habitant morbi tristique senectus et netus et
	malesuada fames ac turpis egestas. Aliquam viverra f"
	EchoHandler('127.0.0.1', 56199): handle_write() -> (225) "ringilla
	leo. Nulla feugiat augue eleifend nulla. Vivamus mauris. Vivamus sed
	mauris in nibh placerat egestas. Suspendisse potenti. Mauris massa. Ut
	eget velit auctor tortor blandit sollicitudin. Suspendisse imperdiet
	justo.
	"
	EchoHandler('127.0.0.1', 56199): writable() -> False
	EchoHandler('127.0.0.1', 56199): handle_close()
	EchoClient: writable() -> False
	EchoClient: handle_read() -> (225) "ringilla
	leo. Nulla feugiat augue eleifend nulla. Vivamus mauris. Vivamus sed
	mauris in nibh placerat egestas. Suspendisse potenti. Mauris massa. Ut
	eget velit auctor tortor blandit sollicitudin. Suspendisse imperdiet
	justo.
	"
	EchoClient: writable() -> False
	EchoClient: handle_close()
	EchoClient: RECEIVED COPY OF MESSAGE
	EchoClient: handle_read() -> (0) ""

.. {{{end}}}

In this example the server, handler, and client objects are all being maintained in the same socket map by asyncore in a single process. To separate the server from the client, simply instantiate them from separate scripts and run ``asyncore.loop()`` in both. When a dispatcher is closed, it is removed from the map maintained by asyncore and the loop exits when the map is empty.

Working with Other Event Loops
==============================

It is sometimes necessary to integrate the asyncore event loop with an event loop from the parent application.  For example, a GUI application would not want the UI to block until all asynchronous transfers are handled -- that would defeat the purpose of making them asynchronous.  To make this sort of integration easy, ``asyncore.loop()`` accepts arguments to set a timeout and to limit the number of times the loop is run.  We can see their effect on the client by re-using HttpClient from the first example.

.. include:: asyncore_loop.py
    :literal:
    :start-after: #end_pymotw_header

Here we see that the client is only asked to read or data once per call into ``asyncore.loop()``.  Instead of our own ``while`` loop, we could call ``asyncore.loop()`` like this from a GUI toolkit idle handler or other mechanism for doing a small amount of work when the UI is not busy with other event handlers.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncore_loop.py'))
.. }}}

::

	$ python asyncore_loop.py
	
	http://www.doughellmann.com/PyMOTW/contents.html: connecting to ('www.doughellmann.com', 80)
	http://www.python.org/: connecting to ('www.python.org', 80)
	root: loop_counter=1
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: writable() -> True
	http://www.python.org/: readable() -> True
	http://www.python.org/: writable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: handle_connect()
	http://www.doughellmann.com/PyMOTW/contents.html: handle_write() -> "GET http://www.doughellmann.com/PyMOTW/contents.html HTTP/1.0
	
	"
	root: loop_counter=2
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: readable() -> True
	http://www.python.org/: writable() -> True
	http://www.python.org/: handle_connect()
	http://www.python.org/: handle_write() -> "GET http://www.python.org/ HTTP/1.0
	
	"
	root: loop_counter=3
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: readable() -> True
	http://www.python.org/: handle_read() -> 2896 bytes
	root: loop_counter=4
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	root: loop_counter=5
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	root: loop_counter=6
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	root: loop_counter=7
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	root: loop_counter=8
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	root: loop_counter=9
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	root: loop_counter=10
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	root: loop_counter=11
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	root: loop_counter=12
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	root: loop_counter=13
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	root: loop_counter=14
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	root: loop_counter=15
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: readable() -> True
	http://www.python.org/: handle_read() -> 1448 bytes
	root: loop_counter=16
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: readable() -> True
	http://www.python.org/: handle_read() -> 1432 bytes
	root: loop_counter=17
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.python.org/: readable() -> True
	http://www.python.org/: handle_close()
	http://www.python.org/: handle_read() -> 0 bytes
	root: loop_counter=18
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	root: loop_counter=19
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 481 bytes
	root: loop_counter=20
	http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
	http://www.doughellmann.com/PyMOTW/contents.html: handle_close()
	http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 0 bytes

.. {{{end}}}

Working with Files
==================

Normally you would want to use asyncore with sockets, but there are times when it is useful to read files asynchronously, too (to use files when testing network servers without requiring the network setup, or to read or write large data files in parts).  For these situations, asyncore provides the :class:`file_dispatcher` and :class:`file_wrapper` classes.

.. include:: asyncore_file_dispatcher.py
    :literal:
    :start-after: #end_pymotw_header

This example was tested under Python 2.5.2, so I am using ``os.open()`` to get a file descriptor for the file.  For Python 2.6 and later, ``file_dispatcher`` automatically converts anything with a ``fileno()`` method to a file descriptor.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncore_file_dispatcher.py'))
.. }}}

::

	$ python asyncore_file_dispatcher.py
	
	READ: (256) "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec
	egestas, enim et consectetuer ullamcorper, lectus ligula rutrum leo, a
	elementum elit tortor eu quam. Duis tincidunt nisi ut ante. Nulla
	facilisi. Sed tristique eros eu libero. Pellentesque ve"
	READ: (256) "l arcu. Vivamus
	purus orci, iaculis ac, suscipit sit amet, pulvinar eu,
	lacus. Praesent placerat tortor sed nisl. Nunc blandit diam egestas
	dui. Pellentesque habitant morbi tristique senectus et netus et
	malesuada fames ac turpis egestas. Aliquam viverra f"
	READ: (225) "ringilla
	leo. Nulla feugiat augue eleifend nulla. Vivamus mauris. Vivamus sed
	mauris in nibh placerat egestas. Suspendisse potenti. Mauris massa. Ut
	eget velit auctor tortor blandit sollicitudin. Suspendisse imperdiet
	justo.
	"
	READ: (0) ""

.. {{{end}}}


.. seealso::

    `asyncore <http://docs.python.org/2.7/library/asyncore.html>`_
        The standard library documentation for this module.
    
    :mod:`asynchat`
        The asynchat module builds on asyncore to make it easier to create clients
        and servers communicate by passing messages back and forth using a set protocol.

    :mod:`SocketServer`
        The SocketServer module article includes another example of the EchoServer with
        threading and forking variants.
