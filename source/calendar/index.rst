==============================
 calendar --- Work with Dates
==============================

.. module:: calendar
    :synopsis: Classes for working with year, month, and week-oriented values.

The ``calendar`` module defines the ``Calendar`` class, which
encapsulates calculations for values such as the dates of the weeks in
a given month or year. In addition, the ``TextCalendar`` and
``HTMLCalendar`` classes can produce pre-formatted output.

Formatting Examples
===================

The ``prmonth()`` method is a simple function that produces the
formatted text output for a month.

.. literalinclude:: calendar_textcalendar.py
    :caption:
    :start-after: #end_pymotw_header

The example configures ``TextCalendar`` to start weeks on Sunday,
following the American convention. The default is to use the European
convention of starting a week on Monday.

The output looks like:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'calendar_textcalendar.py'))
.. }}}

.. code-block:: none

	$ python3 calendar_textcalendar.py
	
	     July 2017
	Su Mo Tu We Th Fr Sa
	                   1
	 2  3  4  5  6  7  8
	 9 10 11 12 13 14 15
	16 17 18 19 20 21 22
	23 24 25 26 27 28 29
	30 31
	 

.. {{{end}}}

A similar HTML table can be produced with ``HTMLCalendar`` and
``formatmonth()``.  The rendered output looks roughly the same as
the plain text version, but is wrapped with HTML tags.  Each table
cell has a class attribute corresponding to the day of the week, so
the HTML can be styled through CSS.

To produce output in a format other than one of the available
defaults, use ``calendar`` to calculate the dates and organize the
values into week and month ranges, then iterate over the result.  The
``weekheader()``, ``monthcalendar()``, and
``yeardays2calendar()`` methods of ``Calendar`` are especially
useful for that.

Calling ``yeardays2calendar()`` produces a sequence of "month row"
lists. Each list includes the months as another list of weeks. The
weeks are lists of tuples made up of day number (1-31) and weekday
number (0-6). Days that fall outside of the month have a day number of
0.

.. literalinclude:: calendar_yeardays2calendar.py
    :caption:
    :start-after: #end_pymotw_header

Calling ``yeardays2calendar(2017, 3)`` returns data for 2017,
organized with three months per row.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'calendar_yeardays2calendar.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 calendar_yeardays2calendar.py
	
	len(cal_data)      : 4
	len(top_months)    : 3
	len(first_month)   : 5
	first_month:
	[[(1, 6), (2, 0), (3, 1), (4, 2), (5, 3), (6, 4), (7, 5)],
	 [(8, 6), (9, 0), (10, 1), (11, 2), (12, 3), (13, 4), (14, 5)],
	 [(15, 6), (16, 0), (17, 1), (18, 2), (19, 3), (20, 4), (21,
	5)],
	 [(22, 6), (23, 0), (24, 1), (25, 2), (26, 3), (27, 4), (28,
	5)],
	 [(29, 6), (30, 0), (31, 1), (0, 2), (0, 3), (0, 4), (0, 5)]]

.. {{{end}}}

This is equivalent to the data used by ``formatyear()``.

.. literalinclude:: calendar_formatyear.py
    :caption:
    :start-after: #end_pymotw_header

For the same arguments, ``formatyear()`` produces this output:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'calendar_formatyear.py'))
.. }}}

.. code-block:: none

	$ python3 calendar_formatyear.py
	
	                              2017
	
	      January               February               March
	Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
	 1  2  3  4  5  6  7            1  2  3  4            1  2  3  4
	 8  9 10 11 12 13 14   5  6  7  8  9 10 11   5  6  7  8  9 10 11
	15 16 17 18 19 20 21  12 13 14 15 16 17 18  12 13 14 15 16 17 18
	22 23 24 25 26 27 28  19 20 21 22 23 24 25  19 20 21 22 23 24 25
	29 30 31              26 27 28              26 27 28 29 30 31
	
	       April                  May                   June
	Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
	                   1      1  2  3  4  5  6               1  2  3
	 2  3  4  5  6  7  8   7  8  9 10 11 12 13   4  5  6  7  8  9 10
	 9 10 11 12 13 14 15  14 15 16 17 18 19 20  11 12 13 14 15 16 17
	16 17 18 19 20 21 22  21 22 23 24 25 26 27  18 19 20 21 22 23 24
	23 24 25 26 27 28 29  28 29 30 31           25 26 27 28 29 30
	30
	
	        July                 August              September
	Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
	                   1         1  2  3  4  5                  1  2
	 2  3  4  5  6  7  8   6  7  8  9 10 11 12   3  4  5  6  7  8  9
	 9 10 11 12 13 14 15  13 14 15 16 17 18 19  10 11 12 13 14 15 16
	16 17 18 19 20 21 22  20 21 22 23 24 25 26  17 18 19 20 21 22 23
	23 24 25 26 27 28 29  27 28 29 30 31        24 25 26 27 28 29 30
	30 31
	
	      October               November              December
	Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
	 1  2  3  4  5  6  7            1  2  3  4                  1  2
	 8  9 10 11 12 13 14   5  6  7  8  9 10 11   3  4  5  6  7  8  9
	15 16 17 18 19 20 21  12 13 14 15 16 17 18  10 11 12 13 14 15 16
	22 23 24 25 26 27 28  19 20 21 22 23 24 25  17 18 19 20 21 22 23
	29 30 31              26 27 28 29 30        24 25 26 27 28 29 30
	                                            31
	

.. {{{end}}}

The ``day_name``, ``day_abbr``, ``month_name``, and
``month_abbr`` module attributes useful for producing custom
formatted output (i.e., to include links in the HTML output). They are
automatically configured correctly for the current locale.

Locales
=======

To produce a calendar formatted for a locale other than the current
default, use ``LocaleTextCalendar`` or
``LocaleHTMLCalendar``.

.. literalinclude:: calendar_locale.py
   :caption:
   :start-after: #end_pymotw_header

The first day of the week is not part of the locale settings, and the
value is taken from the argument to the calendar class just as with
the regular ``TextCalendar``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'calendar_locale.py'))
.. }}}

.. code-block:: none

	$ python3 calendar_locale.py
	
	     July 2017
	Mo Tu We Th Fr Sa Su
	                1  2
	 3  4  5  6  7  8  9
	10 11 12 13 14 15 16
	17 18 19 20 21 22 23
	24 25 26 27 28 29 30
	31
	 
	    juillet 2017
	Lu Ma Me Je Ve Sa Di
	                1  2
	 3  4  5  6  7  8  9
	10 11 12 13 14 15 16
	17 18 19 20 21 22 23
	24 25 26 27 28 29 30
	31
	 

.. {{{end}}}



Calculating Dates
=================

Although the calendar module focuses mostly on printing full calendars
in various formats, it also provides functions useful for working with
dates in other ways, such as calculating dates for a recurring
event. For example, the Python Atlanta User's Group meets on the
second Thursday of every month. To calculate the dates for the
meetings for a year, use the return value of ``monthcalendar()``.

.. literalinclude:: calendar_monthcalendar.py
    :caption:
    :start-after: #end_pymotw_header

Some days have a 0 value. Those are days of the week that overlap with
the given month, but that are part of another month.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'calendar_monthcalendar.py'))
.. }}}

.. code-block:: none

	$ python3 calendar_monthcalendar.py
	
	[[0, 0, 0, 0, 0, 1, 2],
	 [3, 4, 5, 6, 7, 8, 9],
	 [10, 11, 12, 13, 14, 15, 16],
	 [17, 18, 19, 20, 21, 22, 23],
	 [24, 25, 26, 27, 28, 29, 30],
	 [31, 0, 0, 0, 0, 0, 0]]

.. {{{end}}}


The first day of the week defaults to Monday. It is possible to change
that by calling ``setfirstweekday()``, but since the calendar module
includes constants for indexing into the date ranges returned by
``monthcalendar()``, it is more convenient to skip that step in this
case.

To calculate the group meeting dates for a year, assuming they are
always on the second Thursday of every month, look at the output of
``monthcalendar()`` to find the dates on which Thursdays fall. The
first and last week of the month are padded with 0 values as
placeholders for the days falling in the preceding or subsequent
month. For example, if a month starts on a Friday, the value in the
first week in the Thursday position will be 0.

.. literalinclude:: calendar_secondthursday.py
    :caption:
    :start-after: #end_pymotw_header

So the meeting schedule for the year is:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'calendar_secondthursday.py 2017'))
.. }}}

.. code-block:: none

	$ python3 calendar_secondthursday.py 2017
	
	Jan: 12
	Feb:  9
	Mar:  9
	Apr: 13
	May: 11
	Jun:  8
	Jul: 13
	Aug: 10
	Sep: 14
	Oct: 12
	Nov:  9
	Dec: 14

.. {{{end}}}


.. seealso::

    * :pydoc:`calendar`

    * :mod:`time` -- Lower-level time functions.

    * :mod:`datetime` -- Manipulate date values, including timestamps
      and time zones.

    * :mod:`locale` -- Locale settings.
