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

.. median
.. median_low
.. median_high
.. median_grouped

Spread
======

.. pstdev
.. pvariance
.. stdev
.. variance
