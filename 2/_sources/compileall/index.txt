=======================================
compileall -- Byte-compile Source Files
=======================================

.. module:: compileall
    :synopsis: Byte-compile Source Files

:Purpose: Convert source files to byte-compiled version.
:Available In: 1.4

The :mod:`compileall` module finds Python source files and compiles
them to the byte-code representation, saving the results in ``.pyc``
or ``.pyo`` files.

Compiling One Directory
=======================

``compile_dir()`` is used to recursively scan a directory and
byte-compile the files within it.

.. include:: compileall_compile_dir.py
    :literal:
    :start-after: #end_pymotw_header

By default, all of the subdirectories are scanned to a depth of 10.
When using a version control system such as subversion, this can lead
to unnecessary scanning, as seen here:

.. {{{cog
.. workdir = path(cog.inFile).dirname()
.. cog.msg('Removing .pyc files from %s' % workdir)
.. sh("cd %s; find . -name '*.pyc' | xargs rm -f" % workdir)
.. cog.out(run_script(cog.inFile, 'compileall_compile_dir.py'))
.. }}}

::

	$ python compileall_compile_dir.py
	
	Listing examples ...
	Listing examples/.svn ...
	Listing examples/.svn/prop-base ...
	Listing examples/.svn/text-base ...
	Compiling examples/a.py ...
	Listing examples/subdir ...
	Listing examples/subdir/.svn ...
	Listing examples/subdir/.svn/prop-base ...
	Listing examples/subdir/.svn/text-base ...
	Compiling examples/subdir/b.py ...

.. {{{end}}}

To filter directories out, use the ``rx`` argument to provide a
regular expression to match the names to exclude.

.. include:: compileall_exclude_dirs.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. workdir = path(cog.inFile).dirname()
.. sh("cd %s; find . -name '*.pyc' | xargs rm -f" % workdir)
.. cog.out(run_script(cog.inFile, 'compileall_exclude_dirs.py'))
.. }}}

::

	$ python compileall_exclude_dirs.py
	
	Listing examples ...
	Listing examples/.svn ...
	Listing examples/.svn/prop-base ...
	Listing examples/.svn/text-base ...
	Compiling examples/a.py ...
	Listing examples/subdir ...
	Listing examples/subdir/.svn ...
	Listing examples/subdir/.svn/prop-base ...
	Listing examples/subdir/.svn/text-base ...
	Compiling examples/subdir/b.py ...

.. {{{end}}}

The maxlevels argument controls the depth of recursion.  For example,
to avoid recursion entirely pass ``0``.

.. include:: compileall_recursion_depth.py
    :literal:
    :start-after: #end_pymotw_header


.. {{{cog
.. workdir = path(cog.inFile).dirname()
.. sh("cd %s; find . -name '*.pyc' | xargs rm -f" % workdir)
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
a single call to ``compile_path()``.

.. include:: compileall_path.py
    :literal:
    :start-after: #end_pymotw_header

This example replaces the default contents of sys.path to avoid
permission errors while running the script, but still illustrates the
default behavior.  Note that the maxlevels value defaults to ``0``.

.. {{{cog
.. workdir = path(cog.inFile).dirname()
.. sh("cd %s; find . -name '*.pyc' | xargs rm -f" % workdir)
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
as you might when integrating it with a build system via a Makefile.
For example:

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m compileall -h', ignore_error=True))
.. }}}

::

	$ python -m compileall -h
	
	option -h not recognized
	usage: python compileall.py [-l] [-f] [-q] [-d destdir] [-x regexp] [-i list] [directory|file ...]
	-l: don't recurse down
	-f: force rebuild even if timestamps are up-to-date
	-q: quiet operation
	-d destdir: purported directory name for error messages
	   if no directory arguments, -l sys.path is assumed
	-x regexp: skip files matching the regular expression regexp
	   the regexp is searched for in the full path of the file
	-i list: expand list with its content (file and directory names)

.. {{{end}}}

To recreate the example above, skipping ``.svn`` directories, one
would run:

.. {{{cog
.. workdir = path(cog.inFile).dirname()
.. sh("cd %s; find . -name '*.pyc' | xargs rm -f" % workdir)
.. cog.out(run_script(cog.inFile, "-m compileall -x '/\.svn' examples"))
.. }}}

::

	$ python -m compileall -x '/\.svn' examples
	
	Listing examples ...
	Listing examples/.svn ...
	Listing examples/.svn/prop-base ...
	Listing examples/.svn/text-base ...
	Compiling examples/a.py ...
	Listing examples/subdir ...
	Listing examples/subdir/.svn ...
	Listing examples/subdir/.svn/prop-base ...
	Listing examples/subdir/.svn/text-base ...
	Compiling examples/subdir/b.py ...

.. {{{end}}}


.. seealso::

    `compileall <http://docs.python.org/2.7/library/compileall.html>`_
        The standard library documentation for this module.
