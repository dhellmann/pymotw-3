=======================================
 Scheduling Calls to Regular Functions
=======================================

In addition to managing coroutines and I/O callbacks, the
:mod:`asyncio` event loop can schedule calls to regular functions
based on the timer value kept in the loop.

Scheduling a Callback "Soon"
============================

If the timing of the callback does not matter, :func:`call_soon` can
be used to schedule the call for the next iteration of the loop. Any
extra arguments after the function are passed in when the callback is
invoked.

.. include:: asyncio_call_soon.py
   :literal:
   :start-after: #end_pymotw_header

The callbacks are invoked in the order they are scheduled. In this
example, ``callback()`` is run followed by ``stopper()``, which uses
the loop's :func:`stop` method to cause the event loop to exit.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_call_soon.py'))
.. }}}

::

	$ python3 asyncio_call_soon.py
	
	registering callbacks
	entering event loop
	callback invoked
	stopper invoked
	closing event loop

.. {{{end}}}

Scheduling a Callback with a Delay
==================================

To postpone a callback until some time in the future, use
:func:`call_later`. The first argument is the delay in seconds and the
second argument is the callback.

.. include:: asyncio_call_later.py
   :literal:
   :start-after: #end_pymotw_header

In this example, the same callback function is scheduled for several
different times with different arguments. The final instance, using
:func:`call_soon`, results in the callback being invoked with the
argument ``3`` before any of the time-scheduled instances, showing
that "soon" usually implies a minimal delay.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_call_later.py'))
.. }}}

::

	$ python3 asyncio_call_later.py
	
	registering callbacks
	entering event loop
	callback 3 invoked
	callback 2 invoked
	callback 1 invoked
	stopper invoked
	closing event loop

.. {{{end}}}

Scheduling a Callback for a Specific Time
=========================================

It is also possible to schedule a call to occur at a specific
time. The loop uses a monotonic clock, rather than a wall-clock time,
to ensure that the value of "now" never regresses. To choose a time
for a scheduled callback it is necessary to start from the internal
state of that clock using the loop's :func:`time` method.

.. include:: asyncio_call_at.py
   :literal:
   :start-after: #end_pymotw_header

Note that the time according to the loop does not match the value
returned by :func:`time.time`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_call_at.py'))
.. }}}

::

	$ python3 asyncio_call_at.py
	
	clock time: 1451746600.330646
	loop  time: 856785.00372738
	registering callbacks
	entering event loop
	callback 3 invoked at 856785.003883249
	callback 2 invoked at 856785.104088092
	callback 1 invoked at 856785.205991229
	stopper invoked at    856785.305830442
	closing event loop

.. {{{end}}}

