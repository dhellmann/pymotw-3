.. _data-persistence:

================
Data Persistence
================

The standard library includes a variety of modules for persisting data.  The most common pattern for storing data from Python objects for reuse is to serialize them with :mod:`pickle` and then either write them directly to a file or store them using one of the many key-value pair database formats available with the *dbm* API.  If you don't care about the underlying dbm format, the best persistence interface is provided by :mod:`shelve`.  If you do care, you can use one of the other dbm-based modules directly.

.. toctree::
    :maxdepth: 1

    anydbm/index
    dbhash/index
    dbm/index
    dumbdbm/index
    gdbm/index
    pickle/index
    shelve/index
    whichdb/index
    sqlite3/index

For serializing over the web, the :mod:`json` module may be a better choice since its format is more portable.

.. seealso::

    :ref:`article-data-persistence`
