=================================
sched -- Generic event scheduler.
=================================

.. module:: sched
    :synopsis: Generic event scheduler.

:Purpose: Generic event scheduler.
:Available In: 1.4

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
example, the ``time.time()`` and ``time.sleep()`` functions meet these
requirements.

To support multi-threaded applications, the delay function is called
with argument 0 after each event is generated, to ensure that other
threads also have a chance to run.

Running Events With a Delay
===========================

Events can be scheduled to run after a delay, or at a specific
time. To schedule them with a delay, use the ``enter()`` method, which
takes 4 arguments:

* A number representing the delay
* A priority value
* The function to call
* A tuple of arguments for the function

This example schedules 2 different events to run after 2 and 3 seconds
respectively. When the event's time comes up, ``print_event()`` is
called and prints the current time and the name argument passed to the
event.

.. include:: sched_basic.py
    :literal:
    :start-after: #end_pymotw_header

The output will look something like this:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sched_basic.py'))
.. }}}

::

	$ python sched_basic.py
	
	START: 1361446599.49
	EVENT: 1361446601.49 first
	EVENT: 1361446602.49 second

.. {{{end}}}

The time printed for the first event is 2 seconds after start, and the
time for the second event is 3 seconds after start.

Overlapping Events
==================

The call to ``run()`` blocks until all of the events have been
processed. Each event is run in the same thread, so if an event takes
longer to run than the delay between events, there will be
overlap. The overlap is resolved by postponing the later event. No
events are lost, but some events may be called later than they were
scheduled. In the next example, ``long_event()`` sleeps but it could
just as easily delay by performing a long calculation or by blocking
on I/O.

.. include:: sched_overlap.py
    :literal:
    :start-after: #end_pymotw_header

The result is the second event is run immediately after the first
finishes, since the first event took long enough to push the clock
past the desired start time of the second event.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sched_overlap.py'))
.. }}}

::

	$ python sched_overlap.py
	
	START: 1361446602.55
	BEGIN EVENT : 1361446604.55 first
	FINISH EVENT: 1361446606.55 first
	BEGIN EVENT : 1361446606.55 second
	FINISH EVENT: 1361446608.55 second

.. {{{end}}}


Event Priorities
================

If more than one event is scheduled for the same time their priority values
are used to determine the order they are run. 

.. include:: sched_priority.py
    :literal:
    :start-after: #end_pymotw_header

This example needs to ensure that they are scheduled for the exact
same time, so the ``enterabs()`` method is used instead of
``enter()``. The first argument to ``enterabs()`` is the time to run
the event, instead of the amount of time to delay.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sched_priority.py'))
.. }}}

::

	$ python sched_priority.py
	
	START: 1361446608.62
	EVENT: 1361446610.62 second
	EVENT: 1361446610.62 first

.. {{{end}}}


Canceling Events
================

Both ``enter()`` and ``enterabs()`` return a reference to the event
which can be used to cancel it later. Since ``run()`` blocks, the
event has to be canceled in a different thread. For this example, a
thread is started to run the scheduler and the main processing thread
is used to cancel the event.

.. include:: sched_cancel.py
    :literal:
    :start-after: #end_pymotw_header

Two events were scheduled, but the first was later canceled. Only the
second event runs, so the counter variable is only incremented one
time.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sched_cancel.py'))
.. }}}

::

	$ python sched_cancel.py
	
	START: 1361446610.65
	EVENT: 1361446613.66 E2
	NOW: 1
	FINAL: 1

.. {{{end}}}


.. seealso::

    `sched <https://docs.python.org/2/library/sched.html>`_
        Standard library documentation for this module.

    :mod:`time`
        The time module.

