==================================
 itertools --- Iterator Functions
==================================

.. module:: itertools
    :synopsis: Iterator functions for efficient looping

The ``itertools`` module includes a set of functions for working
with sequence data sets.  The functions provided are inspired by
similar features of functional programming languages such as Clojure,
Haskell, APL, and SML. They are intended to be fast and use memory
efficiently, and also to be hooked together to express more
complicated iteration-based algorithms.

Iterator-based code offers better memory consumption characteristics
than code that uses lists.  Since data is not produced from the
iterator until it is needed, all of the data does not need to be
stored in memory at the same time.  This "lazy" processing model uses
less memory, which can reduce swapping and other side-effects of large
data sets, improving performance.

In addition to the functions defined in ``itertools``, the examples
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

If the iterables to be combined are not all known in advance, or need
to be evaluated lazily, :func:`chain.from_iterable` can be used to
construct the chain instead.

.. literalinclude:: itertools_chain_from_iterable.py
   :caption:
   :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_chain_from_iterable.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_chain_from_iterable.py
	
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

:func:`zip` stops when the first input iterator is exhausted. To
process all of the inputs, even if the iterators produce different
numbers of values, use :func:`zip_longest`.

.. literalinclude:: itertools_zip_longest.py
   :caption:
   :start-after: #end_pymotw_header

By default, :func:`zip_longest` substitutes ``None`` for any missing
values. Use the ``fillvalue`` argument to use a different substitute
value.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_zip_longest.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_zip_longest.py
	
	zip stops early:
	[(0, 0), (1, 1)]
	
	zip_longest processes all of the values:
	[(0, 0), (1, 1), (2, None)]

.. {{{end}}}


The :func:`islice` function returns an iterator which returns selected
items from the input iterator, by index.

.. literalinclude:: itertools_islice.py
   :caption:
   :start-after: #end_pymotw_header

:func:`islice` takes the same arguments as the slice operator for
lists: ``start``, ``stop``, and ``step``. The start and step arguments
are optional.

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

:func:`tee` has semantics similar to the Unix ``tee`` utility,
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
	(0, 0, 0)
	(1, 1, 1)

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

The start and step arguments to :func:`count` can be any numerical
values that can be added together.

.. literalinclude:: itertools_count_step.py
   :caption:
   :start-after: #end_pymotw_header

In this example, the start point and steps are :class:`Fraction`
objects from the :mod:`fraction` module.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_count_step.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_count_step.py
	
	1/3: a
	2/3: b
	1: c

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
unless the optional ``times`` argument is provided to limit it.

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

:func:`compress` offers another way to filter the contents of an
iterable. Instead of calling a function, it uses the values in another
iterable to indicate when to accept a value and when to ignore it.

.. literalinclude:: itertools_compress.py
   :caption:
   :start-after: #end_pymotw_header

The first argument is the data iterable to process and the second is a
selector iterable producing Boolean values indicating which elements
to take from the data input (a true value causes the value to be
produced, a false value causes it to be ignored).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_compress.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_compress.py
	
	3 6 9 

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
.. cog.out(run_script(cog.inFile, 'itertools_groupby_seq.py'))
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

Combining Inputs
================

The :func:`accumulate` function processes the input iterable, passing
the nth and n+1st item to a function and producing the return value
instead of either input. The default function used to combine the two
values adds them, so :func:`accumulate` can be used to produce the
cumulative sum of a series of numerical inputs.

.. literalinclude:: itertools_accumulate.py
   :caption:
   :start-after: #end_pymotw_header

When used with a sequence of non-integer values, the results depend on
what it means to "add" two items together. The second example in this
script shows that when :func:`accumulate` receives a string input each
response is a progressively longer prefix of that string.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_accumulate.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_accumulate.py
	
	[0, 1, 3, 6, 10]
	['a', 'ab', 'abc', 'abcd', 'abcde']

.. {{{end}}}

It is possible to combine :func:`accumulate` with any other function
that takes two input values to achieve different results.

.. literalinclude:: itertools_accumulate_custom.py
   :caption:
   :start-after: #end_pymotw_header

This example combines the string values in a way that makes a series
of (nonsensical) palindromes. Each step of the way when ``f()`` is
called, it prints the input values passed to it by :func:`accumulate`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_accumulate_custom.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_accumulate_custom.py
	
	a b
	bab c
	cbabc d
	dcbabcd e
	['a', 'bab', 'cbabc', 'dcbabcd', 'edcbabcde']

.. {{{end}}}

Nested ``for`` loops that iterate over multiple sequences can often be
replaced with :func:`product`, which produces a single iterable whose
values are the Cartesian product of the set of input values.

.. literalinclude:: itertools_product.py
   :caption:
   :start-after: #end_pymotw_header

The values produced by :func:`product` are tuples, with the members
taken from each of the iterables passed in as arguments in the order
they are passed. The first tuple returned includes the first value
from each iterable. The *last* iterable passed to :func:`product` is
processed first, followed by the next to last, and so on. The result
is that the return values are in order based on the first iterable,
then the next iterable, etc.

In this example, the cards are ordered by value and then by suit.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_product.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_product.py
	
	 2♥  2♦  2♣  2♠ 
	 3♥  3♦  3♣  3♠ 
	 4♥  4♦  4♣  4♠ 
	 5♥  5♦  5♣  5♠ 
	 6♥  6♦  6♣  6♠ 
	 7♥  7♦  7♣  7♠ 
	 8♥  8♦  8♣  8♠ 
	 9♥  9♦  9♣  9♠ 
	10♥ 10♦ 10♣ 10♠ 
	 J♥  J♦  J♣  J♠ 
	 Q♥  Q♦  Q♣  Q♠ 
	 K♥  K♦  K♣  K♠ 
	 A♥  A♦  A♣  A♠ 

.. {{{end}}}

To change the order of the cards, change the order of the arguments to
:func:`product`.

.. literalinclude:: itertools_product_ordering.py
   :caption:
   :start-after: #end_pymotw_header
   :emphasize-lines: 10-11,17

The print loop in this example looks for an Ace card, instead of the
spade suit, and then adds a newline to break up the output.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_product_ordering.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_product_ordering.py
	
	 2♥  3♥  4♥  5♥  6♥  7♥  8♥  9♥ 10♥  J♥  Q♥  K♥  A♥ 
	 2♦  3♦  4♦  5♦  6♦  7♦  8♦  9♦ 10♦  J♦  Q♦  K♦  A♦ 
	 2♣  3♣  4♣  5♣  6♣  7♣  8♣  9♣ 10♣  J♣  Q♣  K♣  A♣ 
	 2♠  3♠  4♠  5♠  6♠  7♠  8♠  9♠ 10♠  J♠  Q♠  K♠  A♠ 

.. {{{end}}}

To compute the product of a sequence with itself, specify how many
times the input should be repeated.

.. literalinclude:: itertools_product_repeat.py
   :caption:
   :start-after: #end_pymotw_header

Since repeating a single iterable is like passing the same iterable
multiple times, each tuple produced by :func:`product` will contain a
number of items equal to the repeat counter.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_product_repeat.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_product_repeat.py
	
	Repeat 2:
	
	(0, 0) (0, 1) (0, 2) 
	(1, 0) (1, 1) (1, 2) 
	(2, 0) (2, 1) (2, 2) 
	
	Repeat 3:
	
	(0, 0, 0) (0, 0, 1) (0, 0, 2) 
	(0, 1, 0) (0, 1, 1) (0, 1, 2) 
	(0, 2, 0) (0, 2, 1) (0, 2, 2) 
	(1, 0, 0) (1, 0, 1) (1, 0, 2) 
	(1, 1, 0) (1, 1, 1) (1, 1, 2) 
	(1, 2, 0) (1, 2, 1) (1, 2, 2) 
	(2, 0, 0) (2, 0, 1) (2, 0, 2) 
	(2, 1, 0) (2, 1, 1) (2, 1, 2) 
	(2, 2, 0) (2, 2, 1) (2, 2, 2) 
	

.. {{{end}}}

The :func:`permutations` function produces items from the input
iterable combined in the possible permutations of the given length. It
defaults to producing the full set of all permutations.

.. literalinclude:: itertools_permutations.py
   :caption:
   :start-after: #end_pymotw_header

Use the ``r`` argument to limit the length and number of the
individual permutations returned.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_permutations.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_permutations.py
	
	All permutations:
	
	abcd abdc acbd acdb adbc adcb 
	bacd badc bcad bcda bdac bdca 
	cabd cadb cbad cbda cdab cdba 
	dabc dacb dbac dbca dcab dcba 
	Pairs:
	
	ab ac ad 
	ba bc bd 
	ca cb cd 
	da db dc 

.. {{{end}}}

To limit the values to unique combinations rather than permutations,
use :func:`combinations`. As long as the members of the input are
unique, the output will not include any repeated values.

.. literalinclude:: itertools_combinations.py
   :caption:
   :start-after: #end_pymotw_header

Unlike with permutations, the ``r`` argument to :func:`combinations`
is required.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_combinations.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_combinations.py
	
	Unique pairs:
	
	ab ac ad 
	bc bd 
	cd 

.. {{{end}}}

While :func:`combinations` does not repeat individual input elements,
sometimes it is useful to consider combinations that do include
repeated elements. For those cases, use
:func:`combinations_with_replacement`.

.. literalinclude:: itertools_combinations_with_replacement.py
   :caption:
   :start-after: #end_pymotw_header

In this output, each input item is paired with itself as well as all
of the other members of the input sequence.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'itertools_combinations_with_replacement.py'))
.. }}}

.. code-block:: none

	$ python3 itertools_combinations_with_replacement.py
	
	Unique pairs:
	
	aa ab ac ad 
	bb bc bd 
	cc cd 
	dd 

.. {{{end}}}



.. seealso::

   * :pydoc:`itertools`

   * :ref:`Porting notes for itertools <porting-itertools>`

   * `The Standard ML Basis Library
     <http://www.standardml.org/Basis/>`_) -- The library for SML.

   * `Definition of Haskell and the Standard Libraries
     <http://www.haskell.org/definition/>`__ -- Standard library
     specification for the functional language Haskell.

   * `Clojure <http://clojure.org/>`__ -- Clojure is a dynamic
     functional language that runs on the Java Virtual Machine.

   * `tee <http://man7.org/linux/man-pages/man1/tee.1.html>`__ -- Unix
     command line tool for splitting one input into multiple identical
     output streams.

   * `Cartesian product
     <https://en.wikipedia.org/wiki/Cartesian_product>`__ --
     Mathematical definition of the Cartesian product of two
     sequences.
