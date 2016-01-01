============================
 Synchronization Primitives
============================

Although :mod:`asyncio` applications usually run as a single-threaded
process, they are still built as concurrent applications. Each
coroutine or task may execute in an unpredictable order, based on
delays and interrupts from I/O and other external events. To support
safe concurrency, :mod:`asyncio` includes implementations of some of
the same low-level primitives found in :mod:`threading` and
:mod:`multiprocessing`.

Locks
=====

A :class:`Lock` can be used to guard access to a shared resource. Only
the holder of the lock can use the resource. Multiple attempts to
acquire the lock will block so that there is only one holder at a
time.

.. include:: asyncio_lock.py
   :literal:
   :start-after: #end_pymotw_header

Locks can be invoked directly, using ``await`` to acquire it and
calling the :func:`release` method when done, or they can be used as
asynchronous context managers with the ``with await`` keywords.

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
without looking for a specific value to be associated with the event.

.. include:: asyncio_event.py
   :literal:
   :start-after: #end_pymotw_header

As with the :class:`Lock`, both :func:`coro1` and :func:`coro2` wait
for the event to be set. The difference is that both can start as soon
as the event state changes, and they do not need to wait to acquire a
unique hold on the event object.

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

.. include:: asyncio_condition.py
   :literal:
   :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_condition.py'))
.. }}}

::

	$ python3 asyncio_condition.py
	
	Using selector: KqueueSelector
	entering event loop
	in consumer 0
	consumer 0 is waiting
	in consumer 1
	consumer 1 is waiting
	in consumer 2
	consumer 2 is waiting
	in consumer 3
	consumer 3 is waiting
	starting manipulate_condition
	notifying 0
	consumer 0 triggered
	notifying 1
	consumer 1 triggered
	notifying remaining
	ending manipulate_condition
	consumer 2 triggered
	consumer 3 triggered
	exited event loop
	closing event loop

.. {{{end}}}

Queues
======

.. include:: asyncio_queue.py
   :literal:
   :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_queue.py'))
.. }}}

::

	$ python3 asyncio_queue.py
	
	asyncio: Using selector: KqueueSelector
	root: entering event loop
	consumer 0: starting
	consumer 0: waiting for item
	consumer 1: starting
	consumer 1: waiting for item
	producer: starting producer
	producer: adding task 0 to the queue
	producer: adding task 1 to the queue
	producer: adding task 2 to the queue
	consumer 0: has item 0
	consumer 1: has item 1
	producer: adding task 3 to the queue
	producer: adding task 4 to the queue
	consumer 0: waiting for item
	consumer 0: has item 2
	producer: adding task 5 to the queue
	consumer 1: waiting for item
	consumer 1: has item 3
	producer: adding stop signals to the queue
	consumer 0: waiting for item
	consumer 0: has item 4
	consumer 1: waiting for item
	consumer 1: has item 5
	producer: producer waiting for queue to empty
	consumer 0: waiting for item
	consumer 0: has item None
	consumer 1: waiting for item
	consumer 1: has item None
	producer: ending producer
	root: exited event loop
	root: closing event loop

.. {{{end}}}

