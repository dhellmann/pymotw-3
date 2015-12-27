=================================================================
 asyncio --- Asynchronous I/O, event loop, and concurrency tools
=================================================================

.. module:: asyncio
   :synopsis: Asynchronous I/O, event loop, and concurrency tools

:Purpose: An asynchronous I/O and concurrency framework.

The :mod:`asyncio` module provides tools for building concurrent
applications using coroutines. While the :mod:`threading` module
implements concurrency through application threads and
:mod:`multiprocessing` implements concurrency using system processes,
:mod:`asyncio` uses a single-threaded, single-process approach in
which parts of an application cooperate to switch tasks explicitly at
optimal times. Most often this context switching occurs when the
program would otherwise block waiting to read or write data, but
:mod:`asyncio` also includes support for scheduling code to run in the
future, to enable one coroutine to wait for another to complete, for
handling system signals, and for recognizing other events that may be
reasons for an application to change what it is working on.

.. note::

   :mod:`asyncio` is still a *provisional* module. The API may change
   in backwards-incompatible ways, and the entire module may be
   removed.

.. toctree::
   :maxdepth: 1

   concepts

..
    - concepts
        - event loop
        - coroutines — cooperative multi-tasking
    - futures & tasks
        - waiting
        - callbacks
    - basic transports and protocols
        - echo server example
            - create connection
            - read data
            - write data
        - echo client example (single)
            - create connection
            - write data
            - read data
    - using coroutines
        - echo server/client example from the previous example reproduced
        - sidebar: difference between async def and generator coroutines
            - maybe put this at the end of the chapter?
            - generator-based coroutines
            - native coroutines
        - chaining coroutines with await
        - streams
    - futures
        - waiting for a future from within another function
        - adding a done callback
            - use a multi-part task to calculate something and then set the result of a future, with a callback or something else waiting on the future (lots of fibonacci examples on the web, so do something else)
    - tasks
        - run_until_complete() vs. run_forever()
        - cancelling a task before it finishes
        - cancelling a task after it finishes (error)
        - adding a done callback (maybe the same as futures example?)
        - waiting for a background task from within a protocol
        - waiting for a task with a timeout
    - subprocesses
        - transport & protocol
        - coroutine
    - non-I/O events
        - scheduling based on the clock
            - call_soon
            - call_later
                - schedule two callbacks out of order using different sleep times, and have them executed in the opposite order they are scheduled
        - UNIX signals
    - sync tools
        - lock
        - event
        - queue
            - rewrite the podcast downloader example?
    - advanced topics
        - connecting with SSL
        - using wait(), gather(), and as_completed() to wait for groups of background tasks
            - multi-client echo example
        - stopping the event loop programmatically
        - pausing transport production in a protocol?
        - calling a blocking function using an executor
            - default, threading
            - other?
        - using existing sockets?
        - alternate event loops, esp. for Windows
    - enabling debugging
    - aiohttp third-party module


.. seealso::

    * :pydoc:`asyncio`

    * :pep:`3156` -- *Asynchronous IO Support Rebooted: the "asyncio"
      Module*

    * :pep:`380` -- *Syntax for Delegating to a Subgenerator*

    * :pep:`492` -- *Coroutines with async and await syntax*

    * :mod:`socket` -- Low-level network communication

    * :mod:`select` -- Low-level asynchronous I/O tools

    * :mod:`socketserver` -- Framework for creating network servers

    * `trollius <https://pypi.python.org/pypi/trollius>`__ -- A port
      of Tulip, the original version of asyncio, to Python 2.

    * `Twisted <https://twistedmatrix.com/>`__ -- An extensible
      framework for Python programming, with special focus on
      event-based network programming and multiprotocol integration.

    * `The New asyncio Module in Python 3.4: Event Loops
      <http://www.drdobbs.com/open-source/the-new-asyncio-module-in-python-34-even/240168401>`__
      -- Article by Gastón Hillar in Dr. Dobb's

    * `Exploring Python 3's Asyncio by Example
      <http://www.giantflyingsaucer.com/blog/?p=5557>`__ -- Blog post
      by Chat Lung

    * `A Web Crawler With asyncio Coroutines
      <http://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html>`__
      -- An article in *The Architecture of Open Source Applications*
      by A. Jesse Jiryu Davis and Guido van Rossum

    * `Playing with asyncio
      <http://www.getoffmalawn.com/blog/playing-with-asyncio>`__ --
      blog post by Nathan Hoad

    * `Async I/O and Python
      <https://blogs.gnome.org/markmc/2013/06/04/async-io-and-python/>`__
      -- blog post by Mark McLoughlin

    * *Unix Network Programming, Volume 1: The Sockets Networking API, 3/E*
      By W. Richard Stevens, Bill Fenner, and Andrew
      M. Rudoff. Published by Addison-Wesley Professional, 2004.
      ISBN-10: 0131411551

    * *Foundations of Python Network Programminng, 3/E* By Brandon
      Rhodes and John Goerzen. Published by Apress, 2014. ISBN-10:
      1430258543
