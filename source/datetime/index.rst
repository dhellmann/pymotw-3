==============================================
 datetime -- Date and Time Value Manipulation
==============================================

.. module:: datetime
    :synopsis: Date and time value manipulation.

:Purpose: The datetime module includes functions and classes for doing date and time parsing, formatting, and arithmetic.
:Python Version: 2.3 and later

:mod:`datetime` contains functions and classes for working with dates
and times, separately and together.

Times
=====

Time values are represented with the :class:`time` class. A
:class:`time` instance has attributes for :attr:`hour`,
:attr:`minute`, :attr:`second`, and :attr:`microsecond` and can also
include time zone information.

.. include:: datetime_time.py
    :literal:
    :start-after: #end_pymotw_header

The arguments to initialize a :class:`time` instance are optional, but
the default of ``0`` is unlikely to be correct.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_time.py'))
.. }}}

::

	$ python datetime_time.py

	01:02:03
	hour       : 1
	minute     : 2
	second     : 3
	microsecond: 0
	tzinfo     : None

.. {{{end}}}

A :class:`time` instance only holds values of time, and not a date
associated with the time.

.. include:: datetime_time_minmax.py
    :literal:
    :start-after: #end_pymotw_header

The :attr:`min` and :attr:`max` class attributes reflect the valid
range of times in a single day.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_time_minmax.py'))
.. }}}

::

	$ python datetime_time_minmax.py

	Earliest  : 00:00:00
	Latest    : 23:59:59.999999
	Resolution: 0:00:00.000001

.. {{{end}}}

The resolution for :class:`time` is limited to whole microseconds. 

.. include:: datetime_time_resolution.py
    :literal:
    :start-after: #end_pymotw_header

The way floating point values are treated depends on the version of
Python.  Version 2.7 raises a :class:`TypeError`, while earlier
versions produce a :class:`DeprecationWarning` and convert the
floating point number to an integer.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_time_resolution.py', interprepter='python2.7'))
.. cog.out(run_script(cog.inFile, 'datetime_time_resolution.py', 
..         interpreter='python2.6', include_prefix=False,
..         break_lines_at=74, line_break_mode='wrap'))
.. }}}

::

    $ python2.7 datetime_time_resolution.py

    1.0 : 00:00:00.000001
    0.0 : 00:00:00
    0.1 : ERROR: integer argument expected, got float
    0.6 : ERROR: integer argument expected, got float
    
    $ python2.6 datetime_time_resolution.py 

    1.0 : 00:00:00.000001
    0.0 : 00:00:00
    datetime_time_resolution.py:16: DeprecationWarning: integer argument 
    expected, got float
      print '%02.1f :' % m, datetime.time(0, 0, 0, microsecond=m)
    0.1 : 00:00:00
    0.6 : 00:00:00

.. {{{end}}}


Dates
=====

Calendar date values are represented with the :class:`date`
class. Instances have attributes for :attr:`year`, :attr:`month`, and
:attr:`day`. It is easy to create a date representing the current date
using the :func:`today` class method.

.. include:: datetime_date.py
    :literal:
    :start-after: #end_pymotw_header

This example prints the current date in several formats:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_date.py', break_lines_at=69))
.. }}}

::

	$ python datetime_date.py

	2010-11-27
	ctime  : Sat Nov 27 00:00:00 2010
	tuple  : tm_year  = 2010
	         tm_mon   = 11
	         tm_mday  = 27
	         tm_hour  = 0
	         tm_min   = 0
	         tm_sec   = 0
	         tm_wday  = 5
	         tm_yday  = 331
	         tm_isdst = -1
	ordinal: 734103
	Year   : 2010
	Mon    : 11
	Day    : 27

.. {{{end}}}

There are also class methods for creating instances from POSIX
timestamps or integers representing date values from the Gregorian
calendar, where January 1 of the year 1 is ``1`` and each subsequent
day increments the value by 1.

.. include:: datetime_date_fromordinal.py
    :literal:
    :start-after: #end_pymotw_header

This example illustrates the different value types used by
:func:`fromordinal()` and :func:`fromtimestamp()`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_date_fromordinal.py'))
.. }}}

::

	$ python datetime_date_fromordinal.py

	o               : 733114
	fromordinal(o)  : 2008-03-13
	t               : 1290874810.14
	fromtimestamp(t): 2010-11-27

.. {{{end}}}

As with :class:`time`, the range of date values supported can be
determined using the :attr:`min` and :attr:`max` attributes.

.. include:: datetime_date_minmax.py
    :literal:
    :start-after: #end_pymotw_header

The resolution for dates is whole days.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_date_minmax.py'))
.. }}}

::

	$ python datetime_date_minmax.py

	Earliest  : 0001-01-01
	Latest    : 9999-12-31
	Resolution: 1 day, 0:00:00

.. {{{end}}}

Another way to create new :class:`date` instances uses the
:func:`replace()` method of an existing :class:`date`.

.. include:: datetime_date_replace.py
    :literal:
    :start-after: #end_pymotw_header

This example changes the year, leaving the day and month unmodified.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_date_replace.py'))
.. }}}

::

	$ python datetime_date_replace.py

	d1: Sat Mar 29 00:00:00 2008
	d2: Sun Mar 29 00:00:00 2009

.. {{{end}}}

timedeltas
==========

Future and past dates can be calculated using basic arithmetic on two
:mod:`datetime` objects, or by combining a :class:`datetime` with a
:class:`timedelta`.  Subtracting dates produces a :class:`timedelta`,
and a :class:`timedelta` can be added or subtracted from a date to
produce another date. The internal values for a :class:`timedelta` are
stored in days, seconds, and microseconds.

.. include:: datetime_timedelta.py
    :literal:
    :start-after: #end_pymotw_header

Intermediate level values passed to the constructor are converted into
days, seconds, and microseconds.  

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_timedelta.py'))
.. }}}

::

	$ python datetime_timedelta.py

	microseconds: 0:00:00.000001
	milliseconds: 0:00:00.001000
	seconds     : 0:00:01
	minutes     : 0:01:00
	hours       : 1:00:00
	days        : 1 day, 0:00:00
	weeks       : 7 days, 0:00:00

.. {{{end}}}

The full duration of a :class:`timedelta` can be retrieved as a number
of seconds using :func:`total_seconds`.

.. include:: datetime_timedelta_total_seconds.py
   :literal:
   :start-after: #end_pymotw_header

The return value is a floating point number, to accommodate sub-second
durations.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_timedelta_total_seconds.py'))
.. }}}

::

	$ python datetime_timedelta_total_seconds.py

	 0:00:00.000001 = 1e-06 seconds
	 0:00:00.001000 = 0.001 seconds
	        0:00:01 = 1.0 seconds
	        0:01:00 = 60.0 seconds
	        1:00:00 = 3600.0 seconds
	 1 day, 0:00:00 = 86400.0 seconds
	7 days, 0:00:00 = 604800.0 seconds

.. {{{end}}}

Date Arithmetic
===============

Date math uses the standard arithmetic operators. 

.. include:: datetime_date_math.py
    :literal:
    :start-after: #end_pymotw_header

This example with date objects illustrates using :class:`timedelta`
objects to compute new dates, and subtracting date instances to
produce timedeltas (including a negative delta value).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_date_math.py'))
.. }}}

::

	$ python datetime_date_math.py

	Today    : 2010-11-27
	One day  : 1 day, 0:00:00
	Yesterday: 2010-11-26
	Tomorrow : 2010-11-28
	
	tomorrow - yesterday: 2 days, 0:00:00
	yesterday - tomorrow: -2 days, 0:00:00

.. {{{end}}}

Comparing Values
================

Both date and time values can be compared using the standard
comparison operators to determine which is earlier or later.

.. include:: datetime_comparing.py
    :literal:
    :start-after: #end_pymotw_header

All of the comparison operators are supported.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_comparing.py'))
.. }}}

::

	$ python datetime_comparing.py

	Times:
	  t1: 12:55:00
	  t2: 13:05:00
	  t1 < t2: True
	
	Dates:
	  d1: 2010-11-27
	  d2: 2010-11-28
	  d1 > d2: False

.. {{{end}}}

Combining Dates and Times
=========================

Use the :class:`datetime` class to hold values consisting of both date
and time components. As with :class:`date`, there are several
convenient class methods to make creating :class:`datetime` instances
from other common values.

.. include:: datetime_datetime.py
    :literal:
    :start-after: #end_pymotw_header

As might be expected, the :class:`datetime` instance has all of the
attributes of both a :class:`date` and a :class:`time` object.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_datetime.py'))
.. }}}

::

	$ python datetime_datetime.py

	Now    : 2010-11-27 11:20:10.479880
	Today  : 2010-11-27 11:20:10.481494
	UTC Now: 2010-11-27 16:20:10.481521
	
	           year: 2010
	          month: 11
	            day: 27
	           hour: 11
	         minute: 20
	         second: 10
	    microsecond: 481752

.. {{{end}}}

Just as with :class:`date`, :class:`datetime` provides convenient
class methods for creating new instances. It also includes
:func:`fromordinal()` and :func:`fromtimestamp()`. 

.. include:: datetime_datetime_combine.py
    :literal:
    :start-after: #end_pymotw_header

:func:`combine()` creates :class:`datetime` instances from one
:class:`date` and one :class:`time` instance.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_datetime_combine.py'))
.. }}}

::

	$ python datetime_datetime_combine.py

	t : 01:02:03
	d : 2010-11-27
	dt: 2010-11-27 01:02:03

.. {{{end}}}

Formatting and Parsing
======================

The default string representation of a datetime object uses the
ISO-8601 format (``YYYY-MM-DDTHH:MM:SS.mmmmmm``). Alternate formats
can be generated using :func:`strftime()`.

.. include:: datetime_datetime_strptime.py
    :literal:
    :start-after: #end_pymotw_header

Use :func:`datetime.strptime()` to convert formatted strings to
:class:`datetime` instances.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_datetime_strptime.py'))
.. }}}

::

	$ python datetime_datetime_strptime.py

	ISO     : 2010-11-27 11:20:10.571582
	strftime: Sat Nov 27 11:20:10 2010
	strptime: Sat Nov 27 11:20:10 2010

.. {{{end}}}

Time Zones
==========

Within :mod:`datetime`, time zones are represented by subclasses of
:class:`tzinfo`. Since :class:`tzinfo` is an abstract base class,
applications need to define a subclass and provide appropriate
implementations for a few methods to make it useful. Unfortunately,
:mod:`datetime` does not include any actual implementations ready to
be used, although the documentation does provide a few sample
implementations. Refer to the standard library documentation page for
examples using fixed offsets as well as a DST-aware class and more
details about creating custom time zone classes.  ``pytz`` is also a
good source for time zone implementation details.

.. seealso::

    `datetime <http://docs.python.org/lib/module-datetime.html>`_
        The standard library documentation for this module.

    :mod:`calendar`
        The ``calendar`` module.

    :mod:`time`
        The ``time`` module.

    `dateutil <http://labix.org/python-dateutil>`_
        ``dateutil`` from Labix extends the ``datetime`` module with additional features.

    `WikiPedia: Proleptic Gregorian calendar <http://en.wikipedia.org/wiki/Proleptic_Gregorian_calendar>`_
        A description of the Gregorian calendar system.

    pytz_
        World Time Zone database

    `ISO 8601`_
        The standard for numeric representation of Dates and Time

.. _ISO 8601: http://www.iso.org/iso/support/faqs/faqs_widely_used_standards/widely_used_standards_other/date_and_time_format.htm

.. _pytz: http://pytz.sourceforge.net/
