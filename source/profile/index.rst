=============================================
 profile and pstats --- Performance Analysis
=============================================

.. module:: profile
    :synopsis: Performance analysis of Python programs.

:Purpose: Performance analysis of Python programs.

The :mod:`profile` module provides APIs for collecting and analyzing
statistics about how Python source consumes processor resources.

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

.. literalinclude:: profile_fibonacci_raw.py
   :caption:
   :start-after: #end_pymotw_header

This recursive version of a Fibonacci sequence calculator is
especially useful for demonstrating the profile because the
performance can be improved significantly.  The standard report format
shows a summary and then details for each function executed.

.. cog.out(run_script(cog.inFile, 'profile_fibonacci_raw.py', line_break_mode='continue'))

.. code-block:: none

	$ python3 profile_fibonacci_raw.py
	
	[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 
	987, 1597, 2584, 4181, 6765]
	
	         57359 function calls (69 primitive calls) in 0.146 \
	seconds
	
	   Ordered by: standard name
	
	   ncalls  tottime  percall  cumtime  percall filename:lineno(\
	function)
	       21    0.000    0.000    0.000    0.000 :0(append)
	        1    0.000    0.000    0.145    0.145 :0(exec)
	       20    0.000    0.000    0.000    0.000 :0(extend)
	        2    0.000    0.000    0.000    0.000 :0(print)
	        1    0.001    0.001    0.001    0.001 :0(setprofile)
	        1    0.000    0.000    0.145    0.145 <string>:1(<module\
	>)
	        1    0.000    0.000    0.146    0.146 profile:0(print(fi\
	b_seq(20)); print())
	        0    0.000             0.000          profile:0(profiler\
	)
	 57291/21    0.145    0.000    0.145    0.007 profile_fibonacci_\
	raw.py:11(fib)
	     21/1    0.000    0.000    0.145    0.145 profile_fibonacci_\
	raw.py:22(fib_seq)

The raw version takes 57291 separate function calls and 0.146 seconds
to run.  The fact that there are only 69 *primitive* calls says that
the vast majority of those 57k calls were recursive.  The details
about where time was spent are broken out by function in the listing
showing the number of calls, total time spent in the function, time
per call (tottime/ncalls), cumulative time spent in a function, and
the ratio of cumulative time to primitive calls.

Not surprisingly, most of the time here is spent calling :func:`fib`
repeatedly.  Adding a memoize decorator reduces the number of
recursive calls, and has a big impact on the performance of this
function.

.. literalinclude:: profile_fibonacci_memoized.py
   :caption:
   :start-after: #end_pymotw_header

By remembering the Fibonacci value at each level, most of the
recursion is avoided and the run drops down to 148 calls that only
take 0.002 seconds.  The :data:`ncalls` count for :func:`fib` shows
that it *never* recurses.

.. cog.out(run_script(cog.inFile, 'profile_fibonacci_memoized.py', line_break_mode='continue'))

.. code-block:: none

	$ python3 profile_fibonacci_memoized.py
	
	[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 
	987, 1597, 2584, 4181, 6765]
	
         148 function calls (90 primitive calls) in 0.002 seconds
	
	   Ordered by: standard name
	
	   ncalls  tottime  percall  cumtime  percall filename:lineno(\
	function)
	       21    0.000    0.000    0.000    0.000 :0(append)
	        1    0.000    0.000    0.001    0.001 :0(exec)
	       20    0.000    0.000    0.000    0.000 :0(extend)
	        2    0.000    0.000    0.000    0.000 :0(print)
	        1    0.001    0.001    0.001    0.001 :0(setprofile)
	        1    0.000    0.000    0.001    0.001 <string>:1(<module\
	>)
	        1    0.000    0.000    0.002    0.002 profile:0(print(fi\
	b_seq(20)); print())
	        0    0.000             0.000          profile:0(profiler\
	)
	    59/21    0.000    0.000    0.000    0.000 profile_fibonacci_\
	memoized.py:19(__call__)
	       21    0.000    0.000    0.000    0.000 profile_fibonacci_\
	memoized.py:27(fib)
	     21/1    0.000    0.000    0.001    0.001 profile_fibonacci_\
	memoized.py:39(fib_seq)


Running in a Context
====================

Sometimes, instead of constructing a complex expression for :func:`run`,
it is easier to build a simple expression and pass it parameters
through a context, using :func:`runctx`.

.. literalinclude:: profile_runctx.py
   :caption:
   :start-after: #end_pymotw_header

In this example, the value of :data:`n` is passed through the local
variable context instead of being embedded directly in the statement
passed to :func:`runctx`.

.. cog.out(run_script(cog.inFile, 'profile_runctx.py', line_break_mode='continue'))

.. code-block:: none

	$ python3 profile_runctx.py
	
	[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 
	987, 1597, 2584, 4181, 6765]
	
	        148 function calls (90 primitive calls) in 0.002 seconds
	
	   Ordered by: standard name
	
	   ncalls  tottime  percall  cumtime  percall filename:lineno(\
	function)
	       21    0.000    0.000    0.000    0.000 :0(append)
	        1    0.000    0.000    0.001    0.001 :0(exec)
	       20    0.000    0.000    0.000    0.000 :0(extend)
	        2    0.000    0.000    0.000    0.000 :0(print)
	        1    0.001    0.001    0.001    0.001 :0(setprofile)
	        1    0.000    0.000    0.001    0.001 <string>:1(<module\
	>)
	        1    0.000    0.000    0.002    0.002 profile:0(print(fi\
	b_seq(n)); print())
	        0    0.000             0.000          profile:0(profiler\
	)
	    59/21    0.000    0.000    0.000    0.000 profile_fibonacci_\
	memoized.py:19(__call__)
	       21    0.000    0.000    0.000    0.000 profile_fibonacci_\
	memoized.py:27(fib)
	     21/1    0.000    0.000    0.001    0.001 profile_fibonacci_\
	memoized.py:39(fib_seq)

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

.. literalinclude:: profile_stats.py
   :caption:
   :start-after: #end_pymotw_header

The output report is sorted in descending order of cumulative time
spent in the function and the directory names are removed from the
printed filenames to conserve horizontal space on the page.

.. cog.out(run_script(cog.inFile, 'profile_stats.py', line_break_mode='continue'))

.. code-block:: none

	$ python3 profile_stats.py
	
	0 [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, \
	987, 1597, 2584, 4181, 6765]
	1 [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, \
	987, 1597, 2584, 4181, 6765]
	2 [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, \
	987, 1597, 2584, 4181, 6765]
	3 [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, \
	987, 1597, 2584, 4181, 6765]
	4 [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, \
	987, 1597, 2584, 4181, 6765]
	Fri Aug  5 17:56:16 2016    profile_stats_0.stats
	Fri Aug  5 17:56:16 2016    profile_stats_1.stats
	Fri Aug  5 17:56:16 2016    profile_stats_2.stats
	Fri Aug  5 17:56:16 2016    profile_stats_3.stats
	Fri Aug  5 17:56:16 2016    profile_stats_4.stats
	
	  494 function calls (356 primitive calls) in 0.001 seconds
	
	   Ordered by: cumulative time
	
	   ncalls  tottime  percall  cumtime  percall filename:lineno(\
	function)
	        5    0.000    0.000    0.001    0.000 {built-in method \
	builtins.exec}
	        5    0.000    0.000    0.001    0.000 <string>:1(<module\
	>)
	    105/5    0.000    0.000    0.001    0.000 profile_fibonacci_\
	memoized.py:39(fib_seq)
	  143/105    0.000    0.000    0.000    0.000 profile_fibonacci_\
	memoized.py:19(__call__)
	        5    0.000    0.000    0.000    0.000 {built-in method b\
	uiltins.print}
	       21    0.000    0.000    0.000    0.000 profile_fibonacci_\
	memoized.py:27(fib)
	      100    0.000    0.000    0.000    0.000 {method 'extend' \
	of 'list' objects}
	      105    0.000    0.000    0.000    0.000 {method 'append' \
	of 'list' objects}
	        5    0.000    0.000    0.000    0.000 {method 'disable' \
	of '_lsprof.Profiler' objects}

Limiting Report Contents
========================

The output can be restricted by function.  This version only shows
information about the performance of :func:`fib` and :func:`fib_seq`
by using a regular expression to match the desired
``filename:lineno(function)`` values.

.. literalinclude:: profile_stats_restricted.py
   :caption:
   :start-after: #end_pymotw_header

The regular expression includes a literal left parenthesis (``(``) to match
against the function name portion of the location value.

.. cog.out(run_script(cog.inFile, 'profile_stats_restricted.py'))

.. code-block:: none

	$ python3 profile_stats_restricted.py
	
	Fri Aug  5 17:56:16 2016    profile_stats_0.stats
	Fri Aug  5 17:56:16 2016    profile_stats_1.stats
	Fri Aug  5 17:56:16 2016    profile_stats_2.stats
	Fri Aug  5 17:56:16 2016    profile_stats_3.stats
	Fri Aug  5 17:56:16 2016    profile_stats_4.stats
	
	       494 function calls (356 primitive calls) in 0.001 seconds
	
	   Ordered by: cumulative time
	   List reduced from 9 to 2 due to restriction <'\\(fib'>
	
	   ncalls  tottime  percall  cumtime  percall filename:lineno(\
	function)
	    105/5    0.000    0.000    0.001    0.000 profile_fibonacci_\
	memoized.py:39(fib_seq)
	       21    0.000    0.000    0.000    0.000 profile_fibonacci_\
	memoized.py:27(fib)

 
Caller / Callee Graphs
======================

:class:`Stats` also includes methods for printing the callers and callees
of functions.

.. literalinclude:: profile_stats_callers.py
   :caption:
   :start-after: #end_pymotw_header

The arguments to :func:`print_callers` and :func:`print_callees` work
the same as the restriction arguments to :func:`print_stats`.  The
output shows the caller, callee, number of calls, and cumulative time.

.. cog.out(run_script(cog.inFile, 'profile_stats_callers.py',
..                    line_break_mode='continue'))

.. code-block:: none

	$ python3 profile_stats_callers.py
	
	INCOMING CALLERS:
	   Ordered by: cumulative time
	   List reduced from 9 to 2 due to restriction <'\\(fib'>
	
	Function                                   was called by...
	                                               ncalls  tottime  \
	cumtime
	profile_fibonacci_memoized.py:39(fib_seq)  <-       5    0.000  \
	  0.001  <string>:1(<module>)
	                                                100/5    0.000  \
	  0.001  profile_fibonacci_memoized.py:39(fib_seq)
	profile_fibonacci_memoized.py:27(fib)      <-      21    0.000  \
	  0.000  profile_fibonacci_memoized.py:19(__call__)
	
	
	OUTGOING CALLEES:
	   Ordered by: cumulative time
	   List reduced from 9 to 2 due to restriction <'\\(fib'>
	
	Function                                   called...
	                                               ncalls  tottime  \
	cumtime
	profile_fibonacci_memoized.py:39(fib_seq)  ->     105    0.000  \
	  0.000  profile_fibonacci_memoized.py:19(__call__)
	                                                100/5    0.000  \
	  0.001  profile_fibonacci_memoized.py:39(fib_seq)
	                                                  105    0.000  \
	  0.000  {method 'append' of 'list' objects}
	                                                  100    0.000  \
	  0.000  {method 'extend' of 'list' objects}
	profile_fibonacci_memoized.py:27(fib)      ->      38    0.000  \
	  0.000  profile_fibonacci_memoized.py:19(__call__)


.. seealso::

   * :pydoc:`profile`

   * `The Stats Class
     <https://docs.python.org/3.5/library/profile.html#the-stats-class>`__
     -- Standard library documentation for :class:`pstats.Stats`.

   * `Gprof2Dot <http://code.google.com/p/jrfonseca/wiki/Gprof2Dot>`__
     -- Visualization tool for profile output data.

   * `Fibonacci numbers (Python) - LiteratePrograms
     <http://en.literateprograms.org/Fibonacci_numbers_(Python)>`__ --
     An implementation of a Fibonacci sequence generator in Python.

   * `Python Decorators: Syntactic Sugar | avinash.vora
     <http://avinashv.net/2008/04/python-decorators-syntactic-sugar/>`__
     -- Another memoized Fibonacci sequence generator in Python.

   * `Smiley <https://github.com/dhellmann/smiley>`__ -- Python
     Application Tracer
