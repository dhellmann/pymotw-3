===============================
 anydbm -- DBM-style Databases
===============================

.. module:: anydbm
    :synopsis: Interface to DBM-style databases

:Purpose: anydbm provides a generic dictionary-like interface to DBM-style, string-keyed databases
:Python Version: 1.4 and later

:mod:`anydbm` is a front-end for DBM-style databases that use simple
string values as keys to access records containing strings.  It uses
:mod:`whichdb` to identify databases, then opens them with the
appropriate module.  It is used as a back-end for :mod:`shelve`, which
stores objects in a DBM database using :mod:`pickle`.

Database Types
==============

Python comes with several modules for accessing DBM-style databases.
The implementation selected depends on the libraries available on the
current system and the options used when Python was compiled.

dbhash
------

The :mod:`dbhash` module is the primary back-end for :mod:`anydbm`.  It
uses the :mod:`bsddb` library to manage database files.  The semantics
for using :mod:`dbhash` databases are the same as those defined by the
:mod:`anydbm` API.

gdbm
----

:mod:`gdbm` is an updated version of the :mod:`dbm` library from the
GNU project.  It works the same as the other DBM implementations
described here, with a few changes to the *flags* supported by
:func:`open`.

Besides the standard ``'r'``, ``'w'``, ``'c'``, and ``'n'`` flags,
:func:`gdbm.open` supports:

    * ``'f'`` to open the database in *fast* mode. In fast mode,
      writes to the database are not synchronized.
    * ``'s'`` to open the database in *synchronized* mode. Changes to
      the database are written to the file as they are made, rather
      than being delayed until the database is closed or synced
      explicitly.
    * ``'u'`` to open the database unlocked.

dbm
---

The :mod:`dbm` module provides an interface to one of several C
implementations of the dbm format, depending on how the module was
configured during compilation.  The module attribute ``library``
identifies the name of the library ``configure`` was able to find when
the extension module was compiled.

dumbdbm
-------

The :mod:`dumbdbm` module is a portable fallback implementation of the
DBM API when no other implementations are available.  No external
dependencies are required to use :mod:`dumbdbm`, but it is slower than
most other implementations.


Creating a New Database
=======================

The storage format for new databases is selected by looking for each
of these modules in order:

- :mod:`dbhash`
- :mod:`gdbm`
- :mod:`dbm`
- :mod:`dumbdbm`

The :func:`open` function takes *flags* to control how the database
file is managed.  To create a new database when necessary, use
``'c'``.  Using ``'n'`` always creates a new database, overwriting an
existing file.

.. include:: anydbm_new.py
    :literal:
    :start-after: #end_pymotw_header

In this example, the file is always re-initialized.  

.. {{{cog
.. workdir = path(cog.inFile).dirname()
.. sh("cd %s; rm -f /tmp/example.db" % workdir)
.. cog.out(run_script(cog.inFile, 'anydbm_new.py'))
.. }}}

::

	$ python anydbm_new.py

	

.. {{{end}}}

:mod:`whichdb` reports the type of database that was created.

.. include:: anydbm_whichdb.py
    :literal:
    :start-after: #end_pymotw_header

Output from the example program will vary, depending on which modules
are installed on the system.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'anydbm_whichdb.py'))
.. }}}

::

	$ python anydbm_whichdb.py

	dbhash

.. {{{end}}}


Opening an Existing Database
============================

To open an existing database, use *flags* of either ``'r'`` (for
read-only) or ``'w'`` (for read-write).  Existing databases are
automatically given to :mod:`whichdb` to identify, so it as long as a
file can be identified, the appropriate module is used to open it.

.. include:: anydbm_existing.py
    :literal:
    :start-after: #end_pymotw_header

Once open, ``db`` is a dictionary-like object, with support for the
usual methods:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'anydbm_existing.py'))
.. }}}

::

	$ python anydbm_existing.py

	keys(): ['author', 'key', 'today']
	iterating: author Doug
	iterating: key value
	iterating: today Sunday
	db["author"] = Doug

.. {{{end}}}

Error Cases
===========

The keys of the database need to be strings.

.. include:: anydbm_intkeys.py
    :literal:
    :start-after: #end_pymotw_header

Passing another type results in a :class:`TypeError`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'anydbm_intkeys.py', ignore_error=True))
.. }}}

::

	$ python anydbm_intkeys.py

	TypeError: Integer keys only allowed for Recno and Queue DB's

.. {{{end}}}

Values must be strings or ``None``.

.. include:: anydbm_intvalue.py
    :literal:
    :start-after: #end_pymotw_header

A similar :class:`TypeError` is raised if a value is not a string.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'anydbm_intvalue.py', ignore_error=True))
.. }}}

::

	$ python anydbm_intvalue.py

	TypeError: Data values must be of type string or None.

.. {{{end}}}

.. seealso::

    `anydbm <http://docs.python.org/library/anydbm.html>`_
        The standard library documentation for this module.

    :mod:`shelve`
        Examples for the ``shelve`` module, which uses
        ``anydbm`` to store data.
