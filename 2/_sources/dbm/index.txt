================================
dbm -- Simple database interface
================================

.. module:: dbm
    :synopsis: Simple database interface

:Purpose: Provides an interface to the Unix (n)dbm library.
:Available In: 1.4 and later

The :mod:`dbm` module provides an interface to one of the dbm
libraries, depending on how the module was configured during
compilation.

Examples
========

The ``library`` attribute identifies the library being used, by name.

.. include:: dbm_library.py
    :literal:
    :start-after: #end_pymotw_header

Your results will depend on what library ``configure`` was able to
find when the interpreter was built.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'dbm_library.py'))
.. }}}

::

	$ python dbm_library.py
	
	GNU gdbm

.. {{{end}}}

The :func:`open()` function follows the same semantics as the
:mod:`anydbm` module.

.. seealso::

    `dbm <http://docs.python.org/2.7/library/dbm.html>`_
        The standard library documentation for this module.

    :mod:`anydbm`
        The :mod:`anydbm` module.
