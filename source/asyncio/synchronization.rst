============================
 Synchronization Primitives
============================

Although :mod:`asyncio` applications usually run as a single-threaded
process, they are still built as concurrent applications. Each
coroutine or task may execute in an unpredictable order, based on
delays and interrupts from I/O and other external events. To support
safe concurrency, :mod:`asyncio` includes implementations of some of
the same low-level primitives found in the :mod:`threading` and
:mod:`multiprocessing` modules.

Locks
=====

A :class:`Lock` can be used to guard access to a shared resource. Only
the holder of the lock can use the resource. Multiple attempts to
acquire the lock will block so that there is only one holder at a
time.

.. literalinclude:: asyncio_lock.py
   :caption:
   :start-after: #end_pymotw_header

Locks can be invoked directly, using ``await`` to acquire it and
calling the :func:`release` method when done as in :func:`coro2` in
this example. They also can be used as asynchronous context managers
with the ``with await`` keywords, as in :func:`coro1`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_lock.py'))
.. }}}

::

	$ python3 asyncio_lock.py
	
	acquiring the lock before starting coroutines
	lock acquired: True
	entering event loop
	coro2 waiting for the lock
	coro1 waiting for the lock
	callback releasing lock
	coro2 acquired lock
	coro2 released lock
	coro1 acquired lock
	coro1 released lock
	exited event loop
	lock status: False

.. {{{end}}}

Events
======

An :class:`asyncio.Event` is based on :class:`threading.Event`, and is
used to allow multiple consumers to wait for something to happen
without looking for a specific value to be associated with the
notification.

.. literalinclude:: asyncio_event.py
   :caption:
   :start-after: #end_pymotw_header

As with the :class:`Lock`, both :func:`coro1` and :func:`coro2` wait
for the event to be set. The difference is that both can start as soon
as the event state changes, and they do not need to acquire a unique
hold on the event object.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_event.py'))
.. }}}

::

	$ python3 asyncio_event.py
	
	event state: False
	entering event loop
	coro2 waiting for event
	coro1 waiting for event
	setting event in callback
	coro2 triggered
	coro1 triggered
	exited event loop
	event state: True

.. {{{end}}}

Conditions
==========

A :class:`Condition` works similarly to an :class:`Event` except that
rather than notifying all waiting coroutines the number of waiters
awakened is controlled with an argument to :func:`notify`.

.. literalinclude:: asyncio_condition.py
   :caption:
   :start-after: #end_pymotw_header

This example starts five consumers of the :class:`Condition`. Each
uses the :func:`wait` method to wait for a notification that they can
proceed. :func:`manipulate_condition` notifies one consumer, then two
consumers, then all of the remaining consumers.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_condition.py'))
.. }}}

::

	$ python3 asyncio_condition.py
	
	entering event loop
	starting manipulate_condition
	consumer 2 is waiting
	consumer 3 is waiting
	consumer 4 is waiting
	consumer 1 is waiting
	consumer 0 is waiting
	notifying 1
	consumer 2 triggered
	ending consumer 2
	notifying 2
	consumer 3 triggered
	ending consumer 3
	consumer 4 triggered
	ending consumer 4
	notifying remaining
	ending manipulate_condition
	consumer 1 triggered
	ending consumer 1
	consumer 0 triggered
	ending consumer 0
	exited event loop
	closing event loop

.. {{{end}}}

Queues
======

An :class:`asyncio.Queue` provides a first-in, first-out data
structure for coroutines like a :class:`queue.Queue` does for threads
or a :class:`multiprocessing.Queue` does for processes.

.. literalinclude:: asyncio_queue.py
   :caption:
   :start-after: #end_pymotw_header

Adding items with :func:`put` or removing items with :func:`get` are
both asynchronous operations, since the queue size might be fixed
(blocking an addition) or the queue might be empty (blocking a call to
fetch an item).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_queue.py'))
.. }}}

::

	$ python3 asyncio_queue.py
	
	consumer 0: starting
	consumer 0: waiting for item
	consumer 1: starting
	consumer 1: waiting for item
	producer: starting
	producer: added task 0 to the queue
	producer: added task 1 to the queue
	consumer 0: has item 0
	consumer 1: has item 1
	producer: added task 2 to the queue
	producer: added task 3 to the queue
	consumer 0: waiting for item
	consumer 0: has item 2
	producer: added task 4 to the queue
	consumer 1: waiting for item
	consumer 1: has item 3
	producer: added task 5 to the queue
	producer: adding stop signals to the queue
	consumer 0: waiting for item
	consumer 0: has item 4
	consumer 1: waiting for item
	consumer 1: has item 5
	producer: waiting for queue to empty
	consumer 0: waiting for item
	consumer 0: has item None
	consumer 0: ending
	consumer 1: waiting for item
	consumer 1: has item None
	consumer 1: ending
	producer: ending

.. {{{end}}}

