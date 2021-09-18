======================================
dumbdbm -- Portable DBM Implementation
======================================

.. module:: dumbdbm
    :synopsis: Portable DBM Implementation

:Purpose: Last-resort backend implementation for :mod:`anydbm`.
:Available In: 1.4 and later

The :mod:`dumbdbm` module is a portable fallback implementation of the DBM API when no other implementations are available.  No external dependencies are required to use :mod:`dumbdbm`, but it is slower than most other implementations.

It follows the semantics of the :mod:`anydbm` module.

.. seealso::

    `dumbdbm <http://docs.python.org/2.7/library/dumbdbm.html>`_
        The standard library documentation for this module.

    :mod:`anydbm`
        The :mod:`anydbm` module.
