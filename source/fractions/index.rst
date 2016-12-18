================================
 fractions --- Rational Numbers
================================

.. module:: fractions
    :synopsis: Implements a class for working with rational numbers.

The ``Fraction`` class implements numerical operations for
rational numbers based on the API defined by ``Rational`` in
the :mod:`numbers` module.

Creating Fraction Instances
===========================

As with the :mod:`decimal` module, new values can be created in
several ways.  One easy way is to create them from separate numerator
and denominator values:

.. literalinclude:: fractions_create_integers.py
    :caption:
    :start-after: #end_pymotw_header

The lowest common denominator is maintained as new values are
computed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fractions_create_integers.py'))
.. }}}

.. code-block:: none

	$ python3 fractions_create_integers.py
	
	1/2 = 1/2
	2/4 = 1/2
	3/6 = 1/2

.. {{{end}}}

Another way to create a ``Fraction`` is using a string representation of
``<numerator> / <denominator>``:

.. literalinclude:: fractions_create_strings.py
    :caption:
    :start-after: #end_pymotw_header 

The string is parsed to find the numerator and denominator values.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fractions_create_strings.py'))
.. }}}

.. code-block:: none

	$ python3 fractions_create_strings.py
	
	1/2 = 1/2
	2/4 = 1/2
	3/6 = 1/2

.. {{{end}}}

Strings can also use the more usual decimal or floating point notation
of series of digits separated by a period. Any string that can be
parsed by ``float()`` and that does not represent "not a number"
(``NaN``) or an infinite value is supported.

.. literalinclude:: fractions_create_strings_floats.py
    :caption:
    :start-after: #end_pymotw_header

The numerator and denominator values represented by the floating point
value is computed automatically.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fractions_create_strings_floats.py'))
.. }}}

.. code-block:: none

	$ python3 fractions_create_strings_floats.py
	
	 0.5 = 1/2
	 1.5 = 3/2
	 2.0 = 2
	5e-1 = 1/2

.. {{{end}}}

It is also possible to create ``Fraction`` instances directly
from other representations of rational values, such as ``float``
or ``Decimal``.

.. literalinclude:: fractions_from_float.py
    :caption:
    :start-after: #end_pymotw_header

Floating point values that cannot be expressed exactly may yield
unexpected results.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fractions_from_float.py'))
.. }}}

.. code-block:: none

	$ python3 fractions_from_float.py
	
	0.1 = 3602879701896397/36028797018963968
	0.5 = 1/2
	1.5 = 3/2
	2.0 = 2

.. {{{end}}}

Using :mod:`decimal` representations of the values gives the expected
results.

.. literalinclude:: fractions_from_decimal.py
    :caption:
    :start-after: #end_pymotw_header

The internal implementation of the :mod:`decimal` does not suffer from
the precision errors of the standard floating point representation.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fractions_from_decimal.py'))
.. }}}

.. code-block:: none

	$ python3 fractions_from_decimal.py
	
	0.1 = 1/10
	0.5 = 1/2
	1.5 = 3/2
	2.0 = 2

.. {{{end}}}



Arithmetic
==========

Once the fractions are instantiated, they can be used in mathematical
expressions.

.. literalinclude:: fractions_arithmetic.py
    :caption:
    :start-after: #end_pymotw_header

All of the standard operators are supported.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fractions_arithmetic.py'))
.. }}}

.. code-block:: none

	$ python3 fractions_arithmetic.py
	
	1/2 + 3/4 = 5/4
	1/2 - 3/4 = -1/4
	1/2 * 3/4 = 3/8
	1/2 / 3/4 = 2/3

.. {{{end}}}

Approximating Values
====================

A useful feature of ``Fraction`` is the ability to convert a floating
point number to an approximate rational value.

.. literalinclude:: fractions_limit_denominator.py
    :caption:
    :start-after: #end_pymotw_header

The value of the fraction can be controlled by limiting the size of
the denominator.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fractions_limit_denominator.py'))
.. }}}

.. code-block:: none

	$ python3 fractions_limit_denominator.py
	
	PI       = 3.141592653589793
	No limit = 3141592653589793/1000000000000000
	       1 = 3
	       6 = 19/6
	      11 = 22/7
	      60 = 179/57
	      70 = 201/64
	      90 = 267/85
	     100 = 311/99

.. {{{end}}}


.. seealso::

    * :pydoc:`fractions`

    * :mod:`decimal` -- The ``decimal`` module provides an API for
      fixed and floating point math.

    * :mod:`numbers` -- Numeric abstract base classes.

    * :ref:`Porting notes for fractions <porting-fractions>`
