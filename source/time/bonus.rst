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

::

	$ python time_strptime.py
	
	Now: Sat Dec  4 16:48:14 2010
	
	Parsed:
	  tm_year : 2010
	  tm_mon  : 12
	  tm_mday : 4
	  tm_hour : 16
	  tm_min  : 48
	  tm_sec  : 14
	  tm_wday : 5
	  tm_yday : 338
	  tm_isdst: -1
	
	Formatted: Sat Dec 04 16:48:14 2010

.. {{{end}}}
