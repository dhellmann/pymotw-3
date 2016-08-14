================================
 math -- Mathematical Functions
================================

.. module:: math
    :synopsis: Mathematical functions

:Purpose: Provides functions for specialized mathematical operations.
:Python Version: 1.4 and later

The :mod:`math` module implements many of the IEEE functions that would
normally be found in the native platform C libraries for complex
mathematical operations using floating point values, including
logarithms and trigonometric operations.

Special Constants
=================
Many math operations depend on special constants.  :mod:`math`
includes values for π (pi) and e.

.. include:: math_constants.py
   :literal:
   :start-after: #end_pymotw_header

Both values are limited in precision only by the platform's floating
point C library.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_constants.py'))
.. }}}

::

	$ python math_constants.py

	π: 3.141592653589793115997963468544
	e: 2.718281828459045090795598298428

.. {{{end}}}

Testing for Exceptional Values
==============================

Floating point calculations can result in two types of exceptional
values.  The first of these, ``INF`` (infinity), appears when the
*double* used to hold a floating point value overflows from a value
with a large absolute value.

.. include:: math_isinf.py
   :literal:
   :start-after: #end_pymotw_header

When the exponent in this example grows large enough, the square of
*x* no longer fits inside a *double*, and the value is recorded as
infinite.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_isinf.py'))
.. }}}

::

	$ python math_isinf.py

	 e   x       x**2    isinf 
	---  ------  ------  ------
	  0  1.0     1.0     False 
	 20  1e+20   1e+40   False 
	 40  1e+40   1e+80   False 
	 60  1e+60   1e+120  False 
	 80  1e+80   1e+160  False 
	100  1e+100  1e+200  False 
	120  1e+120  1e+240  False 
	140  1e+140  1e+280  False 
	160  1e+160  inf     True  
	180  1e+180  inf     True  
	200  1e+200  inf     True  

.. {{{end}}}

Not all floating point overflows result in ``INF`` values, however.
Calculating an exponent with floating point values, in particular,
raises :class:`OverflowError` instead of preserving the ``INF``
result.

.. include:: math_overflow.py
   :literal:
   :start-after: #end_pymotw_header

This discrepancy is caused by an implementation difference in the
library used by C Python.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_overflow.py'))
.. }}}

::

	$ python math_overflow.py

	x    = 1e+200
	x*x  = inf
	x**2 = (34, 'Result too large')

.. {{{end}}}

Division operations using infinite values are undefined.  The result
of dividing a number by infinity is ``NaN`` (not a number).

.. include:: math_isnan.py
   :literal:
   :start-after: #end_pymotw_header

``NaN`` does not compare as equal to any value, even itself, so to
check for ``NaN`` use :func:`isnan`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_isnan.py'))
.. }}}

::

	$ python math_isnan.py

	x = inf
	isnan(x) = False
	y = x / x = nan
	y == nan = False
	isnan(y) = True

.. {{{end}}}

Converting to Integers
======================

The :mod:`math` module includes three functions for converting
floating point values to whole numbers.  Each takes a different
approach, and will be useful in different circumstances.

The simplest is :func:`trunc`, which truncates the digits following
the decimal, leaving only the significant digits making up the whole
number portion of the value.  :func:`floor` converts its input to the
largest preceding integer, and :func:`ceil` (ceiling) produces the
largest integer following sequentially after the input value.

.. include:: math_integers.py
   :literal:
   :start-after: #end_pymotw_header

:func:`trunc` is equivalent to converting to :class:`int` directly.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_integers.py'))
.. }}}

::

	$ python math_integers.py

	  i     int   trunk  floor  ceil 
	-----  -----  -----  -----  -----
	 -1.5   -1.0   -1.0   -2.0   -1.0
	 -0.8    0.0    0.0   -1.0   -0.0
	 -0.5    0.0    0.0   -1.0   -0.0
	 -0.2    0.0    0.0   -1.0   -0.0
	  0.0    0.0    0.0    0.0    0.0
	  0.2    0.0    0.0    0.0    1.0
	  0.5    0.0    0.0    0.0    1.0
	  0.8    0.0    0.0    0.0    1.0
	  1.0    1.0    1.0    1.0    1.0

.. {{{end}}}

Alternate Representations
=========================

:func:`modf` takes a single floating point number and returns a tuple
containing the fractional and whole number parts of the input value.

.. include:: math_modf.py
   :literal:
   :start-after: #end_pymotw_header

Both numbers in the return value are floats.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_modf.py'))
.. }}}

::

	$ python math_modf.py

	0/2 = (0.0, 0.0)
	1/2 = (0.5, 0.0)
	2/2 = (0.0, 1.0)
	3/2 = (0.5, 1.0)
	4/2 = (0.0, 2.0)
	5/2 = (0.5, 2.0)

.. {{{end}}}

:func:`frexp` returns the mantissa and exponent of a floating point
number, and can be used to create a more portable representation of
the value.

.. include:: math_frexp.py
   :literal:
   :start-after: #end_pymotw_header

:func:`frexp` uses the formula ``x = m * 2**e``, and returns the
values *m* and *e*.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_frexp.py'))
.. }}}

::

	$ python math_frexp.py

	   x        m        e   
	-------  -------  -------
	   0.10     0.80       -3
	   0.50     0.50        0
	   4.00     0.50        3

.. {{{end}}}

:func:`ldexp` is the inverse of :func:`frexp`.  

.. include:: math_ldexp.py
   :literal:
   :start-after: #end_pymotw_header

Using the same formula as :func:`frexp`, :func:`ldexp` takes the
mantissa and exponent values as arguments and returns a floating point
number.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_ldexp.py'))
.. }}}

::

	$ python math_ldexp.py

	   m        e        x   
	-------  -------  -------
	   0.80       -3     0.10
	   0.50        0     0.50
	   0.50        3     4.00

.. {{{end}}}


Positive and Negative Signs
===========================

The absolute value of a number is its value without a sign.  Use
:func:`fabs` to calculate the absolute value of a floating point
number.

.. include:: math_fabs.py
   :literal:
   :start-after: #end_pymotw_header

In practical terms, the absolute value of a :class:`float` is
represented as a positive value.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_fabs.py'))
.. }}}

::

	$ python math_fabs.py

	1.1
	0.0
	0.0
	1.1

.. {{{end}}}

To determine the sign of a value, either to give a set of values the
same sign or to compare two values, use :func:`copysign` to set the
sign of a known good value.

.. include:: math_copysign.py
   :literal:
   :start-after: #end_pymotw_header

An extra function like :func:`copysign` is needed because comparing
NaN and -NaN directly with other values does not work.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_copysign.py'))
.. }}}

::

	$ python math_copysign.py

	  f      s     < 0    > 0    = 0 
	-----  -----  -----  -----  -----
	 -1.0     -1  True   False  False
	  0.0      1  False  False  True 
	  1.0      1  False  True   False
	 -inf     -1  True   False  False
	  inf      1  False  True   False
	  nan     -1  False  False  False
	  nan      1  False  False  False

.. {{{end}}}

Commonly Used Calculations
==========================

Representing precise values in binary floating point memory is
challenging.  Some values cannot be represented exactly, and the more
often a value is manipulated through repeated calculations, the more
likely a representation error will be introduced.  :mod:`math`
includes a function for computing the sum of a series of floating
point numbers using an efficient algorithm that minimize such errors.

.. include:: math_fsum.py
   :literal:
   :start-after: #end_pymotw_header

Given a sequence of ten values, each equal to ``0.1``, the expected
value for the sum of the sequence is ``1.0``.  Since ``0.1`` cannot be
represented exactly as a floating point value, however, errors are
introduced into the sum unless it is calculated with :func:`fsum`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_fsum.py'))
.. }}}

::

	$ python math_fsum.py

	Input values: [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
	sum()       : 0.99999999999999988898
	for-loop    : 0.99999999999999988898
	math.fsum() : 1.00000000000000000000

.. {{{end}}}

:func:`factorial` is commonly used to calculate the number of
permutations and combinations of a series of objects.  The factorial
of a positive integer *n*, expressed ``n!``, is defined recursively as
``(n-1)! * n`` and stops with ``0! == 1``.

.. include:: math_factorial.py
   :literal:
   :start-after: #end_pymotw_header

:func:`factorial` only works with whole numbers, but does accept
:class:`float` arguments as long as they can be converted to an
integer without losing value.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_factorial.py', break_lines_at=65))
.. }}}

::

	$ python math_factorial.py

	 0       1
	 1       1
	 2       2
	 3       6
	 4      24
	 5     120
	Error computing factorial(6.1): factorial() only accepts integral
	 values

.. {{{end}}}

:func:`gamma` is like :func:`factorial`, except it works with real
numbers and the value is shifted down by one (gamma is equal to ``(n -
1)!``).

.. include:: math_gamma.py
   :literal:
   :start-after: #end_pymotw_header

Since zero causes the start value to be negative, it is not allowed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_gamma.py'))
.. }}}

::

	$ python math_gamma.py

	Error computing gamma(0): math domain error
	1.1    0.95
	2.2    1.10
	3.3    2.68
	4.4   10.14
	5.5   52.34
	6.6  344.70

.. {{{end}}}

:func:`lgamma` returns the natural logarithm of the absolute value of
gamma for the input value.

.. include:: math_lgamma.py
   :literal:
   :start-after: #end_pymotw_header

Using :func:`lgamma` retains more precision than calculating the
logarithm separately using the results of :func:`gamma`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_lgamma.py'))
.. }}}

::

	$ python math_lgamma.py

	Error computing lgamma(0): math domain error
	1.1  -0.04987244125984036103  -0.04987244125983997245
	2.2  0.09694746679063825923  0.09694746679063866168
	3.3  0.98709857789473387513  0.98709857789473409717
	4.4  2.31610349142485727469  2.31610349142485727469
	5.5  3.95781396761871651080  3.95781396761871606671
	6.6  5.84268005527463252236  5.84268005527463252236

.. {{{end}}}

The modulo operator (``%``) computes the remainder of a division
expression (i.e., ``5 % 2 = 1``).  The operator built into the
language works well with integers but, as with so many other floating
point operations, intermediate calculations cause representational
issues that result in a loss of data.  :func:`fmod` provides a more
accurate implementation for floating point values.

.. include:: math_fmod.py
   :literal:
   :start-after: #end_pymotw_header

A potentially more frequent source of confusion is the fact that the
algorithm used by :mod:`fmod` for computing modulo is also different
from that used by ``%``, so the sign of the result is different.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_fmod.py'))
.. }}}

::

	$ python math_fmod.py

	 x     y      %    fmod 
	----  ----  -----  -----
	 5.0   2.0   1.00   1.00
	 5.0  -2.0  -1.00   1.00
	-5.0   2.0   1.00  -1.00

.. {{{end}}}

Exponents and Logarithms
========================

Exponential growth curves appear in economics, physics, and other
sciences.  Python has a built-in exponentiation operator ("``**``"),
but :func:`pow` can be useful when a callable function is needed as an
argument to another function.

.. include:: math_pow.py
   :literal:
   :start-after: #end_pymotw_header

Raising ``1`` to any power always returns ``1.0``, as does raising any
value to a power of ``0.0``.  Most operations on the not-a-number
value ``nan`` return ``nan``.  If the exponent is less than ``1``,
:func:`pow` computes a root.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_pow.py'))
.. }}}

::

	$ python math_pow.py

	  2.0 ** 3.000 =  8.000
	  2.1 ** 3.200 = 10.742
	  1.0 ** 5.000 =  1.000
	  2.0 ** 0.000 =  1.000
	  2.0 **   nan =    nan
	  9.0 ** 0.500 =  3.000
	 27.0 ** 0.333 =  3.000

.. {{{end}}}

Since square roots (exponent of ``1/2``) are used so frequently, there
is a separate function for computing them.

.. include:: math_sqrt.py
   :literal:
   :start-after: #end_pymotw_header

Computing the square roots of negative numbers requires *complex
numbers*, which are not handled by :mod:`math`.  Any attempt to
calculate a square root of a negative value results in a
:class:`ValueError`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_sqrt.py'))
.. }}}

::

	$ python math_sqrt.py

	3.0
	1.73205080757
	Cannot compute sqrt(-1): math domain error

.. {{{end}}}

The logarithm function finds *y* where ``x = b ** y``.  By default,
:func:`log` computes the natural logarithm (the base is *e*).  If a
second argument is provided, that value is used as the base.

.. include:: math_log.py
   :literal:
   :start-after: #end_pymotw_header

Logarithms where *x* is less than one yield negative results.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_log.py'))
.. }}}

::

	$ python math_log.py

	2.07944154168
	3.0
	-1.0

.. {{{end}}}

There are two variations of :func:`log`.  Given floating point
representation and rounding errors, the computed value produced by
``log(x, b)`` has limited accuracy, especially for some bases.
:func:`log10` computes ``log(x, 10)``, using a more accurate algorithm
than :func:`log`.

.. include:: math_log10.py
   :literal:
   :start-after: #end_pymotw_header

The lines in the output with trailing ``*`` highlight the inaccurate
values.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_log10.py'))
.. }}}

::

	$ python math_log10.py

	i        x         accurate        inaccurate       mismatch
	--  ------------  ----------  --------------------  --------
	 0           1.0  0.00000000  0.000000000000000000       
	 1          10.0  1.00000000  1.000000000000000000       
	 2         100.0  2.00000000  2.000000000000000000       
	 3        1000.0  3.00000000  2.999999999999999556    *  
	 4       10000.0  4.00000000  4.000000000000000000       
	 5      100000.0  5.00000000  5.000000000000000000       
	 6     1000000.0  6.00000000  5.999999999999999112    *  
	 7    10000000.0  7.00000000  7.000000000000000000       
	 8   100000000.0  8.00000000  8.000000000000000000       
	 9  1000000000.0  9.00000000  8.999999999999998224    *  

.. {{{end}}}

:func:`log1p` calculates the Newton-Mercator series (the natural
logarithm of ``1+x``).

.. include:: math_log1p.py
   :literal:
   :start-after: #end_pymotw_header

:func:`log1p` is more accurate for values of *x* very close to zero
because it uses an algorithm that compensates for round-off errors
from the initial addition.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_log1p.py'))
.. }}}

::

	$ python math_log1p.py

	x       : 1e-25
	1 + x   : 1.0
	log(1+x): 0.0
	log1p(x): 1e-25

.. {{{end}}}

:func:`exp` computes the exponential function (``e**x``).  

.. include:: math_exp.py
   :literal:
   :start-after: #end_pymotw_header

As with other special-case functions, it uses an algorithm that
produces more accurate results than the general-purpose equivalent
``math.pow(math.e, x)``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_exp.py'))
.. }}}

::

	$ python math_exp.py

	7.38905609893064951876
	7.38905609893064951876
	7.38905609893065040694

.. {{{end}}}

:func:`expm1` is the inverse of :func:`log1p`, and calculates ``e**x -
1``.

.. include:: math_expm1.py
   :literal:
   :start-after: #end_pymotw_header

Small values of *x* lose precision when the subtraction is performed
separately, like with :func:`log1p`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_expm1.py'))
.. }}}

::

	$ python math_expm1.py

	1e-25
	0.0
	1e-25

.. {{{end}}}

Angles
======

Although degrees are more commonly used in everyday discussions of
angles, radians are the standard unit of angular measure in science
and math.  A radian is the angle created by two lines intersecting at
the center of a circle, with their ends on the circumference of the
circle spaced one radius apart.  

The circumference is calculated as ``2πr``, so there is a relationship
between radians and π, a value that shows up frequently in
trigonometric calculations.  That relationship leads to radians being
used in trigonometry and calculus, because they result in more compact
formulas.

To convert from degrees to radians, use :func:`radians`.

.. include:: math_radians.py
   :literal:
   :start-after: #end_pymotw_header

The formula for the conversion is ``rad = deg * π / 180``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_radians.py'))
.. }}}

::

	$ python math_radians.py

	Degrees  Radians  Expected
	-------  -------  -------
	      0     0.00     0.00
	     30     0.52     0.52
	     45     0.79     0.79
	     60     1.05     1.05
	     90     1.57     1.57
	    180     3.14     3.14
	    270     4.71     4.71
	    360     6.28     6.28

.. {{{end}}}

To convert from radians to degrees, use :func:`degrees`.

.. include:: math_degrees.py
   :literal:
   :start-after: #end_pymotw_header

The formula is ``deg = rad * 180 / π``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_degrees.py'))
.. }}}

::

	$ python math_degrees.py

	Radians   Degrees   Expected
	--------  --------  --------
	    0.00      0.00      0.00
	    0.52     30.00     30.00
	    0.79     45.00     45.00
	    1.05     60.00     60.00
	    1.57     90.00     90.00
	    3.14    180.00    180.00
	    4.71    270.00    270.00
	    6.28    360.00    360.00

.. {{{end}}}


Trigonometry
============

Trigonometric functions relate angles in a triangle to the lengths of
its sides.  They show up in formulas with periodic properties such as
harmonics, circular motion, or when dealing with angles.  All of the
trigonometric functions in the standard library take angles expressed
as radians.

Given an angle in a right triangle, the *sine* is the ratio of the
length of the side opposite the angle to the hypotenuse (``sin A =
opposite/hypotenuse``).  The *cosine* is the ratio of the length of
the adjacent side to the hypotenuse (``cos A = adjacent/hypotenuse``).
And the *tangent* is the ratio of the opposite side to the adjacent
side (``tan A = opposite/adjacent``).

.. include:: math_trig.py
   :literal:
   :start-after: #end_pymotw_header

The tangent can also be defined as the ratio of the sine of the angle
to its cosine, and since the cosine is 0 for π/2 and 3π/2 radians, the
tangent is infinite.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_trig.py'))
.. }}}

::

	$ python math_trig.py

	Degrees  Radians  Sine     Cosine    Tangent
	-------  -------  -------  --------  -------
	   0.00     0.00     0.00     1.00     0.00
	  30.00     0.52     0.50     0.87     0.58
	  60.00     1.05     0.87     0.50     1.73
	  90.00     1.57     1.00     0.00      inf
	 120.00     2.09     0.87    -0.50    -1.73
	 150.00     2.62     0.50    -0.87    -0.58
	 180.00     3.14     0.00    -1.00    -0.00
	 210.00     3.67    -0.50    -0.87     0.58
	 240.00     4.19    -0.87    -0.50     1.73
	 270.00     4.71    -1.00    -0.00      inf
	 300.00     5.24    -0.87     0.50    -1.73
	 330.00     5.76    -0.50     0.87    -0.58
	 360.00     6.28    -0.00     1.00    -0.00

.. {{{end}}}

Given a point (*x*, *y*), the length of the hypotenuse for the
triangle between the points [(0, 0), (*x*, 0), (*x*, *y*)] is
``(x**2 + y**2) ** 1/2``, and can be computed with :func:`hypot`.

.. include:: math_hypot.py
   :literal:
   :start-after: #end_pymotw_header

Points on the circle always have hypotenuse == ``1``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_hypot.py'))
.. }}}

::

	$ python math_hypot.py

	   X        Y     Hypotenuse
	-------  -------  ----------
	   1.00     1.00     1.41
	  -1.00    -1.00     1.41
	   1.41     1.41     2.00
	   3.00     4.00     5.00
	   0.71     0.71     1.00
	   0.50     0.87     1.00

.. {{{end}}}

The same function can be used to find the distance between two points.

.. include:: math_distance_2_points.py
   :literal:
   :start-after: #end_pymotw_header

Use the difference in the *x* and *y* values to move one endpoint to
the origin, and then pass the results to :func:`hypot`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_distance_2_points.py'))
.. }}}

::

	$ python math_distance_2_points.py

	   X1        Y1        X2        Y2     Distance
	--------  --------  --------  --------  --------
	    5.00      5.00      6.00      6.00      1.41
	   -6.00     -6.00     -5.00     -5.00      1.41
	    0.00      0.00      3.00      4.00      5.00
	   -1.00     -1.00      2.00      3.00      5.00

.. {{{end}}}

:mod:`math` also defines inverse trigonometric functions.

.. include:: math_inverse_trig.py
   :literal:
   :start-after: #end_pymotw_header

``1.57`` is roughly equal to ``π/2``, or 90 degrees, the angle at
which the sine is 1 and the cosine is 0.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_inverse_trig.py'))
.. }}}

::

	$ python math_inverse_trig.py

	arcsine(0.0)    =  0.00
	arccosine(0.0)  =  1.57
	arctangent(0.0) =  0.00
	
	arcsine(0.5)    =  0.52
	arccosine(0.5)  =  1.05
	arctangent(0.5) =  0.46
	
	arcsine(1.0)    =  1.57
	arccosine(1.0)  =  0.00
	arctangent(1.0) =  0.79
	

.. {{{end}}}

.. atan2

Hyperbolic Functions
====================

Hyperbolic functions appear in linear differential equations and are
used when working with electromagnetic fields, fluid dynamics, special
relativity, and other advanced physics and mathematics.

.. include:: math_hyperbolic.py
   :literal:
   :start-after: #end_pymotw_header

Whereas the cosine and sine functions enscribe a circle, the
hyperbolic cosine and hyperbolic sine form half of a hyperbola.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_hyperbolic.py'))
.. }}}

::

	$ python math_hyperbolic.py

	  X      sinh    cosh    tanh 
	------  ------  ------  ------
	0.0000  0.0000  1.0000  0.0000
	0.2000  0.2013  1.0201  0.1974
	0.4000  0.4108  1.0811  0.3799
	0.6000  0.6367  1.1855  0.5370
	0.8000  0.8881  1.3374  0.6640
	1.0000  1.1752  1.5431  0.7616

.. {{{end}}}

Inverse hyperbolic functions :func:`acosh`, :func:`asinh`, and
:func:`atanh` are also available.

Special Functions
=================

The Gauss Error function is used in statistics.

.. include:: math_erf.py
   :literal:
   :start-after: #end_pymotw_header

For the error function, ``erf(-x) == -erf(x)``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_erf.py'))
.. }}}

::

	$ python math_erf.py

	  x    erf(x) 
	-----  -------
	-3.00  -1.0000
	-2.00  -0.9953
	-1.00  -0.8427
	-0.50  -0.5205
	-0.25  -0.2763
	 0.00   0.0000
	 0.25   0.2763
	 0.50   0.5205
	 1.00   0.8427
	 2.00   0.9953
	 3.00   1.0000

.. {{{end}}}

The complimentary error function is ``1 - erf(x)``.

.. include:: math_erfc.py
   :literal:
   :start-after: #end_pymotw_header

The implementation of :func:`erfc` avoids precision errors for small
values of *x* when subtracting from 1.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'math_erfc.py'))
.. }}}

::

	$ python math_erfc.py

	  x    erfc(x)
	-----  -------
	-3.00   2.0000
	-2.00   1.9953
	-1.00   1.8427
	-0.50   1.5205
	-0.25   1.2763
	 0.00   1.0000
	 0.25   0.7237
	 0.50   0.4795
	 1.00   0.1573
	 2.00   0.0047
	 3.00   0.0000

.. {{{end}}}


.. seealso::

    `math <http://docs.python.org/library/math.html>`_
        The standard library documentation for this module.

    `IEEE floating point arithmetic in Python <http://www.johndcook.com/blog/2009/07/21/ieee-arithmetic-python/>`__
        Blog post by John Cook about how special values arise and are
        dealt with when doing math in Python.

    `SciPy <http://scipy.org/>`_
        Open source libraryes for scientific and mathematical
        calculations in Python.
