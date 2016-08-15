=========================================
 statistics --- Statistical Calculations
=========================================

.. module:: statistics
   :synopsis: Statistical Calculations

:Purpose: Implementations of common statistical calculations.

The :mod:`statistics` module implements many common statistical
formulas for efficient calculations using Python's various numerical
types (:class:`int`, :class:`float`, :class:`Decimal`, and
:class:`Fraction`).

Averages
========

There are three forms of "averages" supported, the mean, the median,
and the mode. Calculate the arithmetic mean with :func:`mean`.

.. literalinclude:: statistics_mean.py
   :caption:
   :start-after: #end_pymotw_header

The return value for integers and floats is always a float. For
:class:`Decimal` and :class:`Fraction` input data, the result is of
the same type as the inputs.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'statistics_mean.py'))
.. }}}

.. code-block:: none

	$ python3 statistics_mean.py
	
	5.33

.. {{{end}}}

Calculate the most common data point in a data set using :func:`mode`.

.. literalinclude:: statistics_mode.py
   :caption:
   :start-after: #end_pymotw_header

The return value is always a member of the input data set. Because
:func:`mode` treats the input as a set of discrete values, and counts
the recurrences, the inputs do not actually need to be numerical
values.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'statistics_mode.py'))
.. }}}

.. code-block:: none

	$ python3 statistics_mode.py
	
	2

.. {{{end}}}

There are four variations for calculating the median, or middle,
value. The first three are straightforward versions of the usual
algorithm, with different solutions for handling data sets with an
even number of elements.

.. literalinclude:: statistics_median.py
   :caption:
   :start-after: #end_pymotw_header

:func:`median` finds the center value, and if the data set has an even
number of values it averages the two middle items. :func:`median_low`
always returns a value from the input data set, using the lower of the
two middle items for data sets with an even number of
items. :func:`median_high` similarly returns the higher of the two
middle items.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'statistics_median.py'))
.. }}}

.. code-block:: none

	$ python3 statistics_median.py
	
	median     : 3.50
	low        : 2.00
	high       : 5.00

.. {{{end}}}

The fourth version of the median calculation, :func:`median_grouped`,
treats the inputs as continuous data and calculates the 50% percentile
median by first finding the median range using the provided interval
width and then interpolating within that range using the position of
the actual value(s) from the data set that fall in that range.

.. literalinclude:: statistics_median_grouped.py
   :caption:
   :start-after: #end_pymotw_header

As the interval width increases, the median computed for the same data
set changes.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'statistics_median_grouped.py'))
.. }}}

.. code-block:: none

	$ python3 statistics_median_grouped.py
	
	1: 29.50
	2: 29.00
	3: 28.50

.. {{{end}}}

Spread
======

.. pstdev
.. pvariance
.. stdev
.. variance
