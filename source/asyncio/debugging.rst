========================
 Debugging with asyncio
========================

There are several useful debugging features built into
``asyncio``.

First, the event loop uses :mod:`logging` to emit status messages as
it runs. Some of these are available if logging is enabled in an
application. Others can be turned on by telling the loop to emit more
debugging messages.  Call ``set_debug()`` passing a boolean value
indicating whether or not debugging should be enabled.

Because applications built on ``asyncio`` are highly sensitive to
greedy coroutines failing to yield control, there is support for
detecting slow callbacks built into the event loop. Turn it on by
enabling debugging, and control the definition of "slow" by setting
the ``slow_callback_duration`` property of the loop to the number of
seconds after which a warning should be emitted.

Finally, if an application using ``asyncio`` exits without cleaning
up some of the coroutines or other resources, that may mean there is a
logic error preventing some of the application code from
running. Enabling ``ResourceWarning`` warnings causes these cases
to be reported when the program exits.

.. literalinclude:: asyncio_debug.py
   :caption:
   :start-after: #end_pymotw_header

When run without debugging enabled, everything looks fine with this
application.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_debug.py'))
.. }}}

.. code-block:: none

	$ python3 asyncio_debug.py
	
	  DEBUG: Using selector: KqueueSelector
	   INFO: entering event loop
	   INFO: outer starting
	   INFO: inner starting
	   INFO: inner completed
	   INFO: outer completed

.. {{{end}}}

Turning on debugging exposes some of the issues it has, including the
fact that although ``inner()`` finishes it takes more time to do so
than the ``slow_callback_duration`` that has been set and that the
event loop is not being properly closed when the program exits.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_debug.py -v', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 asyncio_debug.py -v
	
	  DEBUG: Using selector: KqueueSelector
	   INFO: enabling debugging
	   INFO: entering event loop
	   INFO: outer starting
	WARNING: Executing <Task pending coro=<outer() running at
	asyncio_debug.py:43> wait_for=<Task pending coro=<inner()
	running at asyncio_debug.py:33> cb=[<TaskWakeupMethWrapper
	object at 0x106e0d288>()] created at asyncio_debug.py:43>
	cb=[_run_until_complete_cb() at
	.../lib/python3.7/asyncio/base_events.py:158] created at
	.../lib/python3.7/asyncio/base_events.py:552> took 0.001 seconds
	   INFO: inner starting
	   INFO: inner completed
	WARNING: Executing <Task finished coro=<inner() done, defined at
	asyncio_debug.py:33> result=None created at asyncio_debug.py:43>
	took 0.101 seconds
	   INFO: outer completed

.. {{{end}}}

