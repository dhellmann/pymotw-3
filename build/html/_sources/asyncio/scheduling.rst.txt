=======================================
 Scheduling Calls to Regular Functions
=======================================

In addition to managing coroutines and I/O callbacks, the
``asyncio`` event loop can schedule calls to regular functions
based on the timer value kept in the loop.

Scheduling a Callback "Soon"
============================

If the timing of the callback does not matter, ``call_soon()`` can be
used to schedule the call for the next iteration of the loop. Any
extra positional arguments after the function are passed to the
callback when it is invoked. To pass keyword arguments to the
callback, use ``partial()`` from the :mod:`functools` module.

.. literalinclude:: asyncio_call_soon.py
   :caption:
   :start-after: #end_pymotw_header

The callbacks are invoked in the order they are scheduled.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_call_soon.py'))
.. }}}

.. code-block:: none

	$ python3 asyncio_call_soon.py
	
	entering event loop
	registering callbacks
	callback invoked with 1 and default
	callback invoked with 2 and not default
	closing event loop

.. {{{end}}}

Scheduling a Callback with a Delay
==================================

To postpone a callback until some time in the future, use
``call_later()``. The first argument is the delay in seconds and the
second argument is the callback.

.. literalinclude:: asyncio_call_later.py
   :caption:
   :start-after: #end_pymotw_header

In this example, the same callback function is scheduled for several
different times with different arguments. The final instance, using
``call_soon()``, results in the callback being invoked with the
argument ``3`` before any of the time-scheduled instances, showing
that "soon" usually implies a minimal delay.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_call_later.py'))
.. }}}

.. code-block:: none

	$ python3 asyncio_call_later.py
	
	entering event loop
	registering callbacks
	callback 3 invoked
	callback 2 invoked
	callback 1 invoked
	closing event loop

.. {{{end}}}

Scheduling a Callback for a Specific Time
=========================================

It is also possible to schedule a call to occur at a specific
time. The loop uses a monotonic clock, rather than a wall-clock time,
to ensure that the value of "now" never regresses. To choose a time
for a scheduled callback it is necessary to start from the internal
state of that clock using the loop's ``time()`` method.

.. literalinclude:: asyncio_call_at.py
   :caption:
   :start-after: #end_pymotw_header

Note that the time according to the loop does not match the value
returned by ``time.time()``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_call_at.py'))
.. }}}

.. code-block:: none

	$ python3 asyncio_call_at.py
	
	entering event loop
	clock time: 1521404411.833459
	loop  time: 715855.398664185
	registering callbacks
	callback 3 invoked at 715855.398744743
	callback 2 invoked at 715855.503897727
	callback 1 invoked at 715855.601119414
	closing event loop

.. {{{end}}}

