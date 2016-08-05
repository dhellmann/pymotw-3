==========================================
profile and pstats -- Performance Analysis
==========================================

.. module:: profile
    :synopsis: Performance analysis of Python programs.

.. module:: cProfile
    :synopsis: Performance analysis of Python programs.

:Purpose: Performance analysis of Python programs.
:Python Version: 1.4 and later

The :mod:`profile` and :mod:`cProfile` modules provide APIs for
collecting and analyzing statistics about how Python source consumes
processor resources.

.. note::

   This output reports in this section have been reformatted to fit on
   the page.  Lines ending with backslash (``\``) are continued on the
   next line.

Running the Profiler
====================

The most basic starting point in the :mod:`profile` module is
:func:`run`.  It takes a string statement as argument, and creates a
report of the time spent executing different lines of code while
running the statement.

.. include:: profile_fibonacci_raw.py
   :literal:
   :start-after: #end_pymotw_header

This recursive version of a Fibonacci sequence calculator is
especially useful for demonstrating the profile because the
performance can be improved significantly.  The standard report format
shows a summary and then details for each function executed.

::

    $ python profile_fibonacci_raw.py

    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 
    2584, 4181, 6765]
    
             57356 function calls (66 primitive calls) in 0.746 CPU seconds
    
       Ordered by: standard name
    
       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
           21    0.000    0.000    0.000    0.000 :0(append)
           20    0.000    0.000    0.000    0.000 :0(extend)
            1    0.001    0.001    0.001    0.001 :0(setprofile)
            1    0.000    0.000    0.744    0.744 <string>:1(<module>)
            1    0.000    0.000    0.746    0.746 profile:0(\
                                                  print fib_seq(20);print)
            0    0.000             0.000          profile:0(profiler)
     57291/21    0.743    0.000    0.743    0.035 profile_fibonacci_raw.py\
                                                  :10(fib)
         21/1    0.001    0.000    0.744    0.744 profile_fibonacci_raw.py\
                                                  :20(fib_seq)


The raw version takes 57356 separate function calls and 3/4 of a
second to run.  The fact that there are only 66 *primitive* calls says
that the vast majority of those 57k calls were recursive.  The details
about where time was spent are broken out by function in the listing
showing the number of calls, total time spent in the function, time
per call (tottime/ncalls), cumulative time spent in a function, and
the ratio of cumulative time to primitive calls.

Not surprisingly, most of the time here is spent calling :func:`fib`
repeatedly.  Adding a memoize decorator reduces the number
of recursive calls, and has a big impact on the performance of this
function.

.. include:: profile_fibonacci_memoized.py
    :literal:
    :start-after: #end_pymotw_header

By remembering the Fibonacci value at each level, most of the
recursion is avoided and the run drops down to 145 calls that only
take 0.003 seconds.  The :data:`ncalls` count for :func:`fib` shows
that it *never* recurses.

::

    $ python profile_fibonacci_memoized.py

    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 
    2584, 4181, 6765]
    
             145 function calls (87 primitive calls) in 0.003 CPU seconds
    
       Ordered by: standard name
    
       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
           21    0.000    0.000    0.000    0.000 :0(append)
           20    0.000    0.000    0.000    0.000 :0(extend)
            1    0.001    0.001    0.001    0.001 :0(setprofile)
            1    0.000    0.000    0.002    0.002 <string>:1(<module>)
            1    0.000    0.000    0.003    0.003 profile:0(\
                                                  print fib_seq(20); print)
            0    0.000             0.000          profile:0(profiler)
        59/21    0.001    0.000    0.001    0.000 profile_fibonacci_\
                                                  memoized.py:17(__call__)
           21    0.000    0.000    0.001    0.000 profile_fibonacci_\
                                                  memoized.py:24(fib)
         21/1    0.001    0.000    0.002    0.002 profile_fibonacci_\
                                                  memoized.py:35(fib_seq)


Running in a Context
====================

Sometimes, instead of constructing a complex expression for :func:`run`,
it is easier to build a simple expression and pass it parameters
through a context, using :func:`runctx`.

.. include:: profile_runctx.py
    :literal:
    :start-after: #end_pymotw_header

In this example, the value of :data:`n` is passed through the local
variable context instead of being embedded directly in the statement
passed to :func:`runctx`.

::

    $ python profile_runctx.py

    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 
    2584, 4181, 6765]

             145 function calls (87 primitive calls) in 0.003 CPU seconds

       Ordered by: standard name

       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
           21    0.000    0.000    0.000    0.000 :0(append)
           20    0.000    0.000    0.000    0.000 :0(extend)
            1    0.001    0.001    0.001    0.001 :0(setprofile)
            1    0.000    0.000    0.002    0.002 <string>:1(<module>)
            1    0.000    0.000    0.003    0.003 profile:0(\
                                                  print fib_seq(n); print)
            0    0.000             0.000          profile:0(profiler)
        59/21    0.001    0.000    0.001    0.000 profile_fibonacci_\
                                                  memoized.py:17(__call__)
           21    0.000    0.000    0.001    0.000 profile_fibonacci_\
                                                  memoized.py:24(fib)
         21/1    0.001    0.000    0.002    0.002 profile_fibonacci_\
                                                  memoized.py:35(fib_seq)

pstats: Saving and Working With Statistics
==========================================

.. module:: pstats
    :synopsis: Manipulate and analyze profile statistics.

The standard report created by the :mod:`profile` functions is not
very flexible.  However, custom reports can be produced by saving the
raw profiling data from :func:`run` and :func:`runctx` and processing
it separately with the :class:`pstats.Stats` class.

This example runs several iterations of the same test and combines the
results:

.. include:: profile_stats.py
    :literal:
    :start-after: #end_pymotw_header

The output report is sorted in descending order of cumulative time
spent in the function and the directory names are removed from the
printed filenames to conserve horizontal space on the page.

::

    $ python profile_stats.py

    0 [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 
     987, 1597, 2584, 4181, 6765]
    1 [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 
     987, 1597, 2584, 4181, 6765]
    2 [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 
     987, 1597, 2584, 4181, 6765]
    3 [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 
     987, 1597, 2584, 4181, 6765]
    4 [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 
     987, 1597, 2584, 4181, 6765]
    Sun Aug 31 11:29:36 2008    profile_stats_0.stats
    Sun Aug 31 11:29:36 2008    profile_stats_1.stats
    Sun Aug 31 11:29:36 2008    profile_stats_2.stats
    Sun Aug 31 11:29:36 2008    profile_stats_3.stats
    Sun Aug 31 11:29:36 2008    profile_stats_4.stats
    
             489 function calls (351 primitive calls) in 0.008 CPU seconds
    
       Ordered by: cumulative time
    
       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            5    0.000    0.000    0.007    0.001 <string>:1(<module>)
        105/5    0.004    0.000    0.007    0.001 profile_fibonacci_\
                                                  memoized.py:36(fib_seq)
            1    0.000    0.000    0.003    0.003 profile:0(print 0, \
                                                  fib_seq(20))
      143/105    0.001    0.000    0.002    0.000 profile_fibonacci_\
                                                  memoized.py:19(__call__)
            1    0.000    0.000    0.001    0.001 profile:0(print 4, \
                                                  fib_seq(20))
            1    0.000    0.000    0.001    0.001 profile:0(print 1, \
                                                  fib_seq(20))
            1    0.000    0.000    0.001    0.001 profile:0(print 2, \
                                                  fib_seq(20))
            1    0.000    0.000    0.001    0.001 profile:0(print 3, \
                                                  fib_seq(20))
           21    0.000    0.000    0.001    0.000 profile_fibonacci_\
                                                  memoized.py:26(fib)
          100    0.001    0.000    0.001    0.000 :0(extend)
          105    0.001    0.000    0.001    0.000 :0(append)
            5    0.001    0.000    0.001    0.000 :0(setprofile)
            0    0.000             0.000          profile:0(profiler)

Limiting Report Contents
========================

The output can be restricted by function.  This version only shows
information about the performance of :func:`fib` and :func:`fib_seq`
by using a regular expression to match the desired
``filename:lineno(function)`` values.

.. include:: profile_stats_restricted.py
    :literal:
    :start-after: #end_pymotw_header

The regular expression includes a literal left parenthesis (``(``) to match
against the function name portion of the location value.

::

    $ python profile_stats_restricted.py

    Sun Aug 31 11:29:36 2008    profile_stats_0.stats
    Sun Aug 31 11:29:36 2008    profile_stats_1.stats
    Sun Aug 31 11:29:36 2008    profile_stats_2.stats
    Sun Aug 31 11:29:36 2008    profile_stats_3.stats
    Sun Aug 31 11:29:36 2008    profile_stats_4.stats
    
             489 function calls (351 primitive calls) in 0.008 CPU seconds
    
       Ordered by: cumulative time
       List reduced from 13 to 2 due to restriction <'\\(fib'>
    
       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        105/5    0.004    0.000    0.007    0.001 profile_fibonacci_\
                                                  memoized.py:36(fib_seq)
           21    0.000    0.000    0.001    0.000 profile_fibonacci_\
                                                  memoized.py:26(fib)
    
    
Caller / Callee Graphs
======================

:class:`Stats` also includes methods for printing the callers and callees
of functions.

.. include:: profile_stats_callers.py
    :literal:
    :start-after: #end_pymotw_header

The arguments to :func:`print_callers` and :func:`print_callees` work
the same as the restriction arguments to :func:`print_stats`.  The
output shows the caller, callee, number of calls, and cumulative time.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'profile_stats_callers.py',
..                    break_lines_at=71, line_break_mode='continue'))
.. }}}

::

	$ python profile_stats_callers.py
	
	INCOMING CALLERS:
	   Ordered by: cumulative time
	   List reduced from 7 to 2 due to restriction <'\\(fib'>
	
	Function                                   was called by...
	                                               ncalls  tottime  cumtime
	profile_fibonacci_memoized.py:35(fib_seq)  <-       5    0.000    0.001\
	  <string>:1(<module>)
	                                                100/5    0.000    0.001\
	  profile_fibonacci_memoized.py:35(fib_seq)
	profile_fibonacci_memoized.py:24(fib)      <-      21    0.000    0.000\
	  profile_fibonacci_memoized.py:17(__call__)
	
	
	OUTGOING CALLEES:
	   Ordered by: cumulative time
	   List reduced from 7 to 2 due to restriction <'\\(fib'>
	
	Function                                   called...
	                                               ncalls  tottime  cumtime
	profile_fibonacci_memoized.py:35(fib_seq)  ->     105    0.000    0.000\
	  profile_fibonacci_memoized.py:17(__call__)
	                                                100/5    0.000    0.001\
	  profile_fibonacci_memoized.py:35(fib_seq)
	                                                  105    0.000    0.000\
	  {method 'append' of 'list' objects}
	                                                  100    0.000    0.000\
	  {method 'extend' of 'list' objects}
	profile_fibonacci_memoized.py:24(fib)      ->      38    0.000    0.000\
	  profile_fibonacci_memoized.py:17(__call__)
	
	

.. {{{end}}}



.. seealso::

    `profile and cProfile <http://docs.python.org/lib/module-profile.html>`_
        Standard library documentation for this module.

    `pstats <http://docs.python.org/lib/profile-stats.html>`_
        Standard library documentation for pstats.

    `Gprof2Dot <http://code.google.com/p/jrfonseca/wiki/Gprof2Dot>`_
        Visualization tool for profile output data.

    `Fibonacci numbers (Python) - LiteratePrograms <http://en.literateprograms.org/Fibonacci_numbers_(Python)>`__
        An implementation of a Fibonacci sequence generator in Python.

    `Python Decorators: Syntactic Sugar | avinash.vora <http://avinashv.net/2008/04/python-decorators-syntactic-sugar/>`__
        Another memoized Fibonacci sequence generator in Python.
        
