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
	Executor.map.<locals>.result_iterator at 0x1014a8f10>
	main: waiting for real results
	Thread-2: done with 4
	Thread-2: sleeping 3
	Thread-1: done with 5
	Thread-1: sleeping 2
	Thread-1: done with 2
	Thread-1: sleeping 1
	Thread-2: done with 3
	Thread-1: done with 1
	main: results: [0.5, 0.4, 0.3, 0.2, 0.1]

.. {{{end}}}

Scheduling Individual Tasks
===========================

Besides using :func:`map`, it is possible to schedule an individual
task with an executor and receive the :class:`Future` instance to wait
for that task's results by using :func:`submit`.

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
	main: future: <Future at 0x101be40b8 state=running>
	main: waiting for results
	Thread-1: done with 5
	main: result: 0.5
	main: future after result: <Future at 0x101be40b8 state=finished
	 returned float>

.. {{{end}}}

Future Callbacks
================

To take some action without explicitly waiting for the result, use
:func:`add_done_callback` to specify a new function to call when the
:class:`Future` is done. The callback should be a callable taking a
single argument, the :class:`Future` instance.

.. literalinclude:: futures_future_callback.py
   :caption:
   :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'futures_future_callback.py', line_break_mode='wrap'))
.. }}}

::

	$ python3 futures_future_callback.py
	
	main: starting
	Thread-1: sleeping 5
	Thread-1: done with 5
	callback checking status of <Future at 0x10155d518
	state=finished returned float>
	done
	value returned: 0.5

.. {{{end}}}



.. seealso::

   * :ref:`asyncio-executors`
