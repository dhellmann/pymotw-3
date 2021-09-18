=========================================================================
profile, cProfile, and pstats -- Performance analysis of Python programs.
=========================================================================

.. module:: profile
    :synopsis: Performance analysis of Python programs.

.. module:: cProfile
    :synopsis: Performance analysis of Python programs.

:Purpose: Performance analysis of Python programs.
:Available In: 1.4 and later, these examples are for Python 2.5

The :mod:`profile` and :mod:`cProfile` modules provide APIs for
collecting and analyzing statistics about how Python source consumes
processor resources.

run()
=====

The most basic starting point in the profile module is ``run()``.  It
takes a string statement as argument, and creates a report of the time
spent executing different lines of code while running the statement.

.. include:: profile_fibonacci_raw.py
   :literal:
   :start-after: #end_pymotw_header

This recursive version of a fibonacci sequence calculator
[#fibonacci]_ is especially useful for demonstrating the profile
because we can improve the performance so much.  The standard report
format shows a summary and then details for each function executed.

::

    $ python profile_fibonacci_raw.py
    RAW
    ================================================================================
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]
    
             57356 function calls (66 primitive calls) in 0.746 CPU seconds
    
       Ordered by: standard name
    
       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
           21    0.000    0.000    0.000    0.000 :0(append)
           20    0.000    0.000    0.000    0.000 :0(extend)
            1    0.001    0.001    0.001    0.001 :0(setprofile)
            1    0.000    0.000    0.744    0.744 <string>:1(<module>)
            1    0.000    0.000    0.746    0.746 profile:0(print fib_seq(20); print)
            0    0.000             0.000          profile:0(profiler)
     57291/21    0.743    0.000    0.743    0.035 profile_fibonacci_raw.py:13(fib)
         21/1    0.001    0.000    0.744    0.744 profile_fibonacci_raw.py:22(fib_seq)

As you can see, it takes 57356 separate function calls and 3/4 of a
second to run.  Since there are only 66 *primitive* calls, we know
that the vast majority of those 57k calls were recursive.  The details
about where time was spent are broken out by function in the listing
showing the number of calls, total time spent in the function, time
per call (tottime/ncalls), cumulative time spent in a function, and
the ratio of cumulative time to primitive calls.

Not surprisingly, most of the time here is spent calling ``fib()``
repeatedly.  We can add a memoize decorator [#memoize]_ to reduce the
number of recursive calls and have a big impact on the performance of
this function.

.. include:: profile_fibonacci_memoized.py
    :literal:
    :start-after: #end_pymotw_header

By remembering the Fibonacci value at each level we can avoid most of
the recursion and drop down to 145 calls that only take 0.003 seconds.
Also notice that the ncalls count for ``fib()`` shows that it *never*
recurses.

::

    $ python profile_fibonacci_memoized.py
    MEMOIZED
    ================================================================================
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]
    
             145 function calls (87 primitive calls) in 0.003 CPU seconds
    
       Ordered by: standard name
    
       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
           21    0.000    0.000    0.000    0.000 :0(append)
           20    0.000    0.000    0.000    0.000 :0(extend)
            1    0.001    0.001    0.001    0.001 :0(setprofile)
            1    0.000    0.000    0.002    0.002 <string>:1(<module>)
            1    0.000    0.000    0.003    0.003 profile:0(print fib_seq(20); print)
            0    0.000             0.000          profile:0(profiler)
        59/21    0.001    0.000    0.001    0.000 profile_fibonacci_memoized.py:19(__call__)
           21    0.000    0.000    0.001    0.000 profile_fibonacci_memoized.py:26(fib)
         21/1    0.001    0.000    0.002    0.002 profile_fibonacci_memoized.py:36(fib_seq)

runctx()
========

Sometimes, instead of constructing a complex expression for ``run()``,
it is easier to build a simple expression and pass it parameters
through a context, using ``runctx()``.

.. include:: profile_runctx.py
    :literal:
    :start-after: #end_pymotw_header

In this example, the value of "n" is passed through the local variable
context instead of being embedded directly in the statement passed to
``runctx()``.

::

    $ python profile_runctx.py
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]

             145 function calls (87 primitive calls) in 0.003 CPU seconds

       Ordered by: standard name

       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
           21    0.000    0.000    0.000    0.000 :0(append)
           20    0.000    0.000    0.000    0.000 :0(extend)
            1    0.001    0.001    0.001    0.001 :0(setprofile)
            1    0.000    0.000    0.002    0.002 <string>:1(<module>)
            1    0.000    0.000    0.003    0.003 profile:0(print fib_seq(n); print)
            0    0.000             0.000          profile:0(profiler)
        59/21    0.001    0.000    0.001    0.000 profile_fibonacci_memoized.py:19(__call__)
           21    0.000    0.000    0.001    0.000 profile_fibonacci_memoized.py:26(fib)
         21/1    0.001    0.000    0.002    0.002 profile_fibonacci_memoized.py:36(fib_seq)

pstats: Saving and Working With Statistics
==========================================

.. module:: pstats
    :synopsis: Manipulate and analyze profile statistics.

The standard report created by the :mod:`profile` functions is not
very flexible.  If it doesn't meet your needs, you can produce your
own reports by saving the raw profiling data from ``run()`` and
``runctx()`` and processing it separately with the **Stats** class
from :mod:`pstats`.

For example, to run several iterations of the same test and combine
the results, you could do something like this:

.. include:: profile_stats.py
    :literal:
    :start-after: #end_pymotw_header

The output report is sorted in descending order of cumulative time
spent in the function and the directory names are removed from the
printed filenames to conserve horizontal space.

::

    $ python profile_stats.py
    0 [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]
    1 [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]
    2 [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]
    3 [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]
    4 [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]
    Sun Aug 31 11:29:36 2008    profile_stats_0.stats
    Sun Aug 31 11:29:36 2008    profile_stats_1.stats
    Sun Aug 31 11:29:36 2008    profile_stats_2.stats
    Sun Aug 31 11:29:36 2008    profile_stats_3.stats
    Sun Aug 31 11:29:36 2008    profile_stats_4.stats
    
             489 function calls (351 primitive calls) in 0.008 CPU seconds
    
       Ordered by: cumulative time
    
       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            5    0.000    0.000    0.007    0.001 <string>:1(<module>)
        105/5    0.004    0.000    0.007    0.001 profile_fibonacci_memoized.py:36(fib_seq)
            1    0.000    0.000    0.003    0.003 profile:0(print 0, fib_seq(20))
      143/105    0.001    0.000    0.002    0.000 profile_fibonacci_memoized.py:19(__call__)
            1    0.000    0.000    0.001    0.001 profile:0(print 4, fib_seq(20))
            1    0.000    0.000    0.001    0.001 profile:0(print 1, fib_seq(20))
            1    0.000    0.000    0.001    0.001 profile:0(print 2, fib_seq(20))
            1    0.000    0.000    0.001    0.001 profile:0(print 3, fib_seq(20))
           21    0.000    0.000    0.001    0.000 profile_fibonacci_memoized.py:26(fib)
          100    0.001    0.000    0.001    0.000 :0(extend)
          105    0.001    0.000    0.001    0.000 :0(append)
            5    0.001    0.000    0.001    0.000 :0(setprofile)
            0    0.000             0.000          profile:0(profiler)

Limiting Report Contents
========================

Since we are studying the performance of ``fib()`` and ``fib_seq()``,
we can also restrict the output report to only include those functions
using a regular expression to match the ``filename:lineno(function)``
values we want.

.. include:: profile_stats_restricted.py
    :literal:
    :start-after: #end_pymotw_header

The regular expression includes a literal left paren (``(``) to match
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
        105/5    0.004    0.000    0.007    0.001 profile_fibonacci_memoized.py:36(fib_seq)
           21    0.000    0.000    0.001    0.000 profile_fibonacci_memoized.py:26(fib)
    
    
Caller / Callee Graphs
======================

**Stats** also includes methods for printing the callers and callees
of functions.

.. include:: profile_stats_callers.py
    :literal:
    :start-after: #end_pymotw_header

The arguments to ``print_callers()`` and ``print_callees()`` work the
same as the restriction arguments to ``print_stats()``.  The output
shows the caller, callee, and cumulative time.

::

    $ python profile_stats_callers.py
    INCOMING CALLERS:
       Ordered by: cumulative time
       List reduced from 13 to 2 due to restriction <'\\(fib'>
    
    Function                                   was called by...
    profile_fibonacci_memoized.py:36(fib_seq)  <- <string>:1(<module>)(5)    0.007
                                                  profile_fibonacci_memoized.py:36(fib_seq)(100)    0.007
    profile_fibonacci_memoized.py:26(fib)      <- profile_fibonacci_memoized.py:19(__call__)(21)    0.002
    
    
    OUTGOING CALLEES:
       Ordered by: cumulative time
       List reduced from 13 to 2 due to restriction <'\\(fib'>
    
    Function                                   called...
    profile_fibonacci_memoized.py:36(fib_seq)  -> :0(append)(105)    0.001
                                                  :0(extend)(100)    0.001
                                                  profile_fibonacci_memoized.py:19(__call__)(105)    0.002
                                                  profile_fibonacci_memoized.py:36(fib_seq)(100)    0.007
    profile_fibonacci_memoized.py:26(fib)      -> profile_fibonacci_memoized.py:19(__call__)(38)    0.002


.. seealso::

    `profile and cProfile <https://docs.python.org/2.7/library/profile.html>`_
        Standard library documentation for this module.

    `pstats <https://docs.python.org/2.7/library/profile.html#the-stats-class>`_
        Standard library documentation for pstats.

    `Gprof2Dot <http://code.google.com/p/jrfonseca/wiki/Gprof2Dot>`_
        Visualization tool for profile output data.

    .. [#fibonacci] `Fibonacci numbers (Python) - LiteratePrograms <http://en.literateprograms.org/Fibonacci_numbers_(Python)>`_

    .. [#memoize] `Python Decorators: Syntactic Sugar | avinash.vora <http://avinashv.net/2008/04/python-decorators-syntactic-sugar/>`_
