===========================================
 bisect --- Maintain Lists in Sorted Order
===========================================

.. module:: bisect
    :synopsis: Maintains a list in sorted order without having to call
               sort each time an item is added to the list.

:Purpose: Maintains a list in sorted order without having to call sort
          each time an item is added to the list.

The :mod:`bisect` module implements an algorithm for inserting
elements into a list while maintaining the list in sorted order.

Inserting in Sorted Order
=========================

Here is a simple example using :func:`insort` to insert items into a
list in sorted order.

.. include:: bisect_example.py
    :literal:
    :start-after: #end_pymotw_header

The first column of the output shows the new random number. The second
column shows the position where the number will be inserted into the
list. The remainder of each line is the current sorted list.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'bisect_example.py'))
.. }}}

::

	$ python3 bisect_example.py
	
	New  Pos  Contents
	---  ---  --------
	 14    0 [14]
	 85    1 [14, 85]
	 77    1 [14, 77, 85]
	 26    1 [14, 26, 77, 85]
	 50    2 [14, 26, 50, 77, 85]
	 45    2 [14, 26, 45, 50, 77, 85]
	 66    4 [14, 26, 45, 50, 66, 77, 85]
	 79    6 [14, 26, 45, 50, 66, 77, 79, 85]
	 10    0 [10, 14, 26, 45, 50, 66, 77, 79, 85]
	  3    0 [3, 10, 14, 26, 45, 50, 66, 77, 79, 85]
	 84    9 [3, 10, 14, 26, 45, 50, 66, 77, 79, 84, 85]
	 77    8 [3, 10, 14, 26, 45, 50, 66, 77, 77, 79, 84, 85]
	  1    0 [1, 3, 10, 14, 26, 45, 50, 66, 77, 77, 79, 84, 85]

.. {{{end}}}

This is a simple example, and for the amount of data being manipulated
it might be faster to simply build the list and then sort it once. But
for long lists, significant time and memory savings can be achieved
using an insertion sort algorithm such as this.

Handling Duplicates
===================

The result set shown previously includes a repeated value,
``77``. The :mod:`bisect` module provides two ways to handle repeats. New
values can be inserted to the left of existing values, or to the
right. The :func:`insort` function is actually an alias for
:func:`insort_right`, which inserts after the existing value. The
corresponding function :func:`insort_left` inserts before the existing
value.

.. include:: bisect_example2.py
    :literal:
    :start-after: #end_pymotw_header

When the same data is manipulates using :func:`bisect_left` and
:func:`insort_left`, the results are the same sorted list but the
insert positions are different for the duplicate values.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'bisect_example2.py'))
.. }}}

::

	$ python3 bisect_example2.py
	
	New  Pos  Contents
	---  ---  --------
	 14    0 [14]
	 85    1 [14, 85]
	 77    1 [14, 77, 85]
	 26    1 [14, 26, 77, 85]
	 50    2 [14, 26, 50, 77, 85]
	 45    2 [14, 26, 45, 50, 77, 85]
	 66    4 [14, 26, 45, 50, 66, 77, 85]
	 79    6 [14, 26, 45, 50, 66, 77, 79, 85]
	 10    0 [10, 14, 26, 45, 50, 66, 77, 79, 85]
	  3    0 [3, 10, 14, 26, 45, 50, 66, 77, 79, 85]
	 84    9 [3, 10, 14, 26, 45, 50, 66, 77, 79, 84, 85]
	 77    7 [3, 10, 14, 26, 45, 50, 66, 77, 77, 79, 84, 85]
	  1    0 [1, 3, 10, 14, 26, 45, 50, 66, 77, 77, 79, 84, 85]

.. {{{end}}}


In addition to the Python implementation, there is a faster C implementation
available. If the C version is present, that implementation overrides the pure
Python implementation automatically when :mod:`bisect` is imported.


.. seealso::

    * :pydoc:`bisect`

    * `WikiPedia: Insertion Sort
      <http://en.wikipedia.org/wiki/Insertion_sort>`_ -- A description
      of the insertion sort algorithm.
