=========================================
 statistics --- Statistical Calculations
=========================================

.. module:: statistics
   :synopsis: Statistical Calculations

:Purpose: Implementations of common statistical calculations.

The ``statistics`` module implements many common statistical
formulas for efficient calculations using Python's various numerical
types (``int``, ``float``, ``Decimal``, and
``Fraction``).

Averages
========

There are three forms of averages supported, the mean, the median,
and the mode. Calculate the arithmetic mean with ``mean()``.

.. literalinclude:: statistics_mean.py
   :caption:
   :start-after: #end_pymotw_header

The return value for integers and floats is always a ``float``. For
``Decimal`` and ``Fraction`` input data, the result is of
the same type as the inputs.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'statistics_mean.py'))
.. }}}

.. code-block:: none

	$ python3 statistics_mean.py
	
	5.33

.. {{{end}}}

Calculate the most common data point in a data set using ``mode()``.

.. literalinclude:: statistics_mode.py
   :caption:
   :start-after: #end_pymotw_header

The return value is always a member of the input data set. Because
``mode()`` treats the input as a set of discrete values, and counts
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

``median()`` finds the center value, and if the data set has an even
number of values it averages the two middle items. ``median_low()``
always returns a value from the input data set, using the lower of the
two middle items for data sets with an even number of
items. ``median_high()`` similarly returns the higher of the two
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

The fourth version of the median calculation, ``median_grouped()``,
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

Variance
========

Statistics uses two values to express how disperse a set of values is
relative to the mean. The *variance* is the average of the square of
the difference of each value and the mean, and the *standard
deviation* is the square root of the variance (which is useful because
taking the square root allows the standard deviation to be expressed
in the same units as the input data). Large values for variance or
standard deviation indicate that a set of data is disperse, while
small values indicate that the data is clustered closer to the mean.

.. literalinclude:: statistics_variance.py
   :caption:
   :start-after: #end_pymotw_header

Python includes two sets of functions for computing variance and
standard deviation, depending on whether the data set represents the
entire population or a sample of the population.  This example uses
``wc`` to count the number of lines in the input files for all of the
example programs and then uses ``pvariance()`` and ``pstdev()`` to
compute the variance and standard deviation for the entire population
before using ``variance()`` and ``stddev()`` to compute the sample
variance and standard deviation for a subset created by using the
length of every second file found.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'statistics_variance.py'))
.. }}}

.. code-block:: none

	$ python3 statistics_variance.py
	
	Basic statistics:
	  count     : 959
	  min       :   4.00
	  max       : 228.00
	  mean      :  28.62
	
	Population variance:
	  pstdev    :  18.52
	  pvariance : 342.95
	
	Estimated variance for sample:
	  count     : 480
	  stdev     :  21.09
	  variance  : 444.61

.. {{{end}}}

.. seealso::

   * :pydoc:`statistics`

   * `mathtips.com: Median for Discrete and Continuous Frequency Type
     Data (grouped data)
     <http://www.mathstips.com/statistics/median-for-discrete-and-continuous-frequency-type.html>`__
     -- Discussion of median for continuous data

   * :pep:`450` -- Adding A Statistics Module To The Standard Library
