=============================================================
 threading --- Manage Concurrent Operations Within a Process
=============================================================

.. module:: threading
    :synopsis: Manage concurrent operations

:Purpose: Manage several threads of execution.

Using threads allows a program to run multiple operations concurrently
in the same process space.

Thread Objects
==============

The simplest way to use a :class:`Thread` is to instantiate it with a
target function and call :func:`start` to let it begin working.

.. literalinclude:: threading_simple.py
    :caption:
    :start-after: #end_pymotw_header

The output is five lines with ``"Worker"`` on each.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_simple.py'))
.. }}}

.. code-block:: none

	$ python3 threading_simple.py
	
	Worker
	Worker
	Worker
	Worker
	Worker

.. {{{end}}}

It is useful to be able to spawn a thread and pass it arguments to
tell it what work to do. Any type of object can be passed as argument
to the thread.  This example passes a number, which the thread then
prints.

.. literalinclude:: threading_simpleargs.py
    :caption:
    :start-after: #end_pymotw_header

The integer argument is now included in the message printed by each
thread.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_simpleargs.py'))
.. }}}

.. code-block:: none

	$ python3 threading_simpleargs.py
	
	Worker: 0
	Worker: 1
	Worker: 2
	Worker: 3
	Worker: 4

.. {{{end}}}

Determining the Current Thread
==============================

Using arguments to identify or name the thread is cumbersome and
unnecessary.  Each :class:`Thread` instance has a name with a default
value that can be changed as the thread is created. Naming threads is
useful in server processes with multiple service threads handling
different operations.

.. literalinclude:: threading_names.py
    :caption:
    :start-after: #end_pymotw_header

The debug output includes the name of the current thread on each
line. The lines with ``"Thread-1"`` in the thread name column
correspond to the unnamed thread :data:`w2`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_names.py'))
.. }}}

.. code-block:: none

	$ python3 threading_names.py
	
	worker Starting
	Thread-1 Starting
	my_service Starting
	worker Exiting
	Thread-1 Exiting
	my_service Exiting

.. {{{end}}}

Most programs do not use ``print`` to debug. The
:mod:`logging` module supports embedding the thread name in every log
message using the formatter code ``%(threadName)s``. Including thread
names in log messages makes it possible to trace those messages back to
their source.

.. literalinclude:: threading_names_log.py
    :caption:
    :start-after: #end_pymotw_header

:mod:`logging` is also thread-safe, so messages from different threads
are kept distinct in the output.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_names_log.py'))
.. }}}

.. code-block:: none

	$ python3 threading_names_log.py
	
	[DEBUG] (worker    ) Starting
	[DEBUG] (Thread-1  ) Starting
	[DEBUG] (my_service) Starting
	[DEBUG] (worker    ) Exiting
	[DEBUG] (Thread-1  ) Exiting
	[DEBUG] (my_service) Exiting

.. {{{end}}}

Daemon vs. Non-Daemon Threads
=============================

Up to this point, the example programs have implicitly waited to exit
until all threads have completed their work. Sometimes programs spawn
a thread as a *daemon* that runs without blocking the main program
from exiting. Using daemon threads is useful for services where there
may not be an easy way to interrupt the thread, or where letting the
thread die in the middle of its work does not lose or corrupt data
(for example, a thread that generates "heart beats" for a service
monitoring tool). To mark a thread as a daemon, pass ``daemon=True``
when constructing it or call its :func:`set_daemon` method with
:data:`True`.  The default is for threads to not be daemons.

.. literalinclude:: threading_daemon.py
    :caption:
    :start-after: #end_pymotw_header

The output does not include the ``"Exiting"`` message from the daemon
thread, since all of the non-daemon threads (including the main
thread) exit before the daemon thread wakes up from the ``sleep()``
call.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_daemon.py'))
.. }}}

.. code-block:: none

	$ python3 threading_daemon.py
	
	(daemon    ) Starting
	(non-daemon) Starting
	(non-daemon) Exiting

.. {{{end}}}

To wait until a daemon thread has completed its work, use the
:func:`join` method.

.. literalinclude:: threading_daemon_join.py
    :caption:
    :start-after: #end_pymotw_header

Waiting for the daemon thread to exit using :func:`join` means it
has a chance to produce its ``"Exiting"`` message.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_daemon_join.py'))
.. }}}

.. code-block:: none

	$ python3 threading_daemon_join.py
	
	(daemon    ) Starting
	(non-daemon) Starting
	(non-daemon) Exiting
	(daemon    ) Exiting

.. {{{end}}}

By default, :func:`join` blocks indefinitely. It is also possible to
pass a float value representing the number of seconds to wait for the
thread to become inactive. If the thread does not complete within the
timeout period, :func:`join` returns anyway.

.. literalinclude:: threading_daemon_join_timeout.py
    :caption:
    :start-after: #end_pymotw_header

Since the timeout passed is less than the amount of time the daemon
thread sleeps, the thread is still "alive" after :func:`join`
returns.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_daemon_join_timeout.py'))
.. }}}

.. code-block:: none

	$ python3 threading_daemon_join_timeout.py
	
	(daemon    ) Starting
	(non-daemon) Starting
	(non-daemon) Exiting
	(daemon    ) Exiting
	d.isAlive() False

.. {{{end}}}

Enumerating All Threads
=======================

It is not necessary to retain an explicit handle to all of the daemon
threads in order to ensure they have completed before exiting the main
process. :func:`enumerate` returns a list of active :class:`Thread`
instances. The list includes the current thread, and since joining the
current thread introduces a deadlock situation, it must be skipped.

.. literalinclude:: threading_enumerate.py
    :caption:
    :start-after: #end_pymotw_header

Because the worker is sleeping for a random amount of time, the output
from this program may vary.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_enumerate.py'))
.. }}}

.. code-block:: none

	$ python3 threading_enumerate.py
	
	(Thread-1  ) sleeping 0.20
	(Thread-2  ) sleeping 0.30
	(Thread-3  ) sleeping 0.40
	(MainThread) joining Thread-1
	(Thread-1  ) ending
	(MainThread) joining Thread-3
	(Thread-2  ) ending
	(Thread-3  ) ending
	(MainThread) joining Thread-2

.. {{{end}}}

Subclassing Thread
==================

At start-up, a :class:`Thread` does some basic initialization and then
calls its :func:`run` method, which calls the target function passed
to the constructor. To create a subclass of :class:`Thread`, override
:func:`run` to do whatever is necessary.

.. literalinclude:: threading_subclass.py
    :caption:
    :start-after: #end_pymotw_header

The return value of :func:`run` is ignored.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_subclass.py'))
.. }}}

.. code-block:: none

	$ python3 threading_subclass.py
	
	(Thread-1  ) running
	(Thread-2  ) running
	(Thread-3  ) running
	(Thread-4  ) running
	(Thread-5  ) running

.. {{{end}}}

Because the ``args`` and ``kwargs`` values passed to the :class:`Thread`
constructor are saved in private variables using names prefixed with
``'__'``, they are not easily accessed from a subclass.  To pass
arguments to a custom thread type, redefine the constructor to save
the values in an instance attribute that can be seen in the subclass.

.. literalinclude:: threading_subclass_args.py
   :caption:
   :start-after: #end_pymotw_header

:class:`MyThreadWithArgs` uses the same API as :class:`Thread`, but
another class could easily change the constructor method to take more
or different arguments more directly related to the purpose of the
thread, as with any other class.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_subclass_args.py'))
.. }}}

.. code-block:: none

	$ python3 threading_subclass_args.py
	
	(Thread-1  ) running with (0,) and {'b': 'B', 'a': 'A'}
	(Thread-2  ) running with (1,) and {'b': 'B', 'a': 'A'}
	(Thread-3  ) running with (2,) and {'b': 'B', 'a': 'A'}
	(Thread-4  ) running with (3,) and {'b': 'B', 'a': 'A'}
	(Thread-5  ) running with (4,) and {'b': 'B', 'a': 'A'}

.. {{{end}}}


Timer Threads
=============

One example of a reason to subclass :class:`Thread` is provided by
:class:`Timer`, also included in :mod:`threading`. A :class:`Timer`
starts its work after a delay, and can be canceled at any point within
that delay time period.

.. literalinclude:: threading_timer.py
    :caption:
    :start-after: #end_pymotw_header

The second timer in this example is never run, and the first timer
appears to run after the rest of the main program is done. Since it is
not a daemon thread, it is joined implicitly when the main thread is
done.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_timer.py'))
.. }}}

.. code-block:: none

	$ python3 threading_timer.py
	
	(MainThread) starting timers
	(MainThread) waiting before canceling t2
	(MainThread) canceling t2
	(MainThread) done
	(t1        ) worker running

.. {{{end}}}

Signaling Between Threads
=========================

Although the point of using multiple threads is to run separate
operations concurrently, there are times when it is important to be
able to synchronize the operations in two or more threads.  Event
objects are a simple way to communicate between threads safely.  An
:class:`Event` manages an internal flag that callers can control with
the :func:`set` and :func:`clear` methods. Other threads can use
:func:`wait` to pause until the flag is set, effectively blocking
progress until allowed to continue.

.. literalinclude:: threading_event.py
    :caption:
    :start-after: #end_pymotw_header

The :func:`wait` method takes an argument representing the number of
seconds to wait for the event before timing out.  It returns a Boolean
indicating whether or not the event is set, so the caller knows why
:func:`wait` returned.  The :func:`is_set` method can be used
separately on the event without fear of blocking.

In this example, :func:`wait_for_event_timeout` checks the event
status without blocking indefinitely.  The :func:`wait_for_event`
blocks on the call to :func:`wait`, which does not return until the
event status changes.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_event.py'))
.. }}}

.. code-block:: none

	$ python3 threading_event.py
	
	(block     ) wait_for_event starting
	(nonblock  ) wait_for_event_timeout starting
	(MainThread) Waiting before calling Event.set()
	(MainThread) Event is set
	(nonblock  ) event set: True
	(nonblock  ) processing event
	(block     ) event set: True

.. {{{end}}}

Controlling Access to Resources
===============================

In addition to synchronizing the operations of threads, it is also
important to be able to control access to shared resources to prevent
corruption or missed data. Python's built-in data structures (lists,
dictionaries, etc.) are thread-safe as a side-effect of having atomic
byte-codes for manipulating them (the GIL is not released in the
middle of an update). Other data structures implemented in Python, or
simpler types like integers and floats, do not have that protection. To
guard against simultaneous access to an object, use a :class:`Lock`
object.

.. literalinclude:: threading_lock.py
    :caption:
    :start-after: #end_pymotw_header

In this example, the :func:`worker` function increments a
:class:`Counter` instance, which manages a :class:`Lock` to prevent
two threads from changing its internal state at the same time. If the
:class:`Lock` was not used, there is a possibility of missing a change
to the value attribute.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_lock.py'))
.. }}}

.. code-block:: none

	$ python3 threading_lock.py
	
	(Thread-1  ) Sleeping 0.18
	(Thread-2  ) Sleeping 0.93
	(MainThread) Waiting for worker threads
	(Thread-1  ) Waiting for lock
	(Thread-1  ) Acquired lock
	(Thread-1  ) Sleeping 0.11
	(Thread-1  ) Waiting for lock
	(Thread-1  ) Acquired lock
	(Thread-1  ) Done
	(Thread-2  ) Waiting for lock
	(Thread-2  ) Acquired lock
	(Thread-2  ) Sleeping 0.81
	(Thread-2  ) Waiting for lock
	(Thread-2  ) Acquired lock
	(Thread-2  ) Done
	(MainThread) Counter: 4

.. {{{end}}}

To find out whether another thread has acquired the lock without
holding up the current thread, pass ``False`` for the ``blocking`` argument
to :func:`acquire`. In the next example, :func:`worker` tries to
acquire the lock three separate times and counts how many attempts it
has to make to do so. In the mean time, :func:`lock_holder` cycles
between holding and releasing the lock, with short pauses in each
state used to simulate load.

.. literalinclude:: threading_lock_noblock.py
    :caption:
    :start-after: #end_pymotw_header

It takes :func:`worker` more than three iterations to acquire the lock
three separate times.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_lock_noblock.py'))
.. }}}

.. code-block:: none

	$ python3 threading_lock_noblock.py
	
	(LockHolder) Starting
	(LockHolder) Holding
	(Worker    ) Starting
	(LockHolder) Not holding
	(Worker    ) Trying to acquire
	(Worker    ) Iteration 1: Acquired
	(LockHolder) Holding
	(Worker    ) Trying to acquire
	(Worker    ) Iteration 2: Not acquired
	(LockHolder) Not holding
	(Worker    ) Trying to acquire
	(Worker    ) Iteration 3: Acquired
	(LockHolder) Holding
	(Worker    ) Trying to acquire
	(Worker    ) Iteration 4: Not acquired
	(LockHolder) Not holding
	(Worker    ) Trying to acquire
	(Worker    ) Iteration 5: Acquired
	(Worker    ) Done after 5 iterations

.. {{{end}}}

Re-entrant Locks
----------------

Normal :class:`Lock` objects cannot be acquired more than once, even
by the same thread. This can introduce undesirable side-effects if a
lock is accessed by more than one function in the same call chain.

.. literalinclude:: threading_lock_reacquire.py
    :caption:
    :start-after: #end_pymotw_header

In this case, the second call to :func:`acquire` is given a zero
timeout to prevent it from blocking because the lock has been obtained
by the first call.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_lock_reacquire.py'))
.. }}}

.. code-block:: none

	$ python3 threading_lock_reacquire.py
	
	First try : True
	Second try: False

.. {{{end}}}

In a situation where separate code from the same thread needs to
"re-acquire" the lock, use an :class:`RLock` instead.

.. literalinclude:: threading_rlock.py
    :caption:
    :start-after: #end_pymotw_header

The only change to the code from the previous example was substituting
:class:`RLock` for :class:`Lock`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_rlock.py'))
.. }}}

.. code-block:: none

	$ python3 threading_rlock.py
	
	First try : True
	Second try: True

.. {{{end}}}

Locks as Context Managers
-------------------------

Locks implement the context manager API and are compatible with the
``with`` statement.  Using ``with`` removes the need to
explicitly acquire and release the lock.

.. literalinclude:: threading_lock_with.py
    :caption:
    :start-after: #end_pymotw_header

The two functions :func:`worker_with` and :func:`worker_no_with`
manage the lock in equivalent ways.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_lock_with.py'))
.. }}}

.. code-block:: none

	$ python3 threading_lock_with.py
	
	(Thread-1  ) Lock acquired via with
	(Thread-2  ) Lock acquired directly

.. {{{end}}}

Synchronizing Threads
=====================

In addition to using :class:`Events`, another way of synchronizing
threads is through using a :class:`Condition` object. Because the
:class:`Condition` uses a :class:`Lock`, it can be tied to a shared
resource, allowing multiple threads to wait for the resource to be
updated.  In this example, the :func:`consumer` threads wait for the
:class:`Condition` to be set before continuing. The :func:`producer`
thread is responsible for setting the condition and notifying the
other threads that they can continue.

.. literalinclude:: threading_condition.py
    :caption:
    :start-after: #end_pymotw_header

The threads use ``with`` to acquire the lock associated with
the :class:`Condition`. Using the :func:`acquire` and
:func:`release` methods explicitly also works.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_condition.py'))
.. }}}

.. code-block:: none

	$ python3 threading_condition.py
	
	2016-07-10 10:45:28,170 (c1) Starting consumer thread
	2016-07-10 10:45:28,376 (c2) Starting consumer thread
	2016-07-10 10:45:28,581 (p ) Starting producer thread
	2016-07-10 10:45:28,581 (p ) Making resource available
	2016-07-10 10:45:28,582 (c1) Resource is available to consumer
	2016-07-10 10:45:28,582 (c2) Resource is available to consumer

.. {{{end}}}

Barriers are another thread synchronization mechanism. A
:class:`Barrier` establishes a control point and all participating
threads block until all of the participating "parties" have reached
that point. It lets threads start up separately and then pause until
they are all ready to proceed.

.. literalinclude:: threading_barrier.py
   :caption:
   :start-after: #end_pymotw_header

In this example, the :class:`Barrier` is configured to block until
three threads are waiting. When the condition is met, all of the
threads are released past the control point at the same time. The
return value from :func:`wait` indicates the number of the party being
released, and can be used to limit some threads from taking an action
like cleaning up a shared resource.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_barrier.py'))
.. }}}

.. code-block:: none

	$ python3 threading_barrier.py
	
	worker-0 starting
	worker-0 waiting for barrier with 0 others
	worker-1 starting
	worker-1 waiting for barrier with 1 others
	worker-2 starting
	worker-2 waiting for barrier with 2 others
	worker-2 after barrier 2
	worker-0 after barrier 0
	worker-1 after barrier 1

.. {{{end}}}

The :func:`abort` method of :class:`Barrier` causes all of the waiting
threads to receive a :class:`BrokenBarrierError`. This allows threads
to clean up if processing is stopped while they are blocked on
:func:`wait`.

.. literalinclude:: threading_barrier_abort.py
   :caption:
   :start-after: #end_pymotw_header

This example configures the :class:`Barrier` to expect one more
participating thread than is actually started so that processing in
all of the threads is blocked. The :func:`abort` call raises an
exception in each blocked thread.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_barrier_abort.py'))
.. }}}

.. code-block:: none

	$ python3 threading_barrier_abort.py
	
	worker-0 starting
	worker-0 waiting for barrier with 0 others
	worker-1 starting
	worker-1 waiting for barrier with 1 others
	worker-2 starting
	worker-2 waiting for barrier with 2 others
	worker-0 aborting
	worker-2 aborting
	worker-1 aborting

.. {{{end}}}

Limiting Concurrent Access to Resources
=======================================

Sometimes it is useful to allow more than one worker access to a
resource at a time, while still limiting the overall number. For
example, a connection pool might support a fixed number of
simultaneous connections, or a network application might support a
fixed number of concurrent downloads. A :class:`Semaphore` is one way
to manage those connections.

.. literalinclude:: threading_semaphore.py
    :caption:
    :start-after: #end_pymotw_header

In this example, the :class:`ActivePool` class simply serves as a
convenient way to track which threads are able to run at a given
moment. A real resource pool would allocate a connection or some other
value to the newly active thread, and reclaim the value when the
thread is done. Here, it is just used to hold the names of the active
threads to show that at most two are running concurrently.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_semaphore.py'))
.. }}}

.. code-block:: none

	$ python3 threading_semaphore.py
	
	2016-07-10 10:45:29,398 (0 ) Waiting to join the pool
	2016-07-10 10:45:29,398 (0 ) Running: ['0']
	2016-07-10 10:45:29,399 (1 ) Waiting to join the pool
	2016-07-10 10:45:29,399 (1 ) Running: ['0', '1']
	2016-07-10 10:45:29,399 (2 ) Waiting to join the pool
	2016-07-10 10:45:29,399 (3 ) Waiting to join the pool
	2016-07-10 10:45:29,501 (1 ) Running: ['0']
	2016-07-10 10:45:29,501 (0 ) Running: []
	2016-07-10 10:45:29,502 (3 ) Running: ['3']
	2016-07-10 10:45:29,502 (2 ) Running: ['3', '2']
	2016-07-10 10:45:29,607 (3 ) Running: ['2']
	2016-07-10 10:45:29,608 (2 ) Running: []

.. {{{end}}}

Thread-specific Data
====================

While some resources need to be locked so multiple threads can use
them, others need to be protected so that they are hidden from threads
that do not "own" them. The :func:`local` class creates an object
capable of hiding values from view in separate threads.

.. literalinclude:: threading_local.py
    :caption:
    :start-after: #end_pymotw_header

The attribute ``local_data.value`` is not present for any thread until
it is set in that thread.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_local.py'))
.. }}}

.. code-block:: none

	$ python3 threading_local.py
	
	(MainThread) No value yet
	(MainThread) value=1000
	(Thread-1  ) No value yet
	(Thread-1  ) value=33
	(Thread-2  ) No value yet
	(Thread-2  ) value=74

.. {{{end}}}

To initialize the settings so all threads start with the same value,
use a subclass and set the attributes in :func:`__init__`.

.. literalinclude:: threading_local_defaults.py
    :caption:
    :start-after: #end_pymotw_header

:func:`__init__` is invoked on the same object (note the :func:`id`
value), once in each thread to set the default values.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_local_defaults.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 threading_local_defaults.py
	
	(MainThread) Initializing <__main__.MyLocal object at
	0x101c6c288>
	(MainThread) value=1000
	(Thread-1  ) Initializing <__main__.MyLocal object at
	0x101c6c288>
	(Thread-1  ) value=1000
	(Thread-1  ) value=18
	(Thread-2  ) Initializing <__main__.MyLocal object at
	0x101c6c288>
	(Thread-2  ) value=1000
	(Thread-2  ) value=77

.. {{{end}}}

.. seealso::

   * :pydoc:`threading`

   * :ref:`Porting notes for threading <porting-threading>`

   * :mod:`thread` -- Lower level thread API.

   * :mod:`Queue` -- Thread-safe queue, useful for passing messages
     between threads.

   * :mod:`multiprocessing` -- An API for working with processes that
     mirrors the ``threading`` API.
