==================================
 ipaddress --- Internet Addresses
==================================

.. module:: ipaddress
   :synopsis: Classes for working with Internet Protocol (IP)
              addresses.

:Purpose: Classes for working with Internet Protocol (IP) addresses.

The :mod:`ipaddress` module includes classes for working with IPv4 and
IPv6 network addresses. The classes support validation, finding
addresses and hosts on a network, and other common operations.

Addresses
=========

The most basic object represents the network address itself. Pass a
string, integer, or byte sequence to :func:`ip_address` to construct
an address. The return value will be a :class:`IPv4Address` or
:class:`IPv6Address` instance, depending on the type of address being
used.

.. literalinclude:: ipaddress_addresses.py
   :caption:
   :start-after: #end_pymotw_header

Both classes can provide various representations of the address for
different purposes, as well as answer basic assertions such as whether
the address is reserved for multicast communication or if it is on a
private network.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ipaddress_addresses.py'))
.. }}}

.. code-block:: none

	$ python3 ipaddress_addresses.py
	
	IPv4Address('10.9.0.6')
	   is private: True
	  packed form: b'0a090006'
	      integer: 168361990
	
	IPv6Address('fdfd:87b5:b475:5e3e:b1bc:e121:a8eb:14aa')
	   is private: True
	  packed form: b'fdfd87b5b4755e3eb1bce121a8eb14aa'
	      integer: 337611086560236126439725644408160982186
	

.. {{{end}}}

Networks
========

A "network" is defined by a range of addresses. It is usually
expressed with a base address and a mask indicating which portions of
the address represent the network, and which portions are remaining to
represent addresses on that network. The mask can be expressed
explicitly, or using a prefix length value as in the example below.

.. literalinclude:: ipaddress_networks.py
   :caption:
   :start-after: #end_pymotw_header

As with addresses, there are two network classes for IPv4 and IPv6
networks. Each class provides properties or methods for accessing
values associated with the network such as the broadcast address and
the addresses on the network available for hosts to use.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ipaddress_networks.py'))
.. }}}

.. code-block:: none

	$ python3 ipaddress_networks.py
	
	IPv4Network('10.9.0.0/24')
	     is private: True
	      broadcast: 10.9.0.255
	     compressed: 10.9.0.0/24
	   with netmask: 10.9.0.0/255.255.255.0
	  with hostmask: 10.9.0.0/0.0.0.255
	  num addresses: 256
	
	IPv6Network('fdfd:87b5:b475:5e3e::/64')
	     is private: True
	      broadcast: fdfd:87b5:b475:5e3e:ffff:ffff:ffff:ffff
	     compressed: fdfd:87b5:b475:5e3e::/64
	   with netmask: fdfd:87b5:b475:5e3e::/ffff:ffff:ffff:ffff::
	  with hostmask: fdfd:87b5:b475:5e3e::/::ffff:ffff:ffff:ffff
	  num addresses: 18446744073709551616
	

.. {{{end}}}



.. seealso::

   * :pydoc:`ipaddress`

   * `An introduction to the ipaddress module
     <https://docs.python.org/3.5/howto/ipaddress.html#ipaddress-howto>`__
