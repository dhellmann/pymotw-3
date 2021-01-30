=================================================================
 asyncio --- Asynchronous I/O, event loop, and concurrency tools
=================================================================

.. module:: asyncio
   :synopsis: Asynchronous I/O, event loop, and concurrency tools

:Purpose: An asynchronous I/O and concurrency framework.

The ``asyncio`` module provides tools for building concurrent
applications using coroutines. While the :mod:`threading` module
implements concurrency through application threads and
:mod:`multiprocessing` implements concurrency using system processes,
``asyncio`` uses a single-threaded, single-process approach in
which parts of an application cooperate to switch tasks explicitly at
optimal times. Most often this context switching occurs when the
program would otherwise block waiting to read or write data, but
``asyncio`` also includes support for scheduling code to run at a
specific future time, to enable one coroutine to wait for another to
complete, for handling system signals, and for recognizing other
events that may be reasons for an application to change what it is
working on.

.. toctree::

   concepts
   coroutines
   scheduling
   futures
   tasks
   control
   synchronization
   io_protocol
   io_coroutine
   ssl
   dns
   subprocesses
   unix_signals
   executors
   debugging

.. note::

   In Python 3.5, ``asyncio`` is still a *provisional* module. The API
   was stablized in Python 3.6, and most of the changes were
   backported to later patch releases of Python 3.5. As a result, the
   module may work slightly differently under different versions of
   Python 3.5.

..
   - run_until_complete() vs. run_forever()
   - stopping the event loop programmatically -- asyncio_stop.py
   - aiohttp third-party module
   - not sure about
     - pausing transport production in a protocol?
     - using existing sockets?
     - alternate event loops, esp. for Windows
     - waiting for a background task from within a protocol


.. seealso::

    * :pydoc:`asyncio`

    * :pep:`3156` -- *Asynchronous IO Support Rebooted: the "asyncio"
      Module*

    * :pep:`380` -- *Syntax for Delegating to a Subgenerator*

    * :pep:`492` -- *Coroutines with async and await syntax*

    * :mod:`concurrent.futures` -- Manage Pools of Concurrent Tasks

    * :mod:`socket` -- Low-level network communication

    * :mod:`select` -- Low-level asynchronous I/O tools

    * :mod:`socketserver` -- Framework for creating network servers

    * `asyncio: What's New in Python 3.6
      <https://docs.python.org/3/whatsnew/3.6.html#asyncio>`__ --
      Summary of the changes to ``asyncio`` as the API stablized in
      Python 3.6.

    * `trollius <https://pypi.python.org/pypi/trollius>`__ -- A port
      of Tulip, the original version of asyncio, to Python 2.

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

    * `A Curious Course on Coroutines and Concurrency
      <http://www.dabeaz.com/coroutines/>`__ -- PyCon 2009 tutorial by
      David Beazley

    * `How the heck does async/await work in Python 3.5?
      <http://www.snarky.ca/how-the-heck-does-async-await-work-in-python-3-5>`__
      -- blog post by Brett Cannon

    * *Unix Network Programming, Volume 1: The Sockets Networking API, 3/E*
      By W. Richard Stevens, Bill Fenner, and Andrew
      M. Rudoff. Published by Addison-Wesley Professional, 2004.
      ISBN-10: 0131411551

    * *Foundations of Python Network Programminng, 3/E* By Brandon
      Rhodes and John Goerzen. Published by Apress, 2014. ISBN-10:
      1430258543
