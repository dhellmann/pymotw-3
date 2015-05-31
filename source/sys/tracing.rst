.. _sys-tracing:

==============================
 Tracing a Program As It Runs
==============================

There are two ways to inject code to watch a program run: *tracing*
and *profiling*.  They are similar, but intended for different
purposes and so have different constraints.  The easiest, but least
efficient, way to monitor a program is through a *trace hook*, which
can be used for writing a debugger, code coverage monitoring, or many
other purposes.

The trace hook is modified by passing a callback function to
:func:`sys.settrace`.  The callback will receive three arguments: the
stack frame from the code being run, a string naming the type of
notification, and an event-specific argument value.  :table:`Event
Hooks for settrace()` lists the seven event types for different
levels of information that occur as a program is being executed.

.. table:: Event Hooks for settrace()

   +-------------------+-------------------------------------+------------------------------------------+
   | Event             | When it occurs                      | Argument value                           |
   +===================+=====================================+==========================================+
   |    call           | Before a function is executed.      | ``None``                                 |
   +-------------------+-------------------------------------+------------------------------------------+
   |    line           | Before a line is executed.          | ``None``                                 |
   +-------------------+-------------------------------------+------------------------------------------+
   |    return         | Before a function returns.          | The value being returned.                |
   +-------------------+-------------------------------------+------------------------------------------+
   |    exception      | After an exception occurs.          | The (exception, value, traceback) tuple. |
   +-------------------+-------------------------------------+------------------------------------------+
   |    c_call         | Before a C function is called.      | The C function object.                   |
   +-------------------+-------------------------------------+------------------------------------------+
   |    c_return       | After a C function returns.         | ``None``                                 |
   +-------------------+-------------------------------------+------------------------------------------+
   |    c_exception    | After a C function throws an error. | ``None``                                 |
   +-------------------+-------------------------------------+------------------------------------------+

Tracing Function Calls
======================

A ``call`` event is generated before every function call.  The frame
passed to the callback can be used to find out which function is being
called and from where.

.. literalinclude:: sys_settrace_call.py
   :linenos:

This example ignores calls to :func:`write`, as used by :command:`print` to
write to :const:`sys.stdout`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_settrace_call.py'))
.. }}}

::

	$ python3 sys_settrace_call.py
	
	* Call to a
	*  on line 32 of sys_settrace_call.py
	*  from line 37 of sys_settrace_call.py
	in a()
	
	* Call to b
	*  on line 28 of sys_settrace_call.py
	*  from line 34 of sys_settrace_call.py
	in b()
	

.. {{{end}}}

Tracing Inside Functions
========================

The trace hook can return a new hook to be used inside the new scope
(the *local* trace function). It is possible, for instance, to control
tracing to only run line-by-line within certain modules or functions.

.. literalinclude:: sys_settrace_line.py
    :linenos:

In this example, the list of functions is kept in the variable
:py:data:`to_be_traced`, so when :func:`trace_calls` runs it can return
:func:`trace_lines` to enable tracing inside of :func:`b`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_settrace_line.py'))
.. }}}

::

	$ python3 sys_settrace_line.py
	
	* Call to a on line 46 of sys_settrace_line.py
	* Call to b on line 40 of sys_settrace_line.py
	*  b line 41
	*  b line 42
	* Call to c on line 35 of sys_settrace_line.py
	input = 10
	Leaving c()
	*  b line 43
	Leaving b()
	Leaving a()

.. {{{end}}}


Watching the Stack
==================

Another useful way to use the hooks is to keep up with which functions
are being called, and what their return values are.  To monitor return
values, watch for the ``return`` event.

.. literalinclude:: sys_settrace_return.py
    :linenos:

The local trace function is used for watching return events, so
:func:`trace_calls_and_returns` needs to return a reference to itself
when a function is called, so the return value can be monitored.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_settrace_return.py'))
.. }}}

::

	$ python3 sys_settrace_return.py
	
	* Call to a on line 29 of sys_settrace_return.py
	in a()
	* Call to b on line 24 of sys_settrace_return.py
	in b()
	* b => response_from_b 
	* a => response_from_b response_from_b 

.. {{{end}}}


Exception Propagation
=====================

Exceptions can be monitored by looking for the ``exception`` event in
a local trace function.  When an exception occurs, the trace hook is
called with a tuple containing the type of exception, the exception
object, and a traceback object.

.. literalinclude:: sys_settrace_exception.py
    :linenos:

Take care to limit where the local function is applied because some of
the internals of formatting error messages generate, and ignore, their
own exceptions.  Every exception is seen by the trace hook,
whether the caller catches and ignores it or not.


.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_settrace_exception.py'))
.. }}}

::

	$ python3 sys_settrace_exception.py
	
	* Tracing exception:
	* RuntimeError "generating exception in c()"
	* on line 28 of c
	
	* Tracing exception:
	* RuntimeError "generating exception in c()"
	* on line 32 of b
	
	* Tracing exception:
	* RuntimeError "generating exception in c()"
	* on line 37 of a
	
	Exception handler: generating exception in c()

.. {{{end}}}


.. seealso::

    :mod:`profile`
        The ``profile`` module documentation shows how to use a ready-made profiler.

    :mod:`trace`
        The ``trace`` module implements several code analysis features.

    `Types and Members <http://docs.python.org/library/inspect.html#types-and-members>`_
        The descriptions of frame and code objects and their attributes.

    `Tracing python code <http://www.dalkescientific.com/writings/diary/archive/2005/04/20/tracing_python_code.html>`_
        Another ``settrace()`` tutorial.

    `Wicked hack: Python bytecode tracing <http://nedbatchelder.com/blog/200804/wicked_hack_python_bytecode_tracing.html>`_
        Ned Batchelder's experiments with tracing with more granularity than source line level.

    `smiley <https://pypi.python.org/pypi/smiley>`_
        Python Application Tracer

.. spelling::

   Batchelder
   settrace
