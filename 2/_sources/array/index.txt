====================================
array -- Sequence of fixed-type data
====================================

.. module:: array
    :synopsis: Manage sequences of fixed-type numerical data efficiently.

:Purpose: Manage sequences of fixed-type numerical data efficiently.
:Available In: 1.4 and later

The :mod:`array` module defines a sequence data structure that looks
very much like a :class:`list` except that all of the members have to
be of the same type.  The types supported are all numeric or other
fixed-size primitive types such as bytes.

+------------+-------------------+--------------------------+
| Code       | Type              | Minimum size (bytes)     |
+============+===================+==========================+
| ``c``      | character         | 1                        |
+------------+-------------------+--------------------------+
| ``b``      | int               | 1                        |
+------------+-------------------+--------------------------+
| ``B``      | int               | 1                        |
+------------+-------------------+--------------------------+
| ``u``      | Unicode character | 2 or 4 (build-dependent) |
+------------+-------------------+--------------------------+
| ``h``      | int               | 2                        |
+------------+-------------------+--------------------------+
| ``H``      | int               | 2                        |
+------------+-------------------+--------------------------+
| ``i``      | int               | 2                        |
+------------+-------------------+--------------------------+
| ``I``      | long              | 2                        |
+------------+-------------------+--------------------------+
| ``l``      | int               | 4                        |
+------------+-------------------+--------------------------+
| ``L``      | long              | 4                        |
+------------+-------------------+--------------------------+
| ``f``      | float             | 4                        |
+------------+-------------------+--------------------------+
| ``d``      | float             | 8                        |
+------------+-------------------+--------------------------+


array Initialization
====================

An :class:`array` is instantiated with an argument describing the type
of data to be allowed, and possibly an initial sequence of data to
store in the array.

.. include:: array_string.py
    :literal:
    :start-after: #end_pymotw_header

In this example, the array is configured to hold a sequence of bytes
and is initialized with a simple string.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'array_string.py'))
.. }}}

::

	$ python array_string.py
	
	As string: This is the array.
	As array : array('c', 'This is the array.')
	As hex   : 54686973206973207468652061727261792e

.. {{{end}}}


Manipulating Arrays
===================

An :class:`array` can be extended and otherwise manipulated in the
same ways as other Python sequences.

.. include:: array_sequence.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'array_sequence.py'))
.. }}}

::

	$ python array_sequence.py
	
	Initial : array('i', [0, 1, 2, 3, 4])
	Extended: array('i', [0, 1, 2, 3, 4, 0, 1, 2, 3, 4])
	Slice   : array('i', [3, 4, 0])
	Iterator: [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 0), (6, 1), (7, 2), (8, 3), (9, 4)]

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

	$ python array_file.py
	
	A1: array('i', [0, 1, 2, 3, 4])
	Raw Contents: 0000000001000000020000000300000004000000
	A2: array('i', [0, 1, 2, 3, 4])

.. {{{end}}}


Alternate Byte Ordering
=======================

If the data in the array is not in the native byte order, or needs to
be swapped before being written to a file intended for a system with a
different byte order, it is easy to convert the entire array without
iterating over the elements from Python.

.. include:: array_byteswap.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'array_byteswap.py'))
.. }}}

::

	$ python array_byteswap.py
	
	    A1 hex         A1     A2 hex         A2
	---------- ---------- ---------- ----------
	  00000000          0   00000000          0
	  01000000          1   00000001   16777216
	  02000000          2   00000002   33554432
	  03000000          3   00000003   50331648
	  04000000          4   00000004   67108864

.. {{{end}}}


.. seealso::

    `array <http://docs.python.org/2.7/library/array.html>`_
        The standard library documentation for this module.

    :mod:`struct`
        The struct module.

    `Numerical Python <http://www.scipy.org>`_
        NumPy is a Python library for working with large datasets efficiently.

    :ref:`article-data-structures`
