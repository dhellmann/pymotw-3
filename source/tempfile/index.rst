===========================================
 tempfile -- Temporary File System Objects
===========================================

.. module:: tempfile
    :synopsis: Temporary file system objects

:Purpose: Create temporary file system objects.
:Python Version: 1.4 and later

Creating temporary files with unique names securely, so they cannot be
guessed by someone wanting to break the application or steal the data, is
challenging. The :mod:`tempfile` module provides several functions for
creating temporary file system resources securely. :func:`TemporaryFile()` opens
and returns an unnamed file, :func:`NamedTemporaryFile()` opens and
returns a named file, and :func:`mkdtemp()` creates a temporary
directory and returns its name.

Temporary Files
===============

Applications that need temporary files to store data, without needing
to share that file with other programs, should use the
:func:`TemporaryFile()` function to create the files. The function
creates a file, and on platforms where it is possible, unlinks it
immediately. This makes it impossible for another program to find or
open the file, since there is no reference to it in the file system
table. The file created by :func:`TemporaryFile()` is removed
automatically when it is closed, whether by calling :func:`close` or by
using the context manager API and ``with`` statement.

.. include:: tempfile_TemporaryFile.py
    :literal:
    :start-after: #end_pymotw_header

This example illustrates the difference in creating a temporary file
using a common pattern for making up a name, versus using the
:func:`TemporaryFile()` function. The file returned by
:func:`TemporaryFile` has no name.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tempfile_TemporaryFile.py', break_lines_at=58))
.. }}}

::

	$ python tempfile_TemporaryFile.py

	Building a filename with PID:
	temp:
	   <open file '/tmp/guess_my_name.1074.txt', mode 'w+b' at
	 0x100d881e0>
	temp.name:
	   /tmp/guess_my_name.1074.txt
	
	TemporaryFile:
	temp:
	   <open file '<fdopen>', mode 'w+b' at 0x100d88780>
	temp.name:
	   <fdopen>

.. {{{end}}}

By default, the file handle is created with mode ``'w+b'`` so it
behaves consistently on all platforms and the caller can write to it
and read from it.

.. include:: tempfile_TemporaryFile_binary.py
    :literal:
    :start-after: #end_pymotw_header

After writing, the file handle must be "rewound" using :func:`seek()`
in order to read the data back from it.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tempfile_TemporaryFile_binary.py'))
.. }}}

::

	$ python tempfile_TemporaryFile_binary.py

	Some data

.. {{{end}}}

To open the file in text mode, set *mode* to ``'w+t'`` when the file
is created.

.. include:: tempfile_TemporaryFile_text.py
    :literal:
    :start-after: #end_pymotw_header

The file handle treats the data as text.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tempfile_TemporaryFile_text.py'))
.. }}}

::

	$ python tempfile_TemporaryFile_text.py

	first
	second

.. {{{end}}}

Named Files
===========

There are situations where having a named temporary file is
important. For applications spanning multiple processes, or even
hosts, naming the file is the simplest way to pass it between parts of
the application. The :func:`NamedTemporaryFile()` function creates a
file without unlinking it, so it retains its name (accessed with
the :attr:`name` attribute).

.. include:: tempfile_NamedTemporaryFile.py
    :literal:
    :start-after: #end_pymotw_header

The file is removed after the handle is closed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tempfile_NamedTemporaryFile.py'))
.. }}}

::

	$ python tempfile_NamedTemporaryFile.py

	temp:
	   <open file '<fdopen>', mode 'w+b' at 0x100d881e0>
	temp.name:
	   /var/folders/9R/9R1t+tR02Raxzk+F71Q50U+++Uw/-Tmp-/tmp926BkT
	Exists after close: False

.. {{{end}}}

Temporary Directories
=====================

When several temporary files are needed, it may be more convenient to
create a single temporary directory with :func:`mkdtemp` and open all
of the files in that directory.

.. include:: tempfile_mkdtemp.py
    :literal:
    :start-after: #end_pymotw_header

Since the directory is not "opened" per se, it must be removed
explicitly when it is no longer needed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tempfile_mkdtemp.py'))
.. }}}

::

	$ python tempfile_mkdtemp.py

	/var/folders/9R/9R1t+tR02Raxzk+F71Q50U+++Uw/-Tmp-/tmpA7DKtP

.. {{{end}}}

Predicting Names
================

While less secure than strictly anonymous temporary files, including a
predictable portion in the name makes it possible to find the file and
examine it for debugging purposes. All of the functions described so
far take three arguments to control the filenames to some
degree. Names are generated using the formula::

    dir + prefix + random + suffix

All of the values except *random* can be passed as arguments to
:func:`TemporaryFile()`, :func:`NamedTemporaryFile()`, and
:func:`mkdtemp()`. For example:

.. include:: tempfile_NamedTemporaryFile_args.py
    :literal:
    :start-after: #end_pymotw_header

The *prefix* and *suffix* arguments are combined with a random string
of characters to build the filename, and the *dir* argument is taken
as-is and used as the location of the new file.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tempfile_NamedTemporaryFile_args.py'))
.. }}}

::

	$ python tempfile_NamedTemporaryFile_args.py

	temp:
	   <open file '<fdopen>', mode 'w+b' at 0x100d881e0>
	temp.name:
	   /tmp/prefix_kjvHYS_suffix

.. {{{end}}}

Temporary File Location
=======================

If an explicit destination is not given using the *dir* argument, the
path used for the temporary files will vary based on the
current platform and settings. The :mod:`tempfile` module includes two
functions for querying the settings being used at runtime.

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

	gettempdir(): /var/folders/9R/9R1t+tR02Raxzk+F71Q50U+++Uw/-Tmp-
	gettempprefix(): tmp

.. {{{end}}}

The value returned by :func:`gettempdir()` is set based on a
straightforward algorithm of looking through a list of locations for
the first place the current process can create a file.  The search
list is:

1. The environment variable ``TMPDIR``
2. The environment variable ``TEMP``
3. The environment variable ``TMP``
4. A fallback, based on the platform.  (RiscOS uses ``Wimp$ScrapDir``.
   Windows uses the first available of ``C:\TEMP``, ``C:\TMP``,
   ``\TEMP``, or ``\TMP``.  Other platforms use ``/tmp``,
   ``/var/tmp``, or ``/usr/tmp``.)
5. If no other directory can be found, the current working directory
   is used.

.. include:: tempfile_tempdir.py
    :literal:
    :start-after: #end_pymotw_header

Programs that need to use a global location for all temporary files
without using any of these environment variables should set
:const:`tempfile.tempdir` directly by assigning a value to the
variable.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tempfile_tempdir.py'))
.. }}}

::

	$ python tempfile_tempdir.py

	gettempdir(): /I/changed/this/path

.. {{{end}}}

.. seealso::

    `tempfile <http://docs.python.org/lib/module-tempfile.html>`_
        Standard library documentation for this module.
