==========================================
Queue -- A thread-safe FIFO implementation
==========================================

.. module:: Queue
    :synopsis: Provides a thread-safe FIFO implementation

:Purpose: Provides a thread-safe FIFO implementation
:Available In: at least 1.4

The :mod:`Queue` module provides a FIFO implementation suitable for
multi-threaded programming. It can be used to pass messages or other
data between producer and consumer threads safely. Locking is handled
for the caller, so it is simple to have as many threads as you want
working with the same Queue instance. A Queue's size (number of
elements) may be restricted to throttle memory usage or processing.

.. note::

    This discussion assumes you already understand the general nature
    of a queue. If you don't, you may want to read some of the
    references before continuing.

Basic FIFO Queue
================

The ``Queue`` class implements a basic first-in, first-out container.
Elements are added to one "end" of the sequence using ``put()``, and
removed from the other end using ``get()``.

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
	
	0
	1
	2
	3
	4

.. {{{end}}}

LIFO Queue
==========

In contrast to the standard FIFO implementation of ``Queue``, the
``LifoQueue`` uses last-in, first-out ordering (normally associated
with a stack data structure).

.. include:: Queue_lifo.py
   :literal:
   :start-after: #end_pymotw_header

The item most recently ``put()`` into the queue is removed by
``get()``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'Queue_lifo.py'))
.. }}}

::

	$ python Queue_lifo.py
	
	4
	3
	2
	1
	0

.. {{{end}}}

.. _Queue-PriorityQueue:

Priority Queue
==============

Sometimes the processing order of the items in a queue needs to be
based on characteristics of those items, rather than just the order
they are created or added to the queue.  For example, print jobs from
the payroll department may take precedence over a code listing printed
by a developer.  ``PriorityQueue`` uses the sort order of the contents
of the queue to decide which to retrieve.

.. include:: Queue_priority.py
   :literal:
   :start-after: #end_pymotw_header

In this single-threaded example, the jobs are pulled out of the queue
in strictly priority order.  If there were multiple threads consuming
the jobs, they would be processed based on the priority of items in
the queue at the time ``get()`` was called.

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



Using Queues with Threads
=========================

As an example of how to use the Queue class with multiple threads, we
can create a very simplistic podcasting client. This client reads one
or more RSS feeds, queues up the enclosures for download, and
processes several downloads in parallel using threads. It is
simplistic and unsuitable for actual use, but the skeleton
implementation gives us enough code to work with to provide an example
of using the Queue module.

.. include:: fetch_podcasts.py
    :literal:
    :start-after: #end_pymotw_header

First, we establish some operating parameters. Normally these would
come from user inputs (preferences, a database, whatever). For our
example we hard code the number of threads to use and the list of URLs
to fetch.

Next, we need to define the function ``downloadEnclosures()`` that
will run in the worker thread, processing the downloads. Again, for
illustration purposes this only simulates the download. To actually
download the enclosure, you might use :mod:`urllib` or
:mod:`urllib2`. In this example, we simulate a download delay by
sleeping a variable amount of time, depending on the thread id.

Once the threads' target function is defined, we can start the worker
threads. Notice that downloadEnclosures() will block on the statement
``url = q.get()`` until the queue has something to return, so it is
safe to start the threads before there is anything in the queue.

The next step is to retrieve the feed contents (using Mark Pilgrim's
`feedparser`_ module) and enqueue the URLs of the enclosures. As soon
as the first URL is added to the queue, one of the worker threads
should pick it up and start downloading it. The loop below will
continue to add items until the feed is exhausted, and the worker
threads will take turns dequeuing URLs to download them.

And the only thing left to do is wait for the queue to empty out
again, using ``join()``.

If you run the sample script, you should see output something like
this:

::

    0: Looking for the next enclosure
    1: Looking for the next enclosure
    Queuing: http://http.earthcache.net/htc-01.media.globix.net/COMP009996MOD1/Danny_Meyer.mp3
    Queuing: http://feeds.feedburner.com/~r/drmoldawer/~5/104445110/moldawerinthemorning_show34_032607.mp3
    Queuing: http://www.podtrac.com/pts/redirect.mp3/twit.cachefly.net/MBW-036.mp3
    Queuing: http://media1.podtech.net/media/2007/04/PID_010848/Podtech_calacaniscast22_ipod.mp4
    Queuing: http://media1.podtech.net/media/2007/03/PID_010592/Podtech_SXSW_KentBrewster_ipod.mp4
    Queuing: http://media1.podtech.net/media/2007/02/PID_010171/Podtech_IDM_ChrisOBrien2.mp3
    Queuing: http://feeds.feedburner.com/~r/drmoldawer/~5/96188661/moldawerinthemorning_show30_022607.mp3
    *** Main thread waiting
    0: Downloading: http://http.earthcache.net/htc-01.media.globix.net/COMP009996MOD1/Danny_Meyer.mp3
    1: Downloading: http://feeds.feedburner.com/~r/drmoldawer/~5/104445110/moldawerinthemorning_show34_032607.mp3
    0: Looking for the next enclosure
    0: Downloading: http://www.podtrac.com/pts/redirect.mp3/twit.cachefly.net/MBW-036.mp3
    1: Looking for the next enclosure
    1: Downloading: http://media1.podtech.net/media/2007/04/PID_010848/Podtech_calacaniscast22_ipod.mp4
    0: Looking for the next enclosure
    0: Downloading: http://media1.podtech.net/media/2007/03/PID_010592/Podtech_SXSW_KentBrewster_ipod.mp4
    0: Looking for the next enclosure
    0: Downloading: http://media1.podtech.net/media/2007/02/PID_010171/Podtech_IDM_ChrisOBrien2.mp3
    1: Looking for the next enclosure
    1: Downloading: http://feeds.feedburner.com/~r/drmoldawer/~5/96188661/moldawerinthemorning_show30_022607.mp3
    0: Looking for the next enclosure
    1: Looking for the next enclosure
    *** Done

The actual output will depend on whether anyone modifies the
subscriptions in the guest account on http://www.CastSampler.com.


.. seealso::

    `Queue <https://docs.python.org/2/library/Queue.html>`_
        Standard library documentation for this module.

    :ref:`deque` from :mod:`collections`
        collections includes a deque (double-ended queue) class
    
    *Wikipedia: Queue data structures*
        http://en.wikipedia.org/wiki/Queue_(data_structure)

    *Wikipedia: FIFO*
        http://en.wikipedia.org/wiki/FIFO

    `feedparser`_
        Mark Pilgrim's feedparser module (http://www.feedparser.org/).
    
    :ref:`article-data-structures`
        Other complex data structures in the standard library.

.. _feedparser: http://www.feedparser.org/
