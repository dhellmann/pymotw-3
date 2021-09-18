==================================
struct -- Working with Binary Data
==================================

.. module:: struct
    :synopsis: Convert between strings and binary data.

:Purpose: Convert between strings and binary data.
:Available In: 1.4 and later

The :mod:`struct` module includes functions for converting between
strings of bytes and native Python data types such as numbers and
strings.

Functions vs. Struct Class
==========================

There are a set of module-level functions for working with structured
values, and there is also the :class:`Struct` class (new in Python
2.5).  Format specifiers are converted from their string format to a
compiled representation, similar to the way regular expressions are.
The conversion takes some resources, so it is typically more efficient
to do it once when creating a :class:`Struct` instance and call
methods on the instance instead of using the module-level functions.
All of the examples below use the :class:`Struct` class.

Packing and Unpacking
=====================

Structs support *packing* data into strings, and *unpacking* data from
strings using format specifiers made up of characters representing the
type of the data and optional count and endian-ness indicators.  For
complete details, refer to `the standard library documentation
<http://docs.python.org/2.7/library/struct.html>`__.

In this example, the format specifier calls for an integer or long
value, a two character string, and a floating point number.  The
spaces between the format specifiers are included here for clarity,
and are ignored when the format is compiled.

.. include:: struct_pack.py
    :literal:
    :start-after: #end_pymotw_header

The example converts the packed value to a sequence of hex bytes for
printing with ``binascii.hexlify()``, since some of the characters are
nulls.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'struct_pack.py'))
.. }}}

::

	$ python struct_pack.py
	
	Original values: (1, 'ab', 2.7)
	Format string  : I 2s f
	Uses           : 12 bytes
	Packed Value   : 0100000061620000cdcc2c40

.. {{{end}}}

If we pass the packed value to :func:`unpack`, we get basically the
same values back (note the discrepancy in the floating point value).

.. include:: struct_unpack.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'struct_unpack.py'))
.. }}}

::

	$ python struct_unpack.py
	
	Unpacked Values: (1, 'ab', 2.700000047683716)

.. {{{end}}}


Endianness
==========

By default values are encoded using the native C library notion of
"endianness".  It is easy to override that choice by providing an
explicit endianness directive in the format string.

.. include:: struct_endianness.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'struct_endianness.py'))
.. }}}

::

	$ python struct_endianness.py
	
	Original values: (1, 'ab', 2.7)
	
	Format string  : @ I 2s f for native, native
	Uses           : 12 bytes
	Packed Value   : 0100000061620000cdcc2c40
	Unpacked Value : (1, 'ab', 2.700000047683716)
	
	Format string  : = I 2s f for native, standard
	Uses           : 10 bytes
	Packed Value   : 010000006162cdcc2c40
	Unpacked Value : (1, 'ab', 2.700000047683716)
	
	Format string  : < I 2s f for little-endian
	Uses           : 10 bytes
	Packed Value   : 010000006162cdcc2c40
	Unpacked Value : (1, 'ab', 2.700000047683716)
	
	Format string  : > I 2s f for big-endian
	Uses           : 10 bytes
	Packed Value   : 000000016162402ccccd
	Unpacked Value : (1, 'ab', 2.700000047683716)
	
	Format string  : ! I 2s f for network
	Uses           : 10 bytes
	Packed Value   : 000000016162402ccccd
	Unpacked Value : (1, 'ab', 2.700000047683716)

.. {{{end}}}

Buffers
=======

Working with binary packed data is typically reserved for highly
performance sensitive situations or passing data into and out of
extension modules.  In such situations, you can optimize by avoiding
the overhead of allocating a new buffer for each packed structure.
The :meth:`pack_into` and :meth:`unpack_from` methods support writing
to pre-allocated buffers directly.

.. include:: struct_buffers.py
    :literal:
    :start-after: #end_pymotw_header

The *size* attribute of the :class:`Struct` tells us how big the
buffer needs to be.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'struct_buffers.py'))
.. }}}

::

	$ python struct_buffers.py
	
	Original: (1, 'ab', 2.7)
	
	ctypes string buffer
	Before  : 000000000000000000000000
	After   : 0100000061620000cdcc2c40
	Unpacked: (1, 'ab', 2.700000047683716)
	
	array
	Before  : 000000000000000000000000
	After   : 0100000061620000cdcc2c40
	Unpacked: (1, 'ab', 2.700000047683716)

.. {{{end}}}


.. seealso::

    `struct <http://docs.python.org/2.7/library/struct.html>`_
        The standard library documentation for this module.

    :mod:`array`
        The array module, for working with sequences of fixed-type values.

    :mod:`binascii`
        The binascii module, for producing ASCII representations of binary data.

    `WikiPedia: Endianness <http://en.wikipedia.org/wiki/Endianness>`_
        Explanation of byte order and endianness in encoding.

    :ref:`article-data-structures`
        More tools for working with data structures.
