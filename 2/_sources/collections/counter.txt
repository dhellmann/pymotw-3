=========
 Counter
=========

A :class:`Counter` is a container that keeps track of how many times
equivalent values are added.  It can be used to implement the same
algorithms for which bag or multiset data structures are commonly used
in other languages.

Initializing
============

:class:`Counter` supports three forms of initialization.  Its
constructor can be called with a sequence of items, a dictionary
containing keys and counts, or using keyword arguments mapping string
names to counts.

.. include:: collections_counter_init.py
   :literal:
   :start-after: #end_pymotw_header

The results of all three forms of initialization are the same.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'collections_counter_init.py'))
.. }}}

::

	$ python collections_counter_init.py
	
	Counter({'b': 3, 'a': 2, 'c': 1})
	Counter({'b': 3, 'a': 2, 'c': 1})
	Counter({'b': 3, 'a': 2, 'c': 1})

.. {{{end}}}

An empty :class:`Counter` can be constructed with no arguments and
populated via the :func:`update` method.

.. include:: collections_counter_update.py
   :literal:
   :start-after: #end_pymotw_header

The count values are increased based on the new data, rather than
replaced.  In this example, the count for ``a`` goes from ``3`` to
``4``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'collections_counter_update.py'))
.. }}}

::

	$ python collections_counter_update.py
	
	Initial : Counter()
	Sequence: Counter({'a': 3, 'b': 2, 'c': 1, 'd': 1})
	Dict    : Counter({'d': 6, 'a': 4, 'b': 2, 'c': 1})

.. {{{end}}}

Accessing Counts
================

Once a :class:`Counter` is populated, its values can be retrieved
using the dictionary API.

.. include:: collections_counter_get_values.py
   :literal:
   :start-after: #end_pymotw_header

:class:`Counter` does not raise :ref:`KeyError <exceptions-KeyError>`
for unknown items.  If a value has not been seen in the input (as with
``e`` in this example), its count is ``0``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'collections_counter_get_values.py'))
.. }}}

::

	$ python collections_counter_get_values.py
	
	a : 3
	b : 2
	c : 1
	d : 1
	e : 0

.. {{{end}}}

The :func:`elements` method returns an iterator that produces all of
the items known to the :class:`Counter`.

.. include:: collections_counter_elements.py
   :literal:
   :start-after: #end_pymotw_header

The order of elements is not guaranteed, and items with counts less
than zero are not included.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'collections_counter_elements.py'))
.. }}}

::

	$ python collections_counter_elements.py
	
	Counter({'e': 3, 'm': 1, 'l': 1, 'r': 1, 't': 1, 'y': 1, 'x': 1, 'z': 0})
	['e', 'e', 'e', 'm', 'l', 'r', 't', 'y', 'x']

.. {{{end}}}

Use :func:`most_common` to produce a sequence of the *n* most
frequently encountered input values and their respective counts.

.. include:: collections_counter_most_common.py
   :literal:
   :start-after: #end_pymotw_header

This example counts the letters appearing in all of the words in the
system dictionary to produce a frequency distribution, then prints the
three most common letters.  Leaving out the argument to
:func:`most_common` produces a list of all the items, in order of
frequency.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'collections_counter_most_common.py'))
.. }}}

::

	$ python collections_counter_most_common.py
	
	Most common:
	e:  235331
	i:  201032
	a:  199554

.. {{{end}}}

Arithmetic
==========

:class:`Counter` instances support arithmetic and set operations for
aggregating results.

.. include:: collections_counter_arithmetic.py
   :literal:
   :start-after: #end_pymotw_header

Each time a new :class:`Counter` is produced through an operation, any
items with zero or negative counts are discarded.  The count for ``a``
is the same in :data:`c1` and :data:`c2`, so subtraction leaves it at
zero.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'collections_counter_arithmetic.py'))
.. }}}

::

	$ python collections_counter_arithmetic.py
	
	C1: Counter({'b': 3, 'a': 2, 'c': 1})
	C2: Counter({'a': 2, 'b': 1, 'e': 1, 'h': 1, 'l': 1, 'p': 1, 't': 1})
	
	Combined counts:
	Counter({'a': 4, 'b': 4, 'c': 1, 'e': 1, 'h': 1, 'l': 1, 'p': 1, 't': 1})
	
	Subtraction:
	Counter({'b': 2, 'c': 1})
	
	Intersection (taking positive minimums):
	Counter({'a': 2, 'b': 1})
	
	Union (taking maximums):
	Counter({'b': 3, 'a': 2, 'c': 1, 'e': 1, 'h': 1, 'l': 1, 'p': 1, 't': 1})

.. {{{end}}}


