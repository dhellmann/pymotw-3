=================================
 itertools -- Iterator Functions
=================================

.. module:: itertools
    :synopsis: Iterator functions for efficient looping

:Purpose:
    The itertools module includes a set of functions for working with 
    sequence data sets. 
:Python Version: 2.3 and later

The functions provided by :mod:`itertools` are inspired by similar
features of functional programming languages such as Clojure and
Haskell. They are intended to be fast and use memory efficiently, and
also to be hooked together to express more complicated iteration-based
algorithms.

Iterator-based code offers better memory consumption characteristics
than code that uses lists.  Since data is not produced from the
iterator until it is needed, all of the data does not need to be
stored in memory at the same time.  This "lazy" processing model uses
less memory, which can reduce swapping and other side-effects of large
data sets, improving performance.

Merging and Splitting Iterators
===============================

The :func:`chain` function takes several iterators as arguments and
returns a single iterator that produces the contents of all of them as
though they came from a single iterator.

.. include:: itertools_chain.py
    :literal:
    :start-after: #end_pymotw_header

:func:`chain` makes it easy to process several sequences without
constructing one large list.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_chain.py'))
.. }}}

::

	$ python itertools_chain.py
	
	1 2 3 a b c

.. {{{end}}}

:func:`izip` returns an iterator that combines the elements of several
iterators into tuples. 

.. include:: itertools_izip.py
    :literal:
    :start-after: #end_pymotw_header

It works like the built-in function :func:`zip`, except that it
returns an iterator instead of a list.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_izip.py'))
.. }}}

::

	$ python itertools_izip.py
	
	(1, 'a')
	(2, 'b')
	(3, 'c')

.. {{{end}}}

The :func:`islice` function returns an iterator which returns selected
items from the input iterator, by index. 

.. include:: itertools_islice.py
    :literal:
    :start-after: #end_pymotw_header

:func:`islice` takes the same arguments as the slice operator for
lists: *start*, *stop*, and *step*. The start and step arguments are
optional.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_islice.py'))
.. }}}

::

	$ python itertools_islice.py
	
	Stop at 5:
	0 1 2 3 4 
	
	Start at 5, Stop at 10:
	5 6 7 8 9 
	
	By tens to 100:
	0 10 20 30 40 50 60 70 80 90 
	

.. {{{end}}}

The :func:`tee` function returns several independent iterators (defaults
to 2) based on a single original input. 

.. include:: itertools_tee.py
    :literal:
    :start-after: #end_pymotw_header

:func:`tee` has semantics similar to the Unix :command:`tee` utility,
which repeats the values it reads from its input and writes them to a
named file and standard output.  The iterators returned by :func:`tee`
can be used to feed the same set of data into multiple algorithms to
be processed in parallel.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_tee.py'))
.. }}}

::

	$ python itertools_tee.py
	
	i1: [0, 1, 2, 3, 4]
	i2: [0, 1, 2, 3, 4]

.. {{{end}}}

The new iterators created by :func:`tee` share their input, so the
original iterator should not be used once the new ones are created.

.. include:: itertools_tee_error.py
    :literal:
    :start-after: #end_pymotw_header

If values are consumed from the original input, the new iterators will
not produce those values:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_tee_error.py'))
.. }}}

::

	$ python itertools_tee_error.py
	
	r: 0 1 2
	i1: [3, 4]
	i2: [3, 4]

.. {{{end}}}

Converting Inputs
=================

The :func:`imap` function returns an iterator that calls a function on
the values in the input iterators, and returns the results. It works
like the built-in :func:`map`, except that it stops when any input
iterator is exhausted (instead of inserting ``None`` values to
completely consume all of the inputs).

.. include:: itertools_imap.py
    :literal:
    :start-after: #end_pymotw_header

In the first example, the lambda function multiplies the input values
by 2. In a second example, the lambda function multiplies two
arguments, taken from separate iterators, and returns a tuple with the
original arguments and the computed value.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_imap.py'))
.. }}}

::

	$ python itertools_imap.py
	
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

.. {{{end}}}


The :func:`starmap` function is similar to :func:`imap`, but instead of
constructing a tuple from multiple iterators, it splits up the items in
a single iterator as arguments to the mapping function using the ``*``
syntax. 

.. include:: itertools_starmap.py
    :literal:
    :start-after: #end_pymotw_header

Where the mapping function to :func:`imap` is called ``f(i1, i2)``,
the mapping function passed to :func:`starmap` is called ``f(*i)``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_starmap.py'))
.. }}}

::

	$ python itertools_starmap.py
	
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
(see the built-in :func:`xrange` for more control over the result
set). 

.. include:: itertools_count.py
    :literal:
    :start-after: #end_pymotw_header

This example stops because the list argument is consumed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_count.py'))
.. }}}

::

	$ python itertools_count.py
	
	(1, 'a')
	(2, 'b')
	(3, 'c')

.. {{{end}}}

The :func:`cycle` function returns an iterator that repeats the contents
of the arguments it is given indefinitely. Since it has to remember
the entire contents of the input iterator, it may consume quite a bit
of memory if the iterator is long. 

.. include:: itertools_cycle.py
    :literal:
    :start-after: #end_pymotw_header

A counter variable is used to break out of the loop after a few cycles
in this example.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_cycle.py'))
.. }}}

::

	$ python itertools_cycle.py
	
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

.. include:: itertools_repeat.py
    :literal:
    :start-after: #end_pymotw_header

The iterator returned by :func:`repeat` keeps returning data forever,
unless the optional *times* argument is provided to limit it.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_repeat.py'))
.. }}}

::

	$ python itertools_repeat.py
	
	over-and-over
	over-and-over
	over-and-over
	over-and-over
	over-and-over

.. {{{end}}}

It is useful to combine :func:`repeat` with :func:`izip` or :func:`imap`
when invariant values need to be included with the values from the
other iterators.

.. include:: itertools_repeat_izip.py
    :literal:
    :start-after: #end_pymotw_header

A counter value is combined with the constant returned by
:func:`repeat` in this example.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_repeat_izip.py'))
.. }}}

::

	$ python itertools_repeat_izip.py
	
	0 over-and-over
	1 over-and-over
	2 over-and-over
	3 over-and-over
	4 over-and-over

.. {{{end}}}

This example uses :func:`imap` to multiply the numbers in the range 0
through 4 by 2.

.. include:: itertools_repeat_imap.py
    :literal:
    :start-after: #end_pymotw_header

The :func:`repeat` iterator does not need to be explicitly limited,
since :func:`imap` stops processing when any of its inputs ends, and
the :func:`xrange` returns only five elements.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_repeat_imap.py'))
.. }}}

::

	$ python itertools_repeat_imap.py
	
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

.. include:: itertools_dropwhile.py
    :literal:
    :start-after: #end_pymotw_header

:func:`dropwhile` does not filter every item of the input; after the
condition is false the first time, all of the remaining items in the
input are returned.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_dropwhile.py'))
.. }}}

::

	$ python itertools_dropwhile.py
	
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

.. include:: itertools_takewhile.py
    :literal:
    :start-after: #end_pymotw_header

As soon as :func:`should_take` returns ``False``, :func:`takewhile`
stops processing the input.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_takewhile.py'))
.. }}}

::

	$ python itertools_takewhile.py
	
	Testing: -1
	Yielding: -1
	Testing: 0
	Yielding: 0
	Testing: 1
	Yielding: 1
	Testing: 2

.. {{{end}}}


:func:`ifilter` returns an iterator that works like the built-in
:func:`filter` does for lists, including only items for which the test
function returns true. 

.. include:: itertools_ifilter.py
    :literal:
    :start-after: #end_pymotw_header

:func:`ifilter` is different from :func:`dropwhile` in that every item
is tested before it is returned.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_ifilter.py'))
.. }}}

::

	$ python itertools_ifilter.py
	
	Testing: -1
	Yielding: -1
	Testing: 0
	Yielding: 0
	Testing: 1
	Testing: 2
	Testing: -2
	Yielding: -2

.. {{{end}}}

:func:`ifilterfalse` returns an iterator that includes only items
where the test function returns false.

.. include:: itertools_ifilterfalse.py
    :literal:
    :start-after: #end_pymotw_header

The test expression in :func:`check_item` is the same, so the results
in this example with :func:`ifilterfalse` are the opposite of the
results from the previous example.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_ifilterfalse.py'))
.. }}}

::

	$ python itertools_ifilterfalse.py
	
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

.. include:: itertools_groupby_seq.py
    :literal:
    :start-after: #end_pymotw_header

The input sequence needs to be sorted on the key value in order for
the groupings to work out as expected.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_groupby_seq.py', break_lines_at=66))
.. }}}

::

	$ python itertools_groupby_seq.py
	
	Data:
	[(0, 0),
	 (1, 1),
	 (2, 2),
	 (0, 3),
	 (1, 4),
	 (2, 5),
	 (0, 6),
	 (1, 7),
	 (2, 8),
	 (0, 9)]
	
	Grouped, unsorted:
	0 [(0, 0)]
	1 [(1, 1)]
	2 [(2, 2)]
	0 [(0, 3)]
	1 [(1, 4)]
	2 [(2, 5)]
	0 [(0, 6)]
	1 [(1, 7)]
	2 [(2, 8)]
	0 [(0, 9)]
	
	Sorted:
	[(0, 0),
	 (0, 3),
	 (0, 6),
	 (0, 9),
	 (1, 1),
	 (1, 4),
	 (1, 7),
	 (2, 2),
	 (2, 5),
	 (2, 8)]
	
	Grouped, sorted:
	0 [(0, 0), (0, 3), (0, 6), (0, 9)]
	1 [(1, 1), (1, 4), (1, 7)]
	2 [(2, 2), (2, 5), (2, 8)]
	

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
