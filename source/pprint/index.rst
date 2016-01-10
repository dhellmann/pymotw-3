=========================================
 pprint --- Pretty-print Data Structures
=========================================

.. module:: pprint
    :synopsis: Pretty-print data structures

:Purpose: Pretty-print data structures

:mod:`pprint` contains a "pretty printer" for producing aesthetically
pleasing views of data structures.  The formatter produces
representations of data structures that can be parsed correctly by the
interpreter, and are also easy for a human to read. The output is kept
on a single line, if possible, and indented when split across multiple
lines.

The examples in this section all depend on ``pprint_data.py``, which
contains:

.. include:: pprint_data.py
    :literal:
    :start-after: #end_pymotw_header

Printing
========

The simplest way to use the module is through the :func:`pprint`
function. 

.. include:: pprint_pprint.py
    :literal:
    :start-after: #end_pymotw_header

:func:`pprint` formats an object and writes it to the data stream
passed as argument (or :data:`sys.stdout` by default).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pprint_pprint.py', break_lines_at=68))
.. }}}

::

	$ python3 pprint_pprint.py
	
	PRINT:
	[(1, {'c': 'C', 'b': 'B', 'd': 'D', 'a': 'A'}), (2, {'k': 'K', 'i': 
	'I', 'g': 'G', 'f': 'F', 'e': 'E', 'h': 'H', 'l': 'L', 'j': 'J'})]
	
	PPRINT:
	[(1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}),
	 (2,
	  {'e': 'E',
	   'f': 'F',
	   'g': 'G',
	   'h': 'H',
	   'i': 'I',
	   'j': 'J',
	   'k': 'K',
	   'l': 'L'})]

.. {{{end}}}

Formatting
==========

To format a data structure without writing it directly to a stream
(i.e., for logging), use :func:`pformat` to build a string
representation.

.. include:: pprint_pformat.py
    :literal:
    :start-after: #end_pymotw_header

The formatted string can then be printed or logged independently.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pprint_pformat.py'))
.. }}}

::

	$ python3 pprint_pformat.py
	
	DEBUG    Logging pformatted data
	DEBUG    [(1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}),
	DEBUG     (2,
	DEBUG      {'e': 'E',
	DEBUG       'f': 'F',
	DEBUG       'g': 'G',
	DEBUG       'h': 'H',
	DEBUG       'i': 'I',
	DEBUG       'j': 'J',
	DEBUG       'k': 'K',
	DEBUG       'l': 'L'})]

.. {{{end}}}

Arbitrary Classes
=================

The :class:`PrettyPrinter` class used by :func:`pprint` can also work
with custom classes, if they define a :func:`__repr__` method.

.. include:: pprint_arbitrary_object.py
    :literal:
    :start-after: #end_pymotw_header

The representations of the nested objects are combined by the
:class:`PrettyPrinter` to return the full string representation.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pprint_arbitrary_object.py'))
.. }}}

::

	$ python3 pprint_arbitrary_object.py
	
	[node('node-1', []),
	 node('node-2', [node('node-2-1', [])]),
	 node('node-3', [node('node-3-1', [])])]

.. {{{end}}}


Recursion
=========

Recursive data structures are represented with a reference to the
original source of the data, with the form ``<Recursion on typename
with id=number>``.

.. include:: pprint_recursion.py
    :literal:
    :start-after: #end_pymotw_header

In this example, the list :data:`local_data` is added to itself,
creating a recursive reference.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pprint_recursion.py'))
.. }}}

::

	$ python3 pprint_recursion.py
	
	id(local_data) => 4327565192
	['a', 'b', 1, 2, <Recursion on list with id=4327565192>]

.. {{{end}}}


Limiting Nested Output
======================

For very deep data structures, it may not be desirable for the output
to include all of the details. The data may not format properly, the
formatted text might be too large to manage, or some of the data may
be extraneous.  

.. include:: pprint_depth.py
    :literal:
    :start-after: #end_pymotw_header

Use the *depth* argument to control how far down into the nested data
structure the pretty printer recurses.  Levels not included in the
output are represented by ellipsis.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pprint_depth.py'))
.. }}}

::

	$ python3 pprint_depth.py
	
	[(...), (...)]

.. {{{end}}}


Controlling Output Width
========================

The default output width for the formatted text is 80 columns. To adjust that
width, use the *width* argument to :func:`pprint`.

.. include:: pprint_width.py
    :literal:
    :start-after: #end_pymotw_header

When the width is too low to accommodate the formatted data structure,
the lines are not truncated or wrapped if that would introduce invalid
syntax.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pprint_width.py'))
.. }}}

::

	$ python3 pprint_width.py
	
	WIDTH = 80
	[(1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}),
	 (2,
	  {'e': 'E',
	   'f': 'F',
	   'g': 'G',
	   'h': 'H',
	   'i': 'I',
	   'j': 'J',
	   'k': 'K',
	   'l': 'L'})]
	
	WIDTH = 5
	[(1,
	  {'a': 'A',
	   'b': 'B',
	   'c': 'C',
	   'd': 'D'}),
	 (2,
	  {'e': 'E',
	   'f': 'F',
	   'g': 'G',
	   'h': 'H',
	   'i': 'I',
	   'j': 'J',
	   'k': 'K',
	   'l': 'L'})]
	

.. {{{end}}}

.. seealso::

   * :pydoc:`pprint`
