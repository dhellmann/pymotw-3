=================
 Dates and Times
=================

Python does not include native types for dates and times as it does
for ``int``, ``float``, and ``str``, but there are
three modules for manipulating date and time values in several
representations.

The :mod:`time` module exposes the time-related functions from the
underlying C library.  It includes functions for retrieving the clock
time and the processor run time, as well as basic parsing and string
formatting tools.

The :mod:`datetime` module provides a higher level interface for date,
time, and combined values.  The classes in :mod:`datetime` support
arithmetic, comparison, and time zone configuration.

The :mod:`calendar` module creates formatted representations of weeks,
months, and years.  It can also be used to compute recurring events,
the day of the week for a given date, and other calendar-based values.

.. toctree::
   :maxdepth: 1

   time/index
   datetime/index
   calendar/index
