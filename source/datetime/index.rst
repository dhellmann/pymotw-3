===============================================
 datetime --- Date and Time Value Manipulation
===============================================

.. module:: datetime
    :synopsis: Date and time value manipulation.

:Purpose: The datetime module includes functions and classes for doing
          date and time parsing, formatting, and arithmetic.

:mod:`datetime` contains functions and classes for working with dates
and times, separately and together.

Times
=====

Time values are represented with the :class:`time` class. A
:class:`time` instance has attributes for :attr:`hour`,
:attr:`minute`, :attr:`second`, and :attr:`microsecond` and can also
include time zone information.

.. literalinclude:: datetime_time.py
    :caption:
    :start-after: #end_pymotw_header

The arguments to initialize a :class:`time` instance are optional, but
the default of ``0`` is unlikely to be correct.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_time.py'))
.. }}}

::

	$ python3 datetime_time.py
	
	01:02:03
	hour       : 1
	minute     : 2
	second     : 3
	microsecond: 0
	tzinfo     : None

.. {{{end}}}

A :class:`time` instance only holds values of time, and not a date
associated with the time.

.. literalinclude:: datetime_time_minmax.py
    :caption:
    :start-after: #end_pymotw_header

The :attr:`min` and :attr:`max` class attributes reflect the valid
range of times in a single day.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_time_minmax.py'))
.. }}}

::

	$ python3 datetime_time_minmax.py
	
	Earliest  : 00:00:00
	Latest    : 23:59:59.999999
	Resolution: 0:00:00.000001

.. {{{end}}}

The resolution for :class:`time` is limited to whole microseconds.

.. literalinclude:: datetime_time_resolution.py
    :caption:
    :start-after: #end_pymotw_header

Floating point values for microseconds cause a :class:`TypeError`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_time_resolution.py'))
.. }}}

::

	$ python3 datetime_time_resolution.py
	
	1.0 : 00:00:00.000001
	0.0 : 00:00:00
	ERROR: integer argument expected, got float
	ERROR: integer argument expected, got float

.. {{{end}}}


Dates
=====

Calendar date values are represented with the :class:`date`
class. Instances have attributes for :attr:`year`, :attr:`month`, and
:attr:`day`. It is easy to create a date representing the current date
using the :func:`today` class method.

.. literalinclude:: datetime_date.py
    :caption:
    :start-after: #end_pymotw_header

This example prints the current date in several formats:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_date.py', break_lines_at=69))
.. }}}

::

	$ python3 datetime_date.py
	
	2015-12-24
	ctime  : Thu Dec 24 00:00:00 2015
	tuple  : tm_year  = 2015
	         tm_mon   = 12
	         tm_mday  = 24
	         tm_hour  = 0
	         tm_min   = 0
	         tm_sec   = 0
	         tm_wday  = 3
	         tm_yday  = 358
	         tm_isdst = -1
	ordinal: 735956
	Year   : 2015
	Mon    : 12
	Day    : 24

.. {{{end}}}

There are also class methods for creating instances from POSIX
timestamps or integers representing date values from the Gregorian
calendar, where January 1 of the year 1 is ``1`` and each subsequent
day increments the value by 1.

.. literalinclude:: datetime_date_fromordinal.py
    :caption:
    :start-after: #end_pymotw_header

This example illustrates the different value types used by
:func:`fromordinal` and :func:`fromtimestamp`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_date_fromordinal.py'))
.. }}}

::

	$ python3 datetime_date_fromordinal.py
	
	o               : 733114
	fromordinal(o)  : 2008-03-13
	t               : 1450968483.121123
	fromtimestamp(t): 2015-12-24

.. {{{end}}}

As with :class:`time`, the range of date values supported can be
determined using the :attr:`min` and :attr:`max` attributes.

.. literalinclude:: datetime_date_minmax.py
    :caption:
    :start-after: #end_pymotw_header

The resolution for dates is whole days.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_date_minmax.py'))
.. }}}

::

	$ python3 datetime_date_minmax.py
	
	Earliest  : 0001-01-01
	Latest    : 9999-12-31
	Resolution: 1 day, 0:00:00

.. {{{end}}}

Another way to create new :class:`date` instances uses the
:func:`replace` method of an existing :class:`date`.

.. literalinclude:: datetime_date_replace.py
    :caption:
    :start-after: #end_pymotw_header

This example changes the year, leaving the day and month unmodified.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_date_replace.py'))
.. }}}

::

	$ python3 datetime_date_replace.py
	
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

.. literalinclude:: datetime_timedelta.py
    :caption:
    :start-after: #end_pymotw_header

Intermediate level values passed to the constructor are converted into
days, seconds, and microseconds.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_timedelta.py'))
.. }}}

::

	$ python3 datetime_timedelta.py
	
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

.. literalinclude:: datetime_timedelta_total_seconds.py
   :caption:
   :start-after: #end_pymotw_header

The return value is a floating point number, to accommodate sub-second
durations.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_timedelta_total_seconds.py'))
.. }}}

::

	$ python3 datetime_timedelta_total_seconds.py
	
	0:00:00.000001  =    1e-06 seconds
	0:00:00.001000  =    0.001 seconds
	0:00:01         =      1.0 seconds
	0:01:00         =     60.0 seconds
	1:00:00         =   3600.0 seconds
	1 day, 0:00:00  =  86400.0 seconds
	7 days, 0:00:00 = 604800.0 seconds

.. {{{end}}}

Date Arithmetic
===============

Date math uses the standard arithmetic operators.

.. literalinclude:: datetime_date_math.py
    :caption:
    :start-after: #end_pymotw_header

This example with date objects illustrates using :class:`timedelta`
objects to compute new dates, and subtracting date instances to
produce timedeltas (including a negative delta value).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_date_math.py'))
.. }}}

::

	$ python3 datetime_date_math.py
	
	Today    : 2015-12-24
	One day  : 1 day, 0:00:00
	Yesterday: 2015-12-23
	Tomorrow : 2015-12-25
	
	tomorrow - yesterday: 2 days, 0:00:00
	yesterday - tomorrow: -2 days, 0:00:00

.. {{{end}}}

A :class:`timedelta` object also supports arithmetic with integers,
floats, and other :class:`timedelta` instances.

.. literalinclude:: datetime_timedelta_math.py
   :caption:
   :start-after: #end_pymotw_header

In this example, several multiples of a single day are computed, with
the resulting :class:`timedelta` holding the appropriate number of
days or hours. The final example demonstrates how to compute values by
combining two :class:`timedelta` objects. In this case, the result is
a floating point number.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_timedelta_math.py'))
.. }}}

::

	$ python3 datetime_timedelta_math.py
	
	1 day    : 1 day, 0:00:00
	5 days   : 5 days, 0:00:00
	1.5 days : 1 day, 12:00:00
	1/4 day  : 6:00:00
	meetings per day : 7.0

.. {{{end}}}

Comparing Values
================

Both date and time values can be compared using the standard
comparison operators to determine which is earlier or later.

.. literalinclude:: datetime_comparing.py
    :caption:
    :start-after: #end_pymotw_header

All comparison operators are supported.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_comparing.py'))
.. }}}

::

	$ python3 datetime_comparing.py
	
	Times:
	  t1: 12:55:00
	  t2: 13:05:00
	  t1 < t2: True
	Dates:
	  d1: 2015-12-24
	  d2: 2015-12-25
	  d1 > d2: False

.. {{{end}}}

Combining Dates and Times
=========================

Use the :class:`datetime` class to hold values consisting of both date
and time components. As with :class:`date`, there are several
convenient class methods to make creating :class:`datetime` instances
from other common values.

.. literalinclude:: datetime_datetime.py
    :caption:
    :start-after: #end_pymotw_header

As might be expected, the :class:`datetime` instance has all of the
attributes of both a :class:`date` and a :class:`time` object.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_datetime.py'))
.. }}}

::

	$ python3 datetime_datetime.py
	
	Now    : 2015-12-24 09:48:03.539040
	Today  : 2015-12-24 09:48:03.539080
	UTC Now: 2015-12-24 14:48:03.539123
	year           : 2015
	month          : 12
	day            : 24
	hour           : 9
	minute         : 48
	second         : 3
	microsecond    : 542174

.. {{{end}}}

Just as with :class:`date`, :class:`datetime` provides convenient
class methods for creating new instances. It also includes
:func:`fromordinal` and :func:`fromtimestamp`.

.. literalinclude:: datetime_datetime_combine.py
    :caption:
    :start-after: #end_pymotw_header

:func:`combine` creates :class:`datetime` instances from one
:class:`date` and one :class:`time` instance.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_datetime_combine.py'))
.. }}}

::

	$ python3 datetime_datetime_combine.py
	
	t : 01:02:03
	d : 2015-12-24
	dt: 2015-12-24 01:02:03

.. {{{end}}}

Formatting and Parsing
======================

The default string representation of a datetime object uses the
ISO-8601 format (``YYYY-MM-DDTHH:MM:SS.mmmmmm``). Alternate formats
can be generated using :func:`strftime`.

.. literalinclude:: datetime_datetime_strptime.py
    :caption:
    :start-after: #end_pymotw_header

Use :func:`datetime.strptime` to convert formatted strings to
:class:`datetime` instances.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_datetime_strptime.py'))
.. }}}

::

	$ python3 datetime_datetime_strptime.py
	
	ISO     : 2015-12-24 09:48:03.639545
	strftime: Thu Dec 24 09:48:03 2015
	strptime: Thu Dec 24 09:48:03 2015

.. {{{end}}}

The same formatting codes can be used with Python's `string formatting
mini-language`_ by placing them after the ``:`` in the field
specification of the format string.

.. literalinclude:: datetime_format.py
   :caption:
   :start-after: #end_pymotw_header

Each datetime format code must still be prefixed with ``%``, and
subsequent colons are treated as literal characters to include in the
output.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_format.py'))
.. }}}

::

	$ python3 datetime_format.py
	
	ISO     : 2015-12-24 09:48:03.699078
	format(): Thu Dec 24 09:48:03 2015

.. {{{end}}}

.. _string formatting mini-language: https://docs.python.org/3.5/library/string.html#formatspec


The following table demonstrates all of the formatting codes for 5:00
PM January 13, 2016 in the US/Eastern time zone.

.. {{{cog
.. import datetime
.. import pytz
.. tz = pytz.timezone('US/Eastern')
.. d = tz.localize(datetime.datetime(2016, 1, 13, 17, 0, 0))
.. symbols = [
..   ('%a', 'Abbreviated weekday name'),
..   ('%A', 'Full weekday name'),
..   ('%w', 'Weekday number -- 0 (Sunday) through 6 (Saturday)'),
..   ('%d', 'Day of the month (zero padded'),
..   ('%b', 'Abbreviated month name'),
..   ('%B', 'Full month name'),
..   ('%m', 'Month of the year'),
..   ('%y', 'Year without century'),
..   ('%Y', 'Year with century'),
..   ('%H', 'Hour from 24-hour clock'),
..   ('%I', 'Hour from 12-hour clock'),
..   ('%p', 'AM/PM'),
..   ('%M', 'Minutes'),
..   ('%S', 'Seconds'),
..   ('%f', 'Microseconds'),
..   ('%z', 'UTC offset for time zone-aware objects'),
..   ('%Z', 'Time Zone name'),
..   ('%j', 'Day of the year'),
..   ('%W', 'Week of the year'),
..   ('%c', 'Date and time representation for the current locale'),
..   ('%x', 'Date representation for the current locale'),
..   ('%X', 'Time representation for the current locale'),
..   ('%%', 'A literal ``%`` character'),
.. ]
.. cog.out('\n')
.. cog.out('.. csv-table:: strptime/strftime format codes\n')
.. cog.out('   :widths: 10, 50, 40\n')
.. cog.out('   :header: "Symbol", "Meaning", "Example"\n')
.. cog.out('\n')
.. for sym, mean in symbols:
..     cog.out('   ``%s``, %s, ``%r``\n' % (sym, mean, d.strftime(sym)))
.. cog.out('\n')
.. }}}

.. csv-table:: strptime/strftime format codes
   :widths: 10, 50, 40
   :header: "Symbol", "Meaning", "Example"

   ``%a``, Abbreviated weekday name, ``'Wed'``
   ``%A``, Full weekday name, ``'Wednesday'``
   ``%w``, Weekday number -- 0 (Sunday) through 6 (Saturday), ``'3'``
   ``%d``, Day of the month (zero padded, ``'13'``
   ``%b``, Abbreviated month name, ``'Jan'``
   ``%B``, Full month name, ``'January'``
   ``%m``, Month of the year, ``'01'``
   ``%y``, Year without century, ``'16'``
   ``%Y``, Year with century, ``'2016'``
   ``%H``, Hour from 24-hour clock, ``'17'``
   ``%I``, Hour from 12-hour clock, ``'05'``
   ``%p``, AM/PM, ``'PM'``
   ``%M``, Minutes, ``'00'``
   ``%S``, Seconds, ``'00'``
   ``%f``, Microseconds, ``'000000'``
   ``%z``, UTC offset for time zone-aware objects, ``'-0500'``
   ``%Z``, Time Zone name, ``'EST'``
   ``%j``, Day of the year, ``'013'``
   ``%W``, Week of the year, ``'02'``
   ``%c``, Date and time representation for the current locale, ``'Wed Jan 13 17:00:00 2016'``
   ``%x``, Date representation for the current locale, ``'01/13/16'``
   ``%X``, Time representation for the current locale, ``'17:00:00'``
   ``%%``, A literal ``%`` character, ``'%'``

.. {{{end}}}

Time Zones
==========

Within :mod:`datetime`, time zones are represented by subclasses of
:class:`tzinfo`. Since :class:`tzinfo` is an abstract base class,
applications need to define a subclass and provide appropriate
implementations for a few methods to make it useful.

:mod:`datetime` does include a somewhat naive implementation in the
class :class:`timezone` that uses a fixed offset from UTC, and does
not support different offset values on different days of the year,
such as where daylight savings time applies, or where the offset from
UTC has changed over time.

.. literalinclude:: datetime_timezone.py
   :caption:
   :start-after: #end_pymotw_header

To convert a datetime value from one time zone to another, use
:func:`astimezone`. In the example above, two separate time zones 6
hours on either side of UTC are shown, and the ``utc`` instance from
``datetime.timezone`` is also used for reference. The final output
line shows the value in the system timezone, acquired by calling
:func:`astimezone` with no argument.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'datetime_timezone.py'))
.. }}}

::

	$ python3 datetime_timezone.py
	
	UTC-06:00 : 2015-12-24 08:48:03.791420-06:00
	UTC+00:00 : 2015-12-24 14:48:03.791420+00:00
	UTC+06:00 : 2015-12-24 20:48:03.791420+06:00
	EST       : 2015-12-24 09:48:03.791420-05:00

.. {{{end}}}


.. note::

   The third party module pytz_ is a better implementation for time
   zones. It supports named time zones, and the offset database is
   kept up to date as changes are made by political bodies around the
   world.

.. seealso::

   * :pydoc:`datetime`

   * :ref:`Porting notes for datetime <porting-datetime>`

   * :mod:`calendar` -- The ``calendar`` module.

   * :mod:`time` -- The ``time`` module.

   * `dateutil <http://labix.org/python-dateutil>`_ -- ``dateutil``
     from Labix extends the ``datetime`` module with additional
     features.

   * pytz_ -- World Time Zone database and classes for making
     :class:`datetime` objects time zone-aware.

   * `WikiPedia: Proleptic Gregorian calendar
     <http://en.wikipedia.org/wiki/Proleptic_Gregorian_calendar>`_ --
     A description of the Gregorian calendar system.

   * `ISO 8601`_ -- The standard for numeric representation of Dates
     and Time

.. _ISO 8601: http://www.iso.org/iso/support/faqs/faqs_widely_used_standards/widely_used_standards_other/date_and_time_format.htm

.. _pytz: http://pytz.sourceforge.net/
