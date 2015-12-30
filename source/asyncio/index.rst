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
:mod:`asyncio` also includes support for scheduling code to run at a
specific future time, to enable one coroutine to wait for another to
complete, for handling system signals, and for recognizing other
events that may be reasons for an application to change what it is
working on.

.. toctree::
   :maxdepth: 1

   concepts
   coroutines
   scheduling
   futures
   tasks
   echo_protocol
   echo_coroutine

.. note::

   :mod:`asyncio` is still a *provisional* module. The API may change
   in backwards-incompatible ways, and the entire module may be
   removed, though that is much less likely.

..
    - futures
        - simple ensure future
        - running the loop until a future is done -- asyncio_future_wait.py
        - waiting for a future from within another coroutine (redundant with task examples)
        - adding a done callback -- asyncio_future_callback.py
    - tasks
        - scheduling a task -- asyncio_create_task.py
        - cancelling a task before it finishes -- asyncio_cancel_task.py
    - I/O examples
    - subprocesses
        - transport & protocol -- asyncio_subprocess_protocol.py
        - coroutine -- asyncio_subprocess_coroutine.py
        - sending data into a command and reading data back (some sort of filter) -- asyncio_subprocess_coroutine_write.py
    - non-I/O events
        - scheduling based on the clock
            - call_soon -- asyncio_call_soon.py
            - call_later -- asyncio_call_later.py
                - schedule two callbacks out of order using different sleep times, and have them executed in the opposite order they are scheduled
        - UNIX signals -- asyncio_signal.py
    - synchronization tools
        - lock -- asyncio_lock.py
        - event -- asyncio_event.py
        - condition -- asyncio_condition.py
        - queue -- asyncio_queue.py
            - rewrite the podcast downloader example?
    - advanced topics
        - connecting with SSL -- asyncio_echo_server_ssl.py and asyncio_echo_client_ssl.py
        - control flow
          - waiting for background tasks from within a coroutine -- asyncio_background_task.py
          - waiting for a task with a timeout -- asyncio_wait_task_timeout.py
          - using wait(), gather(), and as_completed() to wait for groups of background tasks
            - asyncio_wait_coroutines.py, asyncio_wait_tasks.py, asyncio_wait_task_timeout.py
            - asyncio_gather.py
            - asyncio_as_completed.py
        - run_until_complete() vs. run_forever()
        - stopping the event loop programmatically -- asyncio_stop.py
        - calling a blocking function using an executor
            - default, threading -- asyncio_executor_thread.py
            - process -- asyncio_executor_process.py
        - looking up a hostname -- asyncio_getaddrinfo.py
    - enabling debugging -- asyncio_debug.py
    - aiohttp third-party module
    - not sure about
        - pausing transport production in a protocol?
        - using existing sockets?
        - alternate event loops, esp. for Windows
        - waiting for a background task from within a protocol


.. seealso::

    * :pydoc:`asyncio`

    * :ref:`Porting notes for asyncio <porting-asyncio>`

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
