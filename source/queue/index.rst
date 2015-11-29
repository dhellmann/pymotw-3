==========================================
 Queue -- Thread-safe FIFO Implementation
==========================================

.. module:: Queue
    :synopsis: Thread-safe FIFO implementation

:Purpose: Provides a thread-safe FIFO implementation
:Python Version: at least 1.4

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

.. toctree::

   normal

.. only:: bonus

   .. toctree:: 

      bonus

.. seealso::

    `Queue <http://docs.python.org/lib/module-Queue.html>`_
        Standard library documentation for this module.

    :ref:`deque` from :mod:`collections`
        The ``collections`` module includes a deque (double-ended queue) class.
    
    `Queue data structures <http://en.wikipedia.org/wiki/Queue_(data_structure)>`__
        Wikipedia article explaining queues.

    `FIFO <http://en.wikipedia.org/wiki/FIFO>`__
        Wikipedia article explaining first in, first out, data structures.
