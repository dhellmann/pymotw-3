=========================================
 uuid --- Universally Unique Identifiers
=========================================

.. module:: uuid
    :synopsis: Universally unique identifiers

:Purpose: The ``uuid`` module implements Universally Unique Identifiers as described in RFC 4122.

:rfc:`4122` defines a system for creating universally unique
identifiers for resources in a way that does not require a central
registrar. UUID values are 128 bits long and, as the reference guide
says, "can guarantee uniqueness across space and time." They are
useful for generating identifiers for documents, hosts, application
clients, and other situations where a unique value is necessary. The
RFC is specifically focused on creating a Uniform Resource Name
namespace and covers three main algorithms:

+ Using IEEE 802 MAC addresses as a source of uniqueness
+ Using pseudo-random numbers
+ Using well-known strings combined with cryptographic hashing

In all cases, the seed value is combined with the system clock and a
clock sequence value used to maintain uniqueness in case the clock is
set backwards.

UUID 1 - IEEE 802 MAC Address
=============================

UUID version 1 values are computed using the MAC address of the host.
The ``uuid`` module uses ``getnode()`` to retrieve the MAC value
of the current system.

.. literalinclude:: uuid_getnode.py
   :caption:
   :start-after: #end_pymotw_header

If a system has more than one network card, and so more than one MAC,
any one of the values may be returned.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'uuid_getnode.py'))
.. }}}

.. code-block:: none

	$ python3 uuid_getnode.py
	
	0xc82a14598875

.. {{{end}}}

To generate a UUID for a host, identified by its MAC address, use the
``uuid1()`` function. The node identifier argument is optional;
leave the field blank to use the value returned by ``getnode()``.

.. literalinclude:: uuid_uuid1.py
   :caption:
   :start-after: #end_pymotw_header

The components of the UUID object returned can be accessed through
read-only instance attributes. Some attributes, such as ``hex``, ``int``,
and ``urn``, are different representations of the UUID value.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'uuid_uuid1.py'))
.. }}}

.. code-block:: none

	$ python3 uuid_uuid1.py
	
	335ea282-cded-11e6-9ede-c82a14598875
	<class 'uuid.UUID'>
	bytes   : b'3^\xa2\x82\xcd\xed\x11\xe6\x9e\xde\xc8*\x14Y\x88u'
	hex     : 335ea282cded11e69edec82a14598875
	int     : 68281999803480928707202152670695098485
	urn     : urn:uuid:335ea282-cded-11e6-9ede-c82a14598875
	variant : specified in RFC 4122
	version : 1
	fields  : (861840002, 52717, 4582, 158, 222, 220083055593589)
	  time_low            :  861840002
	  time_mid            :  52717
	  time_hi_version     :  4582
	  clock_seq_hi_variant:  158
	  clock_seq_low       :  222
	  node                :  220083055593589
	  time                :  137023257334162050
	  clock_seq           :  7902

.. {{{end}}}

Because of the time component, each call to ``uuid1()`` returns a
new value.

.. literalinclude:: uuid_uuid1_repeat.py
   :caption:
   :start-after: #end_pymotw_header

In this output, only the time component (at the beginning of the
string) changes.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'uuid_uuid1_repeat.py'))
.. }}}

.. code-block:: none

	$ python3 uuid_uuid1_repeat.py
	
	3369ab5c-cded-11e6-8d5e-c82a14598875
	336eea22-cded-11e6-9943-c82a14598875
	336eeb5e-cded-11e6-9e22-c82a14598875

.. {{{end}}}

Because each computer has a different MAC address, running the sample
program on different systems will produce entirely different values.
This example passes explicit node IDs to simulate running on different
hosts.

.. literalinclude:: uuid_uuid1_othermac.py
   :caption:
   :start-after: #end_pymotw_header

In addition to a different time value the node identifier at the end
of the UUID also changes.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'uuid_uuid1_othermac.py'))
.. }}}

.. code-block:: none

	$ python3 uuid_uuid1_othermac.py
	
	337969be-cded-11e6-97fa-001ec200d9e0 0x1ec200d9e0
	3379b7e6-cded-11e6-9d72-001e5274040e 0x1e5274040e

.. {{{end}}}


UUID 3 and 5 - Name-Based Values
================================

It is also useful in some contexts to create UUID values from names
instead of random or time-based values. Versions 3 and 5 of the UUID
specification use cryptographic hash values (MD5 or SHA-1,
respectively) to combine namespace-specific seed values with
names. There are several well-known namespaces, identified by
pre-defined UUID values, for working with DNS, URLs, ISO OIDs, and
X.500 Distinguished Names. New application-specific namespaces can be
defined by generating and saving UUID values.

.. literalinclude:: uuid_uuid3_uuid5.py
   :caption:
   :start-after: #end_pymotw_header

To create a UUID from a DNS name, pass ``uuid.NAMESPACE_DNS`` as
the namespace argument to ``uuid3()`` or ``uuid5()``:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'uuid_uuid3_uuid5.py'))
.. }}}

.. code-block:: none

	$ python3 uuid_uuid3_uuid5.py
	
	www.doughellmann.com
	  MD5   : bcd02e22-68f0-3046-a512-327cca9def8f
	  SHA-1 : e3329b12-30b7-57c4-8117-c2cd34a87ce9
	
	blog.doughellmann.com
	  MD5   : 9bdabfce-dfd6-37ab-8a3f-7f7293bcf111
	  SHA-1 : fa829736-7ef8-5239-9906-b4775a5abacb
	

.. {{{end}}}

The UUID value for a given name in a namespace is always the same, no
matter when or where it is calculated.

.. literalinclude:: uuid_uuid3_repeat.py
   :caption:
   :start-after: #end_pymotw_header

Values for the same name in the namespaces are different.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'uuid_uuid3_repeat.py'))
.. }}}

.. code-block:: none

	$ python3 uuid_uuid3_repeat.py
	
	NAMESPACE_DNS
	  bcd02e22-68f0-3046-a512-327cca9def8f
	  bcd02e22-68f0-3046-a512-327cca9def8f
	
	NAMESPACE_OID
	  e7043ac1-4382-3c45-8271-d5c083e41723
	  e7043ac1-4382-3c45-8271-d5c083e41723
	
	NAMESPACE_URL
	  5d0fdaa9-eafd-365e-b4d7-652500dd1208
	  5d0fdaa9-eafd-365e-b4d7-652500dd1208
	
	NAMESPACE_X500
	  4a54d6e7-ce68-37fb-b0ba-09acc87cabb7
	  4a54d6e7-ce68-37fb-b0ba-09acc87cabb7
	

.. {{{end}}}


UUID 4 - Random Values
======================

Sometimes host-based and namespace-based UUID values are not
"different enough." For example, in cases where UUID is intended to be
used as a hash key, a more random sequence of values with more
differentiation is desirable to avoid collisions in the hash
table. Having values with fewer common digits also makes it easier to
find them in log files. To add greater differentiation in UUIDs, use
``uuid4()`` to generate them using random input values.

.. literalinclude:: uuid_uuid4.py
   :caption:
   :start-after: #end_pymotw_header

The source of randomness depends on which C libraries are available
when ``uuid`` is imported.  If ``libuuid`` (or ``uuid.dll``) can be
loaded and it contains a function for generating random values, it is
used.  Otherwise ``os.urandom()`` or the :mod:`random` module are
used.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'uuid_uuid4.py'))
.. }}}

.. code-block:: none

	$ python3 uuid_uuid4.py
	
	7821863a-06f0-4109-9b88-59ba1ca5cc04
	44846e16-4a59-4a21-8c8e-008f169c2dd5
	1f3cef3c-e2bc-4877-96c8-eba43bf15bb6

.. {{{end}}}


Working with UUID Objects
=========================

In addition to generating new UUID values, it is possible to parse
strings in standard formats to create UUID objects, making it easier
to handle comparisons and sorting operations.

.. literalinclude:: uuid_uuid_objects.py
   :caption:
   :start-after: #end_pymotw_header

Surrounding curly braces are removed from the input, as are dashes
(``-``).  If the string has a prefix containing ``urn:`` and/or
``uuid:``, it is also removed.  The remaining text must be a string of
16 hexadecimal digits, which are then interpreted as a UUID value.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'uuid_uuid_objects.py'))
.. }}}

.. code-block:: none

	$ python3 uuid_uuid_objects.py
	
	input_values
	  urn:uuid:f2f84497-b3bf-493a-bba9-7c68e6def80b
	  {417a5ebb-01f7-4ed5-aeac-3d56cd5037b0}
	  2115773a-5bf1-11dd-ab48-001ec200d9e0
	
	converted to uuids
	  f2f84497-b3bf-493a-bba9-7c68e6def80b
	  417a5ebb-01f7-4ed5-aeac-3d56cd5037b0
	  2115773a-5bf1-11dd-ab48-001ec200d9e0
	
	sorted
	  2115773a-5bf1-11dd-ab48-001ec200d9e0
	  417a5ebb-01f7-4ed5-aeac-3d56cd5037b0
	  f2f84497-b3bf-493a-bba9-7c68e6def80b
	

.. {{{end}}}

.. seealso::

   * :pydoc:`uuid`

   * :ref:`Python 2 to 3 porting notes for uuid <porting-uuid>`

   * :rfc:`4122` -- A Universally Unique Identifier (UUID) URN
     Namespace
