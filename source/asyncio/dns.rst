=======================================
 Interacting with Domain Name Services
=======================================

Applications use the network to communicate with servers for domain
name service (DNS) operations like converting between hostnames and IP
addresses. :mod:`asyncio` has convenience methods on the event loop to
take care of those operations in the background, to avoid blocking
during the queries.

Address Lookup by Name
======================

Use the coroutine :func:`getaddrinfo` to convert a hostname and port
number to an IP or IPv6 address. As with the version of the function
in the :mod:`socket` module, the return value is a list of tuples
containing five pieces of information.

#. The address family
#. The address type
#. The protocol
#. The canonical name for the server
#. A socket address tuple suitable for opening a connection to the
   server on the port originally specified

Queries can be filtered by protocol, as in this example, where only
TCP responses are returned.

.. include:: asyncio_getaddrinfo.py
   :literal:
   :start-after: #end_pymotw_header

The example program converts a hostname and protocol name to IP
address and port number.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_getaddrinfo.py'))
.. }}}

::

	$ python3 asyncio_getaddrinfo.py
	
	pymotw.com          : 66.33.211.242
	doughellmann.com    : 66.33.211.240
	python.org          : 104.130.43.121
	python.org          : 2001:4802:7901::e60a:1375:0:5

.. {{{end}}}

Name Lookup by Address
======================

The coroutine :func:`getnameinfo` works in the reverse direction,
converting an IP address to a hostname and a port number to a protocol
name, where possible.

.. include:: asyncio_getnameinfo.py
   :literal:
   :start-after: #end_pymotw_header

This example shows that the IP address for ``pymotw.com`` refers to a
server at DreamHost, the hosting company where the site runs. The
second IP address examined is for ``python.org``, and it does not
resolve back to a hostname.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_getnameinfo.py'))
.. }}}

::

	$ python3 asyncio_getnameinfo.py
	
	66.33.211.242  : apache2-echo.catalina.dreamhost.com https
	104.130.43.121 : 104.130.43.121 https

.. {{{end}}}



.. seealso::

   * The :mod:`socket` module discussion includes a more detailed
     examination of these operations.
