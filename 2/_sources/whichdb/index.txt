####################################################
whichdb -- Identify DBM-style database formats
####################################################

.. module:: whichdb
    :synopsis: Identify DBM-style database formats

:Purpose: Examine existing DBM-style database file to determine what library should be used to open it.
:Available In: 1.4 and later

The :mod:`whichdb` module contains one function, ``whichdb()``.  It can be used to examine an existing database file to determine which dbm library should be used to open it.  It returns ``None`` if there is a problem opening the file, or the string name of the module to use to open the file.  If it can open the file but cannot determine the library to use, it returns the empty string.

.. include:: whichdb_whichdb.py
    :literal:
    :start-after: #end_pymotw_header

Your results will vary, depending on what modules are available in your PYTHONPATH.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'whichdb_whichdb.py'))
.. }}}

::

	$ python whichdb_whichdb.py
	
	dbhash

.. {{{end}}}


.. seealso::

    `whichdb <https://docs.python.org/2/library/whichdb.html>`_
        Standard library documentation for this module.

    :mod:`anydbm`
        The anydbm module uses the best available DBM implementation when creating new databases.
    
    :mod:`shelve`
        The shelve module provides a mapping-style API for DBM databases.
