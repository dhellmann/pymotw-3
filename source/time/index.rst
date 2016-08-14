====================
 time --- Clock Time
====================

.. module:: time
    :synopsis: Clock time

:Purpose: Functions for manipulating clock time.

The :mod:`time` module exposes C library functions for manipulating
dates and times.  Since it is tied to the underlying C implementation,
some details (such as the start of the epoch and maximum date value
supported) are platform-specific.  Refer to the library documentation
for complete details.

Choosing a Clock
================

The :mod:`time` module provides access to several different types of
clocks, each useful for different purposes. The standard system calls
like :func:`time` report the system "wall clock" time. The
:func:`monotonic` clock can be used to measure elapsed time in a
long-running process because it is guaranteed never to move backwards,
even if the system time is changed. For performance testing,
:func:`perf_counter` provides access to the clock with the highest
available resolution to make short time measurements more
accurate. The CPU time is available through :func:`time`, and
:func:`process_time` returns the combined processor time and system
time.

Implementation details for the clocks varies by platform. Use
:func:`get_clock_info` to access basic information about the current
implementation, including the clock's resolution.

.. literalinclude:: time_get_clock_info.py
   :caption:
   :start-after: #end_pymotw_header

This output for Mac OS X shows that the monotonic and perf_counter
clocks are implemented using the same underlying system call.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'time_get_clock_info.py'))
.. }}}

.. code-block:: none

	$ python3 time_get_clock_info.py
	
	clock:
	    adjustable    : False
	    implementation: clock()
	    monotonic     : True
	    resolution    : 1e-06
	
	monotonic:
	    adjustable    : False
	    implementation: mach_absolute_time()
	    monotonic     : True
	    resolution    : 1e-09
	
	perf_counter:
	    adjustable    : False
	    implementation: mach_absolute_time()
	    monotonic     : True
	    resolution    : 1e-09
	
	process_time:
	    adjustable    : False
	    implementation: getrusage(RUSAGE_SELF)
	    monotonic     : True
	    resolution    : 1e-06
	
	time:
	    adjustable    : True
	    implementation: gettimeofday()
	    monotonic     : False
	    resolution    : 1e-06
	

.. {{{end}}}

Wall Clock Time
===============

One of the core functions of the :mod:`time` module is :func:`time`,
which returns the number of seconds since the start of the epoch as a
floating point value.

.. literalinclude:: time_time.py
    :caption:
    :start-after: #end_pymotw_header

Although the value is always a float, actual precision is
platform-dependent.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'time_time.py'))
.. }}}

.. code-block:: none

	$ python3 time_time.py
	
	The time is: 1470780871.120458

.. {{{end}}}

The float representation is useful when storing or comparing dates,
but not as useful for producing human readable representations. For
logging or printing time :func:`ctime` can be more useful.

.. literalinclude:: time_ctime.py
    :caption:
    :start-after: #end_pymotw_header

The second :func:`print` call in this example shows how to use
:func:`ctime` to format a time value other than the current time.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'time_ctime.py'))
.. }}}

.. code-block:: none

	$ python3 time_ctime.py
	
	The time is      : Tue Aug  9 18:14:31 2016
	15 secs from now : Tue Aug  9 18:14:46 2016

.. {{{end}}}

Processor Clock Time
====================

While :func:`time` returns a wall clock time, :func:`clock`
returns processor clock time.  The values returned from
:func:`clock` should be used for performance testing, benchmarking,
etc. since they reflect the actual time used by the program, and can
be more precise than the values from :func:`time`.

.. literalinclude:: time_clock.py
    :caption:
    :start-after: #end_pymotw_header

In this example, the formatted :func:`ctime` is printed along with
the floating point values from :func:`time`, and :func:`clock` for
each iteration through the loop.

.. note::

  If you want to run the example on your system, you may have to add
  more cycles to the inner loop or work with a larger amount of data
  to actually see a difference in the times.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'time_clock.py'))
.. }}}

.. code-block:: none

	$ python3 time_clock.py
	
	Tue Aug  9 18:14:31 2016 : 1470780871.206 0.029
	Tue Aug  9 18:14:31 2016 : 1470780871.733 0.555
	Tue Aug  9 18:14:32 2016 : 1470780872.312 1.103
	Tue Aug  9 18:14:32 2016 : 1470780872.903 1.669
	Tue Aug  9 18:14:33 2016 : 1470780873.500 2.263

.. {{{end}}}

Typically, the processor clock does not tick if a program is not doing
anything.

.. literalinclude:: time_clock_sleep.py
    :caption:
    :start-after: #end_pymotw_header

In this example, the loop does very little work by going to sleep
after each iteration. The :func:`time` value increases even while
the application is asleep, but the :func:`clock` value does not.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u time_clock_sleep.py'))
.. }}}

.. code-block:: none

	$ python3 -u time_clock_sleep.py
	
	Tue Aug  9 18:14:34 2016 - 1470780874.18 - 0.05
	Sleeping 3
	Tue Aug  9 18:14:37 2016 - 1470780877.19 - 0.05
	Sleeping 2
	Tue Aug  9 18:14:39 2016 - 1470780879.19 - 0.05
	Sleeping 1
	Tue Aug  9 18:14:40 2016 - 1470780880.19 - 0.05

.. {{{end}}}


Calling :func:`sleep` yields control from the current thread and
asks it to wait for the system to wake it back up. If a program has
only one thread, this effectively blocks the app and it does no work.

Time Components
===============

Storing times as elapsed seconds is useful in some situations, but
there are times when a program needs to have access to the individual
fields of a date (year, month, etc.). The :mod:`time` module defines
:class:`struct_time` for holding date and time values with components
broken out so they are easy to access. There are several functions
that work with :class:`struct_time` values instead of floats.

.. literalinclude:: time_struct.py
    :caption:
    :start-after: #end_pymotw_header

The :func:`gmtime` function returns the current time in
UTC. :func:`localtime` returns the current time with the current
time zone applied. :func:`mktime` takes a :class:`struct_time` and
converts it to the floating point representation.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'time_struct.py'))
.. }}}

.. code-block:: none

	$ python3 time_struct.py
	
	gmtime:
	  tm_year : 2016
	  tm_mon  : 8
	  tm_mday : 9
	  tm_hour : 22
	  tm_min  : 14
	  tm_sec  : 40
	  tm_wday : 1
	  tm_yday : 222
	  tm_isdst: 0
	
	localtime:
	  tm_year : 2016
	  tm_mon  : 8
	  tm_mday : 9
	  tm_hour : 18
	  tm_min  : 14
	  tm_sec  : 40
	  tm_wday : 1
	  tm_yday : 222
	  tm_isdst: 1
	
	mktime: 1470780880.0

.. {{{end}}}



Working with Time Zones
=======================

The functions for determining the current time depend on having the
time zone set, either by the program or by using a default time zone
set for the system. Changing the time zone does not change the actual
time, just the way it is represented.

To change the time zone, set the environment variable ``TZ``, then
call :func:`tzset`.  The time zone can be specified with a lot of
detail, right down to the start and stop times for daylight savings
time. It is usually easier to use the time zone name and let the
underlying libraries derive the other information, though.

This example program changes the time zone to a few different values
and shows how the changes affect other settings in the time module.

.. literalinclude:: time_timezone.py
    :caption:
    :start-after: #end_pymotw_header

The default time zone on the system used to prepare the examples is
US/Eastern. The other zones in the example change the tzname, daylight
flag, and timezone offset value.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'time_timezone.py'))
.. }}}

.. code-block:: none

	$ python3 time_timezone.py
	
	Default :
	  TZ    : (not set)
	  tzname: ('EST', 'EDT')
	  Zone  : 18000 (5.0)
	  DST   : 1
	  Time  : Tue Aug  9 18:14:40 2016
	
	GMT :
	  TZ    : GMT
	  tzname: ('GMT', 'GMT')
	  Zone  : 0 (0.0)
	  DST   : 0
	  Time  : Tue Aug  9 22:14:40 2016
	
	Europe/Amsterdam :
	  TZ    : Europe/Amsterdam
	  tzname: ('CET', 'CEST')
	  Zone  : -3600 (-1.0)
	  DST   : 1
	  Time  : Wed Aug 10 00:14:40 2016
	

.. {{{end}}}

Parsing and Formatting Times
============================

The two functions :func:`strptime` and :func:`strftime` convert
between :class:`struct_time` and string representations of time
values. There is a long list of formatting instructions available to
support input and output in different styles. The complete list is
documented in the library documentation for the :mod:`time` module.

This example converts the current time from a string to a
:class:`struct_time` instance and back to a string.

.. literalinclude:: time_strptime.py
    :caption:
    :start-after: #end_pymotw_header

The output string is not exactly like the input, since the day of the
month is prefixed with a zero.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'time_strptime.py'))
.. }}}

.. code-block:: none

	$ python3 time_strptime.py
	
	Now: Tue Aug  9 18:14:40 2016
	
	Parsed:
	  tm_year : 2016
	  tm_mon  : 8
	  tm_mday : 9
	  tm_hour : 18
	  tm_min  : 14
	  tm_sec  : 40
	  tm_wday : 1
	  tm_yday : 222
	  tm_isdst: -1
	
	Formatted: Tue Aug 09 18:14:40 2016

.. {{{end}}}

.. seealso::

   * :pydoc:`time`

   * :ref:`Porting notes for time <porting-time>`

   * :mod:`datetime` -- The ``datetime`` module includes other classes
     for doing calculations with dates and times.

   * :mod:`calendar` -- Work with higher-level date functions to
     produce calendars or calculate recurring events.
