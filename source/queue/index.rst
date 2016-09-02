===========================================
 queue --- Thread-safe FIFO Implementation
===========================================

.. module:: queue
    :synopsis: Thread-safe FIFO implementation

:Purpose: Provides a thread-safe FIFO implementation

The :mod:`queue` module provides a first-in, first-out (FIFO) data
structure suitable for multi-threaded programming. It can be used to
pass messages or other data between producer and consumer threads
safely. Locking is handled for the caller, so many threads can work
with the same :class:`Queue` instance safely and easily. The size of a
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

.. literalinclude:: queue_fifo.py
   :caption:
   :start-after: #end_pymotw_header

This example uses a single thread to illustrate that elements are
removed from the queue in the same order they are inserted.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'queue_fifo.py'))
.. }}}

.. code-block:: none

	$ python3 queue_fifo.py
	
	0 1 2 3 4 

.. {{{end}}}

LIFO Queue
==========

In contrast to the standard FIFO implementation of :class:`Queue`, the
:class:`LifoQueue` uses last-in, first-out ordering (normally associated
with a stack data structure).

.. literalinclude:: queue_lifo.py
   :caption:
   :start-after: #end_pymotw_header

The item most recently :class:`put` into the queue is removed by
:class:`get`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'queue_lifo.py'))
.. }}}

.. code-block:: none

	$ python3 queue_lifo.py
	
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

.. literalinclude:: queue_priority.py
   :caption:
   :start-after: #end_pymotw_header

This example has multiple threads consuming the jobs, which are be
processed based on the priority of items in the queue at the time
:func:`get` was called.  The order of processing for items added to
the queue while the consumer threads are running depends on thread
context switching.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'queue_priority.py'))
.. }}}

.. code-block:: none

	$ python3 queue_priority.py
	
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
five most recent episodes from each feed to be downloaded, and
processes several downloads in parallel using threads. It does not
have enough error handling for production use, but the skeleton
implementation provides an example of using the :mod:`queue` module.

First, some operating parameters are established. Normally these would
come from user inputs (preferences, a database, etc.). The example
uses hard-coded values for the number of threads and list of URLs to
fetch.

.. literalinclude:: fetch_podcasts.py
   :caption:
   :lines: 6-25

The function :func:`download_enclosures` will run in the worker thread
and process the downloads using :mod:`urllib`.

.. literalinclude:: fetch_podcasts.py
   :lines: 28-46

Once the target function for the threads is defined, the worker
threads can be started. When :func:`download_enclosures` processes the
statement ``url = q.get()``, it blocks and waits until the queue has
something to return.  That means it is safe to start the threads
before there is anything in the queue.

.. literalinclude:: fetch_podcasts.py
   :lines: 49-57

The next step is to retrieve the feed contents using the
``feedparser`` module and enqueue the URLs of the enclosures. As soon
as the first URL is added to the queue, one of the worker threads
picks it up and starts downloading it. The loop will continue to add
items until the feed is exhausted, and the worker threads will take
turns dequeuing URLs to download them.

.. literalinclude:: fetch_podcasts.py
   :lines: 59-68

The only thing left to do is wait for the queue to empty out again,
using :func:`join`.

.. literalinclude:: fetch_podcasts.py
   :lines: 70-

Running the sample script produces output similar to the following.

.. code-block:: none

    $ python3 fetch_podcasts.py 
    
    worker-0: looking for the next enclosure
    worker-1: looking for the next enclosure
    MainThread: queuing turbogears-and-the-future-of-python-web-frameworks.mp3
    MainThread: queuing continuum-scientific-python-and-the-business-of-open-source.mp3
    MainThread: queuing openstack-cloud-computing-built-on-python.mp3
    MainThread: queuing pypy.js-pypy-python-in-your-browser.mp3
    MainThread: queuing machine-learning-with-python-and-scikit-learn.mp3
    MainThread: *** main thread waiting
    worker-0: downloading turbogears-and-the-future-of-python-web-frameworks.mp3
    worker-1: downloading continuum-scientific-python-and-the-business-of-open-source.mp3
    worker-0: looking for the next enclosure
    worker-0: downloading openstack-cloud-computing-built-on-python.mp3
    worker-1: looking for the next enclosure
    worker-1: downloading pypy.js-pypy-python-in-your-browser.mp3
    worker-0: looking for the next enclosure
    worker-0: downloading machine-learning-with-python-and-scikit-learn.mp3
    worker-1: looking for the next enclosure
    worker-0: looking for the next enclosure
    MainThread: *** done

The actual output will depend on the contents of the RSS feed used.

.. seealso::

    * :pydoc:`queue`

    * :ref:`deque` from :mod:`collections`

    * `Queue data structures
      <http://en.wikipedia.org/wiki/Queue_(data_structure)>`__ --
      Wikipedia article explaining queues.

    * `FIFO <http://en.wikipedia.org/wiki/FIFO>`__ -- Wikipedia
      article explaining first in, first out, data structures.

    * `feedparser module <https://pypi.python.org/pypi/feedparser>`__
      -- A module for parsing RSS and Atom feeds, created by Mark
      Pilgrim and maintained by Kurt McKee.
