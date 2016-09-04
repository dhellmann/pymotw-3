================================
 sched -- Timed Event Scheduler
================================

.. module:: sched
    :synopsis: Generic event scheduler.

:Purpose: Generic event scheduler.

The :mod:`sched` module implements a generic event scheduler for
running tasks at specific times. The scheduler class uses a *time*
function to learn the current time, and a *delay* function to wait for
a specific period of time. The actual units of time are not important,
which makes the interface flexible enough to be used for many
purposes.

The *time* function is called without any arguments, and should return
a number representing the current time. The *delay* function is called
with a single integer argument, using the same scale as the time
function, and should wait that many time units before returning. For
example, the :func:`time.time` and :func:`time.sleep` functions meet
these requirements.

To support multi-threaded applications, the delay function is called
with argument 0 after each event is generated, to ensure that other
threads also have a chance to run.

Running Events With a Delay
===========================

Events can be scheduled to run after a delay, or at a specific
time. To schedule them with a delay, use the :func:`enter` method,
which takes four arguments:

* A number representing the delay
* A priority value
* The function to call
* A tuple of arguments for the function

This example schedules two different events to run after two and three
seconds respectively. When the event's time comes up,
:func:`print_event` is called and prints the current time and the name
argument passed to the event.

.. literalinclude:: sched_basic.py
    :caption:
    :start-after: #end_pymotw_header

Running the program produces:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sched_basic.py'))
.. }}}

::

	$ python sched_basic.py

	START: Sun Oct 31 20:48:47 2010
	EVENT: Sun Oct 31 20:48:49 2010 elapsed=2 name=first
	EVENT: Sun Oct 31 20:48:50 2010 elapsed=3 name=second

.. {{{end}}}

The time printed for the first event is two seconds after start, and
the time for the second event is three seconds after start.

Overlapping Events
==================

The call to :func:`run` blocks until all of the events have been
processed. Each event is run in the same thread, so if an event takes
longer to run than the delay between events, there will be
overlap. The overlap is resolved by postponing the later event. No
events are lost, but some events may be called later than they were
scheduled. In the next example, :func:`long_event` sleeps but it could
just as easily delay by performing a long calculation or by blocking
on I/O.

.. literalinclude:: sched_overlap.py
    :caption:
    :start-after: #end_pymotw_header

The result is the second event is run immediately after the first
finishes, since the first event took long enough to push the clock
past the desired start time of the second event.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sched_overlap.py'))
.. }}}

::

	$ python sched_overlap.py

	START: Sun Oct 31 20:48:50 2010
	BEGIN EVENT : Sun Oct 31 20:48:52 2010 first
	FINISH EVENT: Sun Oct 31 20:48:54 2010 first
	BEGIN EVENT : Sun Oct 31 20:48:54 2010 second
	FINISH EVENT: Sun Oct 31 20:48:56 2010 second

.. {{{end}}}


Event Priorities
================

If more than one event is scheduled for the same time their priority values
are used to determine the order they are run. 

.. literalinclude:: sched_priority.py
    :caption:
    :start-after: #end_pymotw_header

This example needs to ensure that they are scheduled for the exact
same time, so the :func:`enterabs` method is used instead of
:func:`enter`. The first argument to :func:`enterabs` is the time to
run the event, instead of the amount of time to delay.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sched_priority.py'))
.. }}}

::

	$ python sched_priority.py

	START: Sun Oct 31 20:48:56 2010
	EVENT: Sun Oct 31 20:48:58 2010 second
	EVENT: Sun Oct 31 20:48:58 2010 first

.. {{{end}}}


Canceling Events
================

Both :func:`enter` and :func:`enterabs` return a reference to the
event that can be used to cancel it later. Since :func:`run` blocks,
the event has to be canceled in a different thread. For this example,
a thread is started to run the scheduler and the main processing
thread is used to cancel the event.

.. literalinclude:: sched_cancel.py
    :caption:
    :start-after: #end_pymotw_header

Two events were scheduled, but the first was later canceled. Only the
second event runs, so the counter variable is only incremented one
time.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sched_cancel.py'))
.. }}}

::

	$ python sched_cancel.py

	START: Sun Oct 31 20:48:58 2010
	EVENT: Sun Oct 31 20:49:01 2010 E2
	NOW: 1
	FINAL: 1

.. {{{end}}}


.. seealso::

    `sched <http://docs.python.org/lib/module-sched.html>`_
        Standard library documentation for this module.

    :mod:`time`
        The ``time`` module.

