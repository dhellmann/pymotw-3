===========================================
 traceback --- Exceptions and Stack Traces
===========================================

.. module:: traceback
    :synopsis: Exceptions and stack traces

:Purpose: Extract, format, and print exceptions and stack traces.

The :mod:`traceback` module works with the call stack to produce error
messages. A *traceback* is a stack trace from the point of an
exception handler down the call chain to the point where the exception
was raised. Tracebacks also can be accessed from the current call
stack up from the point of a call (and without the context of an
error), which is useful for finding out the paths being followed into
a function.

The functions in :mod:`traceback` fall into several common categories.
There are functions for extracting raw tracebacks from the current
runtime environment (either an exception handler for a traceback, or
the regular stack). The extracted stack trace is a sequence of tuples
containing the filename, line number, function name, and text of the
source line.

Once extracted, the stack trace can be formatted using functions like
:func:`format_exception`, :func:`format_stack`, etc. The format
functions return a list of strings with messages formatted to be
printed. There are shorthand functions for printing the formatted
values, as well.

Although the functions in :mod:`traceback` mimic the behavior of the
interactive interpreter by default, they also are useful for handling
exceptions in situations where dumping the full stack trace to the console
is not desirable. For example, a web application may need to format
the traceback so it looks good in HTML and an IDE may convert the
elements of the stack trace into a clickable list that lets the user
browse the source.

Supporting Functions
====================

The examples in this section use the module ``traceback_example.py``:

.. literalinclude:: traceback_example.py
    :caption:
    :start-after: #end_pymotw_header


Working With Exceptions
=======================

The simplest way to handle exception reporting is with
:func:`print_exc`. It uses :func:`sys.exc_info` to obtain the
exception information for the current thread, formats the results, and
prints the text to a file handle (:data:`sys.stderr`, by default).

.. literalinclude:: traceback_print_exc.py
    :caption:
    :start-after: #end_pymotw_header


In this example, the file handle for :data:`sys.stdout` is substituted so
the informational and traceback messages are mingled correctly:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'traceback_print_exc.py'))
.. }}}

.. code-block:: none

	$ python3 traceback_print_exc.py
	
	print_exc() with no exception:
	NoneType
	
	print_exc():
	Traceback (most recent call last):
	  File "traceback_print_exc.py", line 20, in <module>
	    produce_exception()
	  File ".../traceback_example.py", line 17, in produce_exception
	    produce_exception(recursion_level - 1)
	  File ".../traceback_example.py", line 17, in produce_exception
	    produce_exception(recursion_level - 1)
	  File ".../traceback_example.py", line 19, in produce_exception
	    raise RuntimeError()
	RuntimeError
	
	print_exc(1):
	Traceback (most recent call last):
	  File "traceback_print_exc.py", line 20, in <module>
	    produce_exception()
	RuntimeError

.. {{{end}}}

:func:`print_exc` is just a shortcut for :func:`print_exception`,
which requires explicit arguments.

.. literalinclude:: traceback_print_exception.py
    :caption:
    :start-after: #end_pymotw_header

The arguments to :func:`print_exception` are produced by :func:`sys.exc_info`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'traceback_print_exception.py'))
.. }}}

.. code-block:: none

	$ python3 traceback_print_exception.py
	
	Traceback (most recent call last):
	  File "traceback_print_exception.py", line 16, in <module>
	    produce_exception()
	  File ".../traceback_example.py", line 17, in produce_exception
	    produce_exception(recursion_level - 1)
	  File ".../traceback_example.py", line 17, in produce_exception
	    produce_exception(recursion_level - 1)
	  File ".../traceback_example.py", line 19, in produce_exception
	    raise RuntimeError()
	RuntimeError
	print_exception():

.. {{{end}}}


:func:`print_exception` uses :func:`format_exception` to prepare
the text.

.. literalinclude:: traceback_format_exception.py
    :caption:
    :start-after: #end_pymotw_header

The same three arguments, exception type, exception value, and
traceback, are used with :func:`format_exception`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'traceback_format_exception.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 traceback_format_exception.py
	
	format_exception():
	['Traceback (most recent call last):\n',
	 '  File "traceback_format_exception.py", line 17, in
	<module>\n'
	 '    produce_exception()\n',
	 '  File '
	 '".../traceback_example.py", '
	 'line 17, in produce_exception\n'
	 '    produce_exception(recursion_level - 1)\n',
	 '  File '
	 '".../traceback_example.py", '
	 'line 17, in produce_exception\n'
	 '    produce_exception(recursion_level - 1)\n',
	 '  File '
	 '".../traceback_example.py", '
	 'line 19, in produce_exception\n'
	 '    raise RuntimeError()\n',
	 'RuntimeError\n']

.. {{{end}}}

To process the traceback in some other way, such as formatting it
differently, use :func:`extract_tb` to get the data in a usable form.

.. literalinclude:: traceback_extract_tb.py
   :caption:
   :start-after: #end_pymotw_header

The return value is a list of entries from each level of the stack
represented by the traceback.  Each entry is a tuple with four parts:
the name of the source file, the line number in that file, the name of
the function, and the source text from that line with whitespace
stripped (if the source is available).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'traceback_extract_tb.py'))
.. }}}

.. code-block:: none

	$ python3 traceback_extract_tb.py
	
	format_exception():
	traceback_extract_tb.py:18:<module>:
	    produce_exception()
	traceback_example.py   :17:produce_exception():
	    produce_exception(recursion_level - 1)
	traceback_example.py   :17:produce_exception():
	    produce_exception(recursion_level - 1)
	traceback_example.py   :19:produce_exception():
	    raise RuntimeError()

.. {{{end}}}



Working With the Stack
======================

There are a similar set of functions for performing the same
operations with the current call stack instead of a traceback.
:func:`print_stack` prints the current stack, without generating an
exception.

.. literalinclude:: traceback_print_stack.py
    :caption:
    :start-after: #end_pymotw_header

The output look like a traceback without an error message.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'traceback_print_stack.py'))
.. }}}

.. code-block:: none

	$ python3 traceback_print_stack.py
	
	Calling f() directly:
	  File "traceback_print_stack.py", line 21, in <module>
	    f()
	  File "traceback_print_stack.py", line 17, in f
	    traceback.print_stack(file=sys.stdout)
	
	Calling f() from 3 levels deep:
	  File "traceback_print_stack.py", line 25, in <module>
	    call_function(f)
	  File ".../traceback_example.py", line 24, in call_function
	    return call_function(f, recursion_level - 1)
	  File ".../traceback_example.py", line 24, in call_function
	    return call_function(f, recursion_level - 1)
	  File ".../traceback_example.py", line 26, in call_function
	    return f()
	  File "traceback_print_stack.py", line 17, in f
	    traceback.print_stack(file=sys.stdout)

.. {{{end}}}

:func:`format_stack` prepares the stack trace in the same way that
:func:`format_exception` prepares the traceback.

.. literalinclude:: traceback_format_stack.py
    :caption:
    :start-after: #end_pymotw_header

It returns a list of strings, each of which makes up one line of the
output.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'traceback_format_stack.py'))
.. }}}

.. code-block:: none

	$ python3 traceback_format_stack.py
	
	['  File "traceback_format_stack.py", line 21, in <module>\n'
	 '    formatted_stack = call_function(f)\n',
	 '  File '
	 '".../traceback_example.py", '
	 'line 24, in call_function\n'
	 '    return call_function(f, recursion_level - 1)\n',
	 '  File '
	 '".../traceback_example.py", '
	 'line 24, in call_function\n'
	 '    return call_function(f, recursion_level - 1)\n',
	 '  File '
	 '".../traceback_example.py", '
	 'line 26, in call_function\n'
	 '    return f()\n',
	 '  File "traceback_format_stack.py", line 18, in f\n'
	 '    return traceback.format_stack()\n']

.. {{{end}}}

The :func:`extract_stack` function works like :func:`extract_tb`.

.. literalinclude:: traceback_extract_stack.py
    :caption:
    :start-after: #end_pymotw_header

It also accepts arguments, not shown here, to start from an alternate
place in the stack frame or to limit the depth of traversal.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'traceback_extract_stack.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 traceback_extract_stack.py
	
	traceback_extract_stack.py:23:<module>:
	    stack = call_function(f)
	traceback_example.py      :24:call_function():
	    return call_function(f, recursion_level - 1)
	traceback_example.py      :24:call_function():
	    return call_function(f, recursion_level - 1)
	traceback_example.py      :26:call_function():
	    return f()
	traceback_extract_stack.py:20:f():
	    return traceback.extract_stack()

.. {{{end}}}

.. seealso::

   * :pydoc:`traceback`

   * :mod:`sys` -- The ``sys`` module includes singletons that hold
     the current exception.

   * :mod:`inspect` -- The ``inspect`` module includes other functions
     for probing the frames on the stack.

   * :mod:`cgitb` -- Another module for formatting tracebacks nicely.
