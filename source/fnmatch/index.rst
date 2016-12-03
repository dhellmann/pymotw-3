==============================================
 fnmatch --- Unix-style Glob Pattern Matching
==============================================

.. module:: fnmatch
    :synopsis: Compare filenames with Unix-style glob patterns.

:Purpose: Handle Unix-style filename comparisons.

The ``fnmatch`` module is used to compare filenames against
glob-style patterns such as used by Unix shells.

Simple Matching
===============

:func:`fnmatch` compares a single filename against a pattern and
returns a boolean, indicating whether or not they match. The comparison
is case-sensitive when the operating system uses a case-sensitive
file system.

.. literalinclude:: fnmatch_fnmatch.py
   :caption:
   :start-after: #end_pymotw_header

In this example, the pattern matches all files starting with
``'fnmatch_'`` and ending in ``'.py'``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fnmatch_fnmatch.py'))
.. }}}

.. code-block:: none

	$ python3 fnmatch_fnmatch.py
	
	Pattern : fnmatch_*.py
	
	Filename: fnmatch_filter.py         True
	Filename: fnmatch_fnmatch.py        True
	Filename: fnmatch_fnmatchcase.py    True
	Filename: fnmatch_translate.py      True
	Filename: index.rst                 False

.. {{{end}}}

To force a case-sensitive comparison, regardless of the file system and
operating system settings, use :func:`fnmatchcase`.

.. literalinclude:: fnmatch_fnmatchcase.py
   :caption:
   :start-after: #end_pymotw_header

Since the OS X system used to test this program uses a case-sensitive
file system, no files match the modified pattern.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fnmatch_fnmatchcase.py'))
.. }}}

.. code-block:: none

	$ python3 fnmatch_fnmatchcase.py
	
	Pattern : FNMATCH_*.PY
	
	Filename: fnmatch_filter.py         False
	Filename: fnmatch_fnmatch.py        False
	Filename: fnmatch_fnmatchcase.py    False
	Filename: fnmatch_translate.py      False
	Filename: index.rst                 False

.. {{{end}}}

Filtering
=========

To test a sequence of filenames, use :func:`filter`, which returns a
list of the names that match the pattern argument.

.. literalinclude:: fnmatch_filter.py
   :caption:
   :start-after: #end_pymotw_header

In this example, :func:`filter` returns the list of names of the
example source files associated with this section.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fnmatch_filter.py'))
.. }}}

.. code-block:: none

	$ python3 fnmatch_filter.py
	
	Pattern : fnmatch_*.py
	
	Files   :
	['fnmatch_filter.py',
	 'fnmatch_fnmatch.py',
	 'fnmatch_fnmatchcase.py',
	 'fnmatch_translate.py',
	 'index.rst']
	
	Matches :
	['fnmatch_filter.py',
	 'fnmatch_fnmatch.py',
	 'fnmatch_fnmatchcase.py',
	 'fnmatch_translate.py']

.. {{{end}}}

Translating Patterns
====================

Internally, ``fnmatch`` converts the glob pattern to a regular
expression and uses the :mod:`re` module to compare the name and
pattern. The :func:`translate` function is the public API for
converting glob patterns to regular expressions.

.. literalinclude:: fnmatch_translate.py
   :caption:
   :start-after: #end_pymotw_header

Some of the characters are escaped to make a valid expression.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fnmatch_translate.py'))
.. }}}

.. code-block:: none

	$ python3 fnmatch_translate.py
	
	Pattern : fnmatch_*.py
	Regex   : fnmatch_.*\.py\Z(?ms)

.. {{{end}}}

.. seealso::

   * :pydoc:`fnmatch`

   * :mod:`glob` -- The glob module combines ``fnmatch`` matching
     with ``os.listdir()`` to produce lists of files and directories
     matching patterns.

   * :mod:`re` -- Regular expression pattern matching.
