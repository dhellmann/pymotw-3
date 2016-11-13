==================================
 Producing Results Asynchronously
==================================

A :class:`Future` represents the result of work that has not been
completed yet. The event loop can watch for a :class:`Future` object's
state to indicate that it is done, allowing one part of an application
to wait for another part to finish some work.

Waiting for a Future
====================

A :class:`Future` acts like a coroutine, so any techniques useful for
waiting for a coroutine can also be used to wait for the future to be
marked done. This example passes the future to the event loop's
``run_until_complete()`` method.

.. literalinclude:: asyncio_future_event_loop.py
   :caption:
   :start-after: #end_pymotw_header

The state of the :class:`Future` changes to done when
:func:`set_result` is called, and the :class:`Future` instance retains
the result given to the method for retrieval later.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_future_event_loop.py'))
.. }}}

.. code-block:: none

	$ python3 asyncio_future_event_loop.py
	
	scheduling mark_done
	entering event loop
	setting future result to 'the result'
	returned result: 'the result'
	closing event loop
	future result: 'the result'

.. {{{end}}}

A :class:`Future` can also be used with the ``await`` keyword, as in
this example.

.. literalinclude:: asyncio_future_await.py
   :caption:
   :start-after: #end_pymotw_header

The result of the :class:`Future` is returned by ``await``, so it is
frequently possible to have the same code work with a regular
coroutine and a :class:`Future` instance.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_future_await.py'))
.. }}}

.. code-block:: none

	$ python3 asyncio_future_await.py
	
	scheduling mark_done
	setting future result to 'the result'
	returned result: 'the result'

.. {{{end}}}

Future Callbacks
================

In addition to working like a coroutine, a :class:`Future` can invoke
callbacks when it is completed. Callbacks are invoked in the order
they are registered.

.. literalinclude:: asyncio_future_callback.py
   :caption:
   :start-after: #end_pymotw_header

The callback should expect one argument, the :class:`Future`
instance. To pass additional arguments to the callbacks, use
:func:`functools.partial` to create a wrapper.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_future_callback.py'))
.. }}}

.. code-block:: none

	$ python3 asyncio_future_callback.py
	
	registering callbacks on future
	setting result of future
	1: future done: the result
	2: future done: the result

.. {{{end}}}

