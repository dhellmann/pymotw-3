=================================
glob -- Filename pattern matching
=================================

.. module:: glob
    :synopsis: Use Unix shell rules to fine filenames matching a pattern.

:Purpose: Use Unix shell rules to fine filenames matching a pattern.
:Available In: 1.4

Even though the glob API is very simple, the module packs a lot of
power. It is useful in any situation where your program needs to look
for a list of files on the filesystem with names matching a
pattern. If you need a list of filenames that all have a certain
extension, prefix, or any common string in the middle, use :mod:`glob`
instead of writing code to scan the directory contents yourself.

The pattern rules for glob are not regular expressions. Instead, they
follow standard Unix path expansion rules. There are only a few
special characters: two different wild-cards, and character ranges are
supported. The patterns rules are applied to segments of the filename
(stopping at the path separator, ``/``). Paths in the pattern can be
relative or absolute. Shell variable names and tilde (``~``) are not
expanded.

Example Data
============

The examples below assume the following test files are present in the
current working directory:

.. {{{cog
.. from paver.path import path
.. outdir = path(cog.inFile).dirname() / 'dir'
.. outdir.rmtree()
.. cog.out(run_script(cog.inFile, 'glob_maketestdata.py'))
.. }}}

::

	$ python glob_maketestdata.py
	
	dir
	dir/file.txt
	dir/file1.txt
	dir/file2.txt
	dir/filea.txt
	dir/fileb.txt
	dir/subdir
	dir/subdir/subfile.txt

.. {{{end}}}

.. note::

   Use ``glob_maketestdata.py`` in the sample code to create these
   files if you want to run the examples.

Wildcards
=========

An asterisk (``*``) matches zero or more characters in a segment of a
name. For example, ``dir/*``.

.. include:: glob_asterisk.py
    :literal:
    :start-after: #end_pymotw_header

The pattern matches every pathname (file or directory) in the directory dir,
without recursing further into subdirectories.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'glob_asterisk.py'))
.. }}}

::

	$ python glob_asterisk.py
	
	dir/file.txt
	dir/file1.txt
	dir/file2.txt
	dir/filea.txt
	dir/fileb.txt
	dir/subdir

.. {{{end}}}

To list files in a subdirectory, you must include the subdirectory in the
pattern:

.. include:: glob_subdir.py
    :literal:
    :start-after: #end_pymotw_header

The first case above lists the subdirectory name explicitly, while the second
case depends on a wildcard to find the directory.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'glob_subdir.py'))
.. }}}

::

	$ python glob_subdir.py
	
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

The other wildcard character supported is the question mark
(``?``). It matches any single character in that position in the
name. For example,

.. include:: glob_question.py
    :literal:
    :start-after: #end_pymotw_header

Matches all of the filenames which begin with "file", have one more character
of any type, then end with ".txt".

.. {{{cog
.. cog.out(run_script(cog.inFile, 'glob_question.py'))
.. }}}

::

	$ python glob_question.py
	
	dir/file1.txt
	dir/file2.txt
	dir/filea.txt
	dir/fileb.txt

.. {{{end}}}


Character Ranges
================

When you need to match a specific character, use a character range instead of
a question mark. For example, to find all of the files which have a digit in
the name before the extension:

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

	$ python glob_charrange.py
	
	dir/file1.txt
	dir/file2.txt

.. {{{end}}}


.. seealso::

    `glob <http://docs.python.org/2.7/library/glob.html>`_
        The standard library documentation for this module.

    `Pattern Matching Notation <http://www.opengroup.org/onlinepubs/000095399/utilities/xcu_chap02.html#tag_02_13>`_
        An explanation of globbing from The Open Group's Shell Command Language specification.

    :mod:`fnmatch`
        Filename matching implementation.

    :ref:`article-file-access`
        Other tools for working with files.
