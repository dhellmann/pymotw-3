==========================================================
timeit -- Time the execution of small bits of Python code.
==========================================================

.. module:: timeit
    :synopsis: Time the execution of small bits of Python code.

:Purpose: Time the execution of small bits of Python code.
:Available In: 2.3

The :mod:`timeit` module provides a simple interface for determining
the execution time of small bits of Python code. It uses a
platform-specific time function to provide the most accurate time
calculation possible. It reduces the impact of startup or shutdown
costs on the time calculation by executing the code repeatedly.

Module Contents
===============

:mod:`timeit` defines a single public class, :class:`Timer`. The
constructor for :class:`Timer` takes a statement to be timed, and a
setup statement (to initialize variables, for example). The Python
statements should be strings and can include embedded newlines.

The :func:`timeit()` method runs the setup statement one time, then
executes the primary statement repeatedly and returns the amount of
time which passes. The argument to timeit() controls how many times to
run the statement; the default is 1,000,000.

Basic Example
=============

To illustrate how the various arguments to :class:`Timer` are used,
here is a simple example which prints an identifying value when each
statement is executed:

.. include:: timeit_example.py
    :literal:
    :start-after: #end_pymotw_header

When run, the output is:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'timeit_example.py'))
.. }}}

::

	$ python timeit_example.py
	
	TIMEIT:
	setup
	main statement
	main statement
	1.90734863281e-06
	REPEAT:
	setup
	main statement
	main statement
	setup
	main statement
	main statement
	setup
	main statement
	main statement
	[9.5367431640625e-07, 9.5367431640625e-07, 1.1920928955078125e-06]

.. {{{end}}}

When called, :func:`timeit()` runs the setup statement one time, then
calls the main statement count times. It returns a single floating
point value representing the amount of time it took to run the main
statement count times.

When :func:`repeat()` is used, it calls :func:`timeit()` severeal
times (3 in this case) and all of the responses are returned in a
list.

Storing Values in a Dictionary
==============================

For a more complex example, let's compare the amount of time it takes
to populate a dictionary with a large number of values using a variety
of methods. First, a few constants are needed to configure the
:class:`Timer`. We'll be using a list of tuples containing strings and
integers. The :class:`Timer` will be storing the integers in a
dictionary using the strings as keys.

::

    # {{{cog include('timeit/timeit_dictionary.py', 'header')}}}
    import timeit
    import sys

    # A few constants
    range_size=1000
    count=1000
    setup_statement="l = [ (str(x), x) for x in range(%d) ]; d = {}" % range_size
    # {{{end}}}

Next, we can define a short utility function to print the results in a
useful format. The :func:`timeit()` method returns the amount of time
it takes to execute the statement repeatedly. The output of
:func:`show_results()` converts that into the amount of time it takes
per iteration, and then further reduces the value to the amount of
time it takes to store one item in the dictionary (as averages, of
course).

::

    # {{{cog include('timeit/timeit_dictionary.py', 'show_results')}}}
    def show_results(result):
        "Print results in terms of microseconds per pass and per item."
        global count, range_size
        per_pass = 1000000 * (result / count)
        print '%.2f usec/pass' % per_pass,
        per_item = per_pass / range_size
        print '%.2f usec/item' % per_item

    print "%d items" % range_size
    print "%d iterations" % count
    print
    # {{{end}}}

To establish a baseline, the first configuration tested will use
:func:`__setitem__`.  All of the other variations avoid overwriting
values already in the dictionary, so this simple version should be the
fastest.

Notice that the first argument to :class:`Timer` is a multi-line
string, with indention preserved to ensure that it parses correctly
when run. The second argument is a constant established above to
initialize the list of values and the dictionary.

::

    # {{{cog include('timeit/timeit_dictionary.py', 'setitem')}}}
    # Using __setitem__ without checking for existing values first
    print '__setitem__:\t',
    sys.stdout.flush()
    # using setitem
    t = timeit.Timer("""
    for s, i in l:
        d[s] = i
    """, 
    setup_statement)
    show_results(t.timeit(number=count))
    # {{{end}}}

The next variation uses :func:`setdefault()` to ensure that values
already in the dictionary are not overwritten.

::

    # {{{cog include('timeit/timeit_dictionary.py', 'setdefault')}}}
    # Using setdefault
    print 'setdefault:\t',
    sys.stdout.flush()
    t = timeit.Timer("""
    for s, i in l:
        d.setdefault(s, i)
    """,
    setup_statement)
    show_results(t.timeit(number=count))
    # {{{end}}}

Another way to avoid overwriting existing values is to use
:func:`has_key()` to check the contents of the dictionary explicitly.

::

    # {{{cog include('timeit/timeit_dictionary.py', 'has_key')}}}
    # Using has_key
    print 'has_key:\t',
    sys.stdout.flush()
    # using setitem
    t = timeit.Timer("""
    for s, i in l:
        if not d.has_key(s):
            d[s] = i
    """, 
    setup_statement)
    show_results(t.timeit(number=count))
    # {{{end}}}

Or by adding the value only if we receive a :ref:`KeyError
<exceptions-KeyError>` exception when looking for the existing value.

::

    # {{{cog include('timeit/timeit_dictionary.py', 'exception')}}}
    # Using exceptions
    print 'KeyError:\t',
    sys.stdout.flush()
    # using setitem
    t = timeit.Timer("""
    for s, i in l:
        try:
            existing = d[s]
        except KeyError:
            d[s] = i
    """, 
    setup_statement)
    show_results(t.timeit(number=count))
    # {{{end}}}

And the last method we will test is the (relatively) new form using
"``in``" to determine if a dictionary has a particular key.

::

    # {{{cog include('timeit/timeit_dictionary.py', 'in')}}}
    # Using "in"
    print '"not in":\t',
    sys.stdout.flush()
    # using setitem
    t = timeit.Timer("""
    for s, i in l:
        if s not in d:
            d[s] = i
    """, 
    setup_statement)
    show_results(t.timeit(number=count))
    # {{{end}}}


When run, the script produces output similar to this:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'timeit_dictionary.py'))
.. }}}

::

	$ python timeit_dictionary.py
	
	1000 items
	1000 iterations
	
	__setitem__:	107.40 usec/pass 0.11 usec/item
	setdefault:	228.97 usec/pass 0.23 usec/item
	has_key:	183.76 usec/pass 0.18 usec/item
	KeyError:	120.74 usec/pass 0.12 usec/item
	"not in":	92.42 usec/pass 0.09 usec/item

.. {{{end}}}

Those times are for a MacBook Pro running Python 2.6. Your times will
be different. Experiment with the *range_size* and *count* variables,
since different combinations will produce different results.

From the Command Line
=====================

In addition to the programmatic interface, timeit provides a command
line interface for testing modules without instrumentation.

To run the module, use the new :option:`-m` option to find the module and
treat it as the main program:

::

    $ python -m timeit

For example, to get help:

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m timeit -h', ignore_error=True))
.. }}}

::

	$ python -m timeit -h
	
	Tool for measuring execution time of small code snippets.
	
	This module avoids a number of common traps for measuring execution
	times.  See also Tim Peters' introduction to the Algorithms chapter in
	the Python Cookbook, published by O'Reilly.
	
	Library usage: see the Timer class.
	
	Command line usage:
	    python timeit.py [-n N] [-r N] [-s S] [-t] [-c] [-h] [--] [statement]
	
	Options:
	  -n/--number N: how many times to execute 'statement' (default: see below)
	  -r/--repeat N: how many times to repeat the timer (default 3)
	  -s/--setup S: statement to be executed once initially (default 'pass')
	  -t/--time: use time.time() (default on Unix)
	  -c/--clock: use time.clock() (default on Windows)
	  -v/--verbose: print raw timing results; repeat for more digits precision
	  -h/--help: print this usage message and exit
	  --: separate options from statement, use when statement starts with -
	  statement: statement to be timed (default 'pass')
	
	A multi-line statement may be given by specifying each line as a
	separate argument; indented lines are possible by enclosing an
	argument in quotes and using leading spaces.  Multiple -s options are
	treated similarly.
	
	If -n is not given, a suitable number of loops is calculated by trying
	successive powers of 10 until the total time is at least 0.2 seconds.
	
	The difference in default timer function is because on Windows,
	clock() has microsecond granularity but time()'s granularity is 1/60th
	of a second; on Unix, clock() has 1/100th of a second granularity and
	time() is much more precise.  On either platform, the default timer
	functions measure wall clock time, not the CPU time.  This means that
	other processes running on the same computer may interfere with the
	timing.  The best thing to do when accurate timing is necessary is to
	repeat the timing a few times and use the best time.  The -r option is
	good for this; the default of 3 repetitions is probably enough in most
	cases.  On Unix, you can use clock() to measure CPU time.
	
	Note: there is a certain baseline overhead associated with executing a
	pass statement.  The code here doesn't try to hide it, but you should
	be aware of it.  The baseline overhead can be measured by invoking the
	program without arguments.
	
	The baseline overhead differs between Python versions!  Also, to
	fairly compare older Python versions to Python 2.3, you may want to
	use python -O for the older versions to avoid timing SET_LINENO
	instructions.

.. {{{end}}}

The statement argument works a little differently than the argument to
:class:`Timer`.  Instead of one long string, you pass each line of the
instructions as a separate command line argument. To indent lines
(such as inside a loop), embed spaces in the string by enclosing the
whole thing in quotes. For example:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'python -m timeit -s "d={}" "for i in range(1000):" "  d[str(i)] = i"', interpreter=None))
.. }}}

::

	$ python -m timeit -s "d={}" "for i in range(1000):" "  d[str(i)] = i"
	
	1000 loops, best of 3: 289 usec per loop

.. {{{end}}}

It is also possible to define a function with more complex code, then
import the module and call the function from the command line:

.. include:: timeit_setitem.py
    :literal:
    :start-after: #end_pymotw_header

Then to run the test:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'python -m timeit "import timeit_setitem; timeit_setitem.test_setitem()"', interpreter=None))
.. }}}

::

	$ python -m timeit "import timeit_setitem; timeit_setitem.test_setitem()\
	"
	
	1000 loops, best of 3: 417 usec per loop

.. {{{end}}}


.. seealso::

    `timeit <https://docs.python.org/2/library/timeit.html>`_
        Standard library documentation for this module.

    :mod:`profile`
        The profile module is also useful for performance analysis.
