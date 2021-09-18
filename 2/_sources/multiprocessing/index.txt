================================================
multiprocessing -- Manage processes like threads
================================================

.. module:: multiprocessing
    :synopsis: Manage processes like threads.

:Purpose: Provides an API for managing processes.
:Available In: 2.6

The :mod:`multiprocessing` module includes a relatively simple API for
dividing work up between multiple processes.  It is based on the API
for :mod:`threading`, and in some cases is a drop-in replacement.  Due
to the similarity, the first few examples here are modified from the
:mod:`threading` examples.  Features provided by
:mod:`multiprocessing` but not available in :mod:`threading` are
covered later.

.. toctree::
    :maxdepth: 2
    
    basics
    communication
    mapreduce


.. seealso::

    `multiprocessing <http://docs.python.org/2.7/library/multiprocessing.html>`_
        The standard library documentation for this module.

    :mod:`threading`
        High-level API for working with threads.
