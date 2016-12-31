.. _sys-limits:

==============================
 Memory Management and Limits
==============================

``sys`` includes several functions for understanding and
controlling memory usage.

Reference Counts
================

The primary implementation of Python (CPython) uses *reference
counting* and *garbage collection* for automatic memory management.
An object is automatically marked to be collected when its reference
count drops to zero.  To examine the reference count of an existing
object, use ``getrefcount()``.

.. literalinclude:: sys_getrefcount.py
    :caption:
    :start-after: #end_pymotw_header

The value reported is actually one higher than expected because there
is a temporary reference to the object held by ``getrefcount()``
itself.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_getrefcount.py'))
.. }}}

.. code-block:: none

	$ python3 sys_getrefcount.py
	
	At start         : 2
	Second reference : 3
	After del        : 2

.. {{{end}}}

.. seealso::

    * :mod:`gc` -- Control the garbage collector via the functions
      exposed in ``gc``.

Object Size
===========

Knowing how many references an object has may help find cycles or a
memory leak, but it is not enough to determine what objects are
consuming the *most* memory.  That requires knowledge about how big
objects are.

.. literalinclude:: sys_getsizeof.py
    :caption:
    :start-after: #end_pymotw_header

``getsizeof()`` reports the size of an object in bytes.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_getsizeof.py'))
.. }}}

.. code-block:: none

	$ python3 sys_getsizeof.py
	
	      list : 64
	     tuple : 48
	      dict : 288
	       str : 50
	       str : 55
	     bytes : 38
	       int : 28
	     float : 24
	      type : 1016
	   MyClass : 56

.. {{{end}}}

The reported size for a custom class does not include the size of the
attribute values.

.. literalinclude:: sys_getsizeof_object.py
    :caption:
    :start-after: #end_pymotw_header

This can give a false impression of the amount of memory being
consumed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_getsizeof_object.py'))
.. }}}

.. code-block:: none

	$ python3 sys_getsizeof_object.py
	
	WithoutAttributes: 56
	WithAttributes: 56

.. {{{end}}}

For a more complete estimate of the space used by a class, provide a
``__sizeof__()`` method to compute the value by aggregating the
sizes of attributes of an object.

.. literalinclude:: sys_getsizeof_custom.py
    :caption:
    :start-after: #end_pymotw_header

This version adds the base size of the object to the sizes of all of
the attributes stored in the internal ``__dict__``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_getsizeof_custom.py'))
.. }}}

.. code-block:: none

	$ python3 sys_getsizeof_custom.py
	
	156

.. {{{end}}}

Recursion
=========

Allowing infinite recursion in a Python application may introduce a
stack overflow in the interpreter itself, leading to a crash. To
eliminate this situation, the interpreter provides a way to control
the maximum recursion depth using ``setrecursionlimit()`` and
``getrecursionlimit()``.

.. literalinclude:: sys_recursionlimit.py
    :caption:
    :start-after: #end_pymotw_header

Once the stack size reaches the recursion limit, the interpreter
raises a ``RuntimeError`` exception so the program has an opportunity
to handle the situation.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_recursionlimit.py',
..                       line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 sys_recursionlimit.py
	
	Initial limit: 1000
	Modified limit: 10
	generate_recursion_error(1)
	generate_recursion_error(2)
	generate_recursion_error(3)
	generate_recursion_error(4)
	generate_recursion_error(5)
	generate_recursion_error(6)
	generate_recursion_error(7)
	generate_recursion_error(8)
	Caught exception: maximum recursion depth exceeded while calling
	a Python object

.. {{{end}}}


Maximum Values
==============

Along with the runtime configurable values, ``sys`` includes
variables defining the maximum values for types that vary from system
to system.

.. literalinclude:: sys_maximums.py
    :caption:
    :start-after: #end_pymotw_header

``maxsize`` is the maximum size of a list, dictionary, string, or
other data structure dictated by the C interpreter's size type.
``maxunicode`` is the largest integer Unicode point supported by
the interpreter as currently configured.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_maximums.py'))
.. }}}

.. code-block:: none

	$ python3 sys_maximums.py
	
	maxsize   : 9223372036854775807
	maxunicode: 1114111

.. {{{end}}}

Floating Point Values
=====================

The structure ``float_info`` contains information about the
floating-point type representation used by the interpreter, based on
the underlying system's :c:type:`float` implementation.

.. literalinclude:: sys_float_info.py
    :caption:
    :start-after: #end_pymotw_header

These values depend on the compiler and underlying system.  These
examples were produced on OS X 10.9.5 on an Intel Core i7.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_float_info.py'))
.. }}}

.. code-block:: none

	$ python3 sys_float_info.py
	
	Smallest difference (epsilon): 2.220446049250313e-16
	
	Digits (dig)              : 15
	Mantissa digits (mant_dig): 53
	
	Maximum (max): 1.7976931348623157e+308
	Minimum (min): 2.2250738585072014e-308
	
	Radix of exponents (radix): 2
	
	Maximum exponent for radix (max_exp): 1024
	Minimum exponent for radix (min_exp): -1021
	
	Max. exponent power of 10 (max_10_exp): 308
	Min. exponent power of 10 (min_10_exp): -307
	
	Rounding for addition (rounds): 1

.. {{{end}}}

.. seealso::

    * The ``float.h`` C header file for the local compiler contains more
      details about these settings.

Integer Values
==============

The structure ``int_info`` holds information about the internal
representation of integers used by the interpreter.

.. literalinclude:: sys_int_info.py
   :caption:
   :start-after: #end_pymotw_header

These examples were produced on OS X 10.9.5 on an Intel Core i7.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_int_info.py'))
.. }}}

.. code-block:: none

	$ python3 sys_int_info.py
	
	Number of bits used to hold each digit: 30
	Size in bytes of C type used to hold each digit: 4

.. {{{end}}}

The C type used to store integers internally is determined when the
interpreter is built. 64-bit architectures automatically use 30-bit
integers by default, and they can be enabled for 32-bit architectures
with the configuration flag ``--enable-big-digits``.

.. seealso::

   * `Build and C API Changes
     <https://docs.python.org/3.1/whatsnew/3.1.html#build-and-c-api-changes>`__
     from *What's New in Python 3.1*


Byte Ordering
=============

``byteorder`` is set to the native byte order.

.. literalinclude:: sys_byteorder.py
   :caption:
   :start-after: #end_pymotw_header

The value is either ``big`` for big-endian or ``little`` for
little-endian.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_byteorder.py'))
.. }}}

.. code-block:: none

	$ python3 sys_byteorder.py
	
	little

.. {{{end}}}

.. seealso::

    * `Wikipedia: Endianness
      <https://en.wikipedia.org/wiki/Byte_order>`__ -- Description of
      big and little endian memory systems.

    * :mod:`array` and :mod:`struct` -- Other modules that depend on
      the byte order of data.

    * ``float.h`` -- The C header file for the local compiler contains
       more details about these settings.
