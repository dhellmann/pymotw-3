=======
 Tasks
=======

Tasks are one of the primary ways to interact with the event
loop. Tasks wrap coroutines and track when they are complete using a
:class:`Future`. Tasks have a result, which can be retrieved after the
task completes.

Starting a Task
===============

To start a task, use :func:`create_task` to create a
:class:`Task` instance. The resulting task will run as part of the
concurrent operations managed by the event loop as long as the loop is
running.

.. include:: asyncio_create_task.py
   :literal:
   :start-after: #end_pymotw_header

This example uses :func:`run_until_complete` to keep the event loop
running until the task returns a result.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_create_task.py', line_break_mode='wrap'))
.. }}}

::

	$ python3 asyncio_create_task.py
	
	Using selector: KqueueSelector
	creating task
	task: <Task pending coro=<task_func() running at
	asyncio_create_task.py:22>>
	entering event loop
	in task_func
	task: <Task finished coro=<task_func() done, defined at
	asyncio_create_task.py:22> result='the result'>
	return value: 'the result'
	closing event loop
	task result: 'the result'

.. {{{end}}}

Chaining Coroutines
===================

A task or other coroutine can start another coroutine and wait for the
results. This makes it easier to decompose a task into reusable parts.

.. include:: asyncio_chain_coroutines.py
   :literal:
   :start-after: #end_pymotw_header

This example has two phases that must be executed in order, but that
can run concurrently with other operations.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_chain_coroutines.py', line_break_mode='wrap'))
.. }}}

::

	$ python3 asyncio_chain_coroutines.py
	
	Using selector: KqueueSelector
	creating task
	task: <Task pending coro=<outer() running at
	asyncio_chain_coroutines.py:22>>
	entering event loop
	in outer
	in phase1
	in phase2
	closing event loop
	task result: ('result1', 'result2 derived from result1')

.. {{{end}}}

Canceling a Task
================

By retaining the :class:`Task` object returned from
:func:`create_task`, it is possible to cancel the operation of the
task before it completes.

.. include:: asyncio_cancel_task.py
   :literal:
   :start-after: #end_pymotw_header

This example creates and then cancels a task before starting the event
loop. The result is a :class:`CancelledError` exception from
:func:`run_until_complete`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_cancel_task.py'))
.. }}}

::

	$ python3 asyncio_cancel_task.py
	
	Using selector: KqueueSelector
	creating task
	canceling task
	entering event loop
	caught error from cancelled task
	closing event loop

.. {{{end}}}

If a task is canceled while it is waiting for another concurrent
operation, the task is notified of its cancellation by having a
:class:`CancelledError` exception raised at the point where it is
waiting.

.. include:: asyncio_cancel_task2.py
   :literal:
   :start-after: #end_pymotw_header

Catching the exception provides an opportunity to clean up work
already done, if necessary.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_cancel_task2.py', line_break_mode='wrap'))
.. }}}

::

	$ python3 asyncio_cancel_task2.py
	
	Using selector: KqueueSelector
	creating task
	entering event loop
	in task_func, sleeping
	in task_canceller
	cancelled the task
	task_func was cancelled
	closing event loop

.. {{{end}}}
