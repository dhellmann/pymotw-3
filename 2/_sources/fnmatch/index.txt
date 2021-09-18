==============================================================
fnmatch -- Compare filenames against Unix-style glob patterns.
==============================================================

.. module:: fnmatch
    :synopsis: Compare filenames against Unix-style glob patterns.

:Purpose: Handle Unix-style filename comparison with the fnmatch module.
:Available In: 1.4 and later.

The fnmatch module is used to compare filenames against glob-style patterns
such as used by Unix shells.

Simple Matching
===============

``fnmatch()`` compares a single filename against a pattern and returns
a boolean indicating whether or not they match. The comparison is
case-sensitive when the operating system uses a case-sensitive
filesystem.

.. include:: fnmatch_fnmatch.py
    :literal:
    :start-after: #end_pymotw_header


In this example, the pattern matches all files starting with 'fnmatch_' and
ending in '.py'.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fnmatch_fnmatch.py'))
.. }}}

::

	$ python fnmatch_fnmatch.py
	
	Pattern : fnmatch_*.py
	
	Filename: __init__.py               False
	Filename: fnmatch_filter.py         True
	Filename: fnmatch_fnmatch.py        True
	Filename: fnmatch_fnmatchcase.py    True
	Filename: fnmatch_translate.py      True
	Filename: index.rst                 False

.. {{{end}}}

To force a case-sensitive comparison, regardless of the filesystem and
operating system settings, use ``fnmatchcase()``.

.. include:: fnmatch_fnmatchcase.py
    :literal:
    :start-after: #end_pymotw_header

Since my laptop uses a case-sensitive filesystem, no files match the modified
pattern.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fnmatch_fnmatchcase.py'))
.. }}}

::

	$ python fnmatch_fnmatchcase.py
	
	Pattern : FNMATCH_*.PY
	
	Filename: __init__.py               False
	Filename: fnmatch_filter.py         False
	Filename: fnmatch_fnmatch.py        False
	Filename: fnmatch_fnmatchcase.py    False
	Filename: fnmatch_translate.py      False
	Filename: index.rst                 False

.. {{{end}}}

Filtering
=========

To test a sequence of filenames, you can use ``filter()``. It returns
a list of the names that match the pattern argument.

.. include:: fnmatch_filter.py
    :literal:
    :start-after: #end_pymotw_header

In this example, ``filter()`` returns the list of names of the example
source files associated with this post.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fnmatch_filter.py'))
.. }}}

::

	$ python fnmatch_filter.py
	
	Pattern : fnmatch_*.py
	Files   : ['__init__.py', 'fnmatch_filter.py', 'fnmatch_fnmatch.py', 'fnmatch_fnmatchcase.py', 'fnmatch_translate.py', 'index.rst']
	Matches : ['fnmatch_filter.py', 'fnmatch_fnmatch.py', 'fnmatch_fnmatchcase.py', 'fnmatch_translate.py']

.. {{{end}}}

Translating Patterns
====================

Internally, fnmatch converts the glob pattern to a regular expression
and uses the :mod:`re` module to compare the name and pattern. The
``translate()`` function is the public API for converting glob patterns to
regular expressions.

.. include:: fnmatch_translate.py
    :literal:
    :start-after: #end_pymotw_header

Notice that some of the characters are escaped to make a valid expression.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fnmatch_translate.py'))
.. }}}

::

	$ python fnmatch_translate.py
	
	Pattern : fnmatch_*.py
	Regex   : fnmatch\_.*\.py\Z(?ms)

.. {{{end}}}

.. seealso::

    `fnmatch <http://docs.python.org/2.7/library/fnmatch.html>`_
        The standard library documentation for this module.

    :mod:`glob`
        The glob module combines :mod:`fnmatch` matching with
        ``os.listdir()`` to produce lists of files and directories
        matching patterns.

    :ref:`article-file-access`
        More modules for working with files.
