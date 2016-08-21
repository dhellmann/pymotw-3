================================================
 Addressing, Protocol Families and Socket Types
================================================

A *socket* is one endpoint of a communication channel used by programs
to pass data back and forth locally or across the Internet.  Sockets
have two primary properties controlling the way they send data: the
*address family* controls the OSI network layer protocol used and the
*socket type* controls the transport layer protocol.

Python supports three address families.  The most common,
:const:`AF_INET`, is used for IPv4 Internet addressing.  IPv4
addresses are four bytes long and are usually represented as a
sequence of four numbers, one per byte, separated by dots (e.g.,
``10.1.1.5`` and ``127.0.0.1``).  These values are more commonly
referred to as "IP addresses."  Almost all Internet networking is done
using IP version 4 at this time.

:const:`AF_INET6` is used for IPv6 Internet addressing.  IPv6 is the
"next generation" version of the Internet protocol, and supports
128-bit addresses, traffic shaping, and routing features not available
under IPv4.  Adoption of IPv6 is still limited, but continues to grow.

:const:`AF_UNIX` is the address family for Unix Domain Sockets (UDS),
an inter-process communication protocol available on POSIX-compliant
systems.  The implementation of UDS typically allows the operating
system to pass data directly from process to process, without going
through the network stack.  This is more efficient than using
:const:`AF_INET`, but because the file system is used as the namespace
for addressing, UDS is restricted to processes on the same system.
The appeal of using UDS over other IPC mechanisms such as named pipes
or shared memory is that the programming interface is the same as for
IP networking, so the application can take advantage of efficient
communication when running on a single host, but use the same code
when sending data across the network.

.. note::

  The :const:`AF_UNIX` constant is only defined on systems where UDS
  is supported.

The socket type is usually either :const:`SOCK_DGRAM` for *user
datagram protocol* (UDP) or :const:`SOCK_STREAM` for *transmission
control protocol* (TCP).  UDP does not require transmission
handshaking or other setup, but offers lower reliability of delivery.
UDP messages may be delivered out of order, more than once, or not at
all.  TCP, by contrast, ensures that each message is delivered exactly
once, and in the correct order.  That extra reliability may impose
additional latency, however, since packets may need to be
retransmitted.  Most application protocols that deliver a large amount
of data, such as HTTP, are built on top of TCP.  UDP is commonly used
for protocols where order is less important (since the message fits in
a single packet, i.e., DNS), or for *multicasting* (sending the same
data to several hosts).

.. note::

  Python's :mod:`socket` module supports other socket types but they
  are less commonly used, so are not covered here.  Refer to the
  standard library documentation for more details.

Looking up Hosts on the Network
===============================

:mod:`socket` includes functions to interface with the domain name
services on the network so a program can convert the host name of a
server into its numerical network address.  Applications do not need
to convert addresses explicitly before using them to connect to a
server, but it can be useful when reporting errors to include the
numerical address as well as the name value being used.

To find the official name of the current host, use
:func:`gethostname`.

.. literalinclude:: socket_gethostname.py
   :caption:
   :start-after: #end_pymotw_header

The name returned will depend on the network settings for the current
system, and may change if it is on a different network (such as a
laptop attached to a wireless LAN).

.. code-block:: none

	$ python3 socket_gethostname.py
	
	apu.hellfly.net

Use :func:`gethostbyname` to consult the operating system hostname
resolution API and convert the name of a server to its numerical
address.

.. literalinclude:: socket_gethostbyname.py
   :caption:
   :start-after: #end_pymotw_header

If the DNS configuration of the current system includes one or more
domains in the search, the name argument does not need to be a fully
qualified name (i.e., it does not need to include the domain name as
well as the base hostname).  If the name cannot be found, an exception
of type :class:`socket.error` is raised.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'socket_gethostbyname.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 socket_gethostbyname.py
	
	apu : 10.9.0.10
	pymotw.com : 66.33.211.242
	www.python.org : 151.101.32.223
	nosuchname : [Errno 8] nodename nor servname provided, or not
	known

.. {{{end}}}

For access to more naming information about a server, use
:func:`gethostbyname_ex`.  It returns the canonical hostname of the
server, any aliases, and all of the available IP addresses that can be
used to reach it.

.. literalinclude:: socket_gethostbyname_ex.py
   :caption:
   :start-after: #end_pymotw_header

Having all known IP addresses for a server lets a client implement its
own load balancing or fail-over algorithms.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'socket_gethostbyname_ex.py'))
.. }}}

.. code-block:: none

	$ python3 socket_gethostbyname_ex.py
	
	apu
	  Hostname: apu.hellfly.net
	  Aliases : ['apu']
	 Addresses: ['10.9.0.10']
	
	pymotw.com
	  Hostname: pymotw.com
	  Aliases : []
	 Addresses: ['66.33.211.242']
	
	www.python.org
	  Hostname: prod.python.map.fastlylb.net
	  Aliases : ['www.python.org', 'python.map.fastly.net']
	 Addresses: ['151.101.32.223']
	
	nosuchname
	ERROR: [Errno 8] nodename nor servname provided, or not known
	

.. {{{end}}}

Use :func:`getfqdn` to convert a partial name to a fully qualified
domain name.

.. literalinclude:: socket_getfqdn.py
   :caption:
   :start-after: #end_pymotw_header

The name returned will not necessarily match the input argument in any
way if the input is an alias, such as ``www`` is here.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'socket_getfqdn.py'))
.. }}}

.. code-block:: none

	$ python3 socket_getfqdn.py
	
	       apu : apu.hellfly.net
	pymotw.com : apache2-echo.catalina.dreamhost.com

.. {{{end}}}

When the address of a server is available, use :func:`gethostbyaddr`
to do a "reverse" lookup for the name.

.. literalinclude:: socket_gethostbyaddr.py
   :caption:
   :start-after: #end_pymotw_header

The return value is a tuple containing the full hostname, any aliases,
and all IP addresses associated with the name.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'socket_gethostbyaddr.py'))
.. }}}

.. code-block:: none

	$ python3 socket_gethostbyaddr.py
	
	Hostname : apu.hellfly.net
	Aliases  : ['apu']
	Addresses: ['10.9.0.10']

.. {{{end}}}

Finding Service Information
===========================

In addition to an IP address, each socket address includes an integer
*port number*.  Many applications can run on the same host, listening
on a single IP address, but only one socket at a time can use a port
at that address.  The combination of IP address, protocol, and port
number uniquely identify a communication channel and ensure that
messages sent through a socket arrive at the correct destination.

Some of the port numbers are pre-allocated for a specific protocol.
For example, communication between email servers using SMTP occurs
over port number 25 using TCP, and web clients and servers use port 80
for HTTP.  The port numbers for network services with standardized
names can be looked up with :func:`getservbyname`.

.. literalinclude:: socket_getservbyname.py
   :caption:
   :start-after: #end_pymotw_header

Although a standardized service is unlikely to change ports, looking
up the value with a system call instead of hard-coding it is more
flexible when new services are added in the future.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'socket_getservbyname.py'))
.. }}}

.. code-block:: none

	$ python3 socket_getservbyname.py
	
	  http : 80
	 https : 443
	   ftp : 21
	gopher : 70
	  smtp : 25
	  imap : 143
	 imaps : 993
	  pop3 : 110
	 pop3s : 995

.. {{{end}}}

To reverse the service port lookup, use :func:`getservbyport`.

.. literalinclude:: socket_getservbyport.py
   :caption:
   :start-after: #end_pymotw_header

The reverse lookup is useful for constructing URLs to services from
arbitrary addresses.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'socket_getservbyport.py'))
.. }}}

.. code-block:: none

	$ python3 socket_getservbyport.py
	
	http://example.com/
	https://example.com/
	ftp://example.com/
	gopher://example.com/
	smtp://example.com/
	imap://example.com/
	imaps://example.com/
	pop3://example.com/
	pop3s://example.com/

.. {{{end}}}

The number assigned to a transport protocol can be retrieved with
:func:`getprotobyname`.

.. literalinclude:: socket_getprotobyname.py
   :caption:
   :start-after: #end_pymotw_header

The values for protocol numbers are standardized, and defined as
constants in :mod:`socket` with the prefix ``IPPROTO_``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'socket_getprotobyname.py'))
.. }}}

.. code-block:: none

	$ python3 socket_getprotobyname.py
	
	icmp ->  1 (socket.IPPROTO_ICMP =  1)
	 udp -> 17 (socket.IPPROTO_UDP  = 17)
	 tcp ->  6 (socket.IPPROTO_TCP  =  6)

.. {{{end}}}


Looking Up Server Addresses
===========================

:func:`getaddrinfo` converts the basic address of a service into a
list of tuples with all of the information necessary to make a
connection.  The contents of each tuple will vary, containing
different network families or protocols.

.. literalinclude:: socket_getaddrinfo.py
   :caption:
   :start-after: #end_pymotw_header

This program demonstrates how to look up the connection information
for ``www.python.org``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'socket_getaddrinfo.py'))
.. }}}

.. code-block:: none

	$ python3 socket_getaddrinfo.py
	
	Family        : AF_INET
	Type          : SOCK_DGRAM
	Protocol      : IPPROTO_UDP
	Canonical name: 
	Socket address: ('151.101.32.223', 80)
	
	Family        : AF_INET
	Type          : SOCK_STREAM
	Protocol      : IPPROTO_TCP
	Canonical name: 
	Socket address: ('151.101.32.223', 80)
	
	Family        : AF_INET6
	Type          : SOCK_DGRAM
	Protocol      : IPPROTO_UDP
	Canonical name: 
	Socket address: ('2a04:4e42:8::223', 80, 0, 0)
	
	Family        : AF_INET6
	Type          : SOCK_STREAM
	Protocol      : IPPROTO_TCP
	Canonical name: 
	Socket address: ('2a04:4e42:8::223', 80, 0, 0)
	

.. {{{end}}}

:func:`getaddrinfo` takes several arguments for filtering the result
list. The *host* and *port* values given in the example are required
arguments.  The optional arguments are *family*, *socktype*, *proto*,
and *flags*.  The optional values should be either ``0`` or one of the
constants defined by :mod:`socket`.

.. literalinclude:: socket_getaddrinfo_extra_args.py
   :caption:
   :start-after: #end_pymotw_header

Since *flags* includes :const:`AI_CANONNAME`, the canonical name of
the server, which may be different from the value used for the lookup
if the host has any aliases, is included in the results this time.
Without the flag, the canonical name value is left empty.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'socket_getaddrinfo_extra_args.py'))
.. }}}

.. code-block:: none

	$ python3 socket_getaddrinfo_extra_args.py
	
	Family        : AF_INET
	Type          : SOCK_STREAM
	Protocol      : IPPROTO_TCP
	Canonical name: prod.python.map.fastlylb.net
	Socket address: ('151.101.32.223', 80)
	

.. {{{end}}}


IP Address Representations
==========================

Network programs written in C use the data type :class:`struct
sockaddr` to represent IP addresses as binary values (instead of the
string addresses usually found in Python programs).  To convert IPv4
addresses between the Python representation and the C representation,
use :func:`inet_aton` and :func:`inet_ntoa`.

.. literalinclude:: socket_address_packing.py
   :caption:
   :start-after: #end_pymotw_header

The four bytes in the packed format can be passed to C libraries,
transmitted safely over the network, or saved to a database compactly.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'socket_address_packing.py'))
.. }}}

.. code-block:: none

	$ python3 socket_address_packing.py
	
	Original: 192.168.1.1
	Packed  : b'c0a80101'
	Unpacked: 192.168.1.1
	
	Original: 127.0.0.1
	Packed  : b'7f000001'
	Unpacked: 127.0.0.1
	

.. {{{end}}}

The related functions :func:`inet_pton` and :func:`inet_ntop` work
with both IPv4 and IPv6 addresses, producing the appropriate format
based on the address family parameter passed in.

.. literalinclude:: socket_ipv6_address_packing.py
   :caption:
   :start-after: #end_pymotw_header

An IPv6 address is already a hexadecimal value, so converting the
packed version to a series of hex digits produces a string similar to
the original value.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'socket_ipv6_address_packing.py'))
.. }}}

.. code-block:: none

	$ python3 socket_ipv6_address_packing.py
	
	Original: 2002:ac10:10a:1234:21e:52ff:fe74:40e
	Packed  : b'2002ac10010a1234021e52fffe74040e'
	Unpacked: 2002:ac10:10a:1234:21e:52ff:fe74:40e

.. {{{end}}}

.. seealso::

   * `Wikipedia: IPv6 <http://en.wikipedia.org/wiki/IPv6>`__ --
     Article discussing Internet Protocol Version 6 (IPv6).

   * `Wikipedia: OSI Networking Model
     <http://en.wikipedia.org/wiki/OSI_model>`__ -- Article describing
     the seven layer model of networking implementation.

   * `Assigned Internet Protocol Numbers
     <http://www.iana.org/assignments/protocol-numbers/protocol-numbers.xml>`__
     -- List of standard protocol names and numbers.
