====================
 time -- Clock Time
====================

.. module:: time
    :synopsis: Clock time

:Purpose: Functions for manipulating clock time.

The :mod:`time` module exposes C library functions for manipulating
dates and times.  Since it is tied to the underlying C implementation,
some details (such as the start of the epoch and maximum date value
supported) are platform-specific.  Refer to the library documentation
for complete details.

.. toctree::

   normal

.. only:: bonus

   .. toctree:: 

      bonus

.. seealso::

    `time <http://docs.python.org/lib/module-time.html>`_
        Standard library documentation for this module.

    :mod:`datetime`
        The ``datetime`` module includes other classes for doing
        calculations with dates and times.

    :mod:`calendar`
        Work with higher-level date functions to produce calendars or
        calculate recurring events.
