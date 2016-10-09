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



.. seealso::

   * :pydoc:`ipaddress`

   * `An introduction to the ipaddress module
     <https://docs.python.org/3.5/howto/ipaddress.html#ipaddress-howto>`__
