==========================================
 shelve --- Persistent Storage of Objects
==========================================

.. module:: shelve
    :synopsis: Persistent storage of objects

The ``shelve`` module can be used as a simple persistent storage
option for Python objects when a relational database is not
required. The shelf is accessed by keys, just as with a
dictionary. The values are pickled and written to a database created
and managed by :mod:`dbm`.

Creating a new Shelf
====================

The simplest way to use ``shelve`` is via the :class:`DbfilenameShelf`
class. It uses :mod:`dbm` to store the data. The class can be used
directly, or by calling :func:`shelve.open()`:

.. literalinclude:: shelve_create.py
   :caption:
   :start-after: #end_pymotw_header

To access the data again, open the shelf and use it like a dictionary:

.. literalinclude:: shelve_existing.py
   :caption:
   :start-after: #end_pymotw_header

Running both sample scripts produces:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shelve_create.py', trailing_newlines=False))
.. cog.out(run_script(cog.inFile, 'shelve_existing.py', include_prefix=False))
.. }}}

.. code-block:: none

	$ python3 shelve_create.py
	$ python3 shelve_existing.py
	
	{'string': 'Sample data', 'int': 10, 'float': 9.5}

.. {{{end}}}


The :mod:`dbm` module does not support multiple applications writing
to the same database at the same time, but it does support concurrent
read-only clients. If a client will not be modifying the shelf, tell
``shelve`` to open the database read-only by passing ``flag='r'``.

.. literalinclude:: shelve_readonly.py
   :caption:
   :start-after: #end_pymotw_header

If the program tries to modify the database while it is opened read-only, an
access error exception is generated. The exception type depends on the
database module selected by :mod:`dbm` when the database was created.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shelve_readonly.py'))
.. }}}

.. code-block:: none

	$ python3 shelve_readonly.py
	
	Existing: {'string': 'Sample data', 'int': 10, 'float': 9.5}
	ERROR: cannot add item to database

.. {{{end}}}

Write-back
==========

Shelves do not track modifications to volatile objects, by
default. That means if the contents of an item stored in the shelf are
changed, the shelf must be updated explicitly by storing the entire item
again.

.. literalinclude:: shelve_withoutwriteback.py
   :caption:
   :start-after: #end_pymotw_header

In this example, the dictionary at ``'key1'`` is not stored again, so when the
shelf is re-opened, the changes have not been preserved.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shelve_create.py', trailing_newlines=False))
.. cog.out(run_script(cog.inFile, 'shelve_withoutwriteback.py', include_prefix=False))
.. }}}

.. code-block:: none

	$ python3 shelve_create.py
	$ python3 shelve_withoutwriteback.py
	
	{'string': 'Sample data', 'int': 10, 'float': 9.5}
	{'string': 'Sample data', 'int': 10, 'float': 9.5}

.. {{{end}}}

To automatically catch changes to volatile objects stored in the
shelf, open it with writeback enabled. The ``writeback`` flag causes the
shelf to remember all of the objects retrieved from the database using
an in-memory cache. Each cache object is also written back to the
database when the shelf is closed.

.. literalinclude:: shelve_writeback.py
   :caption:
   :start-after: #end_pymotw_header

Although it reduces the chance of programmer error, and can make
object persistence more transparent, using writeback mode may not be
desirable in every situation. The cache consumes extra memory while
the shelf is open, and pausing to write every cached object back to
the database when it is closed slows down the application.  All of the
cached objects are written back to the database because there is no
way to tell if they have been modified. If the application reads data
more than it writes, writeback will impact performance unnecessarily.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shelve_create.py', trailing_newlines=False))
.. cog.out(run_script(cog.inFile, 'shelve_writeback.py', include_prefix=False))
.. }}}

.. code-block:: none

	$ python3 shelve_create.py
	$ python3 shelve_writeback.py
	
	Initial data:
	{'float': 9.5, 'int': 10, 'string': 'Sample data'}
	
	Modified:
	{'float': 9.5,
	 'int': 10,
	 'new_value': 'this was not here before',
	 'string': 'Sample data'}
	
	Preserved:
	{'float': 9.5,
	 'int': 10,
	 'new_value': 'this was not here before',
	 'string': 'Sample data'}

.. {{{end}}}

.. _shelve-shelf-types:

Specific Shelf Types
====================

The earlier examples all used the default shelf implementation. Using
:func:`shelve.open()` instead of one of the shelf implementations
directly is a common usage pattern, especially if it does not matter
what type of database is used to store the data. There are times,
however, when the database format is important. In those situations,
use :class:`DbfilenameShelf` or :class:`BsdDbShelf` directly, or even
subclass :class:`Shelf` for a custom solution.

.. seealso::

   * :pydoc:`shelve`

   * :mod:`dbm` -- The ``dbm`` module finds an available DBM
     library to create a new database.

   * `feedcache <https://bitbucket.org/dhellmann/feedcache>`_ -- The
     ``feedcache`` module uses ``shelve`` as a default storage option.

   * `shove <http://pypi.python.org/pypi/shove/>`_ -- Shove implements
     a similar API with more back-end formats.
