.. _multiprocessing-queues:

Passing Messages to Processes
=============================

As with threads, a common use pattern for multiple processes is to
divide a job up among several workers to run in parallel.  Effective
use of multiple processes usually requires some communication between
them, so that work can be divided and results can be aggregated.  A
simple way to communicate between processes with
``multiprocessing`` is to use a :class:`Queue` to pass messages
back and forth.  Any object that can be serialized with :mod:`pickle`
can pass through a :class:`Queue`.

.. literalinclude:: multiprocessing_queue.py
    :caption:
    :start-after: #end_pymotw_header

This short example only passes a single message to a single worker,
then the main process waits for the worker to finish.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_queue.py'))
.. }}}

.. code-block:: none

	$ python3 multiprocessing_queue.py
	
	Doing something fancy in Process-1 for Fancy Dan!

.. {{{end}}}

A more complex example shows how to manage several workers consuming
data from a :class:`JoinableQueue` and passing results back to the
parent process.  The *poison pill* technique is used to stop the
workers.  After setting up the real tasks, the main program adds one
"stop" value per worker to the job queue.  When a worker encounters
the special value, it breaks out of its processing loop.  The main
process uses the task queue's :func:`join` method to wait for all of
the tasks to finish before processing the results.

.. literalinclude:: multiprocessing_producer_consumer.py
    :caption:
    :start-after: #end_pymotw_header

Although the jobs enter the queue in order, their execution is
parallelized so there is no guarantee about the order they will be
completed.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u multiprocessing_producer_consumer.py'))
.. }}}

.. code-block:: none

	$ python3 -u multiprocessing_producer_consumer.py
	
	Creating 8 consumers
	Consumer-1: 0 * 0
	Consumer-2: 1 * 1
	Consumer-3: 2 * 2
	Consumer-4: 3 * 3
	Consumer-5: 4 * 4
	Consumer-6: 5 * 5
	Consumer-7: 6 * 6
	Consumer-8: 7 * 7
	Consumer-3: 8 * 8
	Consumer-7: 9 * 9
	Consumer-4: Exiting
	Consumer-1: Exiting
	Consumer-2: Exiting
	Consumer-5: Exiting
	Consumer-6: Exiting
	Consumer-8: Exiting
	Consumer-7: Exiting
	Consumer-3: Exiting
	Result: 6 * 6 = 36
	Result: 2 * 2 = 4
	Result: 3 * 3 = 9
	Result: 0 * 0 = 0
	Result: 1 * 1 = 1
	Result: 7 * 7 = 49
	Result: 4 * 4 = 16
	Result: 5 * 5 = 25
	Result: 8 * 8 = 64
	Result: 9 * 9 = 81

.. {{{end}}}



Signaling between Processes
===========================

The :class:`Event` class provides a simple way to communicate state
information between processes.  An event can be toggled between set
and unset states.  Users of the event object can wait for it to change
from unset to set, using an optional timeout value.

.. literalinclude:: multiprocessing_event.py
    :caption:
    :start-after: #end_pymotw_header

When :func:`wait` times out it returns without an error.  The caller
is responsible for checking the state of the event using
:func:`is_set`.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u multiprocessing_event.py'))
.. }}}

.. code-block:: none

	$ python3 -u multiprocessing_event.py
	
	main: waiting before calling Event.set()
	wait_for_event: starting
	wait_for_event_timeout: starting
	wait_for_event_timeout: e.is_set()-> False
	main: event is set
	wait_for_event: e.is_set()-> True

.. {{{end}}}

Controlling Access to Resources
===============================

In situations when a single resource needs to be shared between
multiple processes, a :class:`Lock` can be used to avoid conflicting
accesses.

.. literalinclude:: multiprocessing_lock.py
    :caption:
    :start-after: #end_pymotw_header

In this example, the messages printed to the console may be jumbled
together if the two processes do not synchronize their access of the
output stream with the lock.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_lock.py'))
.. }}}

.. code-block:: none

	$ python3 multiprocessing_lock.py
	
	Lock acquired via with
	Lock acquired directly

.. {{{end}}}


Synchronizing Operations
========================

:class:`Condition` objects can be used to synchronize parts of a
workflow so that some run in parallel but others run sequentially,
even if they are in separate processes.

.. literalinclude:: multiprocessing_condition.py
    :caption:
    :start-after: #end_pymotw_header

In this example, two process run the second stage of a job in
parallel, but only after the first stage is done.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_condition.py'))
.. }}}

.. code-block:: none

	$ python3 multiprocessing_condition.py
	
	Starting s1
	s1 done and ready for stage 2
	Starting stage_2[2]
	stage_2[2] running
	Starting stage_2[1]
	stage_2[1] running

.. {{{end}}}


Controlling Concurrent Access to Resources
==========================================

Sometimes it is useful to allow more than one worker access to a
resource at a time, while still limiting the overall number. For
example, a connection pool might support a fixed number of
simultaneous connections, or a network application might support a
fixed number of concurrent downloads. A :class:`Semaphore` is one way
to manage those connections.

.. literalinclude:: multiprocessing_semaphore.py
    :caption:
    :start-after: #end_pymotw_header

In this example, the :class:`ActivePool` class simply serves as a
convenient way to track which processes are running at a given
moment. A real resource pool would probably allocate a connection or
some other value to the newly active process, and reclaim the value
when the task is done. Here, the pool is just used to hold the names
of the active processes to show that only three are running
concurrently.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u multiprocessing_semaphore.py'))
.. }}}

.. code-block:: none

	$ python3 -u multiprocessing_semaphore.py
	
	Activating 0 now running ['0', '1', '2']
	Activating 1 now running ['0', '1', '2']
	Activating 2 now running ['0', '1', '2']
	Now running ['0', '1', '2']
	Now running ['0', '1', '2']
	Now running ['0', '1', '2']
	Now running ['0', '1', '2']
	Activating 3 now running ['0', '1', '3']
	Activating 4 now running ['1', '3', '4']
	Activating 6 now running ['1', '4', '6']
	Now running ['1', '4', '6']
	Now running ['1', '4', '6']
	Activating 5 now running ['1', '4', '5']
	Now running ['1', '4', '5']
	Now running ['1', '4', '5']
	Now running ['1', '4', '5']
	Activating 8 now running ['4', '5', '8']
	Now running ['4', '5', '8']
	Now running ['4', '5', '8']
	Now running ['4', '5', '8']
	Now running ['4', '5', '8']
	Now running ['4', '5', '8']
	Activating 7 now running ['5', '8', '7']
	Now running ['5', '8', '7']
	Activating 9 now running ['8', '7', '9']
	Now running ['8', '7', '9']
	Now running ['8', '9']
	Now running ['8', '9']
	Now running ['9']
	Now running ['9']
	Now running ['9']
	Now running ['9']
	Now running []

.. {{{end}}}

Managing Shared State
=====================

In the previous example, the list of active processes is maintained
centrally in the :class:`ActivePool` instance via a special type of
list object created by a :class:`Manager`.  The :class:`Manager` is
responsible for coordinating shared information state between all of
its users.  

.. literalinclude:: multiprocessing_manager_dict.py
    :caption:
    :start-after: #end_pymotw_header

By creating the list through the manager, it is shared and updates are
seen in all processes.  Dictionaries are also supported.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_manager_dict.py',
..                    break_lines_at=61))
.. }}}

.. code-block:: none

	$ python3 multiprocessing_manager_dict.py
	
	Results: {0: 0, 1: 2, 2: 4, 3: 6, 4: 8, 5: 10, 6: 12, 7: 14, 
	8: 16, 9: 18}

.. {{{end}}}

Shared Namespaces
=================

In addition to dictionaries and lists, a :class:`Manager` can create a
shared :class:`Namespace`.  

.. literalinclude:: multiprocessing_namespaces.py
    :caption:
    :start-after: #end_pymotw_header

Any named value added to the :class:`Namespace` is visible to all of
the clients that receive the :class:`Namespace` instance.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_namespaces.py'))
.. }}}

.. code-block:: none

	$ python3 multiprocessing_namespaces.py
	
	Before event, error: 'Namespace' object has no attribute 'value'
	After event: This is the value

.. {{{end}}}

It is important to know that updates to the contents of mutable
values in the namespace are not propagated automatically.

.. literalinclude:: multiprocessing_namespaces_mutable.py
    :caption:
    :start-after: #end_pymotw_header

To update the list, attach it to the namespace object again.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_namespaces_mutable.py'))
.. }}}

.. code-block:: none

	$ python3 multiprocessing_namespaces_mutable.py
	
	Before event: []
	After event : []

.. {{{end}}}


Process Pools
=============

The :class:`Pool` class can be used to manage a fixed number of
workers for simple cases where the work to be done can be broken up
and distributed between workers independently.  The return values from
the jobs are collected and returned as a list.  The pool arguments
include the number of processes and a function to run when starting
the task process (invoked once per child).

.. literalinclude:: multiprocessing_pool.py
    :caption:
    :start-after: #end_pymotw_header

The result of the :func:`map` method is functionally equivalent to the
built-in :func:`map`, except that individual tasks run in parallel.
Since the pool is processing its inputs in parallel, :func:`close` and
:func:`join` can be used to synchronize the main process with the task
processes to ensure proper cleanup.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_pool.py'))
.. }}}

.. code-block:: none

	$ python3 multiprocessing_pool.py
	
	Input   : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	Built-in: <map object at 0x1007b2be0>
	Starting ForkPoolWorker-3
	Starting ForkPoolWorker-4
	Starting ForkPoolWorker-5
	Starting ForkPoolWorker-6
	Starting ForkPoolWorker-1
	Starting ForkPoolWorker-7
	Starting ForkPoolWorker-2
	Starting ForkPoolWorker-8
	Pool    : [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

.. {{{end}}}

By default, :class:`Pool` creates a fixed number of worker processes
and passes jobs to them until there are no more jobs.  Setting the
``maxtasksperchild`` parameter tells the pool to restart a worker
process after it has finished a few tasks, preventing long-running
workers from consuming ever more system resources.

.. literalinclude:: multiprocessing_pool_maxtasksperchild.py
   :caption:
   :start-after: #end_pymotw_header

The pool restarts the workers when they have completed their allotted
tasks, even if there is no more work.  In this output, eight workers
are created, even though there are only 10 tasks, and each worker can
complete two of them at a time.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_pool_maxtasksperchild.py'))
.. }}}

.. code-block:: none

	$ python3 multiprocessing_pool_maxtasksperchild.py
	
	Input   : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	Built-in: <map object at 0x1007b21d0>
	Starting ForkPoolWorker-1
	Starting ForkPoolWorker-2
	Starting ForkPoolWorker-4
	Starting ForkPoolWorker-5
	Starting ForkPoolWorker-6
	Starting ForkPoolWorker-3
	Starting ForkPoolWorker-7
	Starting ForkPoolWorker-8
	Pool    : [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

.. {{{end}}}

