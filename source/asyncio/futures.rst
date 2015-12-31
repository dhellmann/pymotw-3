==================================
 Producing Results Asynchronously
==================================

A :class:`Future` represents the result of work that has not been
completed yet. The event loop can watch for a :class:`Future` object
to be set to done, allowing one part of an application to wait for
another part to finish some work.

Waiting for a Future
====================

A :class:`Future` acts like a coroutine, so any techniques useful for
waiting for a coroutine can also be used to wait for the future to be
marked done.

.. include:: asyncio_future_wait.py
   :literal:
   :start-after: #end_pymotw_header

The state of the :class:`Future` changes to done when
:func:`set_result` is called, and the :class:`Future` instance retains
the result given to the method for retrieval later.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_future_wait.py'))
.. }}}

::

	$ python3 asyncio_future_wait.py
	
	scheduling mark_done
	entering event loop
	setting future result to 'the result'
	returned result: 'the result'
	closing event loop
	future result: 'the result'

.. {{{end}}}

Future Callbacks
================

In addition to working like a coroutine, a :class:`Future` can invoke
callbacks when it is completed. Callbacks are invoked in the order
they are registered.

.. include:: asyncio_future_callback.py
   :literal:
   :start-after: #end_pymotw_header

The callback should expect one argument, the :class:`Future`
instance. To pass additional arguments to the callbacks, so use
:func:`functools.partial` to create a wrapper.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_future_callback.py'))
.. }}}

::

	$ python3 asyncio_future_callback.py
	
	registering callbacks on future
	setting result of future
	entering event loop
	1: future done: the result
	2: future done: the result

.. {{{end}}}

