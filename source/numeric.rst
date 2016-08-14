=============
 Mathematics
=============

As a general purpose programming language, Python is frequently used
to solve mathematical problems.  It includes built-in types for
managing integer and floating point numbers, which are suitable for
the basic math that might appear in an average application.  The standard
library includes modules for more advanced needs.

Python's built-in floating point numbers use the underlying
:class:`double` representation.  They are sufficiently precise for
most programs with mathematical requirements, but when more accurate
representations of non-integer values are needed the :mod:`decimal`
and :mod:`fractions` modules will be useful.  Arithmetic with decimal
and fractional values retains precision, but is not as fast as the
native :class:`float`.

The :mod:`random` module includes a uniform distribution
pseudorandom number generator, as well as functions for simulating
many common non-uniform distributions.

The :mod:`math` module contains fast implementations of advanced
mathematical functions such as logarithms and trigonometric
functions.  The full complement of IEEE functions usually found in
the native platform C libraries is available through the module.

.. toctree::
   :maxdepth: 1

   decimal/index
   fractions/index
   random/index
   math/index

..
   .. toctree::
       :maxdepth: 1

       decimal/index
       fractions/index
       random/index
       math/index

       statistics
