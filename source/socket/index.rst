==================================
 socket --- Network Communication
==================================

.. module:: socket
    :synopsis: Network communication

:Purpose: Provides access to network communication

The ``socket`` module exposes the low-level C API for communicating
over a network using the BSD socket interface.  It includes the
:class:`socket` class, for handling the actual data channel, and also
includes functions for network-related tasks such as converting a
server's name to an address and formatting data to be sent across the
network.

.. toctree::

   addressing
   tcp
   udp
   uds
   multicast
   binary
   nonblocking


.. seealso::

   * :pydoc:`socket`

   * :ref:`Porting notes for socket <porting-socket>`

   * :mod:`select` -- Testing a socket to see if it is ready for
     reading or writing for non-blocking I/O.

   * :mod:`SocketServer` -- Framework for creating network servers.

   * :mod:`asyncore` and :mod:`asynchat` -- Frameworks for
     asynchronous communication.

   * :mod:`urllib` and :mod:`urllib2` -- Most network clients should
     use the more convenient libraries for accessing remote resources
     through a URL.

   * `Socket Programming HOWOTO
     <https://docs.python.org/3/howto/sockets.html>`__ -- An
     instructional guide by Gordon McMillan, included in the standard
     library documentation.

   * *Foundations of Python Network Programming, 3/E* -- By Brandon
     Rhodes and John Goerzen. Published by
     Apress, 2014. ISBN-10: 1430258543.

   * *Unix Network Programming, Volume 1: The Sockets Networking API,
     3/E* -- By W. Richard Stevens, Bill Fenner, and
     Andrew M. Rudoff. Published by Addison-Wesley
     Professional, 2004. ISBN-10: 0131411551
