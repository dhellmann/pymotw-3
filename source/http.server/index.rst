===========================================================
 http.server --- Base Classes for Implementing Web Servers
===========================================================

.. module:: http.server
    :synopsis: Base classes for implementing web servers.

:Purpose: http.server includes classes that can form the basis of a
          web server.

:mod:`http.server` uses classes from :mod:`socketserver` to create
base classes for making HTTP servers. :class:`HTTPServer` can be used
directly, but the :class:`BaseHTTPRequestHandler` is intended to be
extended to handle each protocol method (GET, POST, etc.).

HTTP GET
========

To add support for an HTTP method in a request handler class,
implement the method :func:`do_METHOD`, replacing *METHOD* with the
name of the HTTP method (e.g., :func:`do_GET`, :func:`do_POST`,
etc.). For consistency, the request handler methods take no
arguments. All of the parameters for the request are parsed by
:class:`BaseHTTPRequestHandler` and stored as instance attributes of
the request instance.

This example request handler illustrates how to return a response to the
client, and some of the local attributes that can be useful in building the
response.

.. literalinclude:: http_server_GET.py
    :caption:
    :start-after: #end_pymotw_header

The message text is assembled and then written to :attr:`wfile`, the
file handle wrapping the response socket. Each response needs a
response code, set via :func:`send_response`. If an error code is used
(404, 501, etc.), an appropriate default error message is included in
the header, or a message can be passed with the error code.

To run the request handler in a server, pass it to the constructor of
:class:`HTTPServer`, as in the ``__main__`` processing portion of the
sample script.

Then start the server:

.. code-block:: none

    $ python3 http_server_GET.py 

    Starting server, use <Ctrl-C> to stop

In a separate terminal, use :command:`curl` to access it:

.. code-block:: none

    $ curl -i http://localhost:8080/?foo=bar
    
    HTTP/1.0 200 OK

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
does not parse the form data automatically. The :mod:`cgi` module
provides the :class:`FieldStorage` class which knows how to parse the
form, if it is given the correct inputs.

.. literalinclude:: http_server_POST.py
    :caption:
    :start-after: #end_pymotw_header

Run the server in one window:

.. code-block:: none

    $ python3 http_server_POST.py 
    
    Starting server, use <Ctrl-C> to stop

The arguments to :command:`curl` can include form data to be posted to
the server by using the ``-F`` option. The last argument, ``-F
datafile=@http_server_GET.py``, posts the contents of the file
``http_server_GET.py`` to illustrate reading file data from the
form.

.. code-block:: none
    
    $ curl http://localhost:8080/ -F name=dhellmann -F foo=bar \
    -F datafile=@http_server_GET.py
    
    Client: ('127.0.0.1', 65029)
    User-agent: curl/7.19.7 (universal-apple-darwin10.0) libcurl/7.19.7 
    OpenSSL/0.9.8l zlib/1.2.3
    Path: /
    Form data:
        Uploaded datafile as "http_server_GET.py" (2580 bytes)
        foo=bar
        name=dhellmann


Threading and Forking
=====================

:class:`HTTPServer` is a simple subclass of
:class:`SocketServer.TCPServer`, and does not use multiple threads or
processes to handle requests. To add threading or forking, create a
new class using the appropriate mix-in from :mod:`SocketServer`.

.. literalinclude:: http_server_threads.py
    :caption:
    :start-after: #end_pymotw_header

Run the server in the same way as the other examples.

.. code-block:: none

    $ python3 http_server_threads.py 
    
    Starting server, use <Ctrl-C> to stop

Each time the server receives a request, it starts a new thread or
process to handle it:

.. code-block:: none

    $ curl http://localhost:8080/

    Thread-1

    $ curl http://localhost:8080/

    Thread-2

    $ curl http://localhost:8080/

    Thread-3

Swapping :class:`ForkingMixIn` for :class:`ThreadingMixIn` would
achieve similar results, using separate processes instead of threads.

Handling Errors
===============

Handle errors by calling :meth:`send_error`, passing the
appropriate error code and an optional error message.  The entire
response (with headers, status code, and body) is generated
automatically.

.. literalinclude:: http_server_errors.py
    :caption:
    :start-after: #end_pymotw_header

In this case, a 404 error is always returned.

.. code-block:: none

    $ python3 http_server_errors.py 
    
    Starting server, use <Ctrl-C> to stop

The error message is reported to the client using an HTML document as
well as the header to indicate an error code.

.. code-block:: none

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
It takes two arguments: the name of the header and the value.

.. literalinclude:: http_server_send_header.py
   :caption:
   :start-after: #end_pymotw_header

This example sets the ``Last-Modified`` header to the current
timestamp, formatted according to RFC 2822.

.. code-block:: none

    $ curl -i http://localhost:8080/

    HTTP/1.0 200 OK
    Server: BaseHTTP/0.3 Python/2.7
    Date: Sun, 10 Oct 2010 13:58:32 GMT
    Last-Modified: Sun, 10 Oct 2010 13:58:32 -0000
    
    Response body

The server logs the request to the terminal, like in the other
examples.

.. code-block:: none

    $ python3 http_server_send_header.py 
    
    Starting server, use <Ctrl-C> to stop


.. seealso::

   * :pydoc:`http.server`

   * :mod:`socketserver` -- The ``socketserver`` module provides the
     base class that handles the raw socket connection.

   * :rfc:`2822` -- The "Internet Message Format" specifies a format
     for text-based messages such as email and HTTP responses.
