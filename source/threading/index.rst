===========================================
 threading -- Manage Concurrent Operations
===========================================

.. module:: threading
    :synopsis: Manage concurrent operations

:Purpose: Builds on the :mod:`thread` module to more easily manage several threads of execution.
:Python Version: 1.5.2 and later

Using threads allows a program to run multiple operations concurrently
in the same process space.  The :mod:`threading` module builds on the
low-level features of :mod:`thread` to make working with threads
easier.

Thread Objects
==============

The simplest way to use a :class:`Thread` is to instantiate it with a
target function and call :func:`start()` to let it begin working.

.. include:: threading_simple.py
    :literal:
    :start-after: #end_pymotw_header

The output is five lines with ``"Worker"`` on each:

::

	$ python threading_simple.py

	Worker
	Worker
	Worker
	Worker
	Worker

It useful to be able to spawn a thread and pass it arguments to tell
it what work to do. Any type of object can be passed as argument to
the thread.  This example passes a number, which the thread then
prints.

.. include:: threading_simpleargs.py
    :literal:
    :start-after: #end_pymotw_header

The integer argument is now included in the message printed by each
thread:

::

	$ python -u threading_simpleargs.py
    
    Worker: 0
    Worker: 1
    Worker: 2
    Worker: 3
    Worker: 4


Determining the Current Thread
==============================

Using arguments to identify or name the thread is cumbersome, and
unnecessary.  Each :class:`Thread` instance has a name with a default
value that can be changed as the thread is created. Naming threads is
useful in server processes with multiple service threads handling
different operations.

.. include:: threading_names.py
    :literal:
    :start-after: #end_pymotw_header

The debug output includes the name of the current thread on each
line. The lines with ``"Thread-1"`` in the thread name column
correspond to the unnamed thread :data:`w2`.

::

	$ python -u threading_names.py

	worker Starting
	Thread-1 Starting
	my_service Starting
	worker Exiting
	Thread-1 Exiting
	my_service Exiting

Most programs do not use :command:`print` to debug. The
:mod:`logging` module supports embedding the thread name in every log
message using the formatter code ``%(threadName)s``. Including thread
names in log messages makes it possible to trace those messages back to
their source.

.. include:: threading_names_log.py
    :literal:
    :start-after: #end_pymotw_header

:mod:`logging` is also thread-safe, so messages from different threads
are kept distinct in the output.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_names_log.py'))
.. }}}

::

	$ python threading_names_log.py

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
monitoring tool). To mark a thread as a daemon, call its
:func:`setDaemon()` method with :data:`True`.  The default is for
threads to not be daemons.

.. include:: threading_daemon.py
    :literal:
    :start-after: #end_pymotw_header

The output does not include the ``"Exiting"`` message from the daemon
thread, since all of the non-daemon threads (including the main
thread) exit before the daemon thread wakes up from its two second
sleep.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_daemon.py'))
.. }}}

::

	$ python threading_daemon.py

	(daemon    ) Starting
	(non-daemon) Starting
	(non-daemon) Exiting

.. {{{end}}}

To wait until a daemon thread has completed its work, use the
:func:`join()` method.

.. include:: threading_daemon_join.py
    :literal:
    :start-after: #end_pymotw_header

Waiting for the daemon thread to exit using :func:`join()` means it
has a chance to produce its ``"Exiting"`` message.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_daemon_join.py'))
.. }}}

::

	$ python threading_daemon_join.py

	(daemon    ) Starting
	(non-daemon) Starting
	(non-daemon) Exiting
	(daemon    ) Exiting

.. {{{end}}}

By default, :func:`join()` blocks indefinitely. It is also possible to
pass a float value representing the number of seconds to wait for the
thread to become inactive. If the thread does not complete within the
timeout period, :func:`join()` returns anyway.

.. include:: threading_daemon_join_timeout.py
    :literal:
    :start-after: #end_pymotw_header

Since the timeout passed is less than the amount of time the daemon
thread sleeps, the thread is still "alive" after :func:`join()`
returns.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_daemon_join_timeout.py'))
.. }}}

::

	$ python threading_daemon_join_timeout.py

	(daemon    ) Starting
	(non-daemon) Starting
	(non-daemon) Exiting
	d.isAlive() True

.. {{{end}}}

Enumerating All Threads
=======================

It is not necessary to retain an explicit handle to all of the daemon
threads in order to ensure they have completed before exiting the main
process. :func:`enumerate()` returns a list of active :class:`Thread`
instances. The list includes the current thread, and since joining the
current thread introduces a deadlock situation, it must be skipped.

.. include:: threading_enumerate.py
    :literal:
    :start-after: #end_pymotw_header

Because the worker is sleeping for a random amount of time, the output
from this program may vary.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_enumerate.py'))
.. }}}

::

	$ python threading_enumerate.py

	(Thread-1  ) sleeping 5
	(Thread-2  ) sleeping 4
	(Thread-3  ) sleeping 2
	(MainThread) joining Thread-1
	(Thread-3  ) ending
	(Thread-2  ) ending
	(Thread-1  ) ending
	(MainThread) joining Thread-2
	(MainThread) joining Thread-3

.. {{{end}}}

Subclassing Thread
==================

At start-up, a :class:`Thread` does some basic initialization and then
calls its :func:`run()` method, which calls the target function passed
to the constructor. To create a subclass of :class:`Thread`, override
:func:`run()` to do whatever is necessary.

.. include:: threading_subclass.py
    :literal:
    :start-after: #end_pymotw_header

The return value of :func:`run` is ignored.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_subclass.py'))
.. }}}

::

	$ python threading_subclass.py

	(Thread-1  ) running
	(Thread-2  ) running
	(Thread-3  ) running
	(Thread-4  ) running
	(Thread-5  ) running

.. {{{end}}}

Because the *args* and *kwargs* values passed to the :class:`Thread`
constructor are saved in private variables using names prefixed with
``'__'``, they are not easily accessed from a subclass.  To pass
arguments to a custom thread type, redefine the constructor to save
the values in an instance attribute that can be seen in the subclass.

.. include:: threading_subclass_args.py
   :literal:
   :start-after: #end_pymotw_header

:class:`MyThreadWithArgs` uses the same API as :class:`Thread`, but
another class could easily change the constructor method to take more
or different arguments more directly related to the purpose of the
thread, as with any other class.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_subclass_args.py'))
.. }}}

::

	$ python threading_subclass_args.py

	(Thread-1  ) running with (0,) and {'a': 'A', 'b': 'B'}
	(Thread-2  ) running with (1,) and {'a': 'A', 'b': 'B'}
	(Thread-3  ) running with (2,) and {'a': 'A', 'b': 'B'}
	(Thread-4  ) running with (3,) and {'a': 'A', 'b': 'B'}
	(Thread-5  ) running with (4,) and {'a': 'A', 'b': 'B'}

.. {{{end}}}


Timer Threads
=============

One example of a reason to subclass :class:`Thread` is provided by
:class:`Timer`, also included in :mod:`threading`. A :class:`Timer`
starts its work after a delay, and can be canceled at any point within
that delay time period.

.. include:: threading_timer.py
    :literal:
    :start-after: #end_pymotw_header

The second timer is never run, and the first timer appears
to run after the rest of the main program is done. Since it is not a
daemon thread, it is joined implicitly when the main thread is done.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_timer.py'))
.. }}}

::

	$ python threading_timer.py

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
the :func:`set()` and :func:`clear()` methods. Other threads can use
:func:`wait()` to pause until the flag is set, effectively blocking
progress until allowed to continue.

.. include:: threading_event.py
    :literal:
    :start-after: #end_pymotw_header

The :func:`wait` method takes an argument representing the number of
seconds to wait for the event before timing out.  It returns a boolean
indicating whether or not the event is set, so the caller knows why
:func:`wait` returned.  The :func:`isSet` method can be used
separately on the event without fear of blocking.

In this example, :func:`wait_for_event_timeout` checks the event
status without blocking indefinitely.  The :func:`wait_for_event`
blocks on the call to :func:`wait`, which does not return until the
event status changes.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_event.py'))
.. }}}

::

	$ python threading_event.py

	(block     ) wait_for_event starting
	(non-block ) wait_for_event_timeout starting
	(MainThread) Waiting before calling Event.set()
	(non-block ) event set: False
	(non-block ) doing other work
	(non-block ) wait_for_event_timeout starting
	(MainThread) Event is set
	(block     ) event set: True
	(non-block ) event set: True
	(non-block ) processing event

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

.. include:: threading_lock.py
    :literal:
    :start-after: #end_pymotw_header

In this example, the :func:`worker()` function increments a
:class:`Counter` instance, which manages a :class:`Lock` to prevent
two threads from changing its internal state at the same time. If the
:class:`Lock` was not used, there is a possibility of missing a change
to the value attribute.

::

	$ python threading_lock.py

	(Thread-1  ) Sleeping 0.94
	(Thread-2  ) Sleeping 0.32
	(MainThread) Waiting for worker threads
	(Thread-2  ) Waiting for lock
	(Thread-2  ) Acquired lock
	(Thread-2  ) Sleeping 0.54
	(Thread-1  ) Waiting for lock
	(Thread-1  ) Acquired lock
	(Thread-1  ) Sleeping 0.84
	(Thread-2  ) Waiting for lock
	(Thread-2  ) Acquired lock
	(Thread-2  ) Done
	(Thread-1  ) Waiting for lock
	(Thread-1  ) Acquired lock
	(Thread-1  ) Done
	(MainThread) Counter: 4

To find out whether another thread has acquired the lock without
holding up the current thread, pass False for the *blocking* argument
to :func:`acquire()`. In the next example, :func:`worker()` tries to
acquire the lock three separate times, and counts how many attempts it
has to make to do so. In the mean time, :func:`lock_holder` cycles
between holding and releasing the lock, with short pauses in each
state used to simulate load.

.. include:: threading_lock_noblock.py
    :literal:
    :start-after: #end_pymotw_header

It takes :func:`worker` more than three iterations to acquire the lock
three separate times.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_lock_noblock.py'))
.. }}}

::

	$ python threading_lock_noblock.py

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

.. include:: threading_lock_reacquire.py
    :literal:
    :start-after: #end_pymotw_header

In this case, the second call to :func:`acquire()` is given a zero
timeout to prevent it from blocking because the lock has been obtained
by the first call.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_lock_reacquire.py'))
.. }}}

::

	$ python threading_lock_reacquire.py

	First try : True
	Second try: False

.. {{{end}}}

In a situation where separate code from the same thread needs to
"re-acquire" the lock, use an :class:`RLock` instead.

.. include:: threading_rlock.py
    :literal:
    :start-after: #end_pymotw_header

The only change to the code from the previous example was substituting
:class:`RLock` for :class:`Lock`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_rlock.py'))
.. }}}

::

	$ python threading_rlock.py

	First try : True
	Second try: 1

.. {{{end}}}

Locks as Context Managers
-------------------------

Locks implement the context manager API and are compatible with the
:command:`with` statement.  Using :command:`with` removes the need to
explicitly acquire and release the lock.

.. include:: threading_lock_with.py
    :literal:
    :start-after: #end_pymotw_header

The two functions :func:`worker_with()` and :func:`worker_no_with()`
manage the lock in equivalent ways.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_lock_with.py'))
.. }}}

::

	$ python threading_lock_with.py

	(Thread-1  ) Lock acquired via with
	(Thread-2  ) Lock acquired directly

.. {{{end}}}

Synchronizing Threads
=====================

In addition to using :class:`Events`, another way of synchronizing
threads is through using a :class:`Condition` object. Because the
:class:`Condition` uses a :class:`Lock`, it can be tied to a shared
resource. This allows threads to wait for the resource to be updated.
In this example, the :func:`consumer()` threads wait for the
:class:`Condition` to be set before continuing. The :func:`producer()`
thread is responsible for setting the condition and notifying the
other threads that they can continue.

.. include:: threading_condition.py
    :literal:
    :start-after: #end_pymotw_header

The threads use :command:`with` to acquire the lock associated with
the :class:`Condition`. Using the :func:`acquire()` and
:func:`release()` methods explicitly also works.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_condition.py'))
.. }}}

::

	$ python threading_condition.py

	2010-11-15 09:24:53,544 (c1) Starting consumer thread
	2010-11-15 09:24:55,545 (c2) Starting consumer thread
	2010-11-15 09:24:57,546 (p ) Starting producer thread
	2010-11-15 09:24:57,546 (p ) Making resource available
	2010-11-15 09:24:57,547 (c2) Resource is available to consumer
	2010-11-15 09:24:57,547 (c1) Resource is available to consumer

.. {{{end}}}

Limiting Concurrent Access to Resources
=======================================

Sometimes it is useful to allow more than one worker access to a
resource at a time, while still limiting the overall number. For
example, a connection pool might support a fixed number of
simultaneous connections, or a network application might support a
fixed number of concurrent downloads. A :class:`Semaphore` is one way
to manage those connections.

.. include:: threading_semaphore.py
    :literal:
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

::

	$ python threading_semaphore.py

	2010-11-15 09:24:57,618 (0 ) Waiting to join the pool
	2010-11-15 09:24:57,619 (0 ) Running: ['0']
	2010-11-15 09:24:57,619 (1 ) Waiting to join the pool
	2010-11-15 09:24:57,619 (1 ) Running: ['0', '1']
	2010-11-15 09:24:57,620 (2 ) Waiting to join the pool
	2010-11-15 09:24:57,620 (3 ) Waiting to join the pool
	2010-11-15 09:24:57,719 (0 ) Running: ['1']
	2010-11-15 09:24:57,720 (1 ) Running: []
	2010-11-15 09:24:57,721 (2 ) Running: ['2']
	2010-11-15 09:24:57,721 (3 ) Running: ['2', '3']
	2010-11-15 09:24:57,821 (2 ) Running: ['3']
	2010-11-15 09:24:57,822 (3 ) Running: []

.. {{{end}}}

Thread-specific Data
====================

While some resources need to be locked so multiple threads can use
them, others need to be protected so that they are hidden from 
threads that do not "own" them. The :func:`local()` function creates
an object capable of hiding values from view in separate threads.

.. include:: threading_local.py
    :literal:
    :start-after: #end_pymotw_header

The attribute ``local_data.value`` is not present for any thread until
it is set in that thread.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_local.py'))
.. }}}

::

	$ python threading_local.py

	(MainThread) No value yet
	(MainThread) value=1000
	(Thread-1  ) No value yet
	(Thread-1  ) value=71
	(Thread-2  ) No value yet
	(Thread-2  ) value=38

.. {{{end}}}

To initialize the settings so all threads start with the same value,
use a subclass and set the attributes in :func:`__init__`.

.. include:: threading_local_defaults.py
    :literal:
    :start-after: #end_pymotw_header

:func:`__init__` is invoked on the same object (note the :func:`id`
value), once in each thread to set the default values.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'threading_local_defaults.py'))
.. }}}

::

	$ python threading_local_defaults.py

	(MainThread) Initializing <__main__.MyLocal object at 0x100e16050>
	(MainThread) value=1000
	(Thread-1  ) Initializing <__main__.MyLocal object at 0x100e16050>
	(Thread-1  ) value=1000
	(Thread-1  ) value=19
	(Thread-2  ) Initializing <__main__.MyLocal object at 0x100e16050>
	(Thread-2  ) value=1000
	(Thread-2  ) value=55

.. {{{end}}}

.. seealso::
    
    `threading <http://docs.python.org/lib/module-threading.html>`_
        Standard library documentation for this module.

    :mod:`thread`
        Lower level thread API.
    
    :mod:`Queue`
        Thread-safe queue, useful for passing messages between threads.

    :mod:`multiprocessing`
        An API for working with processes that mirrors the ``threading`` API.
