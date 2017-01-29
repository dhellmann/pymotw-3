===================================
 struct --- Binary Data Structures
===================================

.. module:: struct
    :synopsis: Convert between strings and binary data.

:Purpose: Convert between strings and binary data.

The ``struct`` module includes functions for converting between
strings of bytes and native Python data types such as numbers and
strings.

Functions versus Struct Class
=============================

A set of module-level functions is available for working with structured
values, as well as the ``Struct`` class.  Format
specifiers are converted from their string format to a compiled
representation, similar to the way regular expressions are handled.
The conversion takes some resources, so it is typically more efficient
to do it once when creating a ``Struct`` instance and call
methods on the instance instead of using the module-level functions.
All of the following examples use the ``Struct`` class.

Packing and Unpacking
=====================

Structs support *packing* data into strings, and *unpacking* data from
strings using format specifiers made up of characters representing the
type of the data and optional count and endianness indicators.  Refer
to the standard library documentation for a complete list of the
supported format specifiers.

In this example, the specifier calls for an integer or long integer value, a
two-byte string, and a floating-point number.  The spaces in the
format specifier are included to separate the type indicators, and are
ignored when the format is compiled.

.. literalinclude:: struct_pack.py
    :caption:
    :start-after: #end_pymotw_header

The example converts the packed value to a sequence of hex bytes for
printing with ``binascii.hexlify()``, since some of the characters are
nulls.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'struct_pack.py'))
.. }}}

.. code-block:: none

	$ python3 struct_pack.py
	
	Original values: (1, b'ab', 2.7)
	Format string  : b'I 2s f'
	Uses           : 12 bytes
	Packed Value   : b'0100000061620000cdcc2c40'

.. {{{end}}}

Use ``unpack()`` to extract data from its packed representation.

.. literalinclude:: struct_unpack.py
    :caption:
    :start-after: #end_pymotw_header

Passing the packed value to ``unpack()``, gives basically the same
values back (note the discrepancy in the floating point value).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'struct_unpack.py'))
.. }}}

.. code-block:: none

	$ python3 struct_unpack.py
	
	Unpacked Values: (1, b'ab', 2.700000047683716)

.. {{{end}}}


Endianness
==========

By default, values are encoded using the native C library notion of
*endianness*.  It is easy to override that choice by providing an
explicit endianness directive in the format string.

.. literalinclude:: struct_endianness.py
    :caption:
    :start-after: #end_pymotw_header

:table:`Byte Order Specifiers for struct` lists the byte order
specifiers used by ``Struct``.

.. table::  Byte Order Specifiers for struct

  =====  =======
  Code   Meaning
  =====  =======
  ``@``  Native order
  ``=``  Native standard
  ``<``  little-endian
  ``>``  big-endian
  ``!``  Network order
  =====  =======

.. {{{cog
.. cog.out(run_script(cog.inFile, 'struct_endianness.py'))
.. }}}

.. code-block:: none

	$ python3 struct_endianness.py
	
	Original values: (1, b'ab', 2.7)
	
	Format string  : b'@ I 2s f' for native, native
	Uses           : 12 bytes
	Packed Value   : b'0100000061620000cdcc2c40'
	Unpacked Value : (1, b'ab', 2.700000047683716)
	
	Format string  : b'= I 2s f' for native, standard
	Uses           : 10 bytes
	Packed Value   : b'010000006162cdcc2c40'
	Unpacked Value : (1, b'ab', 2.700000047683716)
	
	Format string  : b'< I 2s f' for little-endian
	Uses           : 10 bytes
	Packed Value   : b'010000006162cdcc2c40'
	Unpacked Value : (1, b'ab', 2.700000047683716)
	
	Format string  : b'> I 2s f' for big-endian
	Uses           : 10 bytes
	Packed Value   : b'000000016162402ccccd'
	Unpacked Value : (1, b'ab', 2.700000047683716)
	
	Format string  : b'! I 2s f' for network
	Uses           : 10 bytes
	Packed Value   : b'000000016162402ccccd'
	Unpacked Value : (1, b'ab', 2.700000047683716)

.. {{{end}}}

Buffers
=======

Working with binary packed data is typically reserved for 
performance-sensitive situations or passing data into and out of
extension modules.  These cases can be optimized by avoiding the
overhead of allocating a new buffer for each packed structure.  The
:meth:`pack_into` and :meth:`unpack_from` methods support writing to
pre-allocated buffers directly.

.. literalinclude:: struct_buffers.py
    :caption:
    :start-after: #end_pymotw_header

The ``size`` attribute of the ``Struct`` tells us how big the
buffer needs to be.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'struct_buffers.py'))
.. }}}

.. code-block:: none

	$ python3 struct_buffers.py
	
	Original: (1, b'ab', 2.7)
	
	ctypes string buffer
	Before  : b'000000000000000000000000'
	After   : b'0100000061620000cdcc2c40'
	Unpacked: (1, b'ab', 2.700000047683716)
	
	array
	Before  : b'000000000000000000000000'
	After   : b'0100000061620000cdcc2c40'
	Unpacked: (1, b'ab', 2.700000047683716)

.. {{{end}}}


.. seealso::

   * :pydoc:`struct`

   * :ref:`Python 2 to 3 porting notes for struct <porting-struct>`

   * :mod:`array` -- The ``array`` module, for working with sequences
     of fixed-type values.

   * :mod:`binascii` -- The ``binascii`` module, for producing ASCII
     representations of binary data.

   * `WikiPedia: Endianness
     <https://en.wikipedia.org/wiki/Endianness>`_ -- Explanation of
     byte order and endianness in encoding.
