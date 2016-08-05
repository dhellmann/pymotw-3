=========================================================
 operator --- Functional Interface to Built-in Operators
=========================================================

.. module:: operator
    :synopsis: Functional interface to built-in operators

:Purpose: Functional interface to built-in operators.

Programming using iterators occasionally requires creating small
functions for simple expressions. Sometimes, these can be implemented
as :command:`lambda` functions, but for some operations new functions
are not needed at all.  The :mod:`operator` module defines functions
that correspond to built-in operations for arithmetic, comparison, and
other operations corresponding to standard object APIs.

Logical Operations
==================

There are functions for determining the boolean equivalent for a
value, negating it to create the opposite boolean value, and
comparing objects to see if they are identical.

.. literalinclude:: operator_boolean.py
   :caption:
   :start-after: #end_pymotw_header

:func:`not_` includes the trailing underscore because :command:`not`
is a Python keyword.  :func:`truth` applies the same logic used when
testing an expression in an :command:`if` statement or converting an
expression to a :class:`bool`.  :func:`is_` implements the same check
used by the :command:`is` keyword, and :func:`is_not` does the same
test and returns the opposite answer.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'operator_boolean.py'))
.. }}}

.. code-block:: none

	$ python3 operator_boolean.py
	
	a = -1
	b = 5
	
	not_(a)     : False
	truth(a)    : True
	is_(a, b)   : False
	is_not(a, b): True

.. {{{end}}}


Comparison Operators
====================

All of the rich comparison operators are supported.

.. literalinclude:: operator_comparisons.py
   :caption:
   :start-after: #end_pymotw_header

The functions are equivalent to the expression syntax using ``<``,
``<=``, ``==``, ``>=``, and ``>``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'operator_comparisons.py'))
.. }}}

.. code-block:: none

	$ python3 operator_comparisons.py
	
	a = 1
	b = 5.0
	lt(a, b): True
	le(a, b): True
	eq(a, b): False
	ne(a, b): True
	ge(a, b): False
	gt(a, b): False

.. {{{end}}}


Arithmetic Operators
====================

The arithmetic operators for manipulating numerical values are also
supported.

.. literalinclude:: operator_math.py
   :caption:
   :start-after: #end_pymotw_header

There are two separate division operators: :func:`floordiv` (integer
division as implemented in Python before version 3.0) and
:func:`truediv` (floating point division).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'operator_math.py'))
.. }}}

.. code-block:: none

	$ python3 operator_math.py
	
	a = -1
	b = 5.0
	c = 2
	d = 6
	
	Positive/Negative:
	abs(a): 1
	neg(a): 1
	neg(b): -5.0
	pos(a): -1
	pos(b): 5.0
	
	Arithmetic:
	add(a, b)     : 4.0
	floordiv(a, b): -1.0
	floordiv(d, c): 3
	mod(a, b)     : 4.0
	mul(a, b)     : -5.0
	pow(c, d)     : 64
	sub(b, a)     : 6.0
	truediv(a, b) : -0.2
	truediv(d, c) : 3.0
	
	Bitwise:
	and_(c, d)  : 2
	invert(c)   : -3
	lshift(c, d): 128
	or_(c, d)   : 6
	rshift(d, c): 1
	xor(c, d)   : 4

.. {{{end}}}



Sequence Operators
==================

The operators for working with sequences can be divided into four
groups: building up sequences, searching for items, accessing
contents, and removing items from sequences.

.. literalinclude:: operator_sequences.py
   :caption:
   :start-after: #end_pymotw_header

Some of these operations, such as :func:`setitem` and :func:`delitem`,
modify the sequence in place and do not return a value.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'operator_sequences.py'))
.. }}}

.. code-block:: none

	$ python3 operator_sequences.py
	
	a = [1, 2, 3]
	b = ['a', 'b', 'c']
	
	Constructive:
	  concat(a, b): [1, 2, 3, 'a', 'b', 'c']
	
	Searching:
	  contains(a, 1)  : True
	  contains(b, "d"): False
	  countOf(a, 1)   : 1
	  countOf(b, "d") : 0
	  indexOf(a, 5)   : 0
	
	Access Items:
	  getitem(b, 1)                  : b
	  getitem(b, slice(1, 3))        : ['b', 'c']
	  setitem(b, 1, "d")             : ['a', 'd', 'c']
	  setitem(a, slice(1, 3), [4, 5]): [1, 4, 5]
	
	Destructive:
	  delitem(b, 1)          : ['a', 'c']
	  delitem(a, slice(1, 3)): [1]

.. {{{end}}}

In-place Operators
==================

In addition to the standard operators, many types of objects support
"in-place" modification through special operators such as
``+=``. There are equivalent functions for in-place modifications,
too:

.. literalinclude:: operator_inplace.py
   :caption:
   :start-after: #end_pymotw_header

These examples only demonstrate a few of the functions. Refer to
the standard library documentation for complete details.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'operator_inplace.py'))
.. }}}

.. code-block:: none

	$ python3 operator_inplace.py
	
	a = -1
	b = 5.0
	c = [1, 2, 3]
	d = ['a', 'b', 'c']
	
	a = iadd(a, b) => 4.0
	
	c = iconcat(c, d) => [1, 2, 3, 'a', 'b', 'c']

.. {{{end}}}

Attribute and Item "Getters"
============================

One of the most unusual features of the :mod:`operator` module is the
concept of *getters*. These are callable objects constructed at
runtime to retrieve attributes of objects or contents from
sequences. Getters are especially useful when working with iterators
or generator sequences, where they are intended to incur less overhead
than a :command:`lambda` or Python function.

.. literalinclude:: operator_attrgetter.py
   :caption:
   :start-after: #end_pymotw_header

Attribute getters work like ``lambda x, n='attrname': getattr(x, n)``:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'operator_attrgetter.py'))
.. }}}

.. code-block:: none

	$ python3 operator_attrgetter.py
	
	objects   : [MyObj(0), MyObj(1), MyObj(2), MyObj(3), MyObj(4)]
	arg values: [0, 1, 2, 3, 4]
	reversed  : [MyObj(4), MyObj(3), MyObj(2), MyObj(1), MyObj(0)]
	sorted    : [MyObj(0), MyObj(1), MyObj(2), MyObj(3), MyObj(4)]

.. {{{end}}}

Item getters work like ``lambda x, y=5: x[y]``:

.. literalinclude:: operator_itemgetter.py
   :caption:
   :start-after: #end_pymotw_header

Item getters work with mappings as well as sequences.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'operator_itemgetter.py'))
.. }}}

.. code-block:: none

	$ python3 operator_itemgetter.py
	
	Dictionaries:
	 original: [{'val': 0}, {'val': -1}, {'val': -2}, {'val': -3}]
	   values: [0, -1, -2, -3]
	   sorted: [{'val': -3}, {'val': -2}, {'val': -1}, {'val': 0}]
	
	Tuples:
	 original: [(0, 0), (1, -2), (2, -4), (3, -6)]
	   values: [0, -2, -4, -6]
	   sorted: [(3, -6), (2, -4), (1, -2), (0, 0)]

.. {{{end}}}

Combining Operators and Custom Classes
======================================

The functions in the :mod:`operator` module work via the standard
Python interfaces for their operations, so they work with user-defined
classes as well as the built-in types.

.. literalinclude:: operator_classes.py
   :caption:
   :start-after: #end_pymotw_header

Refer to the Python reference guide for a complete list of the special
methods used by each operator.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'operator_classes.py'))
.. }}}

.. code-block:: none

	$ python3 operator_classes.py
	
	Comparison:
	Testing MyObj(1) < MyObj(2)
	True
	
	Arithmetic:
	Adding MyObj(1) + MyObj(2)
	MyObj(3)

.. {{{end}}}


.. seealso::

   * :pydoc:`operator`

   * :mod:`functools` -- Functional programming tools, including the
     :func:`total_ordering` decorator for adding rich comparison
     methods to a class.

   * :mod:`itertools` -- Iterator operations.

   * :mod:`collections` -- Abstract types for collections.

   * :mod:`numbers` -- Abstract types for numerical values.

    ..
       :mod:`abc`
         The ``abc`` module includes :ref:`abstract base classes
         <abc-collection-types>` that define the APIs for collection
         types.
