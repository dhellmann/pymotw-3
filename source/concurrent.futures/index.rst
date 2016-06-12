=========================================================
 concurrent.futures --- Manage Pools of Concurrent Tasks
=========================================================

.. module:: concurrent.futures
   :synopsis: Managing Pools of Concurrent Tasks

:Purpose: Easily manage tasks running concurrently and in parallel.

The :mod:`concurrent.futures` modules provides interfaces for running
tasks using thread pools or process pools. The APIs are the same, so
applications can switch between threads and processes with minimal
changes.

The module provides two types of classes. "Executors" are used for
managing pools of workers, and "futures" are used for managing results
computed by the workers. To use a pool of workers, an application
creates an instance of the appropriate executor class and then submits
tasks for it to run. When each task is started, a :class:`Future`
instance is returned. When the result of the task is needed, an
application can use the :class:`Future` to block until the result is
available.

Using map() with a Basic Thread Pool
====================================

The :class:`ThreadPoolExecutor` manages a set of worker threads,
passing tasks to them as they become available for more work. This
example uses :func:`map` to concurrently produce a set of results from
an input iterable.  The task uses :func:`time.sleep` to pause a
different amount of time to demonstrate how execution of concurrent
tasks might be interleaved, but that :func:`map` returns the values in
order based on the inputs.

.. literalinclude:: futures_thread_pool_map.py
   :caption:
   :start-after: #end_pymotw_header

The return value from :func:`map` is actually a special type of
iterator that knows to wait for each response as the main program
iterates over it (in this case, in the call to convert the results to
a :class:`list`).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'futures_thread_pool_map.py', line_break_mode='wrap'))
.. }}}

::

	$ python3 futures_thread_pool_map.py
	
	main: starting
	Thread-1: sleeping 5
	Thread-2: sleeping 4
	main: unprocessed results <generator object
	Executor.map.<locals>.result_iterator at 0x1016c80a0>
	main: waiting for real results
	Thread-2: done with 4
	Thread-2: sleeping 3
	Thread-1: done with 5
	Thread-1: sleeping 2
	Thread-2: done with 3
	Thread-2: sleeping 1
	Thread-1: done with 2
	Thread-2: done with 1
	main: results: [0.5, 0.4, 0.3, 0.2, 0.1]

.. {{{end}}}

Scheduling Individual Tasks
===========================

In addition to using :func:`map`, it is possible to schedule an
individual task with an executor using :func:`submit`, and use the
:class:`Future` instance returned to wait for that task's results.

.. literalinclude:: futures_thread_pool_submit.py
   :caption:
   :start-after: #end_pymotw_header

The status of the future changes after the tasks is completed and the
result is made available.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'futures_thread_pool_submit.py'))
.. }}}

::

	$ python3 futures_thread_pool_submit.py
	
	main: starting
	Thread-1: sleeping 5
	main: future: <Future at 0x1024c60b8 state=running>
	main: waiting for results
	Thread-1: done with 5
	main: result: 0.5
	main: future after result: <Future at 0x1024c60b8 state=finished
	 returned float>

.. {{{end}}}

Future Callbacks
================

To take some action when a task completed, without explicitly waiting
for the result, use :func:`add_done_callback` to specify a new
function to call when the :class:`Future` is done. The callback should
be a callable taking a single argument, the :class:`Future` instance.

.. literalinclude:: futures_future_callback.py
   :caption:
   :start-after: #end_pymotw_header

The callback is invoked regardless of the reason the :class:`Future`
is considered "done," so it is necessary to check the status of the
object passed in to the callback before using it in any way.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'futures_future_callback.py', line_break_mode='wrap'))
.. }}}

::

	$ python3 futures_future_callback.py
	
	main: starting
	5: sleeping
	5: done
	5: no longer running
	5: value returned: 0.5

.. {{{end}}}

Canceling Tasks
===============

A :class:`Future` can be cancelled, if it has been submitted but not
started, by calling its :func:`cancel` method.

.. literalinclude:: futures_future_callback_cancel.py
   :caption:
   :start-after: #end_pymotw_header

:func:`cancel` returns a Boolean indicating whether or not the task
was able to be cancelled.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'futures_future_callback_cancel.py'))
.. }}}

::

	$ python3 futures_future_callback_cancel.py
	
	main: starting
	main: submitting 10
	10: sleeping
	10: done
	main: submitting 9
	main: submitting 8
	main: submitting 7
	main: submitting 6
	main: submitting 5
	main: submitting 4
	main: submitting 3
	main: submitting 2
	main: submitting 1
	1: cancelled
	2: cancelled
	3: cancelled
	4: cancelled
	5: cancelled
	6: cancelled
	7: cancelled
	8: cancelled
	9: cancelled
	main: did not cancel 10
	10: no longer running
	10: value returned: 1.0

.. {{{end}}}

Exceptions in Tasks
===================

If a task raises an unhandled exception, it is saved to the
:class:`Future` for the task and made available through the
:func:`result` or :func:`exception` methods.

.. literalinclude:: futures_future_exception.py
   :caption:
   :start-after: #end_pymotw_header

If :func:`result` is called after an unhandled exception is raised
within a task function, the same exception is re-raised in the current
context.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'futures_future_exception.py'))
.. }}}

::

	$ python3 futures_future_exception.py
	
	main: starting
	5: starting
	main: error: the value 5 is no good
	main: saw error the value 5 is no good when accessing result

.. {{{end}}}

Process Pools
=============

The :class:`ProcessPoolExecutor` works in the same way as
:class:`ThreadPoolExecutor`, but uses processes instead of
threads. This allows CPU-intensive operations to use a separate CPU
and not be blocked by the CPython interpreter's global interpreter
lock.

.. literalinclude:: futures_process_pool_map.py
   :caption:
   :start-after: #end_pymotw_header

As with the thread pool, individual worker processes are reused for
multiple tasks.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'futures_process_pool_map.py'))
.. }}}

::

	$ python3 futures_process_pool_map.py
	
	ran task 5 in process 40976
	ran task 4 in process 40977
	ran task 3 in process 40976
	ran task 2 in process 40976
	ran task 1 in process 40977

.. {{{end}}}

.. seealso::

   * :pydoc:`concurrent.futures`

   * :pep:`3148` -- The proposal for creating the
     :mod:`concurrent.futures` feature set.

   * :ref:`asyncio-executors`
