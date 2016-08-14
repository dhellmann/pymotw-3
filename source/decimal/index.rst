==========================================
 decimal -- Fixed and Floating Point Math
==========================================

.. module:: decimal
    :synopsis: Fixed and floating point math

:Purpose: Decimal arithmetic using fixed and floating point numbers
:Python Version: 2.4 and later

The :mod:`decimal` module implements fixed and floating point
arithmetic using the model familiar to most people, rather than the
IEEE floating point version implemented by most computer hardware and
familiar to programmers.  A :class:`Decimal` instance can represent
any number exactly, round up or down, and apply a limit to the number
of significant digits.

Decimal
=======

Decimal values are represented as instances of the :class:`Decimal`
class.  The constructor takes as argument one integer or string.
Floating point numbers can be converted to a string before being used
to create a :class:`Decimal`, letting the caller explicitly deal with
the number of digits for values that cannot be expressed exactly using
hardware floating point representations.  Alternately, the class
method :func:`from_float` converts to the exact decimal
representation.

.. include:: decimal_create.py
    :literal:
    :start-after: #end_pymotw_header

The floating point value of ``0.1`` is not represented as an exact
value in binary, so the representation as a :class:`float` is
different from the :class:`Decimal` value.  It is truncated to 25
characters in this output.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'decimal_create.py'))
.. }}}

::

	$ python decimal_create.py
	
	Input                     Output                   
	------------------------- -------------------------
	5                         5                        
	3.14                      3.14                     
	0.1                       0.1                      
	0.10000000000000000555112 0.10000000000000000555111

.. {{{end}}}

:class:`Decimals` can also be created from tuples
containing a sign flag (``0`` for positive, ``1`` for negative), a
:class:`tuple` of digits, and an integer exponent.

.. include:: decimal_tuple.py
    :literal:
    :start-after: #end_pymotw_header

The tuple-based representation is less convenient to create, but does
offer a portable way of exporting decimal values without losing
precision.  The tuple form can be transmitted through the network or
stored in a database that does not support accurate decimal values,
then turned back into a :class:`Decimal` instance later.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'decimal_tuple.py'))
.. }}}

::

	$ python decimal_tuple.py
	
	Input  : (1, (1, 1), -2)
	Decimal: -0.11

.. {{{end}}}


Arithmetic
==========

:class:`Decimal` overloads the simple arithmetic operators so
instances can be manipulated in much the same way as the built-in
numeric types.

.. include:: decimal_operators.py
    :literal:
    :start-after: #end_pymotw_header

:class:`Decimal` operators also accept integer arguments, but floating
point values must be converted to :class:`Decimal` instances.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'decimal_operators.py'))
.. }}}

::

	$ python decimal_operators.py
	
	a     = Decimal('5.1')
	b     = Decimal('3.14')
	c     = 4
	d     = 3.14
	
	a + b = 8.24
	a - b = 1.96
	a * b = 16.014
	a / b = 1.624203821656050955414012739
	
	a + c = 9.1
	a - c = 1.1
	a * c = 20.4
	a / c = 1.275
	
	a + d = unsupported operand type(s) for +: 'Decimal' and 'float'

.. {{{end}}}


Beyond basic arithmetic, :class:`Decimal` includes the methods to find
the base 10 and natural logarithms.  The return values from
:func:`log10` and :func:`ln` are :class:`Decimal` instances, so they
can be used directly in formulas with other values.

Special Values
==============

In addition to the expected numerical values, :class:`Decimal` can
represent several special values, including positive and negative
values for infinity, "not a number", and zero.

.. include:: decimal_special.py
    :literal:
    :start-after: #end_pymotw_header

Adding to infinite values returns another infinite value.  Comparing
for equality with :const:`NaN` always returns false and comparing for
inequality always returns true.  Comparing for sort order against
:const:`NaN` is undefined and results in an error.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'decimal_special.py'))
.. }}}

::

	$ python decimal_special.py
	
	Infinity -Infinity
	NaN -NaN
	0 -0
	
	Infinity + 1: Infinity
	-Infinity + 1: -Infinity
	False
	True

.. {{{end}}}


Context
=======

So far, all of the examples have used the default behaviors of the
:mod:`decimal` module. It is possible to override settings such as the
precision maintained, how rounding is performed, error handling,
etc. by using a *context*.  Contexts can be applied for all
:class:`Decimal` instances in a thread or locally within a small code
region.

Current Context
---------------

To retrieve the current global context, use ``getcontext()``.

.. include:: decimal_getcontext.py
    :literal:
    :start-after: #end_pymotw_header

This example script shows the public properties of a :class:`Context`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'decimal_getcontext.py', break_lines_at=76))
.. }}}

::

	$ python decimal_getcontext.py
	
	Emax     = 999999999
	Emin     = -999999999
	capitals = 1
	prec     = 28
	rounding = ROUND_HALF_EVEN
	flags    =
	{<class 'decimal.Clamped'>: 0,
	 <class 'decimal.InvalidOperation'>: 0,
	 <class 'decimal.DivisionByZero'>: 0,
	 <class 'decimal.Inexact'>: 0,
	 <class 'decimal.Rounded'>: 0,
	 <class 'decimal.Subnormal'>: 0,
	 <class 'decimal.Overflow'>: 0,
	 <class 'decimal.Underflow'>: 0}
	traps    =
	{<class 'decimal.Clamped'>: 0,
	 <class 'decimal.InvalidOperation'>: 1,
	 <class 'decimal.DivisionByZero'>: 1,
	 <class 'decimal.Inexact'>: 0,
	 <class 'decimal.Rounded'>: 0,
	 <class 'decimal.Subnormal'>: 0,
	 <class 'decimal.Overflow'>: 1,
	 <class 'decimal.Underflow'>: 0}

.. {{{end}}}


Precision
---------

The :attr:`prec` attribute of the context controls the precision maintained
for new values created as a result of arithmetic.  Literal values are
maintained as described.

.. include:: decimal_precision.py
    :literal:
    :start-after: #end_pymotw_header

To change the precision, assign a new value directly to the attribute.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'decimal_precision.py'))
.. }}}

::

	$ python decimal_precision.py
	
	0 : 0.123456 0
	1 : 0.123456 0.1
	2 : 0.123456 0.12
	3 : 0.123456 0.123

.. {{{end}}}


Rounding
--------

There are several options for rounding to keep values within the
desired precision.

:const:`ROUND_CEILING`  
  Always round upwards towards infinity.

:const:`ROUND_DOWN`
  Always round toward zero.

:const:`ROUND_FLOOR`
  Always round down towards negative infinity.

:const:`ROUND_HALF_DOWN`
  Rounds away from zero if the last significant digit is greater than
  or equal to 5, otherwise toward zero.

:const:`ROUND_HALF_EVEN`
  Like :const:`ROUND_HALF_DOWN` except that if the value is 5 then the
  preceding digit is examined.  Even values cause the result to be
  rounded down and odd digits cause the result to be rounded up.

:const:`ROUND_HALF_UP`
  Like :const:`ROUND_HALF_DOWN` except if the last significant digit
  is 5 the value is rounded away from zero.

:const:`ROUND_UP`
  Round away from zero.

:const:`ROUND_05UP`
  Round away from zero if the last digit is ``0`` or ``5``, otherwise
  towards zero.

.. include:: decimal_rounding.py
    :literal:
    :start-after: #end_pymotw_header

This program shows the effect of rounding the same value to different
levels of precision using the different algorithms.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'decimal_rounding.py'))
.. }}}

::

	$ python decimal_rounding.py
	
	           1/8 (1)  -1/8 (1) 1/8 (2)  -1/8 (2) 1/8 (3)  -1/8 (3)
	CEILING      0.2      -0.1     0.13    -0.12    0.125    -0.125 
	DOWN         0.1      -0.1     0.12    -0.12    0.125    -0.125 
	FLOOR        0.1      -0.2     0.12    -0.13    0.125    -0.125 
	HALF_DOWN    0.1      -0.1     0.12    -0.12    0.125    -0.125 
	HALF_EVEN    0.1      -0.1     0.12    -0.12    0.125    -0.125 
	HALF_UP      0.1      -0.1     0.13    -0.13    0.125    -0.125 
	UP           0.2      -0.2     0.13    -0.13    0.125    -0.125 
	05UP         0.1      -0.1     0.12    -0.12    0.125    -0.125 

.. {{{end}}}

Local Context
-------------

Using Python 2.5 or later, the context can be applied to a block of
code using the :command:`with` statement.

.. include:: decimal_context_manager.py
    :literal:
    :start-after: #end_pymotw_header

The :class:`Context` supports the context manager API used by
:command:`with`, so the settings only apply within the block.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'decimal_context_manager.py'))
.. }}}

::

	$ python decimal_context_manager.py
	
	Local precision: 2
	3.14 / 3 = 1.0
	
	Default precision: 28
	3.14 / 3 = 1.046666666666666666666666667

.. {{{end}}}

Per-Instance Context
--------------------

Contexts also can be used to construct :class:`Decimal` instances, which
then inherit the precision and rounding arguments to the conversion
from the context.

.. include:: decimal_instance_context.py
    :literal:
    :start-after: #end_pymotw_header

This lets an application select the precision of constant values
separately from the precision of user data, for example.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'decimal_instance_context.py'))
.. }}}

::

	$ python decimal_instance_context.py
	
	PI    : 3.14
	RESULT: 6.3114

.. {{{end}}}


Threads
-------

The "global" context is actually thread-local, so each thread can
potentially be configured using different values.

.. include:: decimal_thread_context.py
    :literal:
    :start-after: #end_pymotw_header

This example creates a new context using the specified, then installs
it within each thread.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'decimal_thread_context.py'))
.. }}}

::

	$ python decimal_thread_context.py
	
	1 	4
	2 	3.9
	3 	3.87
	4 	3.875
	5 	3.8748

.. {{{end}}}


.. seealso::

    `decimal <http://docs.python.org/library/decimal.html>`_
        The standard library documentation for this module.

    `Wikipedia: Floating Point <http://en.wikipedia.org/wiki/Floating_point>`_
        Article on floating point representations and arithmetic.

    `Floating Point Arithmetic: Issues and Limitations <http://docs.python.org/tutorial/floatingpoint.html>`__
        Article from the Python tutorial describing floating point math representation issues.
