.. _sys-threads:

========================
Low-level Thread Support
========================

:mod:`sys` includes low-level functions for controlling and debugging
thread behavior.

Check Interval
==============

Python 2 uses a form of cooperative multitasking in its thread
implementation.  At a fixed interval, bytecode execution is paused and
the interpreter checks if any signal handlers need to be executed.
During the same interval check, the global interpreter lock is also
released by the current thread and then reacquired, giving other
threads an opportunity to take over execution by grabbing the lock
first.

The default check interval is 100 bytecodes and the current value can
always be retrieved with :func:`sys.getcheckinterval`.  Changing the
interval with :func:`sys.setcheckinterval` may have an impact on the
performance of an application, depending on the nature of the
operations being performed.

.. include:: sys_checkinterval.py
    :literal:
    :start-after: #end_pymotw_header

When the check interval is smaller than the number of bytecodes in a
thread, the interpreter may give another thread control so that it
runs for a while.  This is illustrated in the first set of output
where the check interval is set to 100 (the default) and 1000 extra
loop iterations are performed for each step through the ``i`` loop.

On the other hand, when the check interval is *greater* than the
number of bytecodes being executed by a thread that doesn't release
control for another reason, the thread will finish its work before the
interval comes up.  This is illustrated by the order of the name
values in the queue in the second example.

.. do not use cog, too unreliable

::

    $ python sys_checkinterval.py
    Default interval = 10 with 1000 extra operations
    Default T0
    Default T0
    Default T0
    Default T1
    Default T2
    Default T2
    Default T0
    Default T1
    Default T2
    Default T0
    Default T1
    Default T2
    Default T1
    Default T2
    Default T1

    Custom interval = 10 with 0 extra operations
    Custom T0
    Custom T0
    Custom T0
    Custom T0
    Custom T0
    Custom T1
    Custom T1
    Custom T1
    Custom T1
    Custom T1
    Custom T2
    Custom T2
    Custom T2
    Custom T2
    Custom T2


Modifying the check interval is not as clearly useful as it might
seem.  Many other factors may control the context switching behavior
of Python's threads.  For example, if a thread performs I/O, it
releases the GIL and may therefore allow another thread to take over
execution.

.. include:: sys_checkinterval_io.py
    :literal:
    :start-after: #end_pymotw_header

This example is modified from the first so that the thread prints
directly to :const:`sys.stdout` instead of appending to a queue.  The
output is much less predictable.

.. do not use cog, too unreliable

::

    $ python sys_checkinterval_io.py
    Default interval = 100 with 1000 extra operations
    Default T0
    Default T1
    Default T1Default T2

    Default T0Default T2

    Default T2
    Default T2
    Default T1
    Default T2
    Default T1
    Default T1
    Default T0
    Default T0
    Default T0

    Custom interval = 10 with 0 extra operations
    Custom T0
    Custom T0
    Custom T0
    Custom T0
    Custom T0
    Custom T1
    Custom T1
    Custom T1
    Custom T1
    Custom T2
    Custom T2
    Custom T2
    Custom T1Custom T2

    Custom T2


.. seealso::

    :mod:`dis`
        Disassembling your Python code with the dis module is one way
        to count bytecodes.


Debugging
=========

Identifying deadlocks can be on of the most difficult aspects of
working with threads.  :func:`sys._current_frames` can help by showing
exactly where a thread is stopped.

.. literalinclude:: sys_current_frames.py
    :linenos:

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

	$ python sys_current_frames.py
	
	Thread-1 with ident 4315942912 going to sleep
	Thread-1 finishing
	Thread-3 with ident 4336926720 going to sleep
	Thread-2 with ident 4332720128 going to sleep
	Thread-3 stopped in block at line 17 of sys_current_frames.py
	Thread-2 stopped in block at line 16 of sys_current_frames.py

.. {{{end}}}


.. seealso::

    :mod:`threading`
        The threading module includes classes for creating Python threads.

    :mod:`Queue`
        The Queue module provides a thread-safe implementation of a FIFO data structure.

    `Python Threads and the Global Interpreter Lock <http://jessenoller.com/2009/02/01/python-threads-and-the-global-interpreter-lock/>`_
        Jesse Noller's article from the December 2007 issue of Python Magazine.

    `Inside the Python GIL <http://www.dabeaz.com/python/GIL.pdf>`_
        Presentation by David Beazley describing thread implementation and performance issues, including how the check interval and GIL are related.
        
