==================================================
tempfile -- Create temporary filesystem resources.
==================================================

.. module:: tempfile
    :synopsis: Create temporary filesystem resources.

:Purpose: Create temporary filesystem resources.
:Available In: Since 1.4 with major security revisions in 2.3

Many programs need to create files to write intermediate
data. Creating files with unique names securely, so they cannot be
guessed by someone wanting to break the application, is
challenging. The :mod:`tempfile` module provides several functions for
creating filesystem resources securely. :func:`TemporaryFile()` opens
and returns an un-named file, :func:`NamedTemporaryFile()` opens and
returns a named file, and :func:`mkdtemp()` creates a temporary
directory and returns its name.

TemporaryFile
=============

If your application needs a temporary file to store data, but does not
need to share that file with other programs, the best option for
creating the file is the :func:`TemporaryFile()` function. It creates
a file, and on platforms where it is possible, unlinks it
immediately. This makes it impossible for another program to find or
open the file, since there is no reference to it in the filesystem
table. The file created by :func:`TemporaryFile()` is removed
automatically when it is closed.

.. include:: tempfile_TemporaryFile.py
    :literal:
    :start-after: #end_pymotw_header

This example illustrates the difference in creating a temporary file
using a common pattern for making up a name, versus using the
:func:`TemporaryFile()` function. Notice that the file returned by
:func:`TemporaryFile` has no name.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tempfile_TemporaryFile.py'))
.. }}}

::

	$ python tempfile_TemporaryFile.py
	
	Building a file name yourself:
	temp: <open file '/tmp/guess_my_name.14891.txt', mode 'w+b' at 0x100458270>
	temp.name: /tmp/guess_my_name.14891.txt
	
	TemporaryFile:
	temp: <open file '<fdopen>', mode 'w+b' at 0x100458780>
	temp.name: <fdopen>

.. {{{end}}}

By default, the file handle is created with mode ``'w+b'`` so it
behaves consistently on all platforms and your program can write to it
and read from it.

.. include:: tempfile_TemporaryFile_binary.py
    :literal:
    :start-after: #end_pymotw_header

After writing, you have to rewind the file handle using :func:`seek()`
in order to read the data back from it.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tempfile_TemporaryFile_binary.py'))
.. }}}

::

	$ python tempfile_TemporaryFile_binary.py
	
	Some data

.. {{{end}}}

If you want the file to work in text mode, set *mode* to ``'w+t'``
when you create it:

.. include:: tempfile_TemporaryFile_text.py
    :literal:
    :start-after: #end_pymotw_header

The file handle treats the data as text:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tempfile_TemporaryFile_text.py'))
.. }}}

::

	$ python tempfile_TemporaryFile_text.py
	
	first
	second

.. {{{end}}}

NamedTemporaryFile
==================

There are situations, however, where having a named temporary file is
important. If your application spans multiple processes, or even
hosts, naming the file is the simplest way to pass it between parts of
the application. The :func:`NamedTemporaryFile()` function creates a
file with a name, accessed from the name attribute.

.. include:: tempfile_NamedTemporaryFile.py
    :literal:
    :start-after: #end_pymotw_header

Even though the file is named, it is still removed after the handle is
closed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tempfile_NamedTemporaryFile.py'))
.. }}}

::

	$ python tempfile_NamedTemporaryFile.py
	
	temp: <open file '<fdopen>', mode 'w+b' at 0x100458270>
	temp.name: /var/folders/5q/8gk0wq888xlggz008k8dr7180000hg/T/tmpIIkknb
	Exists after close: False

.. {{{end}}}

mkdtemp
=======

If you need several temporary files, it may be more convenient to
create a single temporary directory and then open all of the files in
that directory.  To create a temporary directory, use
:func:`mkdtemp()`.

.. include:: tempfile_mkdtemp.py
    :literal:
    :start-after: #end_pymotw_header

Since the directory is not "opened" per se, you have to remove it
yourself when you are done with it.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tempfile_mkdtemp.py'))
.. }}}

::

	$ python tempfile_mkdtemp.py
	
	/var/folders/5q/8gk0wq888xlggz008k8dr7180000hg/T/tmpE4plSY

.. {{{end}}}

Predicting Names
================

For debugging purposes, it is useful to be able to include some
indication of the origin of the temporary files. While obviously less
secure than strictly anonymous temporary files, including a
predictable portion in the name lets you find the file to examine it
while your program is using it. All of the functions described so far
take three arguments to allow you to control the filenames to some
degree. Names are generated using the formula::

    dir + prefix + random + suffix

where all of the values except random can be passed as arguments to
:func:`TemporaryFile()`, :func:`NamedTemporaryFile()`, and
:func:`mkdtemp()`. For example:

.. include:: tempfile_NamedTemporaryFile_args.py
    :literal:
    :start-after: #end_pymotw_header

The *prefix* and *suffix* arguments are combined with a random string
of characters to build the file name, and the *dir* argument is taken
as-is and used as the location of the new file.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tempfile_NamedTemporaryFile_args.py'))
.. }}}

::

	$ python tempfile_NamedTemporaryFile_args.py
	
	temp: <open file '<fdopen>', mode 'w+b' at 0x100458270>
	temp.name: /tmp/prefix_SMkGcX_suffix

.. {{{end}}}

Temporary File Location
=======================

If you don't specify an explicit destination using the *dir* argument,
the actual path used for the temporary files will vary based on your
platform and settings. The tempfile module includes two functions for
querying the settings being used at runtime:

.. include:: tempfile_settings.py
    :literal:
    :start-after: #end_pymotw_header

:func:`gettempdir()` returns the default directory that will hold all
of the temporary files and :func:`gettempprefix()` returns the string
prefix for new file and directory names.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tempfile_settings.py'))
.. }}}

::

	$ python tempfile_settings.py
	
	gettempdir(): /var/folders/5q/8gk0wq888xlggz008k8dr7180000hg/T
	gettempprefix(): tmp

.. {{{end}}}

The value returned by :func:`gettempdir()` is set based on a
straightforward algorithm of looking through a list of locations for
the first place the current process can create a file. From the
library documentation:

Python searches a standard list of directories and sets tempdir to the
first one which the calling user can create files in. The list is:

1. The directory named by the ``TMPDIR`` environment variable.

2. The directory named by the ``TEMP`` environment variable.

3. The directory named by the ``TMP`` environment variable.

4. A platform-specific location:

   * On RiscOS, the directory named by the ``Wimp$ScrapDir`` environment
     variable.

   * On Windows, the directories ``C:\TEMP``, ``C:\TMP``, ``\TEMP``,
     and ``\TMP``, in that order.

   * On all other platforms, the directories ``/tmp``, ``/var/tmp``,
     and ``/usr/tmp``, in that order.

5. As a last resort, the current working directory.

If your program needs to use a global location for all temporary files
that you need to set explicitly but do not want to set through one of
these environment variables, you can set ``tempfile.tempdir``
directly.

.. include:: tempfile_tempdir.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tempfile_tempdir.py'))
.. }}}

::

	$ python tempfile_tempdir.py
	
	gettempdir(): /I/changed/this/path

.. {{{end}}}

.. seealso::

    `tempfile <https://docs.python.org/2/library/tempfile.html>`_
        Standard library documentation for this module.

    :ref:`article-file-access`
        More modules for working with files.
