##############################################################
shelve -- Persistent storage of arbitrary Python objects
##############################################################

.. module:: shelve
    :synopsis: Persistent storage of arbitrary Python objects

:Purpose: The shelve module implements persistent storage for arbitrary Python objects which can be pickled, using a dictionary-like API.

The :mod:`shelve` module can be used as a simple persistent storage
option for Python objects when a relational database is overkill. The
shelf is accessed by keys, just as with a dictionary. The values are
pickled and written to a database created and managed by
:mod:`anydbm`.

====================
Creating a new Shelf
====================

The simplest way to use shelve is via the :class:`DbfilenameShelf`
class. It uses anydbm to store the data. You can use the class
directly, or simply call :func:`shelve.open()`:

.. include:: shelve_create.py
    :literal:
    :start-after: #end_pymotw_header

To access the data again, open the shelf and use it like a dictionary:

.. include:: shelve_existing.py
    :literal:
    :start-after: #end_pymotw_header

If you run both sample scripts, you should see:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shelve_create.py', trailing_newlines=False))
.. cog.out(run_script(cog.inFile, 'shelve_existing.py', include_prefix=False))
.. }}}

::

	$ python shelve_create.py
	$ python shelve_existing.py
	
	{'int': 10, 'float': 9.5, 'string': 'Sample data'}

.. {{{end}}}


The :mod:`dbm` module does not support multiple applications writing to the same
database at the same time. If you know your client will not be modifying the
shelf, you can tell shelve to open the database read-only.

.. include:: shelve_readonly.py
    :literal:
    :start-after: #end_pymotw_header

If your program tries to modify the database while it is opened read-only, an
access error exception is generated. The exception type depends on the
database module selected by anydbm when the database was created.

==========
Write-back
==========

Shelves do not track modifications to volatile objects, by default. That means
if you change the contents of an item stored in the shelf, you must update the
shelf explicitly by storing the item again.

.. include:: shelve_withoutwriteback.py
    :literal:
    :start-after: #end_pymotw_header

In this example, the dictionary at 'key1' is not stored again, so when the
shelf is re-opened, the changes have not been preserved.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shelve_create.py', trailing_newlines=False))
.. cog.out(run_script(cog.inFile, 'shelve_withoutwriteback.py', include_prefix=False))
.. }}}

::

	$ python shelve_create.py
	$ python shelve_withoutwriteback.py
	
	{'int': 10, 'float': 9.5, 'string': 'Sample data'}
	{'int': 10, 'float': 9.5, 'string': 'Sample data'}

.. {{{end}}}

To automatically catch changes to volatile objects stored in the shelf, open
the shelf with writeback enabled. The writeback flag causes the shelf to
remember all of the objects retrieved from the database using an in-memory
cache. Each cache object is also written back to the database when the shelf
is closed. 

.. include:: shelve_writeback.py
    :literal:
    :start-after: #end_pymotw_header

Although it reduces the chance of programmer error, and can make object
persistence more transparent, using writeback mode may not be desirable in
every situation. The cache consumes extra memory while the shelf is open, and
pausing to write every cached object back to the database when it is closed
can take extra time. Since there is no way to tell if the cached objects have
been modified, they are all written back. If your application reads data more
than it writes, writeback will add more overhead than you might want.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shelve_create.py', trailing_newlines=False))
.. cog.out(run_script(cog.inFile, 'shelve_writeback.py', include_prefix=False))
.. }}}

::

	$ python shelve_create.py
	$ python shelve_writeback.py
	
	{'int': 10, 'float': 9.5, 'string': 'Sample data'}
	{'int': 10, 'new_value': 'this was not here before', 'float': 9.5, 'string': 'Sample data'}
	{'int': 10, 'new_value': 'this was not here before', 'float': 9.5, 'string': 'Sample data'}

.. {{{end}}}


.. _shelve-shelf-types:

====================
Specific Shelf Types
====================

The examples above all use the default shelf implementation. Using
:func:`shelve.open()` instead of one of the shelf implementations
directly is a common usage pattern, especially if you do not care what
type of database is used to store the data. There are times, however,
when you do care. In those situations, you may want to use
:class:`DbfilenameShelf` or :class:`BsdDbShelf` directly, or even
subclass :class:`Shelf` for a custom solution.

.. seealso::

    `shelve <https://docs.python.org/2/library/shelve.html>`_
        Standard library documentation for this module.

    :mod:`anydbm`
        The anydbm module.

    `feedcache <http://www.doughellmann.com/projects/feedcache/>`_
        The feedcache module uses shelve as a default storage option.

    `shove <http://pypi.python.org/pypi/shove/>`_
        Shove implements a similar API with more backend formats.

    :ref:`article-data-persistence`
        Other mechanisms for storing data using standard library modules.
