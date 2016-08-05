Logical Operations
==================

There are functions for determining the boolean equivalent for a
value, negating it to create the opposite boolean value, and
comparing objects to see if they are identical.

.. include:: operator_boolean.py
    :literal:
    :start-after: #end_pymotw_header

:func:`not_` includes the trailing underscore because :command:`not`
is a Python keyword.  :func:`truth` applies the same logic used when
testing an expression in an :command:`if` statement.  :func:`is_`
implements the same check used by the :command:`is` keyword, and
:func:`is_not` does the same test and returns the opposite answer.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'operator_boolean.py'))
.. }}}

::

	$ python operator_boolean.py
	
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

.. include:: operator_comparisons.py
    :literal:
    :start-after: #end_pymotw_header

The functions are equivalent to the expression syntax using ``<``,
``<=``, ``==``, ``>=``, and ``>``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'operator_comparisons.py'))
.. }}}

::

	$ python operator_comparisons.py
	
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

The arithmetic operators for manipulating numerical values are also supported.

.. include:: operator_math.py
    :literal:
    :start-after: #end_pymotw_header

There are two separate division operators: :func:`floordiv` (integer
division as implemented in Python before version 3.0) and
:func:`truediv` (floating point division).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'operator_math.py'))
.. }}}

::

	$ python operator_math.py
	
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
	div(a, b)     : -0.2
	div(d, c)     : 3
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

.. include:: operator_sequences.py
    :literal:
    :start-after: #end_pymotw_header

Some of these operations, such as :func:`setitem` and :func:`delitem`,
modify the sequence in place and do not return a value.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'operator_sequences.py'))
.. }}}

::

	$ python operator_sequences.py
	
	a = [1, 2, 3]
	b = ['a', 'b', 'c']
	
	Constructive:
	  concat(a, b): [1, 2, 3, 'a', 'b', 'c']
	  repeat(a, 3): [1, 2, 3, 1, 2, 3, 1, 2, 3]
	
	Searching:
	  contains(a, 1)  : True
	  contains(b, "d"): False
	  countOf(a, 1)   : 1
	  countOf(b, "d") : 0
	  indexOf(a, 5)   : 0
	
	Access Items:
	  getitem(b, 1)            : b
	  getslice(a, 1, 3)        : [2, 3]
	  setitem(b, 1, "d")       : None , after b = ['a', 'd', 'c']
	  setslice(a, 1, 3, [4, 5]): None , after a = [1, 4, 5]
	
	Destructive:
	  delitem(b, 1)    : None , after b = ['a', 'c']
	  delslice(a, 1, 3): None , after a = [1]

.. {{{end}}}



In-place Operators
==================

In addition to the standard operators, many types of objects support
"in-place" modification through special operators such as ``+=``. There are
equivalent functions for in-place modifications, too:

.. include:: operator_inplace.py
    :literal:
    :start-after: #end_pymotw_header

These examples only demonstrate a few of the functions. Refer to
the standard library documentation for complete details.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'operator_inplace.py'))
.. }}}

::

	$ python operator_inplace.py
	
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

.. include:: operator_attrgetter.py
    :literal:
    :start-after: #end_pymotw_header

Attribute getters work like ``lambda x, n='attrname': getattr(x, n)``:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'operator_attrgetter.py'))
.. }}}

::

	$ python operator_attrgetter.py
	
	objects   : [MyObj(0), MyObj(1), MyObj(2), MyObj(3), MyObj(4)]
	arg values: [0, 1, 2, 3, 4]
	reversed  : [MyObj(4), MyObj(3), MyObj(2), MyObj(1), MyObj(0)]
	sorted    : [MyObj(0), MyObj(1), MyObj(2), MyObj(3), MyObj(4)]

.. {{{end}}}

Item getters work like ``lambda x, y=5: x[y]``:

.. include:: operator_itemgetter.py
    :literal:
    :start-after: #end_pymotw_header

Item getters work with mappings as well as sequences.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'operator_itemgetter.py'))
.. }}}

::

	$ python operator_itemgetter.py
	
	Dictionaries: [{'val': 0}, {'val': -1}, {'val': -2}, {'val': -3}]
	      values: [0, -1, -2, -3]
	      sorted: [{'val': -3}, {'val': -2}, {'val': -1}, {'val': 0}]
	
	Tuples      : [(0, 0), (1, -2), (2, -4), (3, -6)]
	      values: [0, -2, -4, -6]
	      sorted: [(3, -6), (2, -4), (1, -2), (0, 0)]

.. {{{end}}}



Combining Operators and Custom Classes
======================================

The functions in the :mod:`operator` module work via the standard
Python interfaces for their operations, so they work with user-defined
classes as well as the built-in types.

.. include:: operator_classes.py
    :literal:
    :start-after: #end_pymotw_header

Refer to the Python reference guide for a complete list of the special
methods used by each operator.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'operator_classes.py'))
.. }}}

::

	$ python operator_classes.py
	
	Comparison:
	Testing MyObj(1) < MyObj(2)
	True
	
	Arithmetic:
	Adding MyObj(1) + MyObj(2)
	MyObj(3)

.. {{{end}}}
