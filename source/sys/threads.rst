.. _sys-threads:

==========================
 Low-level Thread Support
==========================

:mod:`sys` includes low-level functions for controlling and debugging
thread behavior.

Switch Interval
===============

Python 3 uses a global lock to prevent separate threads from
corrupting the interpreter state.  After a configurable time interval,
bytecode execution is paused and the interpreter checks if any signal
handlers need to be executed. During the same check, the global
interpreter lock (GIL) is also released by the current thread and then
reacquired, with other threads given priority over the thread which
has just released the lock.

The default switch interval is 5 milliseconds and the current value
can always be retrieved with :func:`sys.getswitchinterval`.  Changing
the interval with :func:`sys.setswitchinterval` may have an impact on
the performance of an application, depending on the nature of the
operations being performed.

.. literalinclude:: sys_switchinterval.py
    :caption:
    :start-after: #end_pymotw_header

When the switch interval is less than the amount of time a thread
takes to run to completion, the interpreter gives another thread
control so that it runs for a while.  This is illustrated in the first
set of output where the interval is set to 1 millisecond.

For longer intervals, the active thread will be able to complete more
work before it is forced to release control. This is illustrated by
the order of the name values in the queue in the second example using
an interval of 10 milliseconds.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_switchinterval.py'))
.. }}}

::

	$ python3 sys_switchinterval.py
	
	interval = 0.001
	T1 T0 T2 T1 T2 T0 T1 T0 T2 T0 T2 T1 T0 T2 T1 
	
	interval = 0.100
	T0 T0 T0 T0 T0 T1 T1 T1 T1 T1 T2 T2 T2 T2 T2 
	

.. {{{end}}}

Many factors other than the switch interval may control the context
switching behavior of Python's threads.  For example, when a thread
performs I/O it releases the GIL and may therefore allow another
thread to take over execution.

Debugging
=========

Identifying deadlocks can be one of the most difficult aspects of
working with threads.  :func:`sys._current_frames` can help by showing
exactly where a thread is stopped.

.. literalinclude:: sys_current_frames.py
   :linenos:
   :caption:
   :start-after: #end_pymotw_header

The dictionary returned by :func:`sys._current_frames` is keyed on the
thread identifier, rather than its name.  A little work is needed to
map those identifiers back to the thread object.

Since **Thread-1** does not sleep, it finishes before its status is
checked.  Since it is no longer active, it does not appear in the
output.  **Thread-2** acquires the lock *blocker*, then sleeps for a
short period.  Meanwhile **Thread-3** tries to acquire *blocker* but
cannot because **Thread-2** already has it.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_current_frames.py'))
.. }}}

::

	$ python3 sys_current_frames.py
	
	Thread-1 with ident 123145307557888 going to sleep
	Thread-1 finishing
	Thread-2 with ident 123145307557888 going to sleep
	Thread-3 with ident 123145312813056 going to sleep
	Thread-3 stopped in block at line 45 of sys_current_frames.py
	Thread-2 stopped in block at line 46 of sys_current_frames.py

.. {{{end}}}

.. spelling::

   Pitrou

.. seealso::

    * :mod:`threading` -- The ``threading`` module includes classes
      for creating Python threads.

    * :mod:`Queue` -- The ``Queue`` module provides a thread-safe
      implementation of a FIFO data structure.

    * `Reworking the GIL
      <https://mail.python.org/pipermail/python-dev/2009-October/093321.html>`_
      -- Email from Antoine Pitrou to the python-dev mailing list
      describing the GIL implementation changes to introduce the
      switch interval.
