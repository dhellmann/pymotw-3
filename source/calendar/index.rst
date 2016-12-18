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
	
	     July 2015
	Su Mo Tu We Th Fr Sa
	          1  2  3  4
	 5  6  7  8  9 10 11
	12 13 14 15 16 17 18
	19 20 21 22 23 24 25
	26 27 28 29 30 31
	 

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

Calling ``yeardays2calendar(2015, 3)`` returns data for 2015,
organized with three months per row.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'calendar_yeardays2calendar.py', break_lines_at=66))
.. }}}

.. code-block:: none

	$ python3 calendar_yeardays2calendar.py
	
	len(cal_data)      : 4
	len(top_months)    : 3
	len(first_month)   : 5
	first_month:
	[[(0, 6), (0, 0), (0, 1), (0, 2), (1, 3), (2, 4), (3, 5)],
	 [(4, 6), (5, 0), (6, 1), (7, 2), (8, 3), (9, 4), (10, 5)],
	 [(11, 6), (12, 0), (13, 1), (14, 2), (15, 3), (16, 4), (17, 5)],
	 [(18, 6), (19, 0), (20, 1), (21, 2), (22, 3), (23, 4), (24, 5)],
	 [(25, 6), (26, 0), (27, 1), (28, 2), (29, 3), (30, 4), (31, 5)]]

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
	
	                              2015
	
	      January               February               March
	Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
	             1  2  3   1  2  3  4  5  6  7   1  2  3  4  5  6  7
	 4  5  6  7  8  9 10   8  9 10 11 12 13 14   8  9 10 11 12 13 14
	11 12 13 14 15 16 17  15 16 17 18 19 20 21  15 16 17 18 19 20 21
	18 19 20 21 22 23 24  22 23 24 25 26 27 28  22 23 24 25 26 27 28
	25 26 27 28 29 30 31                        29 30 31
	
	       April                  May                   June
	Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
	          1  2  3  4                  1  2      1  2  3  4  5  6
	 5  6  7  8  9 10 11   3  4  5  6  7  8  9   7  8  9 10 11 12 13
	12 13 14 15 16 17 18  10 11 12 13 14 15 16  14 15 16 17 18 19 20
	19 20 21 22 23 24 25  17 18 19 20 21 22 23  21 22 23 24 25 26 27
	26 27 28 29 30        24 25 26 27 28 29 30  28 29 30
	                      31
	
	        July                 August              September
	Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
	          1  2  3  4                     1         1  2  3  4  5
	 5  6  7  8  9 10 11   2  3  4  5  6  7  8   6  7  8  9 10 11 12
	12 13 14 15 16 17 18   9 10 11 12 13 14 15  13 14 15 16 17 18 19
	19 20 21 22 23 24 25  16 17 18 19 20 21 22  20 21 22 23 24 25 26
	26 27 28 29 30 31     23 24 25 26 27 28 29  27 28 29 30
	                      30 31
	
	      October               November              December
	Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
	             1  2  3   1  2  3  4  5  6  7         1  2  3  4  5
	 4  5  6  7  8  9 10   8  9 10 11 12 13 14   6  7  8  9 10 11 12
	11 12 13 14 15 16 17  15 16 17 18 19 20 21  13 14 15 16 17 18 19
	18 19 20 21 22 23 24  22 23 24 25 26 27 28  20 21 22 23 24 25 26
	25 26 27 28 29 30 31  29 30                 27 28 29 30 31
	

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
	
	     July 2015
	Mo Tu We Th Fr Sa Su
	       1  2  3  4  5
	 6  7  8  9 10 11 12
	13 14 15 16 17 18 19
	20 21 22 23 24 25 26
	27 28 29 30 31
	 
	    juillet 2015
	Lu Ma Me Je Ve Sa Di
	       1  2  3  4  5
	 6  7  8  9 10 11 12
	13 14 15 16 17 18 19
	20 21 22 23 24 25 26
	27 28 29 30 31
	 

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
	
	[[0, 0, 1, 2, 3, 4, 5],
	 [6, 7, 8, 9, 10, 11, 12],
	 [13, 14, 15, 16, 17, 18, 19],
	 [20, 21, 22, 23, 24, 25, 26],
	 [27, 28, 29, 30, 31, 0, 0]]

.. {{{end}}}


The first day of the week defaults to Monday. It is possible to change
that by calling ``setfirstweekday()``, but since the calendar module
includes constants for indexing into the date ranges returned by
``monthcalendar()``, it is more convenient to skip that step in this
case.

To calculate the group meeting dates for 2015, assuming the second
Thursday of every month, the 0 values indicate whether the Thursday of
the first week is included in the month (or if the month starts, for
example, on a Friday).

.. literalinclude:: calendar_secondthursday.py
    :caption:
    :start-after: #end_pymotw_header

So the meeting schedule for the year is:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'calendar_secondthursday.py'))
.. }}}

.. code-block:: none

	$ python3 calendar_secondthursday.py
	
	Jan:  8
	Feb: 12
	Mar: 12
	Apr:  9
	May: 14
	Jun: 11
	Jul:  9
	Aug: 13
	Sep: 10
	Oct:  8
	Nov: 12
	Dec: 10

.. {{{end}}}


.. seealso::

    * :pydoc:`calendar`

    * :mod:`time` -- Lower-level time functions.

    * :mod:`datetime` -- Manipulate date values, including timestamps
      and time zones.

    * :mod:`locale` -- Locale settings.
