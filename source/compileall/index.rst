==========================================
 compileall --- Byte-compile Source Files
==========================================

.. module:: compileall
    :synopsis: Byte-compile Source Files

:Purpose: Convert source files to byte-compiled version.

The ``compileall`` module finds Python source files and compiles
them to the byte-code representation, saving the results in ``.pyc``.

Compiling One Directory
=======================

``compile_dir()`` is used to recursively scan a directory and
byte-compile the files within it.

.. literalinclude:: compileall_compile_dir.py
    :caption:
    :start-after: #end_pymotw_header

By default, all of the subdirectories are scanned to a depth of 10.
The output files are written to a ``__pycache__`` directory and named
based on the Python interpreter version.

.. {{{cog
.. workdir = path(cog.inFile).dirname()
.. cog.msg('Removing .pyc files from %s' % workdir)
.. sh("find %s -name '*.pyc' | xargs rm" % workdir) #* fix emacs syntax highlighting
.. cog.out(run_script(cog.inFile, 'compileall_compile_dir.py'))
.. }}}

.. code-block:: none

	$ python3 compileall_compile_dir.py
	
	Before: []
	
	Listing 'examples'...
	Compiling 'examples/a.py'...
	Listing 'examples/subdir'...
	Compiling 'examples/subdir/b.py'...
	
	After: ['examples/__pycache__/a.cpython-35.pyc']

.. {{{end}}}

Ignoring Files
==============

To filter directories out, use the ``rx`` argument to provide a
regular expression to match the names to exclude.

.. literalinclude:: compileall_exclude_dirs.py
    :caption:
    :start-after: #end_pymotw_header

This version excludes files in the ``subdir`` subdirectory.

.. {{{cog
.. workdir = path(cog.inFile).dirname()
.. cog.msg('Removing .pyc files from %s' % workdir)
.. sh("find %s -name '*.pyc' | xargs rm" % workdir) #* fix emacs syntax highlighting
.. cog.out(run_script(cog.inFile, 'compileall_exclude_dirs.py'))
.. }}}

.. code-block:: none

	$ python3 compileall_exclude_dirs.py
	
	Listing 'examples'...
	Compiling 'examples/a.py'...
	Listing 'examples/subdir'...

.. {{{end}}}

The ``maxlevels`` argument controls the depth of recursion.  For example,
to avoid recursion entirely pass ``0``.

.. literalinclude:: compileall_recursion_depth.py
    :caption:
    :start-after: #end_pymotw_header

Only files within the directory passed to ``compile_dir()`` are
compiled.

.. {{{cog
.. workdir = path(cog.inFile).dirname()
.. cog.msg('Removing .pyc files from %s' % workdir)
.. sh("find %s -name '*.pyc' | xargs rm" % workdir) #* fix emacs syntax highlighting
.. cog.out(run_script(cog.inFile, 'compileall_recursion_depth.py'))
.. }}}

.. code-block:: none

	$ python3 compileall_recursion_depth.py
	
	Listing 'examples'...
	Compiling 'examples/a.py'...

.. {{{end}}}

Compiling sys.path
==================

All of the Python source files found in sys.path can be compiled with
a single call to ``compile_path()``.

.. literalinclude:: compileall_path.py
    :caption:
    :start-after: #end_pymotw_header

This example replaces the default contents of ``sys.path`` to
avoid permission errors while running the script, but still
illustrates the default behavior.  Note that the ``maxlevels`` value
defaults to ``0``.

.. {{{cog
.. workdir = path(cog.inFile).dirname()
.. cog.msg('Removing .pyc files from %s' % workdir)
.. sh("find %s -name '*.pyc' | xargs rm" % workdir) #* fix emacs syntax highlighting
.. cog.out(run_script(cog.inFile, 'compileall_path.py'))
.. }}}

.. code-block:: none

	$ python3 compileall_path.py
	
	sys.path = ['examples', 'notthere']
	Listing 'examples'...
	Compiling 'examples/a.py'...
	Listing 'notthere'...
	Can't list 'notthere'

.. {{{end}}}

Compiling Individual Files
==========================

To compile a single file, rather than an entire directory of files,
use ``compile_file()``.

.. literalinclude:: compileall_compile_file.py
   :caption:
   :start-after: #end_pymotw_header

The first argument should be the name to the file, either a full path
or a relative path.

.. {{{cog
.. workdir = path(cog.inFile).dirname()
.. cog.msg('Removing .pyc files from %s' % workdir)
.. sh("find %s -name '*.pyc' | xargs rm" % workdir) #* fix emacs syntax highlighting
.. cog.out(run_script(cog.inFile, 'compileall_compile_file.py'))
.. }}}

.. code-block:: none

	$ python3 compileall_compile_file.py
	
	Before: []
	
	Compiling 'examples/a.py'...
	
	After: ['examples/__pycache__/a.cpython-35.pyc']

.. {{{end}}}


From the Command Line
=====================

It is also possible to invoke ``compileall`` from the command line,
so it can be integrated with a build system via a Makefile.  For
example:

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m compileall -h', ignore_error=True, 
..                    line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 -m compileall -h
	
	usage: compileall.py [-h] [-l] [-r RECURSION] [-f] [-q] [-b] [-d
	DESTDIR]
	                     [-x REGEXP] [-i FILE] [-j WORKERS]
	                     [FILE|DIR [FILE|DIR ...]]
	
	Utilities to support installing Python libraries.
	
	positional arguments:
	  FILE|DIR              zero or more file and directory names to
	compile; if
	                        no arguments given, defaults to the
	equivalent of -l
	                        sys.path
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -l                    don't recurse into subdirectories
	  -r RECURSION          control the maximum recursion level. if
	`-l` and `-r`
	                        options are specified, then `-r` takes
	precedence.
	  -f                    force rebuild even if timestamps are up
	to date
	  -q                    output only error messages; -qq will
	suppress the
	                        error messages as well.
	  -b                    use legacy (pre-PEP3147) compiled file
	locations
	  -d DESTDIR            directory to prepend to file paths for
	use in compile-
	                        time tracebacks and in runtime
	tracebacks in cases
	                        where the source file is unavailable
	  -x REGEXP             skip files matching the regular
	expression; the regexp
	                        is searched for in the full path of each
	file
	                        considered for compilation
	  -i FILE               add all the files and directories listed
	in FILE to
	                        the list considered for compilation; if
	"-", names are
	                        read from stdin
	  -j WORKERS, --workers WORKERS
	                        Run compileall concurrently

.. {{{end}}}

To recreate the earlier example, skipping the ``subdir`` directory, run:

.. {{{cog
.. workdir = path(cog.inFile).dirname()
.. cog.msg('Removing .pyc files from %s' % workdir)
.. sh("find %s -name '*.pyc' | xargs rm" % workdir) #* fix emacs syntax highlighting
.. cog.out(run_script(cog.inFile, "-m compileall -x '/subdir' examples"))
.. }}}

.. code-block:: none

	$ python3 -m compileall -x '/subdir' examples
	
	Listing 'examples'...
	Compiling 'examples/a.py'...
	Listing 'examples/subdir'...

.. {{{end}}}


.. seealso::

    * :pydoc:`compileall`
