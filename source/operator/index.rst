========================================================
 operator -- Functional Interface to Built-in Operators
========================================================

.. module:: operator
    :synopsis: Functional interface to built-in operators

:Purpose: Functional interface to built-in operators.
:Python Version: 1.4 and later

Programming using iterators occasionally requires creating small
functions for simple expressions. Sometimes, these can be implemented
as :command:`lambda` functions, but for some operations new functions
are not needed at all.  The :mod:`operator` module defines functions
that correspond to built-in operations for arithmetic and comparison.

.. toctree::

   normal

.. only:: bonus

   .. include:: bonus.rst

.. seealso::

    `operator <http://docs.python.org/lib/module-operator.html>`_
        Standard library documentation for this module.

    :mod:`functools`
        Functional programming tools, including the
        :func:`total_ordering` decorator for adding rich comparison
        methods to a class.

    :mod:`itertools`
        Iterator operations.

    :mod:`abc`
      The ``abc`` module includes :ref:`abstract base classes
      <abc-collection-types>` that define the APIs for collection
      types.
