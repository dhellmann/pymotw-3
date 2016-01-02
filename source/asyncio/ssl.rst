===========
 Using SSL
===========

:mod:`asyncio` has built-in support for enabling SSL communication on
sockets. Passing an :class:`SSLContext` instance to the coroutines
that create server or client connections enables the support and
ensures that the SSL protocol setup is taken care of before the socket
is presented as ready for the application to use.

The coroutine-based echo server and client from the previous section
can be updated with a few small changes. The first step is to create
the certificate and key files. A self-signed certificate can be
created with a command like:

::

  $ openssl req -newkey rsa:2048 -nodes -keyout pymotw.key \
  -x509 -days 365 -out pymotw.crt

The ``openssl`` command will prompt for several values that are used
to generate the certificate, and then produce the output files
requested.

The insecure socket setup in the previous server example uses
:func:`start_server` to create the listening socket.

.. literalinclude:: asyncio_echo_server_coroutine.py
   :lines: 45-46

To add encryption, create an :class:`SSLContext` with the certificate
and key just generated and then pass the context to
:func:`start_server`.

.. literalinclude:: asyncio_echo_server_ssl.py
   :lines: 44-55

Similar changes are needed in the client. The old version uses
:func:`open_connection` to create the socket connected to the server.

.. literalinclude:: asyncio_echo_client_coroutine.py
   :lines: 27-28

An :class:`SSLContext` is needed again to secure the client-side of
the socket. Client identity is not being enforced, so only the
certificate needs to be loaded.

.. literalinclude:: asyncio_echo_client_ssl.py
   :lines: 27-34,37-38

One other small changes is needed in the client. Because the SSL
connection does not support sending an end-of-file (EOF), the client
closes its outgoing connection to the server to signal that it is
done.

The old version of the client send loop uses :func:`write_eof`.

.. literalinclude:: asyncio_echo_client_coroutine.py
   :lines: 30-37

The new version uses :func:`close`.

.. literalinclude:: asyncio_echo_client_ssl.py
   :lines: 40-50

Running the server in one window, and the client in another, produces
this output.

::

    $ python3 asyncio_echo_server_ssl.py
    asyncio: Using selector: KqueueSelector
    main: starting up on localhost port 10000
    echo_::1_55235: connection accepted
    echo_::1_55235: received b'This is the message. '
    echo_::1_55235: sent b'This is the message. '
    echo_::1_55235: received b'It will be sent in parts.'
    echo_::1_55235: sent b'It will be sent in parts.'
    echo_::1_55235: closing

::

    $ python3 asyncio_echo_client_ssl.py
    asyncio: Using selector: KqueueSelector
    echo_client: connecting to localhost port 10000
    echo_client: sending b'This is the message. '
    echo_client: sending b'It will be sent '
    echo_client: sending b'in parts.'
    echo_client: waiting for response
    asyncio: returning true from eof_received() has no effect when using ssl
    echo_client: closing
    main: closing event loop
    
