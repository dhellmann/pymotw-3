==================================
 dbm --- Unix Key-Value Databases
==================================

.. module:: dbm
    :synopsis: Unix Key-Value Databases

:Purpose: dbm provides a generic dictionary-like interface to DBM-style, string-keyed databases

``dbm`` is a front-end for DBM-style databases that use simple
string values as keys to access records containing strings.  It uses
:func:`whichdb` to identify databases, then opens them with the
appropriate module.  It is used as a back-end for :mod:`shelve`, which
stores objects in a DBM database using :mod:`pickle`.

Database Types
==============

Python comes with several modules for accessing DBM-style databases.
The default implementation selected depends on the libraries available
on the current system and the options used when Python was
compiled. Separate interfaces to the specific implementations allow
Python programs to exchange data with programs in other languages that
do not automatically switch between available formats, or to write
portable data files that will work on multiple platforms.

dbm.gnu
-------

:mod:`dbm.gnu` is an interface to the version of the ``dbm``
library from the GNU project.  It works the same as the other DBM
implementations described here, with a few changes to the ``flags``
supported by :func:`open`.

Besides the standard ``'r'``, ``'w'``, ``'c'``, and ``'n'`` flags,
:func:`dbm.gnu.open` supports:

    * ``'f'`` to open the database in *fast* mode. In fast mode,
      writes to the database are not synchronized.
    * ``'s'`` to open the database in *synchronized* mode. Changes to
      the database are written to the file as they are made, rather
      than being delayed until the database is closed or synced
      explicitly.
    * ``'u'`` to open the database unlocked.

dbm.ndbm
--------

The :mod:`dbm.ndbm` module provides an interface to the Unix ndbm
implementations of the dbm format, depending on how the module was
configured during compilation.  The module attribute ``library``
identifies the name of the library ``configure`` was able to find when
the extension module was compiled.

dbm.dumb
--------

The :mod:`dbm.dumb` module is a portable fallback implementation of
the DBM API when no other implementations are available.  No external
dependencies are required to use :mod:`dbm.dumb`, but it is slower
than most other implementations.


Creating a New Database
=======================

The storage format for new databases is selected by looking for usable
versions of each of the sub-modules in order.

.. {{{cog
.. import dbm
.. cog.out('\n')
.. for n in dbm._names:
..   cog.out('- ``{}``\n'.format(n))
.. cog.out('\n')
.. }}}

- ``dbm.gnu``
- ``dbm.ndbm``
- ``dbm.dumb``

.. {{{end}}}

The :func:`open` function takes ``flags`` to control how the database
file is managed.  To create a new database when necessary, use
``'c'``.  Using ``'n'`` always creates a new database, overwriting an
existing file.

.. literalinclude:: dbm_new.py
    :caption:
    :start-after: #end_pymotw_header

In this example, the file is always re-initialized.

.. {{{cog
.. workdir = path(cog.inFile).dirname()
.. sh("cd %s; rm -f /tmp/example.db" % workdir)
.. cog.out(run_script(cog.inFile, 'dbm_new.py'))
.. }}}

.. code-block:: none

	$ python3 dbm_new.py
	

.. {{{end}}}

:func:`whichdb` reports the type of database that was created.

.. literalinclude:: dbm_whichdb.py
    :caption:
    :start-after: #end_pymotw_header

Output from the example program will vary, depending on which modules
are installed on the system.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'dbm_whichdb.py'))
.. }}}

.. code-block:: none

	$ python3 dbm_whichdb.py
	
	dbm.ndbm

.. {{{end}}}


Opening an Existing Database
============================

To open an existing database, use ``flags`` of either ``'r'`` (for
read-only) or ``'w'`` (for read-write).  Existing databases are
automatically given to :func:`whichdb` to identify, so it as long as a
file can be identified, the appropriate module is used to open it.

.. literalinclude:: dbm_existing.py
    :caption:
    :start-after: #end_pymotw_header

Once open, ``db`` is a dictionary-like object. New keys are always
converted to byte strings when added to the database, and returned as
byte strings.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'dbm_existing.py'))
.. }}}

.. code-block:: none

	$ python3 dbm_existing.py
	
	keys(): [b'key', b'today', b'author']
	iterating: b'key' b'value'
	iterating: b'today' b'Sunday'
	iterating: b'author' b'Doug'
	db["author"] = b'Doug'

.. {{{end}}}

Error Cases
===========

The keys of the database need to be strings.

.. literalinclude:: dbm_intkeys.py
    :caption:
    :start-after: #end_pymotw_header

Passing another type results in a :class:`TypeError`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'dbm_intkeys.py', ignore_error=True))
.. }}}

.. code-block:: none

	$ python3 dbm_intkeys.py
	
	dbm mappings have bytes or string keys only

.. {{{end}}}

Values must be strings or ``None``.

.. literalinclude:: dbm_intvalue.py
    :caption:
    :start-after: #end_pymotw_header

A similar :class:`TypeError` is raised if a value is not a string.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'dbm_intvalue.py', ignore_error=True))
.. }}}

.. code-block:: none

	$ python3 dbm_intvalue.py
	
	dbm mappings have byte or string elements only

.. {{{end}}}

.. seealso::

    * :pydoc:`dbm`

    * :ref:`Porting notes for anydbm <porting-anydbm>`

    * :ref:`Porting notes for whichdb <porting-whichdb>`

    * :mod:`shelve` -- Examples for the ``shelve`` module, which uses
      ``dbm`` to store data.
