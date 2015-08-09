======================================
 array -- Sequence of Fixed-type Data
======================================

.. module:: array
    :synopsis: Manage sequences of fixed-type data efficiently.

:Purpose: Manage sequences of fixed-type numerical data efficiently.

The :mod:`array` module defines a sequence data structure that looks
very much like a :class:`list`, except that all of the members have to
be of the same primitive type. The types supported are all numeric or
other fixed-size primitive types such as bytes.

.. list-table:: Type Codes for array Members
   :header-rows: 1
   :widths: 20 20 30

   * - Code
     - Type
     - Minimum size (bytes)
   * - ``b``
     - int
     - 1
   * - ``B``
     - int
     - 1
   * - ``h``
     - signed short
     - 2
   * - ``H``
     - unsigned short
     - 2
   * - ``i``
     - signed int
     - 2
   * - ``I``
     - unsigned int
     - 2
   * - ``l``
     - signed long
     - 4
   * - ``L``
     - unsigned long
     - 4
   * - ``q``
     - signed long long
     - 8
   * - ``Q``
     - unsigned long long
     - 8
   * - ``f``
     - float
     - 4
   * - ``d``
     - double float
     - 8

Refer to the standard library documentation for :mod:`array` for a
complete list of type codes.

Initialization
==============

An :class:`array` is instantiated with an argument describing the type
of data to be allowed, and possibly an initial sequence of data to
store in the array.

.. include:: array_string.py
    :literal:
    :start-after: #end_pymotw_header

In this example, the array is configured to hold a sequence of bytes
and is initialized with a simple byte string.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'array_string.py'))
.. }}}

::

	$ python3 array_string.py
	
	As byte string: b'This is the array.'
	As array      : array('b', [84, 104, 105, 115, 32, 105, 115, 32,
	 116, 104, 101, 32, 97, 114, 114, 97, 121, 46])
	As hex        : b'54686973206973207468652061727261792e'

.. {{{end}}}


Manipulating Arrays
===================

An :class:`array` can be extended and otherwise manipulated in the
same ways as other Python sequences.

.. include:: array_sequence.py
    :literal:
    :start-after: #end_pymotw_header

The supported operations include slicing, iterating, and adding
elements to the end.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'array_sequence.py'))
.. }}}

::

	$ python3 array_sequence.py
	
	Initial : array('i', [0, 1, 2])
	Extended: array('i', [0, 1, 2, 0, 1, 2])
	Slice   : array('i', [2, 0, 1])
	Iterator:
	[(0, 0), (1, 1), (2, 2), (3, 0), (4, 1), (5, 2)]

.. {{{end}}}


Arrays and Files
================

The contents of an array can be written to and read from files using
built-in methods coded efficiently for that purpose.

.. include:: array_file.py
    :literal:
    :start-after: #end_pymotw_header

This example illustrates reading the data "raw", directly from the
binary file, versus reading it into a new array and converting the
bytes to the appropriate types.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'array_file.py'))
.. }}}

::

	$ python3 array_file.py
	
	A1: array('i', [0, 1, 2, 3, 4])
	Raw Contents: b'0000000001000000020000000300000004000000'
	A2: array('i', [0, 1, 2, 3, 4])

.. {{{end}}}

:func:`tofile` uses :func:`tobytes` to format the data and `fromfile`
uses :func:`frombytes` to convert it back to an array instance.

.. include:: array_tobytes.py
   :literal:
   :start-after: #end_pymotw_header

Both :func:`tobytes` and :func:`frombytes` work on byte strings, not
unicode strings.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'array_tobytes.py'))
.. }}}

::

	$ python3 array_tobytes.py
	
	A1: array('i', [0, 1, 2, 3, 4])
	Bytes: b'0000000001000000020000000300000004000000'
	A2: array('i', [0, 1, 2, 3, 4])

.. {{{end}}}

Alternate Byte Ordering
=======================

If the data in the array is not in the native byte order, or needs to
be swapped before being sent to a system with a different byte order
(or over the network), it is possible to convert the entire array without
iterating over the elements from Python.

.. include:: array_byteswap.py
    :literal:
    :start-after: #end_pymotw_header

The :func:`byteswap` method switches the byte order of the items in
the array from within C, so it is much more efficient than looping
over the data in Python.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'array_byteswap.py'))
.. }}}

::

	$ python3 array_byteswap.py
	
	      A1 hex           A1       A2 hex           A2
	------------ ------------ ------------ ------------
	 b'78563412'    305419896  b'12345678'   2018915346
	 b'79563412'    305419897  b'12345679'   2035692562
	 b'7a563412'    305419898  b'1234567a'   2052469778
	 b'7b563412'    305419899  b'1234567b'   2069246994
	 b'7c563412'    305419900  b'1234567c'   2086024210

.. {{{end}}}


.. seealso::

    * `array <http://docs.python.org/library/array.html>`_ -- The
      standard library documentation for this module.

    * :mod:`struct` -- The ``struct`` module.

    * `Numerical Python <http://www.scipy.org>`_ -- NumPy is a Python
      library for working with large data sets efficiently.

    * :ref:`Porting notes for array <porting-array>`
