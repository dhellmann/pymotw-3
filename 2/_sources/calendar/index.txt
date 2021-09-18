===========================
calendar -- Work with dates
===========================

.. module:: calendar
    :synopsis: The calendar module implements classes for working with dates to manage year/month/week oriented values.

:Purpose: The calendar module implements classes for working with dates to manage year/month/week oriented values.
:Available In: 1.4, with updates in 2.5

The calendar module defines the Calendar class, which encapsulates
calculations for values such as the dates of the weeks in a given month or
year. In addition, the TextCalendar and HTMLCalendar classes can produce
pre-formatted output.

Formatting Examples
===================

A very simple example which produces formatted text output for a month
using TextCalendar might use the prmonth() method.

.. include:: calendar_textcalendar.py
    :literal:
    :start-after: #end_pymotw_header

The example configures TextCalendar to start weeks on Sunday,
following the American convention. The default is to use the European
convention of starting a week on Monday.

The output looks like:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'calendar_textcalendar.py'))
.. }}}

::

	$ python calendar_textcalendar.py
	
	     July 2007
	Su Mo Tu We Th Fr Sa
	 1  2  3  4  5  6  7
	 8  9 10 11 12 13 14
	15 16 17 18 19 20 21
	22 23 24 25 26 27 28
	29 30 31

.. {{{end}}}


The HTML output for the same time period is slightly different, since there is
no prmonth() method:

.. include:: calendar_htmlcalendar.py
    :literal:
    :start-after: #end_pymotw_header

The rendered output looks roughly the same, but is wrapped with HTML tags.  You can also see that each table cell has a class attribute corresponding to the day of the week.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'calendar_htmlcalendar.py'))
.. }}}

::

	$ python calendar_htmlcalendar.py
	
	<table border="0" cellpadding="0" cellspacing="0" class="month">
	<tr><th colspan="7" class="month">July 2007</th></tr>
	<tr><th class="sun">Sun</th><th class="mon">Mon</th><th class="tue">Tue</th><th class="wed">Wed</th><th class="thu">Thu</th><th class="fri">Fri</th><th class="sat">Sat</th></tr>
	<tr><td class="sun">1</td><td class="mon">2</td><td class="tue">3</td><td class="wed">4</td><td class="thu">5</td><td class="fri">6</td><td class="sat">7</td></tr>
	<tr><td class="sun">8</td><td class="mon">9</td><td class="tue">10</td><td class="wed">11</td><td class="thu">12</td><td class="fri">13</td><td class="sat">14</td></tr>
	<tr><td class="sun">15</td><td class="mon">16</td><td class="tue">17</td><td class="wed">18</td><td class="thu">19</td><td class="fri">20</td><td class="sat">21</td></tr>
	<tr><td class="sun">22</td><td class="mon">23</td><td class="tue">24</td><td class="wed">25</td><td class="thu">26</td><td class="fri">27</td><td class="sat">28</td></tr>
	<tr><td class="sun">29</td><td class="mon">30</td><td class="tue">31</td><td class="noday">&nbsp;</td><td class="noday">&nbsp;</td><td class="noday">&nbsp;</td><td class="noday">&nbsp;</td></tr>
	</table>
	

.. {{{end}}}

If you need to produce output in a format other than one of the available
defaults, you can use :mod:`calendar` to calculate the dates and organize
the values into week and month ranges, then iterate over the result yourself.
The weekheader(), monthcalendar(), and yeardays2calendar() methods of Calendar
are especially useful for that sort of work.

Calling yeardays2calendar() produces a sequence of "month row" lists. Each
list includes the months as another list of weeks. The weeks are lists of
tuples made up of day number (1-31) and weekday number (0-6). Days that fall
outside of the month have a day number of 0.

.. include:: calendar_yeardays2calendar.py
    :literal:
    :start-after: #end_pymotw_header

Calling yeardays2calendar(2007, 2) returns data for 2007, organized with 2
months per row.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'calendar_yeardays2calendar.py'))
.. }}}

::

	$ python calendar_yeardays2calendar.py
	
	[[[[(0, 6), (1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5)],
	   [(7, 6), (8, 0), (9, 1), (10, 2), (11, 3), (12, 4), (13, 5)],
	   [(14, 6), (15, 0), (16, 1), (17, 2), (18, 3), (19, 4), (20, 5)],
	   [(21, 6), (22, 0), (23, 1), (24, 2), (25, 3), (26, 4), (27, 5)],
	   [(28, 6), (29, 0), (30, 1), (31, 2), (0, 3), (0, 4), (0, 5)]],
	  [[(0, 6), (0, 0), (0, 1), (0, 2), (1, 3), (2, 4), (3, 5)],
	   [(4, 6), (5, 0), (6, 1), (7, 2), (8, 3), (9, 4), (10, 5)],
	   [(11, 6), (12, 0), (13, 1), (14, 2), (15, 3), (16, 4), (17, 5)],
	   [(18, 6), (19, 0), (20, 1), (21, 2), (22, 3), (23, 4), (24, 5)],
	   [(25, 6), (26, 0), (27, 1), (28, 2), (0, 3), (0, 4), (0, 5)]]],
	 [[[(0, 6), (0, 0), (0, 1), (0, 2), (1, 3), (2, 4), (3, 5)],
	   [(4, 6), (5, 0), (6, 1), (7, 2), (8, 3), (9, 4), (10, 5)],
	   [(11, 6), (12, 0), (13, 1), (14, 2), (15, 3), (16, 4), (17, 5)],
	   [(18, 6), (19, 0), (20, 1), (21, 2), (22, 3), (23, 4), (24, 5)],
	   [(25, 6), (26, 0), (27, 1), (28, 2), (29, 3), (30, 4), (31, 5)]],
	  [[(1, 6), (2, 0), (3, 1), (4, 2), (5, 3), (6, 4), (7, 5)],
	   [(8, 6), (9, 0), (10, 1), (11, 2), (12, 3), (13, 4), (14, 5)],
	   [(15, 6), (16, 0), (17, 1), (18, 2), (19, 3), (20, 4), (21, 5)],
	   [(22, 6), (23, 0), (24, 1), (25, 2), (26, 3), (27, 4), (28, 5)],
	   [(29, 6), (30, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]]],
	 [[[(0, 6), (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
	   [(6, 6), (7, 0), (8, 1), (9, 2), (10, 3), (11, 4), (12, 5)],
	   [(13, 6), (14, 0), (15, 1), (16, 2), (17, 3), (18, 4), (19, 5)],
	   [(20, 6), (21, 0), (22, 1), (23, 2), (24, 3), (25, 4), (26, 5)],
	   [(27, 6), (28, 0), (29, 1), (30, 2), (31, 3), (0, 4), (0, 5)]],
	  [[(0, 6), (0, 0), (0, 1), (0, 2), (0, 3), (1, 4), (2, 5)],
	   [(3, 6), (4, 0), (5, 1), (6, 2), (7, 3), (8, 4), (9, 5)],
	   [(10, 6), (11, 0), (12, 1), (13, 2), (14, 3), (15, 4), (16, 5)],
	   [(17, 6), (18, 0), (19, 1), (20, 2), (21, 3), (22, 4), (23, 5)],
	   [(24, 6), (25, 0), (26, 1), (27, 2), (28, 3), (29, 4), (30, 5)]]],
	 [[[(1, 6), (2, 0), (3, 1), (4, 2), (5, 3), (6, 4), (7, 5)],
	   [(8, 6), (9, 0), (10, 1), (11, 2), (12, 3), (13, 4), (14, 5)],
	   [(15, 6), (16, 0), (17, 1), (18, 2), (19, 3), (20, 4), (21, 5)],
	   [(22, 6), (23, 0), (24, 1), (25, 2), (26, 3), (27, 4), (28, 5)],
	   [(29, 6), (30, 0), (31, 1), (0, 2), (0, 3), (0, 4), (0, 5)]],
	  [[(0, 6), (0, 0), (0, 1), (1, 2), (2, 3), (3, 4), (4, 5)],
	   [(5, 6), (6, 0), (7, 1), (8, 2), (9, 3), (10, 4), (11, 5)],
	   [(12, 6), (13, 0), (14, 1), (15, 2), (16, 3), (17, 4), (18, 5)],
	   [(19, 6), (20, 0), (21, 1), (22, 2), (23, 3), (24, 4), (25, 5)],
	   [(26, 6), (27, 0), (28, 1), (29, 2), (30, 3), (31, 4), (0, 5)]]],
	 [[[(0, 6), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 5)],
	   [(2, 6), (3, 0), (4, 1), (5, 2), (6, 3), (7, 4), (8, 5)],
	   [(9, 6), (10, 0), (11, 1), (12, 2), (13, 3), (14, 4), (15, 5)],
	   [(16, 6), (17, 0), (18, 1), (19, 2), (20, 3), (21, 4), (22, 5)],
	   [(23, 6), (24, 0), (25, 1), (26, 2), (27, 3), (28, 4), (29, 5)],
	   [(30, 6), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]],
	  [[(0, 6), (1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5)],
	   [(7, 6), (8, 0), (9, 1), (10, 2), (11, 3), (12, 4), (13, 5)],
	   [(14, 6), (15, 0), (16, 1), (17, 2), (18, 3), (19, 4), (20, 5)],
	   [(21, 6), (22, 0), (23, 1), (24, 2), (25, 3), (26, 4), (27, 5)],
	   [(28, 6), (29, 0), (30, 1), (31, 2), (0, 3), (0, 4), (0, 5)]]],
	 [[[(0, 6), (0, 0), (0, 1), (0, 2), (1, 3), (2, 4), (3, 5)],
	   [(4, 6), (5, 0), (6, 1), (7, 2), (8, 3), (9, 4), (10, 5)],
	   [(11, 6), (12, 0), (13, 1), (14, 2), (15, 3), (16, 4), (17, 5)],
	   [(18, 6), (19, 0), (20, 1), (21, 2), (22, 3), (23, 4), (24, 5)],
	   [(25, 6), (26, 0), (27, 1), (28, 2), (29, 3), (30, 4), (0, 5)]],
	  [[(0, 6), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 5)],
	   [(2, 6), (3, 0), (4, 1), (5, 2), (6, 3), (7, 4), (8, 5)],
	   [(9, 6), (10, 0), (11, 1), (12, 2), (13, 3), (14, 4), (15, 5)],
	   [(16, 6), (17, 0), (18, 1), (19, 2), (20, 3), (21, 4), (22, 5)],
	   [(23, 6), (24, 0), (25, 1), (26, 2), (27, 3), (28, 4), (29, 5)],
	   [(30, 6), (31, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]]]]

.. {{{end}}}


This is equivalent to the data used by formatyear()

.. include:: calendar_formatyear.py
    :literal:
    :start-after: #end_pymotw_header

which for the same arguments produces output like:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'calendar_formatyear.py'))
.. }}}

::

	$ python calendar_formatyear.py
	
	                   2007
	
	      January               February
	Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
	    1  2  3  4  5  6               1  2  3
	 7  8  9 10 11 12 13   4  5  6  7  8  9 10
	14 15 16 17 18 19 20  11 12 13 14 15 16 17
	21 22 23 24 25 26 27  18 19 20 21 22 23 24
	28 29 30 31           25 26 27 28
	
	       March                 April
	Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
	             1  2  3   1  2  3  4  5  6  7
	 4  5  6  7  8  9 10   8  9 10 11 12 13 14
	11 12 13 14 15 16 17  15 16 17 18 19 20 21
	18 19 20 21 22 23 24  22 23 24 25 26 27 28
	25 26 27 28 29 30 31  29 30
	
	        May                   June
	Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
	       1  2  3  4  5                  1  2
	 6  7  8  9 10 11 12   3  4  5  6  7  8  9
	13 14 15 16 17 18 19  10 11 12 13 14 15 16
	20 21 22 23 24 25 26  17 18 19 20 21 22 23
	27 28 29 30 31        24 25 26 27 28 29 30
	
	        July                 August
	Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
	 1  2  3  4  5  6  7            1  2  3  4
	 8  9 10 11 12 13 14   5  6  7  8  9 10 11
	15 16 17 18 19 20 21  12 13 14 15 16 17 18
	22 23 24 25 26 27 28  19 20 21 22 23 24 25
	29 30 31              26 27 28 29 30 31
	
	     September              October
	Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
	                   1      1  2  3  4  5  6
	 2  3  4  5  6  7  8   7  8  9 10 11 12 13
	 9 10 11 12 13 14 15  14 15 16 17 18 19 20
	16 17 18 19 20 21 22  21 22 23 24 25 26 27
	23 24 25 26 27 28 29  28 29 30 31
	30
	
	      November              December
	Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
	             1  2  3                     1
	 4  5  6  7  8  9 10   2  3  4  5  6  7  8
	11 12 13 14 15 16 17   9 10 11 12 13 14 15
	18 19 20 21 22 23 24  16 17 18 19 20 21 22
	25 26 27 28 29 30     23 24 25 26 27 28 29
	                      30 31
	

.. {{{end}}}

If you want to format the output yourself for some reason (such as including
links in HTML output), you will find the day_name, day_abbr, month_name, and
month_abbr module attributes useful. They are automatically configured
correctly for the current locale.

Calculating Dates
=================

Although the calendar module focuses mostly on printing full calendars in
various formats, it also provides functions useful for working with dates in
other ways, such as calculating dates for a recurring event. For example, the
Python Atlanta User's Group meets the 2nd Thursday of every month. To
calculate the dates for the meetings for a year, you could use the return
value of monthcalendar().

.. include:: calendar_monthcalendar.py
    :literal:
    :start-after: #end_pymotw_header

Notice that some days are 0. Those are days of the week that overlap
with the given month but which are part of another month.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'calendar_monthcalendar.py'))
.. }}}

::

	$ python calendar_monthcalendar.py
	
	[[0, 0, 0, 0, 0, 0, 1],
	 [2, 3, 4, 5, 6, 7, 8],
	 [9, 10, 11, 12, 13, 14, 15],
	 [16, 17, 18, 19, 20, 21, 22],
	 [23, 24, 25, 26, 27, 28, 29],
	 [30, 31, 0, 0, 0, 0, 0]]

.. {{{end}}}


As mentioned earlier, the first day of the week is Monday. It is possible
to change that by calling setfirstweekday(). On the other hand, since the
calendar module includes constants for indexing into the date ranges returned
by monthcalendar(), it is more convenient to skip that step in this case.

To calculate the PyATL meeting dates for 2007, assuming the second Thursday of
every month, we can use the 0 values to tell us whether the Thursday of the
first week is included in the month (or if the month starts, for example on a
Friday).

.. include:: calendar_secondthursday.py
    :literal:
    :start-after: #end_pymotw_header

So the PyATL meeting schedule for the year is:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'calendar_secondthursday.py'))
.. }}}

::

	$ python calendar_secondthursday.py
	
	  1: 11
	  2:  8
	  3:  8
	  4: 12
	  5: 10
	  6: 14
	  7: 12
	  8:  9
	  9: 13
	 10: 11
	 11:  8
	 12: 13

.. {{{end}}}


.. seealso::

    `calendar <http://docs.python.org/2.7/library/calendar.html>`_
        The standard library documentation for this module.

    :mod:`time`
        Lower-level time functions.

    :mod:`datetime`
        Manipulate date values, including timestamps and time zones.

