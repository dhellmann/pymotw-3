===========================================================
BaseHTTPServer -- base classes for implementing web servers
===========================================================

.. module:: BaseHTTPServer
    :synopsis: Provides base classes for implementing web servers.

:Purpose: BaseHTTPServer includes classes that can form the basis of a web server.
:Available In: 1.4 and later


:mod:`BaseHTTPServer` uses classes from :mod:`SocketServer` to create
base classes for making HTTP servers. :class:`HTTPServer` can be used
directly, but the :class:`BaseHTTPRequestHandler` is intended to be
extended to handle each protocol method (GET, POST, etc.).

HTTP GET
========

To add support for an HTTP method in your request handler class,
implement the method :func:`do_METHOD`, replacing *METHOD* with the
name of the HTTP method. For example, :func:`do_GET`, :func:`do_POST`,
etc. For consistency, the method takes no arguments. All of the
parameters for the request are parsed by
:class:`BaseHTTPRequestHandler` and stored as instance attributes of
the request instance.

This example request handler illustrates how to return a response to the
client and some of the local attributes which can be useful in building the
response:

.. include:: BaseHTTPServer_GET.py
    :literal:
    :start-after: #end_pymotw_header

The message text is assembled and then written to :attr:`wfile`, the
file handle wrapping the response socket. Each response needs a
response code, set via :func:`send_response`. If an error code is used
(404, 501, etc.), an appropriate default error message is included in
the header, or a message can be passed with the error code.

To run the request handler in a server, pass it to the constructor of
HTTPServer, as in the ``__main__`` processing portion of the sample script.

Then start the server:

::

    $ python BaseHTTPServer_GET.py 
    Starting server, use <Ctrl-C> to stop

In a separate terminal, use :command:`curl` to access it:

::

    $ curl -i http://localhost:8080/?foo=barHTTP/1.0 200 OK
    Server: BaseHTTP/0.3 Python/2.5.1
    Date: Sun, 09 Dec 2007 16:00:34 GMT

    CLIENT VALUES:
    client_address=('127.0.0.1', 51275) (localhost)
    command=GET
    path=/?foo=bar
    real path=/
    query=foo=bar
    request_version=HTTP/1.1

    SERVER VALUES:
    server_version=BaseHTTP/0.3
    sys_version=Python/2.5.1
    protocol_version=HTTP/1.0



HTTP POST
=========

Supporting POST requests is a little more work, because the base class
does not parse the form data for us. The :mod:`cgi` module provides
the :class:`FieldStorage` class which knows how to parse the form, if
it is given the correct inputs.

.. include:: BaseHTTPServer_POST.py
    :literal:
    :start-after: #end_pymotw_header

:command:`curl` can include form data in the message it posts to the
server. The last argument, ``-F datafile=@BaseHTTPServer_GET.py``,
posts the contents of the file ``BaseHTTPServer_GET.py`` to illustrate
reading file data from the form.

::

    $ curl http://localhost:8080/ -F name=dhellmann -F foo=bar -F  datafile=@BaseHTTPServer_GET.py
    Client: ('127.0.0.1', 51128)
    Path: /
    Form data:
            name=dhellmann
            foo=bar
            Uploaded datafile (2222 bytes)


Threading and Forking
=====================

:class:`HTTPServer` is a simple subclass of
:class:`SocketServer.TCPServer`, and does not use multiple threads or
processes to handle requests. To add threading or forking, create a
new class using the appropriate mix-in from :mod:`SocketServer`.

.. include:: BaseHTTPServer_threads.py
    :literal:
    :start-after: #end_pymotw_header

Each time a request comes in, a new thread or process is created to
handle it:

::

    $ curl http://localhost:8080/
    Thread-1
    $ curl http://localhost:8080/
    Thread-2
    $ curl http://localhost:8080/
    Thread-3

Swapping :class:`ForkingMixIn` for :class:`ThreadingMixIn` above would
achieve similar results, using separate processes instead of threads.

Handling Errors
===============

Error handling is made easy with :meth:`send_error()`. Simply pass the
appropriate error code and an optional error message, and the entire
response (with headers, status code, and body) is generated
automatically.

.. include:: BaseHTTPServer_errors.py
    :literal:
    :start-after: #end_pymotw_header

In this case, a 404 error is always returned.

::

    $ curl -i http://localhost:8080/
    HTTP/1.0 404 Not Found
    Server: BaseHTTP/0.3 Python/2.5.1
    Date: Sun, 09 Dec 2007 15:49:44 GMT
    Content-Type: text/html
    Connection: close

    <head>
    <title>Error response</title>
    </head>
    <body>
    <h1>Error response</h1>
    <p>Error code 404.
    <p>Message: Not Found.
    <p>Error code explanation: 404 = Nothing matches the given URI.
    </body>

Setting Headers
===============

The :mod:`send_header` method adds header data to the HTTP response.
It takes two arguments, the name of the header and the value.

.. include:: BaseHTTPServer_send_header.py
   :literal:
   :start-after: #end_pymotw_header

This example sets the ``Last-Modified`` header to the current
timestamp formatted according to :rfc:`2822`.

::

    $ curl -i http://localhost:8080/
    HTTP/1.0 200 OK
    Server: BaseHTTP/0.3 Python/2.7
    Date: Sun, 10 Oct 2010 13:58:32 GMT
    Last-Modified: Sun, 10 Oct 2010 13:58:32 -0000
    
    Response body


.. seealso::

    `BaseHTTPServer <http://docs.python.org/2.7/library/basehttpserver.html>`_
        The standard library documentation for this module.

    :mod:`SocketServer`
        The SocketServer module provides the base class which handles
        the raw socket connection.
