=========================================
 pathlib --- Filesystem Paths as Objects
=========================================

.. module:: pathlib
    :synopsis: Treat filesystem paths as objects.

:Purpose: Parse, build, test, and otherwise work on filenames and
          paths using an object-oriented API instead of low-level
          string operations.

Path Representations
====================

:mod:`pathlib` includes classes for managing filesystem paths
formatted using either the POSIX standard or Microsoft Windows
syntax. It includes so called "pure" classes, which operate on strings
but do not interact with an actual filesystem, and "concrete" classes,
which extend the API to include operations that reflect or modify data
on the local filesystem.

The pure classes :class:`PurePosixPath` and :class:`PureWindowsPath`
can be instantiated and used on any operating system, since they only
work on names. To instantiate the correct class for working with a
real filesystem, use :class:`Path` to get either a :class:`PosixPath`
or :class:`WindowsPath`, depending on the platform.

Building Paths
==============

To instantiate a new path, give a string as the first argument. The
string representation of the path object is this name value. To create
a new path referring to a value relative to an existing path, use the
``/`` operator to extend the path. The argument to the operator can
either be a string or another path object.

.. literalinclude:: pathlib_operator.py
   :caption:
   :start-after: #end_pymotw_header

As the value for ``root`` in the example output shows, the operator
combines the path values as they are given, and does not normalize the
result when it contains the parent directory reference
``".."``. However, if a segment begins with the path separator it is
interpreted as a new "root" reference in the same way as
:func:`os.path.join`.  Extra path separators are removed from the
middle of the path value, as in the ``etc`` example here.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pathlib_operator.py'))
.. }}}

.. code-block:: none

	$ python3 pathlib_operator.py
	
	/usr
	/usr/local
	/usr/share
	/usr/..
	/etc

.. {{{end}}}

The concrete path classes include a :func:`resolve` method for
normalizing a path by looking at the filesystem for directories and
symbolic links and producing the absolute path referred to by a name.

.. literalinclude:: pathlib_resolve.py
   :caption:
   :start-after: #end_pymotw_header

Here the relative path is converted to the absolute path to
``/usr/share``. If the input path includes symlinks, those are
expanded as well to allow the resolved path to refer directly to the
target.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pathlib_resolve.py'))
.. }}}

.. code-block:: none

	$ python3 pathlib_resolve.py
	
	/usr/share

.. {{{end}}}

To build paths when the segments are not known in advance, use
:func:`joinpath`, passing each path segment as a separate argument.

.. literalinclude:: pathlib_joinpath.py
   :caption:
   :start-after: #end_pymotw_header

As with the ``/`` operator, calling :func:`joinpath` creates a new
instance.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pathlib_joinpath.py'))
.. }}}

.. code-block:: none

	$ python3 pathlib_joinpath.py
	
	/usr/local

.. {{{end}}}

Given an existing path object, it is easy to build a new one with
minor differences such as referring to a different file in the same
directory. Use :func:`with_name` to create a new path that replaces
the name portion of a path with a different file name. Use
:func:`with_suffix` to create a new path that replaces the file name's
extension with a different value.

.. literalinclude:: pathlib_from_existing.py
   :caption:
   :start-after: #end_pymotw_header

Both methods return new objects, and the original is left unchanged.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pathlib_from_existing.py'))
.. }}}

.. code-block:: none

	$ python3 pathlib_from_existing.py
	
	source/pathlib/index.rst
	source/pathlib/pathlib_from_existing.py
	source/pathlib/pathlib_from_existing.pyc

.. {{{end}}}

Parsing Paths
=============

Path objects have methods and properties for extracting partial values
from the name. For example, the ``parts`` property produces a sequence
of path segments parsed based on the path separator value.

.. literalinclude:: pathlib_parts.py
   :caption:
   :start-after: #end_pymotw_header

The sequence is a tuple, reflecting the immutability of the path
instance.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pathlib_parts.py'))
.. }}}

.. code-block:: none

	$ python3 pathlib_parts.py
	
	('/', 'usr', 'local')

.. {{{end}}}

There are two ways to navigate "up" the filesystem hierarchy from a
given path object. The ``parent`` property refers to a new path
instance for the directory containing the path, the value returned by
:func:`os.path.dirname`.  The ``parents`` property is an iterable that
produces parent directory references, continually going "up" the path
hierarchy until reaching the root.

.. literalinclude:: pathlib_parents.py
   :caption:
   :start-after: #end_pymotw_header

The example converts the ``parents`` iterator to a :class:`list`
before printing it so the member values can be printed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pathlib_parents.py'))
.. }}}

.. code-block:: none

	$ python3 pathlib_parents.py
	
	parent: /usr/local
	
	hierarchy:
	/usr/local
	/usr
	/

.. {{{end}}}

Other parts of the path can be accessed through properties of the path
object.  The ``name`` property holds the last part of the path, after
the final path separator (the same value that :func:`os.path.basename`
produces). The ``suffix`` property holds the value after the extension
separator (usually ".") and the ``stem`` property holds the portion of
the name before the suffix (these match the values produced by
:func:`os.path.splitext`).

.. literalinclude:: pathlib_name.py
   :caption:
   :start-after: #end_pymotw_header

Unlike with :func:`os.path.splitext`, the ``suffix`` and ``stem``
values are based on the value of ``name`` and not the full path.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pathlib_name.py'))
.. }}}

.. code-block:: none

	$ python3 pathlib_name.py
	
	path  : source/pathlib/pathlib_name.py
	name  : pathlib_name.py
	suffix: .py
	stem  : pathlib_name

.. {{{end}}}

Creating Concrete Paths
=======================

Instances of the concrete :class:`Path` class can be created from
string arguments referring to the name (or potential name) of a file,
directory, or symbolic link on the file system. The class also
provides several convenience methods for building instances using
commonly used locations that change, such as the current working
directory and the user's home directory.

.. literalinclude:: pathlib_convenience.py
   :caption:
   :start-after: #end_pymotw_header

Both methods create :class:`Path` instances pre-populated with an
absolute file system reference.

.. {{{cog
.. # replace long cwd value from build with a shorter faux value
.. def _faux_cwd(infile, line):
..     bad = '/Users/dhellmann/Dropbox/PyMOTW/Python3/pymotw-3/source/pathlib'
..     return line.replace(bad, '/Users/dhellmann/PyMOTW')
.. cog.out(run_script(cog.inFile, 'pathlib_convenience.py', line_cleanups=[_faux_cwd]))
.. }}}

.. code-block:: none

	$ python3 pathlib_convenience.py
	
	home:  /Users/dhellmann
	cwd :  /Users/dhellmann/PyMOTW

.. {{{end}}}

Directory Contents
==================

There are three methods for accessing the directory listings to
discover the names of files available on the file
system. :func:`iterdir` is a generator, yielding a new :class:`Path`
instance for each item in the containing directory.

.. literalinclude:: pathlib_iterdir.py
   :caption:
   :start-after: #end_pymotw_header

If the :class:`Path` does not refer to a directory, :func:`iterdir`
raises :class:`NotADirectoryError`.

.. {{{cog
.. run_script(cog.inFile, 'rm -f *~', interpreter='')
.. run_script(cog.inFile, 'rm -rf test_files', interpreter='')
.. cog.out(run_script(cog.inFile, 'pathlib_iterdir.py'))
.. }}}

.. code-block:: none

	$ python3 pathlib_iterdir.py
	
	index.rst
	pathlib_convenience.py
	pathlib_from_existing.py
	pathlib_glob.py
	pathlib_iterdir.py
	pathlib_joinpath.py
	pathlib_name.py
	pathlib_operator.py
	pathlib_parents.py
	pathlib_parts.py
	pathlib_resolve.py
	pathlib_rglob.py
	pathlib_types.py

.. {{{end}}}

Use :func:`glob` to find only files matching a pattern.

.. literalinclude:: pathlib_glob.py
   :caption:
   :start-after: #end_pymotw_header

This example shows all of the reStructuredText_ input files in the
parent directory of the script.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pathlib_glob.py'))
.. }}}

.. code-block:: none

	$ python3 pathlib_glob.py
	
	../about.rst
	../algorithm_tools.rst
	../compression.rst
	../concurrency.rst
	../cryptographic.rst
	../data_types.rst
	../dates.rst
	../dev_tools.rst
	../email.rst
	../file_access.rst
	../frameworks.rst
	../i18n.rst
	../importing.rst
	../index.rst
	../internet_protocols.rst
	../language.rst
	../networking.rst
	../numeric.rst
	../persistence.rst
	../porting_notes.rst
	../runtime_services.rst
	../text.rst
	../unix.rst

.. {{{end}}}

The glob processor support recursive scanning using the pattern prefix
``**`` or by calling :func:`rglob` instead of :func:`glob`.

.. literalinclude:: pathlib_rglob.py
   :caption:
   :start-after: #end_pymotw_header

Because this example starts from the parent directory, a recursive
search is necessary to find the example files matching
``pathlib_*.py``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pathlib_rglob.py'))
.. }}}

.. code-block:: none

	$ python3 pathlib_rglob.py
	
	../pathlib/pathlib_convenience.py
	../pathlib/pathlib_from_existing.py
	../pathlib/pathlib_glob.py
	../pathlib/pathlib_iterdir.py
	../pathlib/pathlib_joinpath.py
	../pathlib/pathlib_name.py
	../pathlib/pathlib_operator.py
	../pathlib/pathlib_parents.py
	../pathlib/pathlib_parts.py
	../pathlib/pathlib_resolve.py
	../pathlib/pathlib_rglob.py
	../pathlib/pathlib_types.py

.. {{{end}}}

File Types
==========

A :class:`Path` instance includes several methods for testing the type
of file refered to by the path. This example creates several files of
different types and tests those as well as a few other device-specific
files available on the local operating system.

.. literalinclude:: pathlib_types.py
   :caption:
   :start-after: #end_pymotw_header

Each of the methods, :func:`is_dir`, :func:`is_file`,
:func:`is_symlink`, :func:`is_socket`, :func:`is_fifo`,
:func:`is_block_device`, and :func:`is_char_device`, takes no
arguments.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pathlib_types.py'))
.. }}}

.. code-block:: none

	$ python3 pathlib_types.py
	
	test_files/fifo
	Is File?             : False
	Is Dir?              : False
	Is Link?             : False
	Is FIFO?             : True
	Is lock device?      : False
	Is character device? : False
	
	test_files/file
	Is File?             : True
	Is Dir?              : False
	Is Link?             : False
	Is FIFO?             : False
	Is lock device?      : False
	Is character device? : False
	
	test_files/symlink
	Is File?             : True
	Is Dir?              : False
	Is Link?             : True
	Is FIFO?             : False
	Is lock device?      : False
	Is character device? : False
	
	/dev/disk0
	Is File?             : False
	Is Dir?              : False
	Is Link?             : False
	Is FIFO?             : False
	Is lock device?      : True
	Is character device? : False
	
	/dev/console
	Is File?             : False
	Is Dir?              : False
	Is Link?             : False
	Is FIFO?             : False
	Is lock device?      : False
	Is character device? : True
	

.. {{{end}}}

Properties?
===========

.. todo:: stat
.. todo:: exists

Permissions
===========

.. todo:: chmod, group, owner

Reading and Writing Files
=========================

.. open
.. read_bytes, write_bytes
.. read_text, write_text

Creating and Deleting Files and Directories
===========================================

.. mkdir, rmdir
.. rename, replace

.. symlink_to
.. touch
.. unlink




.. examples of windows paths

.. sorting, hashing

.. match

.. relative_to

.. expanduser


.. seealso::

   * :pydoc:`pathlib`

   * :mod:`os.path` -- Platform-independent manipulation of filenames

   * :mod:`glob` -- UNIX shell pattern matching for filenames

   * :pep:`428` -- The pathlib module

.. _reStructuredText: http://docutils.sourceforge.net/
