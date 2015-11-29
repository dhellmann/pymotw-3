Basic FIFO Queue
================

The :class:`Queue` class implements a basic first-in, first-out
container.  Elements are added to one "end" of the sequence using
:func:`put`, and removed from the other end using :func:`get`.

.. include:: Queue_fifo.py
   :literal:
   :start-after: #end_pymotw_header

This example uses a single thread to illustrate that elements are
removed from the queue in the same order they are inserted.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'Queue_fifo.py'))
.. }}}

::

	$ python Queue_fifo.py
	
	0 1 2 3 4

.. {{{end}}}

LIFO Queue
==========

In contrast to the standard FIFO implementation of :class:`Queue`, the
:class:`LifoQueue` uses last-in, first-out ordering (normally associated
with a stack data structure).

.. include:: Queue_lifo.py
   :literal:
   :start-after: #end_pymotw_header

The item most recently :class:`put` into the queue is removed by
:class:`get`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'Queue_lifo.py'))
.. }}}

::

	$ python Queue_lifo.py
	
	4 3 2 1 0

.. {{{end}}}

.. _Queue-PriorityQueue:

Priority Queue
==============

Sometimes the processing order of the items in a queue needs to be
based on characteristics of those items, rather than just the order
they are created or added to the queue.  For example, print jobs from
the payroll department may take precedence over a code listing printed
by a developer.  :class:`PriorityQueue` uses the sort order of the
contents of the queue to decide which to retrieve.

.. include:: Queue_priority.py
   :literal:
   :start-after: #end_pymotw_header

This example has multiple threads consuming the jobs, which are be
processed based on the priority of items in the queue at the time
:func:`get` was called.  The order of processing for items added to
the queue while the consumer threads are running depends on thread
context switching.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'Queue_priority.py'))
.. }}}

::

	$ python Queue_priority.py
	
	New job: Mid-level job
	New job: Low-level job
	New job: Important job
	Processing job: Important job
	Processing job: Mid-level job
	Processing job: Low-level job

.. {{{end}}}
