=======================================================
atexit -- Call functions when a program is closing down
=======================================================

.. module:: atexit
    :synopsis: Register function(s) to be called when a program is closing down.

:Purpose: Register function(s) to be called when a program is closing down.
:Available In: 2.1.3 and later

The atexit module provides a simple interface to register functions to be
called when a program closes down normally. The sys module also provides a
hook, sys.exitfunc, but only one function can be registered there. The atexit
registry can be used by multiple modules and libraries simultaneously.

Examples
========

A simple example of registering a function via atexit.register() looks like:

.. include:: atexit_simple.py
    :literal:
    :start-after: #end_pymotw_header

Since the program doesn't do anything else, all_done() is called right away:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'atexit_simple.py'))
.. }}}

::

	$ python atexit_simple.py
	
	Registering
	Registered
	all_done()

.. {{{end}}}

It is also possible to register more than one function, and to pass arguments.
That can be useful to cleanly disconnect from databases, remove temporary
files, etc. Since it is possible to pass arguments to the registered
functions, we don't even need to keep a separate list of things to clean up --
we can just register a clean up function more than once.

.. include:: atexit_multiple.py
    :literal:
    :start-after: #end_pymotw_header

Notice that order in which the exit functions are called is the reverse of
the order they are registered. This allows modules to be cleaned up in the
reverse order from which they are imported (and therefore register their
atexit functions), which should reduce dependency conflicts.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'atexit_multiple.py'))
.. }}}

::

	$ python atexit_multiple.py
	
	my_cleanup(third)
	my_cleanup(second)
	my_cleanup(first)

.. {{{end}}}

When are atexit functions not called?
=====================================

The callbacks registered with atexit are not invoked if:

* the program dies because of a signal

* os._exit() is invoked directly

* a Python fatal error is detected (in the interpreter)

To illustrate a program being killed via a signal, we can modify one
of the examples from the :mod:`subprocess` article. There are 2 files
involved, the parent and the child programs. The parent starts the
child, pauses, then kills it:

.. include:: atexit_signal_parent.py
    :literal:
    :start-after: #end_pymotw_header


The child sets up an atexit callback, to prove that it is not called.

.. include:: atexit_signal_child.py
    :literal:
    :start-after: #end_pymotw_header


When run, the output should look something like this:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'atexit_signal_parent.py'))
.. }}}

::

	$ python atexit_signal_parent.py
	
	CHILD: Registering atexit handler
	CHILD: Pausing to wait for signal
	PARENT: Pausing before sending signal...
	PARENT: Signaling child

.. {{{end}}}

Note that the child does not print the message embedded in not_called().

Similarly, if a program bypasses the normal exit path it can avoid having the
atexit callbacks invoked.

.. include:: atexit_os_exit.py
    :literal:
    :start-after: #end_pymotw_header


Since we call os._exit() instead of exiting normally, the callback is not
invoked. 

.. {{{cog
.. cog.out(run_script(cog.inFile, 'atexit_os_exit.py'))
.. }}}

::

	$ python atexit_os_exit.py
	

.. {{{end}}}

If we had instead used sys.exit(), the callbacks would still have been called.

.. include:: atexit_sys_exit.py
    :literal:
    :start-after: #end_pymotw_header


.. {{{cog
.. cog.out(run_script(cog.inFile, 'atexit_sys_exit.py'))
.. }}}

::

	$ python atexit_sys_exit.py
	
	Registering
	Registered
	Exiting...
	all_done()

.. {{{end}}}

Simulating a fatal error in the Python interpreter is left as an exercise to
the reader.

Exceptions in atexit Callbacks
==============================

Tracebacks for exceptions raised in atexit callbacks are printed to the
console and the last exception raised is re-raised to be the final error
message of the program.

.. include:: atexit_exception.py
    :literal:
    :start-after: #end_pymotw_header

Notice again that the registration order controls the execution order. If an
error in one callback introduces an error in another (registered earlier, but
called later), the final error message might not be the most useful error
message to show the user.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'atexit_exception.py'))
.. }}}

::

	$ python atexit_exception.py
	
	Error in atexit._run_exitfuncs:
	Traceback (most recent call last):
	  File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/atexit.py", line 24, in _run_exitfuncs
	    func(*targs, **kargs)
	  File "atexit_exception.py", line 37, in exit_with_exception
	    raise RuntimeError(message)
	RuntimeError: Registered second
	Error in atexit._run_exitfuncs:
	Traceback (most recent call last):
	  File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/atexit.py", line 24, in _run_exitfuncs
	    func(*targs, **kargs)
	  File "atexit_exception.py", line 37, in exit_with_exception
	    raise RuntimeError(message)
	RuntimeError: Registered first
	Error in sys.exitfunc:
	Traceback (most recent call last):
	  File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/atexit.py", line 24, in _run_exitfuncs
	    func(*targs, **kargs)
	  File "atexit_exception.py", line 37, in exit_with_exception
	    raise RuntimeError(message)
	RuntimeError: Registered first

.. {{{end}}}


In general you will probably want to handle and quietly log all exceptions in
your cleanup functions, since it is messy to have a program dump errors on
exit.

.. seealso::

    `atexit <http://docs.python.org/2.7/library/atexit.html>`_
        The standard library documentation for this module.

