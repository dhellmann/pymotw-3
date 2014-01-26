======================================
 atexit -- Program Shutdown Callbacks
======================================

.. module:: atexit
    :synopsis: Register shutdown callbacks

:Purpose: Register function(s) to be called when a program is closing down.

The :mod:`atexit` module provides an interface to register
functions to be called when a program closes down normally. The
:mod:`sys` module also provides a hook, :data:`sys.exitfunc`, but only
one function can be registered there. The :mod:`atexit` registry can
be used by multiple modules and libraries simultaneously.

Registering Exit Callbacks
==========================

This is an example of registering a function explicitly by calling
:func:`register`.

.. include:: atexit_simple.py
    :literal:
    :start-after: #end_pymotw_header

Since the program does not do anything else, :func:`all_done` is
called right away.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'atexit_simple.py'))
.. }}}

::

	$ python3 atexit_simple.py
	
	Registering
	Registered
	all_done()

.. {{{end}}}

It is also possible to register more than one function, and to pass
arguments to the registered functions.  That can be useful to cleanly
disconnect from databases, remove temporary files, etc.  Instead of
keeping a separate list of resources that need to be freed, a separate
clean-up function can be registered for each resource.

.. include:: atexit_multiple.py
    :literal:
    :start-after: #end_pymotw_header

The exit functions are called in the reverse of the order they are
registered. This allows modules to be cleaned up in the reverse order
from which they are imported (and therefore register their
:mod:`atexit` functions), which should reduce dependency conflicts.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'atexit_multiple.py'))
.. }}}

::

	$ python3 atexit_multiple.py
	
	my_cleanup(third)
	my_cleanup(second)
	my_cleanup(first)

.. {{{end}}}


Decorator Syntax
================

Functions that require no arguments can be registered by using
:func:`register` as a decorator.  This alternative syntax is
convenient for cleanup functions that operate on module-level global
data.

.. include:: atexit_decorator.py
   :literal:
   :start-after: #end_pymotw_header

Because the function is registered as it is defined, it is also
important to ensure that it works properly even if no other work is
performed by the module. If the resources it is supposed to clean up
were never initialized, calling the exit callback should not produce
an error.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'atexit_decorator.py'))
.. }}}

::

	$ python3 atexit_decorator.py
	
	starting main program
	all_done()

.. {{{end}}}



When Are atexit Callbacks Not Called?
=====================================

The callbacks registered with :mod:`atexit` are not invoked if any of
these conditions is met:

* The program dies because of a signal.

* :func:`os._exit()` is invoked directly.

* A fatal error is detected in the interpreter.

An example from the :mod:`subprocess` section can be updated to show
what happens when a program is killed by a signal. Two files are
involved, the parent and the child programs. The parent starts the
child, pauses, then kills it.

.. include:: atexit_signal_parent.py
    :literal:
    :start-after: #end_pymotw_header

The child sets up an :mod:`atexit` callback, then sleeps until the
signal arrives.

.. include:: atexit_signal_child.py
    :literal:
    :start-after: #end_pymotw_header

When run, the output is:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'atexit_signal_parent.py'))
.. }}}

::

	$ python3 atexit_signal_parent.py
	
	CHILD: Registering atexit handler
	CHILD: Pausing to wait for signal
	PARENT: Pausing before sending signal...
	PARENT: Signaling child

.. {{{end}}}

The child does not print the message embedded in :func:`not_called()`.

If a program uses :func:`os._exit`, it can avoid having the
:mod:`atexit` callbacks invoked.

.. include:: atexit_os_exit.py
    :literal:
    :start-after: #end_pymotw_header

Because this example bypasses the normal exit path, the callback is
not run.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'atexit_os_exit.py'))
.. }}}

::

	$ python3 atexit_os_exit.py
	

.. {{{end}}}

To ensure that the callbacks are run, allow the program to terminate
by running out of statements to execute or by calling
:func:`sys.exit`.

.. include:: atexit_sys_exit.py
    :literal:
    :start-after: #end_pymotw_header

This example calls :func:`sys.exit`, so the registered callbacks are
invoked.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'atexit_sys_exit.py'))
.. }}}

::

	$ python3 atexit_sys_exit.py
	
	Registering
	Registered
	Exiting...
	all_done()

.. {{{end}}}


Handling Exceptions
===================

Tracebacks for exceptions raised in :mod:`atexit` callbacks are
printed to the console and the last exception raised is re-raised to
be the final error message of the program.

.. include:: atexit_exception.py
    :literal:
    :start-after: #end_pymotw_header

The registration order controls the execution order. If an error in
one callback introduces an error in another (registered earlier, but
called later), the final error message might not be the most useful
error message to show the user.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'atexit_exception.py', break_lines_at=68))
.. }}}

::

	$ python3 atexit_exception.py
	
	Error in atexit._run_exitfuncs:
	Traceback (most recent call last):
	  File "atexit_exception.py", line 36, in exit_with_exception
	    raise RuntimeError(message)
	RuntimeError: Registered second
	Error in atexit._run_exitfuncs:
	Traceback (most recent call last):
	  File "atexit_exception.py", line 36, in exit_with_exception
	    raise RuntimeError(message)
	RuntimeError: Registered first

.. {{{end}}}


It is usually best to handle and quietly log all exceptions in cleanup
functions, since it is messy to have a program dump errors on exit.

.. seealso::

    `atexit <http://docs.python.org/library/atexit.html>`_
        The standard library documentation for this module.

