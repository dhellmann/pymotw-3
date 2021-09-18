##############################################
gdbm -- GNU's version of the dbm library
##############################################

.. module:: gdbm
    :synopsis: GNU's version of the dbm library

:Purpose: GNU's version of the dbm library
:Available In: 1.4 and later

:mod:`gdbm` is GNU's updated version of the :mod:`dbm` library.  It follows the same semantics as the other DBM implementations described under :mod:`anydbm`, with a few changes to the *flags* supported by ``open()``.

Besides the standard ``'r'``, ``'w'``, ``'c'``, and ``'n'`` flags, ``gdbm.open()`` supports:

    * ``'f'`` to open the database in *fast* mode. In fast mode, writes to the database are not synchronized.
    * ``'s'`` to open the database in *synchronized* mode. Changes to the database are written to the file as they are made, rather than being delayed until the database is closed or synced explicitly.
    * ``'u'`` to open the database unlocked.


.. seealso::

    `gdbm <http://docs.python.org/2.7/library/gdbm.html>`_
        The standard library documentation for this module.

    :mod:`dbm`
        The :mod:`dbm` module.
    
    :mod:`anydbm`
        The :mod:`anydbm` module.
