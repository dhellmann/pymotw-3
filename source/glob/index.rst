===================================
 glob -- Filename Pattern Matching
===================================

.. module:: glob
    :synopsis: Use Unix shell rules to find filenames matching a pattern.

:Purpose: Use Unix shell rules to find filenames matching a pattern.

Even though the :mod:`glob` API is small, the module packs a lot of
power. It is useful in any situation where a program needs to look for
a list of files on the file system with names matching a pattern. To
create a list of filenames that all have a certain extension, prefix,
or any common string in the middle, use :mod:`glob` instead of writing
custom code to scan the directory contents.

The pattern rules for :mod:`glob` are not the same as the regular
expressions used by the :mod:`re` module. Instead, they follow
standard Unix path expansion rules. There are only a few special
characters: two different wild-cards, and character ranges are
supported. The patterns rules are applied to segments of the filename
(stopping at the path separator, ``/``). Paths in the pattern can be
relative or absolute. Shell variable names and tilde (``~``) are not
expanded.

Example Data
============

The examples in this section assume the following test files are
present in the current working directory:

.. {{{cog
.. from paver.path import path
.. outdir = path(cog.inFile).dirname() / 'dir'
.. outdir.rmtree()
.. cog.out(run_script(cog.inFile, 'glob_maketestdata.py'))
.. }}}

::

	$ python3 glob_maketestdata.py
	
	dir
	dir/file.txt
	dir/file1.txt
	dir/file2.txt
	dir/filea.txt
	dir/fileb.txt
	dir/file?.txt
	dir/file*.txt
	dir/file[.txt
	dir/subdir
	dir/subdir/subfile.txt

.. {{{end}}}

If these files do not exist, use ``glob_maketestdata.py`` in the
sample code to create them before running the following examples.

Wildcards
=========

An asterisk (``*``) matches zero or more characters in a segment of a
name. For example, ``dir/*``.

.. include:: glob_asterisk.py
    :literal:
    :start-after: #end_pymotw_header

The pattern matches every path name (file or directory) in the
directory dir, without recursing further into subdirectories. The data
returned by :func:`glob` comes in the order it is found, so the
examples here sort it to make studying the results easier.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'glob_asterisk.py'))
.. }}}

::

	$ python3 glob_asterisk.py
	
	dir/file*.txt
	dir/file.txt
	dir/file1.txt
	dir/file2.txt
	dir/file?.txt
	dir/file[.txt
	dir/filea.txt
	dir/fileb.txt
	dir/subdir

.. {{{end}}}

To list files in a subdirectory, the subdirectory must be included in
the pattern:

.. include:: glob_subdir.py
    :literal:
    :start-after: #end_pymotw_header

The first case shown earlier lists the subdirectory name
explicitly, while the second case depends on a wildcard to find the
directory.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'glob_subdir.py'))
.. }}}

::

	$ python3 glob_subdir.py
	
	Named explicitly:
		 dir/subdir/subfile.txt
	Named with wildcard:
		 dir/subdir/subfile.txt

.. {{{end}}}

The results, in this case, are the same. If there was another subdirectory,
the wildcard would match both subdirectories and include the filenames from
both.

Single Character Wildcard
=========================

A question mark (``?``) is another wildcard character. It matches any
single character in that position in the name.

.. include:: glob_question.py
    :literal:
    :start-after: #end_pymotw_header

The previous example matches all of the filenames that begin with
"file", have one more character of any type, then end with "``.txt``".

.. {{{cog
.. cog.out(run_script(cog.inFile, 'glob_question.py'))
.. }}}

::

	$ python3 glob_question.py
	
	dir/file*.txt
	dir/file1.txt
	dir/file2.txt
	dir/file?.txt
	dir/file[.txt
	dir/filea.txt
	dir/fileb.txt

.. {{{end}}}


Character Ranges
================

Use a character range (``[a-z]``) instead of a question mark to match
one of several characters.  This example finds all of the files with a
digit in the name before the extension.

.. include:: glob_charrange.py
    :literal:
    :start-after: #end_pymotw_header

The character range ``[0-9]`` matches any single digit. The range is
ordered based on the character code for each letter/digit, and the
dash indicates an unbroken range of sequential characters. The same
range value could be written ``[0123456789]``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'glob_charrange.py'))
.. }}}

::

	$ python3 glob_charrange.py
	
	dir/file1.txt
	dir/file2.txt

.. {{{end}}}

Escaping Meta-characters
========================

Sometimes it is necessary to search for files with names containing
the special meta-characters :mod:`glob` uses for its patterns. The
:func:`escape` function builds a suitable pattern.

.. include:: glob_escape.py
   :literal:
   :start-after: #end_pymotw_header

Each special character is escaped by building a character range
containing a single entry.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'glob_escape.py'))
.. }}}

::

	$ python3 glob_escape.py
	
	Searching for: "dir/*[?].txt"
	dir/file?.txt
	
	Searching for: "dir/*[*].txt"
	dir/file*.txt
	
	Searching for: "dir/*[[].txt"
	dir/file[.txt
	

.. {{{end}}}



.. seealso::

    * `glob <http://docs.python.org/3/library/glob.html>`_ -- The
      standard library documentation for this module.

    * `Pattern Matching Notation
      <http://www.opengroup.org/onlinepubs/000095399/utilities/xcu_chap02.html#tag_02_13>`_
      -- An explanation of globbing from The Open Group's Shell
      Command Language specification.

    * :mod:`fnmatch` -- Filename matching implementation.
