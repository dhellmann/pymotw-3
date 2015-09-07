=======================================
compileall -- Byte-compile Source Files
=======================================

.. module:: compileall
    :synopsis: Byte-compile Source Files

:Purpose: Convert source files to byte-compiled version.
:Python Version: 1.4 and later

The :mod:`compileall` module finds Python source files and compiles
them to the byte-code representation, saving the results in ``.pyc``
or ``.pyo`` files.

Compiling One Directory
=======================

:func:`compile_dir` is used to recursively scan a directory and
byte-compile the files within it.

.. include:: compileall_compile_dir.py
    :literal:
    :start-after: #end_pymotw_header

By default, all of the subdirectories are scanned to a depth of 10.

.. {{{cog
.. workdir = path(cog.inFile).dirname()
.. cog.msg('Removing .pyc files from %s' % workdir)
.. sh("find %s -name '*.pyc' | xargs rm" % workdir) #* fix emacs syntax highlighting
.. cog.out(run_script(cog.inFile, 'compileall_compile_dir.py'))
.. }}}

::

	$ python compileall_compile_dir.py
	
	Listing examples ...
	Compiling examples/a.py ...
	Listing examples/subdir ...
	Compiling examples/subdir/b.py ...

.. {{{end}}}

To filter directories out, use the ``rx`` argument to provide a
regular expression to match the names to exclude.

.. include:: compileall_exclude_dirs.py
    :literal:
    :start-after: #end_pymotw_header

This version excludes files in the ``subdir`` subdirectory.

.. {{{cog
.. workdir = path(cog.inFile).dirname()
.. cog.msg('Removing .pyc files from %s' % workdir)
.. sh("find %s -name '*.pyc' | xargs rm" % workdir) #* fix emacs syntax highlighting
.. cog.out(run_script(cog.inFile, 'compileall_exclude_dirs.py'))
.. }}}

::

	$ python compileall_exclude_dirs.py
	
	Listing examples ...
	Compiling examples/a.py ...
	Listing examples/subdir ...

.. {{{end}}}

The *maxlevels* argument controls the depth of recursion.  For example,
to avoid recursion entirely pass ``0``.

.. include:: compileall_recursion_depth.py
    :literal:
    :start-after: #end_pymotw_header

Only files within the directory passed to :func:`compile_dir` are
compiled.

.. {{{cog
.. workdir = path(cog.inFile).dirname()
.. cog.msg('Removing .pyc files from %s' % workdir)
.. sh("find %s -name '*.pyc' | xargs rm" % workdir) #* fix emacs syntax highlighting
.. cog.out(run_script(cog.inFile, 'compileall_recursion_depth.py'))
.. }}}

::

	$ python compileall_recursion_depth.py
	
	Listing examples ...
	Compiling examples/a.py ...

.. {{{end}}}


Compiling sys.path
==================

All of the Python source files found in sys.path can be compiled with
a single call to :func:`compile_path`.

.. include:: compileall_path.py
    :literal:
    :start-after: #end_pymotw_header

This example replaces the default contents of :data:`sys.path` to
avoid permission errors while running the script, but still
illustrates the default behavior.  Note that the *maxlevels* value
defaults to ``0``.

.. {{{cog
.. workdir = path(cog.inFile).dirname()
.. cog.msg('Removing .pyc files from %s' % workdir)
.. sh("find %s -name '*.pyc' | xargs rm" % workdir) #* fix emacs syntax highlighting
.. cog.out(run_script(cog.inFile, 'compileall_path.py'))
.. }}}

::

	$ python compileall_path.py
	
	sys.path = ['examples', 'notthere']
	Listing examples ...
	Compiling examples/a.py ...
	Listing notthere ...
	Can't list notthere

.. {{{end}}}


From the Command Line
=====================

It is also possible to invoke :mod:`compileall` from the command line,
so it can be integrated with a build system via a Makefile.  For
example:

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m compileall -h', ignore_error=True, 
..                    break_lines_at=65, line_break_mode='wrap'))
.. }}}

::

	$ python -m compileall -h
	
	option -h not recognized
	usage: python compileall.py [-l] [-f] [-q] [-d destdir] [-x
	regexp] [-i list] [directory|file ...]
	-l: don't recurse down
	-f: force rebuild even if timestamps are up-to-date
	-q: quiet operation
	-d destdir: purported directory name for error messages
	   if no directory arguments, -l sys.path is assumed
	-x regexp: skip files matching the regular expression regexp
	   the regexp is searched for in the full path of the file
	-i list: expand list with its content (file and directory names)

.. {{{end}}}

To recreate the earlier example, skipping the ``subdir`` directory, run:

.. {{{cog
.. workdir = path(cog.inFile).dirname()
.. cog.msg('Removing .pyc files from %s' % workdir)
.. sh("find %s -name '*.pyc' | xargs rm" % workdir) #* fix emacs syntax highlighting
.. cog.out(run_script(cog.inFile, "-m compileall -x '/subdir' examples"))
.. }}}

::

	$ python -m compileall -x '/subdir' examples
	
	Listing examples ...
	Compiling examples/a.py ...
	Listing examples/subdir ...

.. {{{end}}}


.. seealso::

    `compileall <http://docs.python.org/library/compileall.html>`_
        The standard library documentation for this module.
