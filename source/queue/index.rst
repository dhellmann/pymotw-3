===========================================
 Queue --- Thread-safe FIFO Implementation
===========================================

.. module:: Queue
    :synopsis: Thread-safe FIFO implementation

:Purpose: Provides a thread-safe FIFO implementation

The :mod:`Queue` module provides a first-in, first-out (FIFO) data
structure suitable for multi-threaded programming. It can be used to
pass messages or other data between producer and consumer threads
safely. Locking is handled for the caller, so many threads can work
with the same :class:`Queue` instance safely. The size of a
:class:`Queue` (the number of elements it contains) may be restricted
to throttle memory usage or processing.

.. note::

    This discussion assumes you already understand the general nature
    of a queue. If you do not, you may want to read some of the
    references before continuing.

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

Building a Threaded Podcast Client
==================================

The source code for the podcasting client in this section demonstrates
how to use the :class:`Queue` class with multiple threads.  The
program reads one or more RSS feeds, queues up the enclosures for the
five most recent episodes to be downloaded, and processes several
downloads in parallel using threads. It does not have enough error
handling for production use, but the skeleton implementation provides an
example of using the :mod:`Queue` module.

First, some operating parameters are established. Normally these would
come from user inputs (preferences, a database, etc.). The example
uses hard-coded values for the number of threads and list of URLs to
fetch.

.. literalinclude:: fetch_podcasts.py
   :lines: 6-20

The function :func:`downloadEnclosures` will run in the worker thread
and process the downloads using :mod:`urllib`.

.. literalinclude:: fetch_podcasts.py
   :lines: 22-41

Once the threads' target function is defined, the worker threads can
be started. When :func:`downloadEnclosures` processes the statement
``url = q.get()``, it blocks and waits until the queue has something
to return.  That means it is safe to start the threads before there is
anything in the queue.

.. literalinclude:: fetch_podcasts.py
   :lines: 44-49

The next step is to retrieve the feed contents using Mark Pilgrim's
:mod:`feedparser` module (http://www.feedparser.org/) and enqueue the
URLs of the enclosures. As soon as the first URL is added to the
queue, one of the worker threads picks it up and starts downloading
it. The loop will continue to add items until the feed is exhausted,
and the worker threads will take turns dequeuing URLs to download
them.

.. literalinclude:: fetch_podcasts.py
   :lines: 51-59

And the only thing left to do is wait for the queue to empty out
again, using :func:`join`.

.. literalinclude:: fetch_podcasts.py
   :lines: 61-

Running the sample script produces:

::

    $ python fetch_podcasts.py 
    
    0: Looking for the next enclosure
    1: Looking for the next enclosure
    Queuing: /podcasts/littlebit/2010-04-18.mp3
    Queuing: /podcasts/littlebit/2010-05-22.mp3
    Queuing: /podcasts/littlebit/2010-06-06.mp3
    Queuing: /podcasts/littlebit/2010-07-26.mp3
    Queuing: /podcasts/littlebit/2010-11-25.mp3
    *** Main thread waiting
    0: Downloading: /podcasts/littlebit/2010-04-18.mp3
    0: Looking for the next enclosure
    0: Downloading: /podcasts/littlebit/2010-05-22.mp3
    0: Looking for the next enclosure
    0: Downloading: /podcasts/littlebit/2010-06-06.mp3
    0: Looking for the next enclosure
    0: Downloading: /podcasts/littlebit/2010-07-26.mp3
    0: Looking for the next enclosure
    0: Downloading: /podcasts/littlebit/2010-11-25.mp3
    0: Looking for the next enclosure
    *** Done

The actual output will depend on the contents of the RSS feed used.

.. seealso::

    `Queue <http://docs.python.org/lib/module-Queue.html>`_
        Standard library documentation for this module.

    :ref:`deque` from :mod:`collections`
        The ``collections`` module includes a deque (double-ended queue) class.
    
    `Queue data structures <http://en.wikipedia.org/wiki/Queue_(data_structure)>`__
        Wikipedia article explaining queues.

    `FIFO <http://en.wikipedia.org/wiki/FIFO>`__
        Wikipedia article explaining first in, first out, data structures.
