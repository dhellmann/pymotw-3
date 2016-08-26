Reading Python Source Files
===========================

Since :mod:`linecache` is used so heavily when producing tracebacks,
one of its key features is the ability to find Python source modules
in the import path by specifying the base name of the module. 

.. include:: linecache_path_search.py
    :literal:
    :start-after: #end_pymotw_header

The cache population code in :mod:`linecache` searches
:data:`sys.path` for the named module if it cannot find a file with
that name in the current directory.  This example looks for
``linecache.py``.  Since there is no copy in the current directory,
the file from the standard library is found instead.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'linecache_path_search.py', 
..                    break_lines_at=76, line_break_mode='wrap'))
.. }}}

::

	$ python linecache_path_search.py
	
	MODULE:
	'This is intended to read lines from modules imported -- hence if a
	filename\n'
	
	FILE:
	'This is intended to read lines from modules imported -- hence if a
	filename\n'

.. {{{end}}}
