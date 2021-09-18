=============================
fractions -- Rational Numbers
=============================

.. module:: fractions
    :synopsis: Implements a class for working with rational numbers.

:Purpose: Implements a class for working with rational numbers.
:Available In: 2.6 and later

The Fraction class implements numerical operations for rational numbers based on the API defined by :class:`Rational` in :mod:`numbers`.

Creating Fraction Instances
===========================

As with :mod:`decimal`, new values can be created in several ways.  One easy way is to create them from separate numerator and denominator values:

.. include:: fractions_create_integers.py
    :literal:
    :start-after: #end_pymotw_header

The lowest common denominator is maintained as new values are computed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fractions_create_integers.py'))
.. }}}

::

	$ python fractions_create_integers.py
	
	1/2 = 1/2
	2/4 = 1/2
	3/6 = 1/2

.. {{{end}}}

Another way to create a Fraction is using a string representation of ``<numerator> / <denominator>``:

.. include:: fractions_create_strings.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fractions_create_strings.py'))
.. }}}

::

	$ python fractions_create_strings.py
	
	1/2 = 1/2
	2/4 = 1/2
	3/6 = 1/2

.. {{{end}}}

Strings can also use the more usual decimal or floating point notation of ``[<digits>].[<digits>]``.

.. include:: fractions_create_strings_floats.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fractions_create_strings_floats.py'))
.. }}}

::

	$ python fractions_create_strings_floats.py
	
	0.5 = 1/2
	1.5 = 3/2
	2.0 = 2

.. {{{end}}}

There are class methods for creating Fraction instances directly from other representations of rational values such as float or :mod:`decimal`.

.. include:: fractions_from_float.py
    :literal:
    :start-after: #end_pymotw_header

Notice that for floating point values that cannot be expressed exactly the rational representation may yield unexpected results.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fractions_from_float.py'))
.. }}}

::

	$ python fractions_from_float.py
	
	0.1 = 3602879701896397/36028797018963968
	0.5 = 1/2
	1.5 = 3/2
	2.0 = 2

.. {{{end}}}

Using :mod:`decimal` representations of the values gives the expected results.

.. include:: fractions_from_decimal.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fractions_from_decimal.py'))
.. }}}

::

	$ python fractions_from_decimal.py
	
	0.1 = 1/10
	0.5 = 1/2
	1.5 = 3/2
	2.0 = 2

.. {{{end}}}



Arithmetic
==========

Once the fractions are instantiated, they can be used in mathematical expressions as you would expect.

.. include:: fractions_arithmetic.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fractions_arithmetic.py'))
.. }}}

::

	$ python fractions_arithmetic.py
	
	1/2 + 3/4 = 5/4
	1/2 - 3/4 = -1/4
	1/2 * 3/4 = 3/8
	1/2 / 3/4 = 2/3

.. {{{end}}}

Approximating Values
====================

A useful feature of Fraction is the ability to convert a floating point number to an approximate rational value by limiting the size of the denominator.

.. include:: fractions_limit_denominator.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fractions_limit_denominator.py'))
.. }}}

::

	$ python fractions_limit_denominator.py
	
	PI       = 3.14159265359
	No limit = 314159265359/100000000000
	       1 = 3
	       6 = 19/6
	      11 = 22/7
	      16 = 22/7
	      21 = 22/7
	      26 = 22/7
	      31 = 22/7
	      36 = 22/7
	      41 = 22/7
	      46 = 22/7
	      51 = 22/7
	      56 = 22/7
	      61 = 179/57
	      66 = 201/64
	      71 = 223/71
	      76 = 223/71
	      81 = 245/78
	      86 = 267/85
	      91 = 267/85
	      96 = 289/92

.. {{{end}}}


.. seealso::

    `fractions <http://docs.python.org/2.7/library/fractions.html>`_
        The standard library documentation for this module.

    :mod:`decimal`
        The decimal module provides an API for fixed and floating point math.

    :mod:`numbers`
        Numeric abstract base classes.
