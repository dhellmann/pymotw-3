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
