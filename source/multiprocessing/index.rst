================================================
multiprocessing -- Manage Processes Like Threads
================================================

.. module:: multiprocessing
    :synopsis: Manage processes like threads.

:Purpose: Provides an API for managing processes.

The :mod:`multiprocessing` module includes an API for dividing work up
between multiple processes based on the API for :mod:`threading`.  In
some cases :mod:`multiprocessing` is a drop-in replacement, and can be
used instead of :mod:`threading` to take advantage of multiple CPU
cores to avoid computational bottlenecks associated with Python's
global interpreter lock.  

Due to the similarity, the first few examples here are modified from
the :mod:`threading` examples.  Features provided by
:mod:`multiprocessing` but not available in :mod:`threading` are
covered later.

.. toctree::
    :maxdepth: 2
    
    basics
    communication
    mapreduce


.. seealso::

    `multiprocessing <http://docs.python.org/library/multiprocessing.html>`_
        The standard library documentation for this module.

    :mod:`threading`
        High-level API for working with threads.

    `MapReduce - Wikipedia <http://en.wikipedia.org/wiki/MapReduce>`_
        Overview of MapReduce on Wikipedia.
    
    `MapReduce: Simplified Data Processing on Large Clusters <http://labs.google.com/papers/mapreduce.html>`_
        Google Labs presentation and paper on MapReduce.

    :mod:`operator`
        Operator tools such as ``itemgetter``.
