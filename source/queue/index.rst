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

.. include:: queue_fifo.py
   :literal:
   :start-after: #end_pymotw_header

This example uses a single thread to illustrate that elements are
removed from the queue in the same order they are inserted.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'queue_fifo.py'))
.. }}}

::

	$ python3 queue_fifo.py
	
	0 1 2 3 4 

.. {{{end}}}

LIFO Queue
==========

In contrast to the standard FIFO implementation of :class:`Queue`, the
:class:`LifoQueue` uses last-in, first-out ordering (normally associated
with a stack data structure).

.. include:: queue_lifo.py
   :literal:
   :start-after: #end_pymotw_header

The item most recently :class:`put` into the queue is removed by
:class:`get`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'queue_lifo.py'))
.. }}}

::

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

.. include:: queue_priority.py
   :literal:
   :start-after: #end_pymotw_header

This example has multiple threads consuming the jobs, which are be
processed based on the priority of items in the queue at the time
:func:`get` was called.  The order of processing for items added to
the queue while the consumer threads are running depends on thread
context switching.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'queue_priority.py'))
.. }}}

::

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
five most recent episodes to be downloaded, and processes several
downloads in parallel using threads. It does not have enough error
handling for production use, but the skeleton implementation provides an
example of using the :mod:`Queue` module.

First, some operating parameters are established. Normally these would
come from user inputs (preferences, a database, etc.). The example
uses hard-coded values for the number of threads and list of URLs to
fetch.

.. literalinclude:: fetch_podcasts.py
   :lines: 6-25

The function :func:`download_enclosures` will run in the worker thread
and process the downloads using :mod:`urllib`.

.. literalinclude:: fetch_podcasts.py
   :lines: 28-47

Once the threads' target function is defined, the worker threads can
be started. When :func:`download_enclosures` processes the statement
``url = q.get()``, it blocks and waits until the queue has something
to return.  That means it is safe to start the threads before there is
anything in the queue.

.. literalinclude:: fetch_podcasts.py
   :lines: 50-58

The next step is to retrieve the feed contents using the
``feedparser`` module and enqueue the URLs of the enclosures. As soon
as the first URL is added to the queue, one of the worker threads
picks it up and starts downloading it. The loop will continue to add
items until the feed is exhausted, and the worker threads will take
turns dequeuing URLs to download them.

.. literalinclude:: fetch_podcasts.py
   :lines: 60-68

And the only thing left to do is wait for the queue to empty out
again, using :func:`join`.

.. literalinclude:: fetch_podcasts.py
   :lines: 70-

Running the sample script produces output similar to this.

::

    $ python fetch_podcasts.py 
    
    worker-0: looking for the next enclosure
    worker-1: looking for the next enclosure
    MainThread: queuing /episodes/download/35/turbogears-and-the-future-of-python-web-frameworks.mp3
    MainThread: queuing /episodes/download/34/continuum-scientific-python-and-the-business-of-open-source.mp3
    MainThread: queuing /episodes/download/33/openstack-cloud-computing-built-on-python.mp3
    MainThread: queuing /episodes/download/32/pypy.js-pypy-python-in-your-browser.mp3
    MainThread: queuing /episodes/download/31/machine-learning-with-python-and-scikit-learn.mp3
    MainThread: *** main thread waiting
    worker-0: downloading: /episodes/download/35/turbogears-and-the-future-of-python-web-frameworks.mp3
    worker-1: downloading: /episodes/download/34/continuum-scientific-python-and-the-business-of-open-source.mp3
    worker-0: writing to turbogears-and-the-future-of-python-web-frameworks.mp3
    worker-0: looking for the next enclosure
    worker-0: downloading: /episodes/download/33/openstack-cloud-computing-built-on-python.mp3
    worker-1: writing to continuum-scientific-python-and-the-business-of-open-source.mp3
    worker-1: looking for the next enclosure
    worker-1: downloading: /episodes/download/32/pypy.js-pypy-python-in-your-browser.mp3
    worker-0: writing to openstack-cloud-computing-built-on-python.mp3
    worker-0: looking for the next enclosure
    worker-0: downloading: /episodes/download/31/machine-learning-with-python-and-scikit-learn.mp3
    worker-1: writing to pypy.js-pypy-python-in-your-browser.mp3
    worker-1: looking for the next enclosure
    worker-0: writing to machine-learning-with-python-and-scikit-learn.mp3
    worker-0: looking for the next enclosure
    MainThread: *** done

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

    * `feedparser module <https://pypi.python.org/pypi/feedparser>`__
