==============================
 trace -- Follow Program Flow
==============================

.. module:: trace
    :synopsis: Follow Program FLow

:Purpose: Monitor which statements and functions are executed as a program runs to produce coverage and call-graph information.

The :mod:`trace` module is useful for understanding the way a program
runs.  It watches the statements executed, produces coverage reports,
and helps investigate the relationships between functions that call
each other.

Example Program
===============

This program will be used in the examples in the rest of the section.
It imports another module called ``recurse`` and then runs a function
from it.

.. literalinclude:: trace_example/main.py
    :caption:
    :start-after: #end_pymotw_header

The :func:`recurse` function invokes itself until the level argument
reaches ``0``.

.. literalinclude:: trace_example/recurse.py
    :caption:
    :start-after: #end_pymotw_header

Tracing Execution
=================

It is easy use :mod:`trace` directly from the command line.  
The statements being executed as the program runs are printed when the
:option:`--trace` option is given.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m trace --trace trace_example/main.py'))
.. }}}

::

	$ python -m trace --trace trace_example/main.py
	
	 --- modulename: threading, funcname: settrace
	threading.py(89):     _trace_hook = func
	 --- modulename: trace, funcname: <module>
	<string>(1):   --- modulename: trace, funcname: <module>
	main.py(7): """
	main.py(12): from recurse import recurse
	 --- modulename: recurse, funcname: <module>
	recurse.py(7): """
	recurse.py(12): def recurse(level):
	recurse.py(18): def not_called():
	main.py(14): def main():
	main.py(19): if __name__ == '__main__':
	main.py(20):     main()
	 --- modulename: trace, funcname: main
	main.py(15):     print 'This is the main program.'
	This is the main program.
	main.py(16):     recurse(2)
	 --- modulename: recurse, funcname: recurse
	recurse.py(13):     print 'recurse(%s)' % level
	recurse(2)
	recurse.py(14):     if level:
	recurse.py(15):         recurse(level-1)
	 --- modulename: recurse, funcname: recurse
	recurse.py(13):     print 'recurse(%s)' % level
	recurse(1)
	recurse.py(14):     if level:
	recurse.py(15):         recurse(level-1)
	 --- modulename: recurse, funcname: recurse
	recurse.py(13):     print 'recurse(%s)' % level
	recurse(0)
	recurse.py(14):     if level:
	recurse.py(16):     return
	recurse.py(16):     return
	recurse.py(16):     return
	main.py(17):     return

.. {{{end}}}

The first part of the output shows the setup operations performed by
:mod:`trace`.  The rest of the output shows the entry into each
function, including the module where the function is located, and then
the lines of the source file as they are executed.  :func:`recurse`
is entered three times, as expected based on the way it is called in
:func:`main`.

Code Coverage
=============

Running :mod:`trace` from the command line with the :option:`--count`
option will produce code coverage report information, detailing which
lines are run and which are skipped.  Since a complex program is
usually made up of multiple files, a separate coverage report is
produced for each.  By default the coverage report files are written
to the same directory as the module, named after the module but with a
``.cover`` extension instead of ``.py``.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m trace --count trace_example/main.py'))
.. }}}

::

	$ python -m trace --count trace_example/main.py
	
	This is the main program.
	recurse(2)
	recurse(1)
	recurse(0)

.. {{{end}}}

Two output files are produced, ``trace_example/main.cover``:

.. literalinclude:: trace_example/main.cover
    :caption:
    :start-after: #end_pymotw_header

and ``trace_example/recurse.cover``:

.. literalinclude:: trace_example/recurse.cover
    :caption:
    :start-after: #end_pymotw_header

.. note:: 

    Although the line ``def recurse(level):`` has a count of ``1``,
    that does not mean the function was only run once.  It means the
    function *definition* was only executed once.

It is also possible to run the program several times, perhaps with
different options, to save the coverage data and produce a combined
report.

.. {{{cog
.. (path(cog.inFile).parent / 'coverdir1').rmtree()
.. (path(cog.inFile).parent / 'coverdir1').mkdir()
.. cog.out(run_script(cog.inFile, '-m trace --coverdir coverdir1 --count --file coverdir1/coverage_report.dat trace_example/main.py', break_lines_at=70))
.. cog.out(run_script(cog.inFile, '-m trace --coverdir coverdir1 --count --file coverdir1/coverage_report.dat trace_example/main.py', include_prefix=False, break_lines_at=70))
.. cog.out(run_script(cog.inFile, '-m trace --coverdir coverdir1 --count --file coverdir1/coverage_report.dat trace_example/main.py', include_prefix=False, break_lines_at=70))
.. }}}

::

	$ python -m trace --coverdir coverdir1 --count --file coverdir1/cove\
	rage_report.dat trace_example/main.py
	
	Skipping counts file 'coverdir1/coverage_report.dat': [Errno 2] No suc
	h file or directory: 'coverdir1/coverage_report.dat'
	This is the main program.
	recurse(2)
	recurse(1)
	recurse(0)

	$ python -m trace --coverdir coverdir1 --count --file coverdir1/cove\
	rage_report.dat trace_example/main.py
	
	This is the main program.
	recurse(2)
	recurse(1)
	recurse(0)

	$ python -m trace --coverdir coverdir1 --count --file coverdir1/cove\
	rage_report.dat trace_example/main.py
	
	This is the main program.
	recurse(2)
	recurse(1)
	recurse(0)

.. {{{end}}}

To produce reports once the coverage information is recorded to the
``.cover`` files, use the :option:`--report` option.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m trace --coverdir coverdir1 --report --summary --missing --file coverdir1/coverage_report.dat trace_example/main.py', break_lines_at=70))
.. }}}

::

	$ python -m trace --coverdir coverdir1 --report --summary --missing \
	--file coverdir1/coverage_report.dat trace_example/main.py
	
	lines   cov%   module   (path)
	  599     0%   threading   (/Library/Frameworks/Python.framework/Versi
	ons/2.7/lib/python2.7/threading.py)
	    8   100%   trace_example.main   (trace_example/main.py)
	    8    87%   trace_example.recurse   (trace_example/recurse.py)

.. {{{end}}}

Since the program ran three times, the coverage report shows values
three times higher than the first report.  The :option:`--summary`
option adds the percent covered information to the output.  The
``recurse`` module is only 87% covered.  Looking at the cover file for
``recurse`` shows that the body of ``not_called`` is indeed never
run, indicated by the ``>>>>>>`` prefix.

.. literalinclude:: coverdir1/trace_example.recurse.cover
    :caption:
    :start-after: #end_pymotw_header

Calling Relationships
=====================

In addition to coverage information, :mod:`trace` will collect and
report on the relationships between functions that call each other.

For a simple list of the functions called, use :option:`--listfuncs`:

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m trace --listfuncs trace_example/main.py', break_lines_at=70))
.. }}}

::

	$ python -m trace --listfuncs trace_example/main.py
	
	This is the main program.
	recurse(2)
	recurse(1)
	recurse(0)
	
	functions called:
	filename: /Library/Frameworks/Python.framework/Versions/2.7/lib/python
	2.7/threading.py, modulename: threading, funcname: settrace
	filename: <string>, modulename: <string>, funcname: <module>
	filename: trace_example/main.py, modulename: main, funcname: <module>
	filename: trace_example/main.py, modulename: main, funcname: main
	filename: trace_example/recurse.py, modulename: recurse, funcname: <mo
	dule>
	filename: trace_example/recurse.py, modulename: recurse, funcname: rec
	urse

.. {{{end}}}

For more details about who is doing the calling, use
:option:`--trackcalls`.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m trace --listfuncs --trackcalls trace_example/main.py', break_lines_at=70))
.. }}}

::

	$ python -m trace --listfuncs --trackcalls trace_example/main.py
	
	This is the main program.
	recurse(2)
	recurse(1)
	recurse(0)
	
	calling relationships:
	
	*** /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/tr
	ace.py ***
	  --> /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/
	threading.py
	    trace.Trace.run -> threading.settrace
	  --> <string>
	    trace.Trace.run -> <string>.<module>
	
	*** <string> ***
	  --> trace_example/main.py
	    <string>.<module> -> main.<module>
	
	*** trace_example/main.py ***
	    main.<module> -> main.main
	  --> trace_example/recurse.py
	    main.<module> -> recurse.<module>
	    main.main -> recurse.recurse
	
	*** trace_example/recurse.py ***
	    recurse.recurse -> recurse.recurse

.. {{{end}}}

Programming Interface
=====================

For more control over the :mod:`trace` interface, it can be
invoked from within a program using a :class:`Trace` object.
:class:`Trace` supports setting up fixtures and other dependencies
before running a single function or executing a Python command to be
traced.

.. literalinclude:: trace_run.py
    :caption:
    :start-after: #end_pymotw_header

Since the example only traces into the :func:`recurse` function, no
information from ``main.py`` is included in the output.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'trace_run.py'))
.. }}}

::

	$ python trace_run.py
	
	 --- modulename: threading, funcname: settrace
	threading.py(89):     _trace_hook = func
	 --- modulename: trace_run, funcname: <module>
	<string>(1):   --- modulename: recurse, funcname: recurse
	recurse.py(13):     print 'recurse(%s)' % level
	recurse(2)
	recurse.py(14):     if level:
	recurse.py(15):         recurse(level-1)
	 --- modulename: recurse, funcname: recurse
	recurse.py(13):     print 'recurse(%s)' % level
	recurse(1)
	recurse.py(14):     if level:
	recurse.py(15):         recurse(level-1)
	 --- modulename: recurse, funcname: recurse
	recurse.py(13):     print 'recurse(%s)' % level
	recurse(0)
	recurse.py(14):     if level:
	recurse.py(16):     return
	recurse.py(16):     return
	recurse.py(16):     return

.. {{{end}}}

That same output can be produced with the :func:`runfunc` method,
too.

.. literalinclude:: trace_runfunc.py
    :caption:
    :start-after: #end_pymotw_header

:func:`runfunc` accepts arbitrary positional and keyword arguments,
which are passed to the function when it is called by the tracer.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'trace_runfunc.py'))
.. }}}

::

	$ python trace_runfunc.py
	
	 --- modulename: recurse, funcname: recurse
	recurse.py(13):     print 'recurse(%s)' % level
	recurse(2)
	recurse.py(14):     if level:
	recurse.py(15):         recurse(level-1)
	 --- modulename: recurse, funcname: recurse
	recurse.py(13):     print 'recurse(%s)' % level
	recurse(1)
	recurse.py(14):     if level:
	recurse.py(15):         recurse(level-1)
	 --- modulename: recurse, funcname: recurse
	recurse.py(13):     print 'recurse(%s)' % level
	recurse(0)
	recurse.py(14):     if level:
	recurse.py(16):     return
	recurse.py(16):     return
	recurse.py(16):     return

.. {{{end}}}

Saving Result Data
==================

Counts and coverage information can be recorded as well, just as with
the command line interface.  The data must be saved explicitly, using
the :class:`CoverageResults` instance from the :class:`Trace` object.

.. literalinclude:: trace_CoverageResults.py
    :caption:
    :start-after: #end_pymotw_header

This example saves the coverage results to the directory
``coverdir2``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'trace_CoverageResults.py'))
.. cog.out(run_script(cog.inFile, 'find coverdir2', interpreter=None, include_prefix=False))
.. }}}

::

	$ python trace_CoverageResults.py
	
	recurse(2)
	recurse(1)
	recurse(0)

	$ find coverdir2
	
	coverdir2
	coverdir2/trace_example.recurse.cover

.. {{{end}}}

The output file contains

.. literalinclude:: coverdir2/trace_example.recurse.cover
    :caption:

To save the counts data for generating reports, use the *infile* and
*outfile* arguments to :class:`Trace`.

.. literalinclude:: trace_report.py
    :caption:
    :start-after: #end_pymotw_header

Pass a filename to *infile* to read previously stored data, and a
filename to *outfile* to write new results after tracing.  If *infile*
and *outfile* are the same, it has the effect of updating the file
with cumulative data.

.. NOT RUNNING
.. cog.out(run_script(cog.inFile, 'trace_report.py', break_lines_at=65))

::

	$ python trace_report.py
	
	recurse(2)
	recurse(1)
	recurse(0)
	lines   cov%   module   (path)
	    7    57%   trace_example.recurse   (.../recurse.py)

Options
=======

The constructor for :class:`Trace` takes several optional parameters
to control runtime behavior.

*count*
  Boolean.  Turns on line number counting.  Defaults to True.
*countfuncs*
  Boolean.  Turns on list of functions called during the run.
  Defaults to False.
*countcallers*
  Boolean.  Turns on tracking for callers and callees.  Defaults to
  False.
*ignoremods*
  Sequence.  List of modules or packages to ignore when tracking
  coverage.  Defaults to an empty tuple.
*ignoredirs*
  Sequence.  List of directories containing modules or packages to be
  ignored.  Defaults to an empty tuple.
*infile*
  Name of the file containing cached count values.  Defaults to None.
*outfile*
  Name of the file to use for storing cached count files.  Defaults to
  None, and data is not stored.

.. seealso::

    `trace <http://docs.python.org/lib/module-trace.html>`_
        Standard library documentation for this module.

    :ref:`sys-tracing`
        The ``sys`` module includes facilities for adding a custom
        tracing function to the interpreter at run-time.

    `coverage.py <http://nedbatchelder.com/code/modules/coverage.html>`_
        Ned Batchelder's coverage module.

    `figleaf <http://darcs.idyll.org/~t/projects/figleaf/doc/>`_
        Titus Brown's coverage application.
