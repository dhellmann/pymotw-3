========================================
bisect -- Maintain lists in sorted order
========================================

.. module:: bisect
    :synopsis: Maintains a list in sorted order without having to call sort each time an item is added to the list.

:Purpose: Maintains a list in sorted order without having to call sort each time an item is added to the list.
:Available In: 1.4

The bisect module implements an algorithm for inserting elements into a list
while maintaining the list in sorted order. This can be much more efficient
than repeatedly sorting a list, or explicitly sorting a large list after it is
constructed.

Example
=======

Let's look at a simple example using bisect.insort(), which inserts items into
a list in sorted order.

.. include:: bisect_example.py
    :literal:
    :start-after: #end_pymotw_header

The output for that script is:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'bisect_example.py'))
.. }}}

::

	$ python bisect_example.py
	
	14  0 [14]
	85  1 [14, 85]
	77  1 [14, 77, 85]
	26  1 [14, 26, 77, 85]
	50  2 [14, 26, 50, 77, 85]
	45  2 [14, 26, 45, 50, 77, 85]
	66  4 [14, 26, 45, 50, 66, 77, 85]
	79  6 [14, 26, 45, 50, 66, 77, 79, 85]
	10  0 [10, 14, 26, 45, 50, 66, 77, 79, 85]
	 3  0 [3, 10, 14, 26, 45, 50, 66, 77, 79, 85]
	84  9 [3, 10, 14, 26, 45, 50, 66, 77, 79, 84, 85]
	44  4 [3, 10, 14, 26, 44, 45, 50, 66, 77, 79, 84, 85]
	77  9 [3, 10, 14, 26, 44, 45, 50, 66, 77, 77, 79, 84, 85]
	 1  0 [1, 3, 10, 14, 26, 44, 45, 50, 66, 77, 77, 79, 84, 85]
	45  7 [1, 3, 10, 14, 26, 44, 45, 45, 50, 66, 77, 77, 79, 84, 85]
	73 10 [1, 3, 10, 14, 26, 44, 45, 45, 50, 66, 73, 77, 77, 79, 84, 85]
	23  4 [1, 3, 10, 14, 23, 26, 44, 45, 45, 50, 66, 73, 77, 77, 79, 84, 85]
	95 17 [1, 3, 10, 14, 23, 26, 44, 45, 45, 50, 66, 73, 77, 77, 79, 84, 85, 95]
	91 17 [1, 3, 10, 14, 23, 26, 44, 45, 45, 50, 66, 73, 77, 77, 79, 84, 85, 91, 95]

.. {{{end}}}

The first column shows the new random number. The second column shows the
position where the number will be inserted into the list. The remainder of
each line is the current sorted list.

This is a simple example, and for the amount of data we are manipulating it
might be faster to simply build the list and then sort it once. But for long
lists, significant time and memory savings can be achieved using an insertion
sort algorithm such as this.

You probably noticed that the result set above includes a few repeated values
(45 and 77). The bisect module provides 2 ways to handle repeats. New values
can be inserted to the left of existing values, or to the right. The insort()
function is actually an alias for insort_right(), which inserts after the
existing value. The corresponding function insort_left() inserts before the
existing value.

If we manipulate the same data using bisect_left() and insort_left(), we end
up with the same sorted list but notice that the insert positions are
different for the duplicate values.

.. include:: bisect_example2.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'bisect_example2.py'))
.. }}}

::

	$ python bisect_example2.py
	
	14  0 [14]
	85  1 [14, 85]
	77  1 [14, 77, 85]
	26  1 [14, 26, 77, 85]
	50  2 [14, 26, 50, 77, 85]
	45  2 [14, 26, 45, 50, 77, 85]
	66  4 [14, 26, 45, 50, 66, 77, 85]
	79  6 [14, 26, 45, 50, 66, 77, 79, 85]
	10  0 [10, 14, 26, 45, 50, 66, 77, 79, 85]
	 3  0 [3, 10, 14, 26, 45, 50, 66, 77, 79, 85]
	84  9 [3, 10, 14, 26, 45, 50, 66, 77, 79, 84, 85]
	44  4 [3, 10, 14, 26, 44, 45, 50, 66, 77, 79, 84, 85]
	77  8 [3, 10, 14, 26, 44, 45, 50, 66, 77, 77, 79, 84, 85]
	 1  0 [1, 3, 10, 14, 26, 44, 45, 50, 66, 77, 77, 79, 84, 85]
	45  6 [1, 3, 10, 14, 26, 44, 45, 45, 50, 66, 77, 77, 79, 84, 85]
	73 10 [1, 3, 10, 14, 26, 44, 45, 45, 50, 66, 73, 77, 77, 79, 84, 85]
	23  4 [1, 3, 10, 14, 23, 26, 44, 45, 45, 50, 66, 73, 77, 77, 79, 84, 85]
	95 17 [1, 3, 10, 14, 23, 26, 44, 45, 45, 50, 66, 73, 77, 77, 79, 84, 85, 95]
	91 17 [1, 3, 10, 14, 23, 26, 44, 45, 45, 50, 66, 73, 77, 77, 79, 84, 85, 91, 95]

.. {{{end}}}


In addition to the Python implementation, there is a faster C implementation
available. If the C version is present, that implementation overrides the pure
Python implementation automatically when you import the bisect module.


.. seealso::

    `bisect <http://docs.python.org/2.7/library/bisect.html>`_
        The standard library documentation for this module.

    `WikiPedia: Insertion Sort <http://en.wikipedia.org/wiki/Insertion_sort>`_
        A description of the insertion sort algorithm.

    :ref:`article-data-structures`
