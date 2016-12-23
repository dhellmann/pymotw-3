===========
 Using SSL
===========

``asyncio`` has built-in support for enabling SSL communication on
sockets. Passing an ``SSLContext`` instance to the coroutines
that create server or client connections enables the support and
ensures that the SSL protocol setup is taken care of before the socket
is presented as ready for the application to use.

The coroutine-based echo server and client from the previous section
can be updated with a few small changes. The first step is to create
the certificate and key files. A self-signed certificate can be
created with a command like:

.. code-block:: none

  $ openssl req -newkey rsa:2048 -nodes -keyout pymotw.key \
  -x509 -days 365 -out pymotw.crt

The ``openssl`` command will prompt for several values that are used
to generate the certificate, and then produce the output files
requested.

The insecure socket setup in the previous server example uses
``start_server()`` to create the listening socket.

.. literalinclude:: asyncio_echo_server_coroutine.py
   :lines: 45-46

To add encryption, create an ``SSLContext`` with the certificate
and key just generated and then pass the context to
``start_server()``.

.. literalinclude:: asyncio_echo_server_ssl.py
   :lines: 46-56

Similar changes are needed in the client. The old version uses
``open_connection()`` to create the socket connected to the server.

.. literalinclude:: asyncio_echo_client_coroutine.py
   :lines: 26

An ``SSLContext`` is needed again to secure the client-side of
the socket. Client identity is not being enforced, so only the
certificate needs to be loaded.

.. literalinclude:: asyncio_echo_client_ssl.py
   :lines: 26-33,36-37

One other small changes is needed in the client. Because the SSL
connection does not support sending an end-of-file (EOF), the client
uses a NULL byte as a message terminator instead.

The old version of the client send loop uses ``write_eof()``.

.. literalinclude:: asyncio_echo_client_coroutine.py
   :lines: 28-36

The new version sends a zero byte (``b'\x00'``).

.. literalinclude:: asyncio_echo_client_ssl.py
   :lines: 39-48

The ``echo()`` coroutine in the server must look for the NULL byte and
close the client connection when it is received.

.. literalinclude:: asyncio_echo_server_ssl.py
   :lines: 17-33

Running the server in one window, and the client in another, produces
this output.

.. NOT RUNNING

.. code-block:: none

    $ python3 asyncio_echo_server_ssl.py
    asyncio: Using selector: KqueueSelector
    main: starting up on localhost port 10000
    echo_::1_53957: connection accepted
    echo_::1_53957: received b'This is the message. '
    echo_::1_53957: sent b'This is the message. '
    echo_::1_53957: received b'It will be sent in parts.'
    echo_::1_53957: sent b'It will be sent in parts.'
    echo_::1_53957: message terminated, closing connection

.. NOT RUNNING

.. code-block:: none

    $ python3 asyncio_echo_client_ssl.py
    asyncio: Using selector: KqueueSelector
    echo_client: connecting to localhost port 10000
    echo_client: sending b'This is the message. '
    echo_client: sending b'It will be sent '
    echo_client: sending b'in parts.'
    echo_client: waiting for response
    echo_client: received b'This is the message. '
    echo_client: received b'It will be sent in parts.'
    echo_client: closing
    main: closing event loop
