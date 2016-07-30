==================================
 itertools --- Iterator Functions
==================================

.. module:: itertools
    :synopsis: Iterator functions for efficient looping

:Purpose:
    The itertools module includes a set of functions for working with
    sequence data sets.

The functions provided by :mod:`itertools` are inspired by similar
features of functional programming languages such as Clojure, Haskell,
and APL. They are intended to be fast and use memory efficiently, and
also to be hooked together to express more complicated iteration-based
algorithms.

Iterator-based code offers better memory consumption characteristics
than code that uses lists.  Since data is not produced from the
iterator until it is needed, all of the data does not need to be
stored in memory at the same time.  This "lazy" processing model uses
less memory, which can reduce swapping and other side-effects of large
data sets, improving performance.

In addition to the functions defined in :mod:`itertools`, the examples
in this section also rely on some of the built-in functions for
iteration.

Merging and Splitting Iterators
===============================

The :func:`chain` function takes several iterators as arguments and
returns a single iterator that produces the contents of all of the
inputs as though they came from a single iterator.

.. literalinclude:: itertools_chain.py
   :caption:
   :start-after: #end_pymotw_header

:func:`chain` makes it easy to process several sequences without
constructing one large list.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_chain.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_chain.py
	
	1 2 3 a b c 

.. {{{end}}}

The built-in function :func:`zip` returns an iterator that combines
the elements of several iterators into tuples.

.. literalinclude:: itertools_zip.py
   :caption:
   :start-after: #end_pymotw_header

As with the other functions in this module, the return value is an
iterable object that produces values one at a time.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_zip.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_zip.py
	
	(1, 'a')
	(2, 'b')
	(3, 'c')

.. {{{end}}}

The :func:`islice` function returns an iterator which returns selected
items from the input iterator, by index.

.. literalinclude:: itertools_islice.py
   :caption:
   :start-after: #end_pymotw_header

:func:`islice` takes the same arguments as the slice operator for
lists: *start*, *stop*, and *step*. The start and step arguments are
optional.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_islice.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_islice.py
	
	Stop at 5:
	0 1 2 3 4 
	
	Start at 5, Stop at 10:
	5 6 7 8 9 
	
	By tens to 100:
	0 10 20 30 40 50 60 70 80 90 
	

.. {{{end}}}

The :func:`tee` function returns several independent iterators (defaults
to 2) based on a single original input. 

.. literalinclude:: itertools_tee.py
   :caption:
   :start-after: #end_pymotw_header

:func:`tee` has semantics similar to the UNIX :command:`tee` utility,
which repeats the values it reads from its input and writes them to a
named file and standard output.  The iterators returned by :func:`tee`
can be used to feed the same set of data into multiple algorithms to
be processed in parallel.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_tee.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_tee.py
	
	i1: [0, 1, 2, 3, 4]
	i2: [0, 1, 2, 3, 4]

.. {{{end}}}

The new iterators created by :func:`tee` share their input, so the
original iterator should not be used after the new ones are created.

.. literalinclude:: itertools_tee_error.py
   :caption:
   :start-after: #end_pymotw_header

If values are consumed from the original input, the new iterators will
not produce those values:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_tee_error.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_tee_error.py
	
	r: 0 1 2 
	i1: [3, 4]
	i2: [3, 4]

.. {{{end}}}

Converting Inputs
=================

The built-in :func:`map` function returns an iterator that calls a
function on the values in the input iterators, and returns the
results. It stops when any input iterator is exhausted.

.. literalinclude:: itertools_map.py
   :caption:
   :start-after: #end_pymotw_header

In the first example, the lambda function multiplies the input values
by 2. In a second example, the lambda function multiplies two
arguments, taken from separate iterators, and returns a tuple with the
original arguments and the computed value. The third example stops
after producing two tuples because the second range is exhausted.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_map.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_map.py
	
	Doubles:
	0
	2
	4
	6
	8
	
	Multiples:
	0 * 5 = 0
	1 * 6 = 6
	2 * 7 = 14
	3 * 8 = 24
	4 * 9 = 36
	
	Stopping:
	(0, 0)
	(1, 1)

.. {{{end}}}


The :func:`starmap` function is similar to :func:`map`, but instead of
constructing a tuple from multiple iterators, it splits up the items
in a single iterator as arguments to the mapping function using the
``*`` syntax.

.. literalinclude:: itertools_starmap.py
   :caption:
   :start-after: #end_pymotw_header

Where the mapping function to :func:`map` is called ``f(i1, i2)``, the
mapping function passed to :func:`starmap` is called ``f(*i)``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_starmap.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_starmap.py
	
	0 * 5 = 0
	1 * 6 = 6
	2 * 7 = 14
	3 * 8 = 24
	4 * 9 = 36

.. {{{end}}}

Producing New Values
====================

The :func:`count` function returns an iterator that produces
consecutive integers, indefinitely. The first number can be passed as
an argument (the default is zero). There is no upper bound argument
(see the built-in :func:`range` for more control over the result set).

.. literalinclude:: itertools_count.py
   :caption:
   :start-after: #end_pymotw_header

This example stops because the list argument is consumed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_count.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_count.py
	
	(1, 'a')
	(2, 'b')
	(3, 'c')

.. {{{end}}}

The :func:`cycle` function returns an iterator that repeats the
contents of the arguments it is given indefinitely. Since it has to
remember the entire contents of the input iterator, it may consume
quite a bit of memory if the iterator is long.

.. literalinclude:: itertools_cycle.py
   :caption:
   :start-after: #end_pymotw_header

A counter variable is used to break out of the loop after a few cycles
in this example.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_cycle.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_cycle.py
	
	(0, 'a')
	(1, 'b')
	(2, 'c')
	(3, 'a')
	(4, 'b')
	(5, 'c')
	(6, 'a')

.. {{{end}}}

The :func:`repeat` function returns an iterator that produces the same
value each time it is accessed.

.. literalinclude:: itertools_repeat.py
   :caption:
   :start-after: #end_pymotw_header

The iterator returned by :func:`repeat` keeps returning data forever,
unless the optional *times* argument is provided to limit it.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_repeat.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_repeat.py
	
	over-and-over
	over-and-over
	over-and-over
	over-and-over
	over-and-over

.. {{{end}}}

It is useful to combine :func:`repeat` with :func:`zip` or :func:`map`
when invariant values need to be included with the values from the
other iterators.

.. literalinclude:: itertools_repeat_zip.py
   :caption:
   :start-after: #end_pymotw_header

A counter value is combined with the constant returned by
:func:`repeat` in this example.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_repeat_zip.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_repeat_zip.py
	
	0 over-and-over
	1 over-and-over
	2 over-and-over
	3 over-and-over
	4 over-and-over

.. {{{end}}}

This example uses :func:`map` to multiply the numbers in the range 0
through 4 by 2.

.. literalinclude:: itertools_repeat_map.py
   :caption:
   :start-after: #end_pymotw_header

The :func:`repeat` iterator does not need to be explicitly limited,
since :func:`map` stops processing when any of its inputs ends, and
the :func:`range` returns only five elements.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_repeat_map.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_repeat_map.py
	
	2 * 0 = 0
	2 * 1 = 2
	2 * 2 = 4
	2 * 3 = 6
	2 * 4 = 8

.. {{{end}}}


Filtering
=========

The :func:`dropwhile` function returns an iterator that produces
elements of the input iterator after a condition becomes false for the
first time.

.. literalinclude:: itertools_dropwhile.py
   :caption:
   :start-after: #end_pymotw_header

:func:`dropwhile` does not filter every item of the input; after the
condition is false the first time, all of the remaining items in the
input are returned.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_dropwhile.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_dropwhile.py
	
	Testing: -1
	Testing: 0
	Testing: 1
	Yielding: 1
	Yielding: 2
	Yielding: -2

.. {{{end}}}

The opposite of :func:`dropwhile` is :func:`takewhile`.  It returns an
iterator that returns items from the input iterator as long as the
test function returns true.

.. literalinclude:: itertools_takewhile.py
   :caption:
   :start-after: #end_pymotw_header

As soon as :func:`should_take` returns ``False``, :func:`takewhile`
stops processing the input.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_takewhile.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_takewhile.py
	
	Testing: -1
	Yielding: -1
	Testing: 0
	Yielding: 0
	Testing: 1
	Yielding: 1
	Testing: 2

.. {{{end}}}


The built-in function :func:`filter` returns an iterator that includes
only items for which the test function returns true.

.. literalinclude:: itertools_filter.py
   :caption:
   :start-after: #end_pymotw_header

:func:`filter` is different from :func:`dropwhile` and
:func:`takewhile` in that every item is tested before it is returned.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_filter.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_filter.py
	
	Testing: -1
	Yielding: -1
	Testing: 0
	Yielding: 0
	Testing: 1
	Testing: 2
	Testing: -2
	Yielding: -2

.. {{{end}}}

:func:`filterfalse` returns an iterator that includes only items
where the test function returns false.

.. literalinclude:: itertools_filterfalse.py
   :caption:
   :start-after: #end_pymotw_header

The test expression in :func:`check_item` is the same, so the results
in this example with :func:`filterfalse` are the opposite of the
results from the previous example.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_filterfalse.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_filterfalse.py
	
	Testing: -1
	Testing: 0
	Testing: 1
	Yielding: 1
	Testing: 2
	Yielding: 2
	Testing: -2

.. {{{end}}}

.. _itertools-groupby:

Grouping Data
=============

The :func:`groupby` function returns an iterator that produces sets of
values organized by a common key.  This example illustrates grouping
related values based on an attribute.

.. literalinclude:: itertools_groupby_seq.py
   :caption:
   :start-after: #end_pymotw_header

The input sequence needs to be sorted on the key value in order for
the groupings to work out as expected.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_groupby_seq.py', break_lines_at=66))
.. }}}

.. code-block:: none

	$ python3 itertools_groupby_seq.py
	
	Data:
	[(0, 0),
	 (1, 1),
	 (2, 2),
	 (0, 3),
	 (1, 4),
	 (2, 5),
	 (0, 6)]
	
	Grouped, unsorted:
	0 [(0, 0)]
	1 [(1, 1)]
	2 [(2, 2)]
	0 [(0, 3)]
	1 [(1, 4)]
	2 [(2, 5)]
	0 [(0, 6)]
	
	Sorted:
	[(0, 0),
	 (0, 3),
	 (0, 6),
	 (1, 1),
	 (1, 4),
	 (2, 2),
	 (2, 5)]
	
	Grouped, sorted:
	0 [(0, 0), (0, 3), (0, 6)]
	1 [(1, 1), (1, 4)]
	2 [(2, 2), (2, 5)]
	

.. {{{end}}}



.. seealso::

    `itertools <http://docs.python.org/library/itertools.html>`_
        The standard library documentation for this module.

    `The Standard ML Basis Library <http://www.standardml.org/Basis/>`_)
        The library for SML.

    `Definition of Haskell and the Standard Libraries <http://www.haskell.org/definition/>`__
        Standard library specification for the functional language Haskell.

    `Clojure <http://clojure.org/>`__
        Clojure is a dynamic functional language that runs on the Java
        Virtual Machine.

    `tee <http://unixhelp.ed.ac.uk/CGI/man-cgi?tee>`__
        Unix command line tool for splitting one input into multiple
        identical output streams.
