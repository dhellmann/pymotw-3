Test Data
=========

This text produced by a Lorem Ipsum generator is used as sample input.

.. include:: linecache_data.py
    :literal:
    :start-after: #end_pymotw_header

Reading Specific Lines
======================

The line numbers of files read by the :mod:`linecache` module start
with 1, but normally lists start indexing the array from 0.

.. include:: linecache_getline.py
    :literal:
    :start-after: #end_pymotw_header

Each line returned includes a trailing newline.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'linecache_getline.py'))
.. }}}

::

	$ python linecache_getline.py
	
	SOURCE:
	'fermentum id, nonummy a, nonummy sit amet, ligula. Curabitur'
	
	CACHE:
	'fermentum id, nonummy a, nonummy sit amet, ligula. Curabitur\n'

.. {{{end}}}

Handling Blank Lines
====================

The return value always includes the newline at the end of the line,
so if the line is empty the return value is just the newline.

.. include:: linecache_empty_line.py
    :literal:
    :start-after: #end_pymotw_header

Line eight of the input file contains no text.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'linecache_empty_line.py'))
.. }}}

::

	$ python linecache_empty_line.py
	
	BLANK : '\n'

.. {{{end}}}

Error Handling
==============

If the requested line number falls out of the range of valid lines in the
file, :func:`getline` returns an empty string. 

.. include:: linecache_out_of_range.py
    :literal:
    :start-after: #end_pymotw_header

The input file only has 12 lines, so requesting line 500 is like
trying to read past the end of the file.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'linecache_out_of_range.py'))
.. }}}

::

	$ python linecache_out_of_range.py
	
	NOT THERE: '' includes 0 characters

.. {{{end}}}

Reading from a file that does not exist is handled in the same way.

.. include:: linecache_missing_file.py
    :literal:
    :start-after: #end_pymotw_header

The module never raises an exception when the caller tries to read data.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'linecache_missing_file.py'))
.. }}}

::

	$ python linecache_missing_file.py
	
	NO FILE: ''

.. {{{end}}}
