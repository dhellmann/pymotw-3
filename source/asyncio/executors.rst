.. _asyncio-executors:

=================================================
 Combining Coroutines with Threads and Processes
=================================================

A lot of existing libraries are not ready to be used with
``asyncio`` natively. They may block, or depend on concurrency
features not available through the module. It is still possible to use
those libraries in an application based on ``asyncio`` by using an
*executor* from :mod:`concurrent.futures` to run the code either in a
separate thread or a separate process.

Threads
=======

The ``run_in_executor()`` method of the event loop takes an executor
instance, a regular callable to invoke, and any arguments to be passed
to the callable. It returns a ``Future`` that can be used to wait
for the function to finish its work and return something. If no
executor is passed in, a ``ThreadPoolExecutor`` is created. This
example explicitly creates an executor to limit the number of worker
threads it will have available.

A ``ThreadPoolExecutor`` starts its worker threads and then calls
each of the provided functions once in a thread. This example shows
how to combine ``run_in_executor()`` and ``wait()`` to have a
coroutine yield control to the event loop while blocking functions run
in separate threads, and then wake back up when those functions are
finished.

.. literalinclude:: asyncio_executor_thread.py
   :caption:
   :start-after: #end_pymotw_header

``asyncio_executor_thread.py`` uses :mod:`logging` to conveniently
indicate which thread and function are producing each log
message. Because a separate logger is used in each call to
``blocks()``, the output clearly shows the same threads being reused
to call multiple copies of the function with different arguments.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_executor_thread.py'))
.. }}}

.. code-block:: none

	$ python3 asyncio_executor_thread.py
	
	MainThread run_blocking_tasks: starting
	MainThread run_blocking_tasks: creating executor tasks
	ThreadPoolExecutor-0_0          blocks(0): running
	ThreadPoolExecutor-0_1          blocks(1): running
	ThreadPoolExecutor-0_2          blocks(2): running
	MainThread run_blocking_tasks: waiting for executor tasks
	ThreadPoolExecutor-0_1          blocks(1): done
	ThreadPoolExecutor-0_0          blocks(0): done
	ThreadPoolExecutor-0_2          blocks(2): done
	ThreadPoolExecutor-0_1          blocks(3): running
	ThreadPoolExecutor-0_0          blocks(4): running
	ThreadPoolExecutor-0_2          blocks(5): running
	ThreadPoolExecutor-0_1          blocks(3): done
	ThreadPoolExecutor-0_2          blocks(5): done
	ThreadPoolExecutor-0_0          blocks(4): done
	MainThread run_blocking_tasks: results: [1, 25, 4, 9, 0, 16]
	MainThread run_blocking_tasks: exiting

.. {{{end}}}

Processes
=========

A ``ProcessPoolExecutor`` works in much the same way, creating a
set of worker processes instead of threads. Using separate processes
requires more system resources, but for computationally-intensive
operations it can make sense to run a separate task on each CPU core.

.. literalinclude:: asyncio_executor_process.py
   :caption:
   :lines: 42-

The only change needed to move from threads to processes is to create
a different type of executor. This example also changes the logging
format string to include the process id instead of the thread name, to
demonstrate that the tasks are in fact running in separate processes.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_executor_process.py'))
.. }}}

.. code-block:: none

	$ python3 asyncio_executor_process.py
	
	PID 77044 run_blocking_tasks: starting
	PID 77044 run_blocking_tasks: creating executor tasks
	PID 77044 run_blocking_tasks: waiting for executor tasks
	PID 77044 run_blocking_tasks: results: [0, 9, 16, 25, 1, 4]
	PID 77044 run_blocking_tasks: exiting

.. {{{end}}}

