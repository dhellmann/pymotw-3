======================================
pprint -- Pretty-print data structures
======================================

.. module:: pprint
    :synopsis: Pretty-print data structures

:Purpose: Pretty-print data structures
:Available In: 1.4

:mod:`pprint` contains a "pretty printer" for producing aesthetically
pleasing representations of your data structures.  The formatter
produces representations of data structures that can be parsed
correctly by the interpreter, and are also easy for a human to
read. The output is kept on a single line, if possible, and indented
when split across multiple lines.

The examples below all depend on ``pprint_data.py``, which contains:

.. include:: pprint_data.py
    :literal:
    :start-after: #end_pymotw_header

Printing
========

The simplest way to use the module is through the ``pprint()``
function. It formats your object and writes it to the data stream
passed as argument (or :ref:`sys.stdout <sys-input-output>` by
default).

.. include:: pprint_pprint.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pprint_pprint.py'))
.. }}}

::

	$ python pprint_pprint.py
	
	PRINT:
	[(0, {'a': 'A', 'c': 'C', 'b': 'B', 'e': 'E', 'd': 'D', 'g': 'G', 'f': 'F', 'h': 'H'}), (1, {'a': 'A', 'c': 'C', 'b': 'B', 'e': 'E', 'd': 'D', 'g': 'G', 'f': 'F', 'h': 'H'}), (2, {'a': 'A', 'c': 'C', 'b': 'B', 'e': 'E', 'd': 'D', 'g': 'G', 'f': 'F', 'h': 'H'})]
	
	PPRINT:
	[(0,
	  {'a': 'A',
	   'b': 'B',
	   'c': 'C',
	   'd': 'D',
	   'e': 'E',
	   'f': 'F',
	   'g': 'G',
	   'h': 'H'}),
	 (1,
	  {'a': 'A',
	   'b': 'B',
	   'c': 'C',
	   'd': 'D',
	   'e': 'E',
	   'f': 'F',
	   'g': 'G',
	   'h': 'H'}),
	 (2,
	  {'a': 'A',
	   'b': 'B',
	   'c': 'C',
	   'd': 'D',
	   'e': 'E',
	   'f': 'F',
	   'g': 'G',
	   'h': 'H'})]

.. {{{end}}}

Formatting
==========

If you need to format a data structure, but do not want to write it
directly to a stream (for logging purposes, for example) you can use
``pformat()`` to build a string representation that can then be passed
to another function.

.. include:: pprint_pformat.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pprint_pformat.py'))
.. }}}

::

	$ python pprint_pformat.py
	
	DEBUG    Logging pformatted data
	DEBUG    [(0,
	  {'a': 'A',
	   'b': 'B',
	   'c': 'C',
	   'd': 'D',
	   'e': 'E',
	   'f': 'F',
	   'g': 'G',
	   'h': 'H'}),
	 (1,
	  {'a': 'A',
	   'b': 'B',
	   'c': 'C',
	   'd': 'D',
	   'e': 'E',
	   'f': 'F',
	   'g': 'G',
	   'h': 'H'}),
	 (2,
	  {'a': 'A',
	   'b': 'B',
	   'c': 'C',
	   'd': 'D',
	   'e': 'E',
	   'f': 'F',
	   'g': 'G',
	   'h': 'H'})]

.. {{{end}}}

Arbitrary Classes
=================

The ``PrettyPrinter`` class used by ``pprint()`` can also work with
your own classes, if they define a ``__repr__()`` method.

.. include:: pprint_arbitrary_object.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pprint_arbitrary_object.py'))
.. }}}

::

	$ python pprint_arbitrary_object.py
	
	[node('node-1', []),
	 node('node-2', [node('node-2-1', [])]),
	 node('node-3', [node('node-3-1', [])])]

.. {{{end}}}


Recursion
=========

Recursive data structures are represented with a reference to the original
source of the data, with the form ``<Recursion on typename with id=number>``. For
example:

.. include:: pprint_recursion.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pprint_recursion.py'))
.. }}}

::

	$ python pprint_recursion.py
	
	id(local_data) => 4299545560
	['a', 'b', 1, 2, <Recursion on list with id=4299545560>]

.. {{{end}}}


Limiting Nested Output
======================

For very deep data structures, you may not want the output to include all of
the details. It might be impossible to format the data properly, the formatted
text might be too large to manage, or you may need all of it. In that case,
the depth argument can control how far down into the nested data structure the
pretty printer goes.

.. include:: pprint_depth.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pprint_depth.py'))
.. }}}

::

	$ python pprint_depth.py
	
	[(...), (...), (...)]

.. {{{end}}}


Controlling Output Width
========================

The default output width for the formatted text is 80 columns. To adjust that
width, use the width argument to ``pprint()``.

.. include:: pprint_width.py
    :literal:
    :start-after: #end_pymotw_header


Notice that when the width is too low to accommodate the formatted data
structure, the lines are not truncated or wrapped if that would introduce
invalid syntax.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pprint_width.py'))
.. }}}

::

	$ python pprint_width.py
	
	WIDTH = 80
	[(0, {'a': 'A', 'b': 'B', 'c': 'C'}),
	 (1, {'a': 'A', 'b': 'B', 'c': 'C'}),
	 (2, {'a': 'A', 'b': 'B', 'c': 'C'})]
	
	WIDTH = 20
	[(0,
	  {'a': 'A',
	   'b': 'B',
	   'c': 'C'}),
	 (1,
	  {'a': 'A',
	   'b': 'B',
	   'c': 'C'}),
	 (2,
	  {'a': 'A',
	   'b': 'B',
	   'c': 'C'})]
	
	WIDTH = 5
	[(0,
	  {'a': 'A',
	   'b': 'B',
	   'c': 'C'}),
	 (1,
	  {'a': 'A',
	   'b': 'B',
	   'c': 'C'}),
	 (2,
	  {'a': 'A',
	   'b': 'B',
	   'c': 'C'})]
	

.. {{{end}}}

.. seealso::

    `pprint <https://docs.python.org/2/library/pprint.html>`_
        Standard library documentation for this module.
