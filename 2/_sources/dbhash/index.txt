====================================================
dbhash -- DBM-style API for the BSD database library
====================================================

.. module:: dbhash
    :synopsis: DBM-style API for the BSD database library

:Purpose: Provides a dictionary-like API for accessing BSD ``db`` files.
:Available In: 1.4 and later

The :mod:`dbhash` module is the primary backend for :mod:`anydbm`.  It uses the :mod:`bsddb` library to manage database files.  The semantics are the same as :mod:`anydbm`, so refer to the examples on that page for details.

.. seealso::

    `dbhash <http://docs.python.org/2.7/library/dbhash.html>`_
        The standard library documentation for this module.

    :mod:`anydbm`
        The :mod:`anydbm` module.
