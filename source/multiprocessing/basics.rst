multiprocessing Basics
======================

The simplest way to spawn a second process is to instantiate a
``Process`` object with a target function and call ``start()``
to let it begin working.

.. literalinclude:: multiprocessing_simple.py
    :caption:
    :start-after: #end_pymotw_header

The output includes the word "Worker" printed five times, although it
may not come out entirely clean, depending on the order of execution,
because each process is competing for access to the output stream.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_simple.py'))
.. }}}

.. code-block:: none

	$ python3 multiprocessing_simple.py
	
	Worker
	Worker
	Worker
	Worker
	Worker

.. {{{end}}}


It usually more useful to be able to spawn a process with arguments to
tell it what work to do.  Unlike with ``threading``, in order to pass
arguments to a ``multiprocessing`` ``Process`` the arguments
must be able to be serialized using :mod:`pickle`.  This example
passes each worker a number to be printed.

.. literalinclude:: multiprocessing_simpleargs.py
    :caption:
    :start-after: #end_pymotw_header

The integer argument is now included in the message printed by each
worker.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_simpleargs.py'))
.. }}}

.. code-block:: none

	$ python3 multiprocessing_simpleargs.py
	
	Worker: 1
	Worker: 0
	Worker: 2
	Worker: 3
	Worker: 4

.. {{{end}}}

Importable Target Functions
===========================

One difference between the ``threading`` and ``multiprocessing``
examples is the extra protection for ``__main__`` used in the
``multiprocessing`` examples.  Due to the way the new processes are
started, the child process needs to be able to import the script
containing the target function.  Wrapping the main part of the
application in a check for ``__main__`` ensures that it is not run
recursively in each child as the module is imported.  Another approach
is to import the target function from a separate script.  For example,
``multiprocessing_import_main.py`` uses a worker function defined in a
second module.

.. literalinclude:: multiprocessing_import_main.py
    :caption:
    :start-after: #end_pymotw_header

The worker function is defined in ``multiprocessing_import_worker.py``.

.. literalinclude:: multiprocessing_import_worker.py
    :caption:
    :start-after: #end_pymotw_header

Calling the main program produces output similar to the first example.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_import_main.py'))
.. }}}

.. code-block:: none

	$ python3 multiprocessing_import_main.py
	
	Worker
	Worker
	Worker
	Worker
	Worker

.. {{{end}}}

Determining the Current Process
===============================

Passing arguments to identify or name the process is cumbersome, and
unnecessary.  Each ``Process`` instance has a name with a default
value that can be changed as the process is created. Naming processes
is useful for keeping track of them, especially in applications with
multiple types of processes running simultaneously.

.. literalinclude:: multiprocessing_names.py
    :caption:
    :start-after: #end_pymotw_header

The debug output includes the name of the current process on each
line. The lines with ``Process-3`` in the name column correspond to
the unnamed process ``worker_2``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_names.py'))
.. }}}

.. code-block:: none

	$ python3 multiprocessing_names.py
	
	worker 1 Starting
	worker 1 Exiting
	Process-3 Starting
	Process-3 Exiting
	my_service Starting
	my_service Exiting

.. {{{end}}}


Daemon Processes
================

By default, the main program will not exit until all of the children
have exited. There are times when starting a background process that
runs without blocking the main program from exiting is useful, such as
in services where there may not be an easy way to interrupt the
worker, or where letting it die in the middle of its work does not
lose or corrupt data (for example, a task that generates "heart beats"
for a service monitoring tool). 

To mark a process as a daemon, set its :attr:`daemon` attribute to
``True``. The default is for processes to not be daemons.

.. literalinclude:: multiprocessing_daemon.py
    :caption:
    :start-after: #end_pymotw_header

The output does not include the "Exiting" message from the daemon
process, since all of the non-daemon processes (including the main
program) exit before the daemon process wakes up from its two second
sleep.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_daemon.py'))
.. }}}

.. code-block:: none

	$ python3 multiprocessing_daemon.py
	
	Starting: daemon 41838
	Starting: non-daemon 41841
	Exiting : non-daemon 41841

.. {{{end}}}

The daemon process is terminated automatically before the main program
exits, which avoids leaving orphaned processes running.  This can be
verified by looking for the process id value printed when the program
runs, and then checking for that process with a command like
``ps``.

Waiting for Processes
=====================

To wait until a process has completed its work and exited, use the
``join()`` method.

.. literalinclude:: multiprocessing_daemon_join.py
    :caption:
    :start-after: #end_pymotw_header

Since the main process waits for the daemon to exit using
``join()``, the "Exiting" message is printed this time.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_daemon_join.py'))
.. }}}

.. code-block:: none

	$ python3 multiprocessing_daemon_join.py
	
	Starting: non-daemon
	Exiting : non-daemon
	Starting: daemon
	Exiting : daemon

.. {{{end}}}

By default, ``join()`` blocks indefinitely. It is also possible to
pass a timeout argument (a float representing the number of seconds to
wait for the process to become inactive). If the process does not
complete within the timeout period, ``join()`` returns anyway.

.. literalinclude:: multiprocessing_daemon_join_timeout.py
    :caption:
    :start-after: #end_pymotw_header

Since the timeout passed is less than the amount of time the daemon
sleeps, the process is still "alive" after ``join()`` returns.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_daemon_join_timeout.py'))
.. }}}

.. code-block:: none

	$ python3 multiprocessing_daemon_join_timeout.py
	
	Starting: non-daemon
	Exiting : non-daemon
	d.is_alive() True

.. {{{end}}}

Terminating Processes
=====================

Although it is better to use the *poison pill* method of signaling to
a process that it should exit (see :ref:`multiprocessing-queues`,
later in this chapter), if a process appears hung or deadlocked it can
be useful to be able to kill it forcibly.  Calling ``terminate()``
on a process object kills the child process.

.. literalinclude:: multiprocessing_terminate.py
    :caption:
    :start-after: #end_pymotw_header

.. note::

    It is important to ``join()`` the process after terminating it
    in order to give the process management code time to update the
    status of the object to reflect the termination.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_terminate.py'))
.. }}}

.. code-block:: none

	$ python3 multiprocessing_terminate.py
	
	BEFORE: <Process(Process-1, initial)> False
	DURING: <Process(Process-1, started)> True
	TERMINATED: <Process(Process-1, started)> True
	JOINED: <Process(Process-1, stopped[SIGTERM])> False

.. {{{end}}}


Process Exit Status
===================

The status code produced when the process exits can be accessed via
the :attr:`exitcode` attribute.  The ranges allowed are listed in
:table:`Multiprocessing Exit Codes`.

.. table:: Multiprocessing Exit Codes

   =========  =======
   Exit Code  Meaning
   =========  =======
   ``== 0``   no error was produced
   ``> 0``    the process had an error, and exited with that code
   ``< 0``    the process was killed with a signal of ``-1 * exitcode``
   =========  =======

.. literalinclude:: multiprocessing_exitcode.py
    :caption:
    :start-after: #end_pymotw_header

Processes that raise an exception automatically get an
:attr:`exitcode` of 1.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_exitcode.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 multiprocessing_exitcode.py
	
	Starting process for exit_error
	Starting process for exit_ok
	Starting process for return_value
	Starting process for raises
	Starting process for terminated
	Process raises:
	Traceback (most recent call last):
	  File ".../lib/python3.6/multiprocessing/process.py", line 258,
	in _bootstrap
	    self.run()
	  File ".../lib/python3.6/multiprocessing/process.py", line 93,
	in run
	    self._target(*self._args, **self._kwargs)
	  File "multiprocessing_exitcode.py", line 28, in raises
	    raise RuntimeError('There was an error!')
	RuntimeError: There was an error!
	     exit_error.exitcode = 1
	        exit_ok.exitcode = 0
	   return_value.exitcode = 0
	         raises.exitcode = 1
	     terminated.exitcode = -15

.. {{{end}}}


Logging
=======

When debugging concurrency issues, it can be useful to have access to
the internals of the objects provided by ``multiprocessing``.
There is a convenient module-level function to enable logging called
``log_to_stderr()``.  It sets up a logger object using
:mod:`logging` and adds a handler so that log messages are sent to the
standard error channel.

.. literalinclude:: multiprocessing_log_to_stderr.py
    :caption:
    :start-after: #end_pymotw_header

By default, the logging level is set to ``NOTSET`` so no messages are
produced.  Pass a different level to initialize the logger to the
level of detail desired.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_log_to_stderr.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 multiprocessing_log_to_stderr.py
	
	[INFO/Process-1] child process calling self.run()
	Doing some work
	[INFO/Process-1] process shutting down
	[DEBUG/Process-1] running all "atexit" finalizers with priority
	>= 0
	[DEBUG/Process-1] running the remaining "atexit" finalizers
	[INFO/Process-1] process exiting with exitcode 0
	[INFO/MainProcess] process shutting down
	[DEBUG/MainProcess] running all "atexit" finalizers with
	priority >= 0
	[DEBUG/MainProcess] running the remaining "atexit" finalizers

.. {{{end}}}

To manipulate the logger directly (change its level setting or add
handlers), use ``get_logger()``.

.. literalinclude:: multiprocessing_get_logger.py
    :caption:
    :start-after: #end_pymotw_header

The logger can also be configured through the ``logging``
configuration file API, using the name "``multiprocessing``".

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_get_logger.py'))
.. }}}

.. code-block:: none

	$ python3 multiprocessing_get_logger.py
	
	[INFO/Process-1] child process calling self.run()
	Doing some work
	[INFO/Process-1] process shutting down
	[INFO/Process-1] process exiting with exitcode 0
	[INFO/MainProcess] process shutting down

.. {{{end}}}


Subclassing Process
===================

Although the simplest way to start a job in a separate process is to
use ``Process`` and pass a target function, it is also possible
to use a custom subclass.

.. literalinclude:: multiprocessing_subclass.py
    :caption:
    :start-after: #end_pymotw_header

The derived class should override :meth:`run` to do its work.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_subclass.py'))
.. }}}

.. code-block:: none

	$ python3 multiprocessing_subclass.py
	
	In Worker-1
	In Worker-3
	In Worker-2
	In Worker-4
	In Worker-5

.. {{{end}}}
