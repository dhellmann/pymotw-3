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

The example iterates over the ``parents`` property and prints the
member values.

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
the name before the suffix.

.. literalinclude:: pathlib_name.py
   :caption:
   :start-after: #end_pymotw_header

Although the ``suffix`` and ``stem`` values are similar to the values
produced by :func:`os.path.splitext`, the values are based only on the
value of ``name`` and not the full path.

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
..     bad = '/Users/dhellmann/Documents/PyMOTW/Python3/pymotw-3/source/pathlib'
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
.. run_script(cog.inFile, 'rm -f *example.txt', interpreter='')
.. cog.out(run_script(cog.inFile, 'pathlib_iterdir.py'))
.. }}}

.. code-block:: none

	$ python3 pathlib_iterdir.py
	
	example_link
	index.rst
	pathlib_chmod.py
	pathlib_convenience.py
	pathlib_from_existing.py
	pathlib_glob.py
	pathlib_iterdir.py
	pathlib_joinpath.py
	pathlib_mkdir.py
	pathlib_name.py
	pathlib_operator.py
	pathlib_ownership.py
	pathlib_parents.py
	pathlib_parts.py
	pathlib_read_write.py
	pathlib_resolve.py
	pathlib_rglob.py
	pathlib_rmdir.py
	pathlib_stat.py
	pathlib_symlink_to.py
	pathlib_touch.py
	pathlib_types.py
	pathlib_unlink.py

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
	
	../pathlib/pathlib_chmod.py
	../pathlib/pathlib_convenience.py
	../pathlib/pathlib_from_existing.py
	../pathlib/pathlib_glob.py
	../pathlib/pathlib_iterdir.py
	../pathlib/pathlib_joinpath.py
	../pathlib/pathlib_mkdir.py
	../pathlib/pathlib_name.py
	../pathlib/pathlib_operator.py
	../pathlib/pathlib_ownership.py
	../pathlib/pathlib_parents.py
	../pathlib/pathlib_parts.py
	../pathlib/pathlib_read_write.py
	../pathlib/pathlib_resolve.py
	../pathlib/pathlib_rglob.py
	../pathlib/pathlib_rmdir.py
	../pathlib/pathlib_stat.py
	../pathlib/pathlib_symlink_to.py
	../pathlib/pathlib_touch.py
	../pathlib/pathlib_types.py
	../pathlib/pathlib_unlink.py

.. {{{end}}}

Reading and Writing Files
=========================

Each :class:`Path` instance includes methods for working with the
contents of the file to which it refers. For immediately retrieving
the contents, use :func:`read_bytes` or :func:`read_text`. To write to
the file, use :func:`write_bytes` or :func:`write_text`.  Use the
:func:`open` method to open the file and retain the file handle,
instead of passing the name to the built-in :func:`open` function.

.. literalinclude:: pathlib_read_write.py
   :caption:
   :start-after: #end_pymotw_header

The convenience methods do some type checking before opening the file
and writing to it, but otherwise they are equivalent to doing the
operation directly.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pathlib_read_write.py'))
.. }}}

.. code-block:: none

	$ python3 pathlib_read_write.py
	
	read from open(): 'This is the content'
	read_text(): 'This is the content'

.. {{{end}}}

Manipulating Directories and Symbolic Links
===========================================

Paths representing directories or symbolic links that do not exist can
be used to create the associated file system entries.

.. literalinclude:: pathlib_mkdir.py
   :caption:
   :start-after: #end_pymotw_header

If the path already exists, :func:`mkdir` raises a
:class:`FileExistsError`.

.. {{{cog
.. run_script(cog.inFile, 'rm -rf example_dir', interpreter='')
.. cog.out(run_script(cog.inFile, 'pathlib_mkdir.py'))
.. cog.out(run_script(cog.inFile, 'pathlib_mkdir.py', include_prefix=False, ignore_error=True))
.. }}}

.. code-block:: none

	$ python3 pathlib_mkdir.py
	
	Creating example_dir

	$ python3 pathlib_mkdir.py
	
	Creating example_dir
	Traceback (most recent call last):
	  File "pathlib_mkdir.py", line 16, in <module>
	    p.mkdir()
	  File ".../lib/python3.5/pathlib.py", line 1214, in mkdir
	    self._accessor.mkdir(self, mode)
	  File ".../lib/python3.5/pathlib.py", line 371, in wrapped
	    return strfunc(str(pathobj), *args)
	FileExistsError: [Errno 17] File exists: 'example_dir'

.. {{{end}}}

Use :func:`symlink_to` to create a symbolic link. The link will be
named based on the path's value and will refer to the name given as
argument to :func:`symlink_to`.

.. literalinclude:: pathlib_symlink_to.py
   :caption:
   :start-after: #end_pymotw_header

This example creates a symbolic link, then uses :func:`resolve` to
read the link to find what it points to and print the name.

.. {{{cog
.. run_script(cog.inFile, 'rm -f example_link', interpreter='')
.. cog.out(run_script(cog.inFile, 'pathlib_symlink_to.py'))
.. }}}

.. code-block:: none

	$ python3 pathlib_symlink_to.py
	
	example_link
	index.rst

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
	Is block device?     : False
	Is character device? : False
	
	test_files/file
	Is File?             : True
	Is Dir?              : False
	Is Link?             : False
	Is FIFO?             : False
	Is block device?     : False
	Is character device? : False
	
	test_files/symlink
	Is File?             : True
	Is Dir?              : False
	Is Link?             : True
	Is FIFO?             : False
	Is block device?     : False
	Is character device? : False
	
	/dev/disk0
	Is File?             : False
	Is Dir?              : False
	Is Link?             : False
	Is FIFO?             : False
	Is block device?     : True
	Is character device? : False
	
	/dev/console
	Is File?             : False
	Is Dir?              : False
	Is Link?             : False
	Is FIFO?             : False
	Is block device?     : False
	Is character device? : True
	

.. {{{end}}}

File Properties
===============

Detailed information about a file can be accessed using the methods
:func:`stat` or :func:`lstat` (for checking the status of something
that might be a symbolic link). These methods produce the same results
as :func:`os.stat` and :func:`os.lstat`.

.. literalinclude:: pathlib_stat.py
   :caption:
   :start-after: #end_pymotw_header

The output will vary depending on how the example code was
installed. Try passing different filenames on the command line to
``pathlib_stat.py``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pathlib_stat.py'))
.. cog.out(run_script(cog.inFile, 'pathlib_stat.py index.rst', include_prefix=False))
.. }}}

.. code-block:: none

	$ python3 pathlib_stat.py
	
	pathlib_stat.py:
		Size: 607
		Permissions: 0o100644
		Owner: 527
		Device: 16777218
		Created      : Sat Aug 27 19:55:05 2016
		Last modified: Sat Aug 27 19:55:04 2016
		Last accessed: Sat Aug 27 21:45:41 2016

	$ python3 pathlib_stat.py index.rst
	
	index.rst:
		Size: 20080
		Permissions: 0o100644
		Owner: 527
		Device: 16777218
		Created      : Sat Aug 27 21:45:33 2016
		Last modified: Sat Aug 27 21:45:33 2016
		Last accessed: Sat Aug 27 21:45:40 2016

.. {{{end}}}

For simpler access to information about the owner of a file, use
:func:`owner` and :func:`group`.

.. literalinclude:: pathlib_ownership.py
   :caption:
   :start-after: #end_pymotw_header

While :func:`stat` returns numerical system ID values, these methods
look up the name associated with the IDs.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pathlib_ownership.py'))
.. }}}

.. code-block:: none

	$ python3 pathlib_ownership.py
	
	pathlib_ownership.py is owned by dhellmann/dhellmann

.. {{{end}}}

The :func:`touch` method works like the UNIX command ``touch``
to create a file or update an existing file's modification time and
permissions.

.. literalinclude:: pathlib_touch.py
   :caption:
   :start-after: #end_pymotw_header

Running this example more than once updates the existing file on
subsequent runs.

.. {{{cog
.. run_script(cog.inFile, 'rm -f touched', interpreter='')
.. cog.out(run_script(cog.inFile, 'pathlib_touch.py'))
.. cog.out(run_script(cog.inFile, 'pathlib_touch.py', include_prefix=False))
.. }}}

.. code-block:: none

	$ python3 pathlib_touch.py
	
	creating new
	Start: Sat Aug 27 21:45:41 2016
	End  : Sat Aug 27 21:45:42 2016

	$ python3 pathlib_touch.py
	
	already exists
	Start: Sat Aug 27 21:45:42 2016
	End  : Sat Aug 27 21:45:43 2016

.. {{{end}}}

Permissions
===========

On UNIX-like systems, file permissions can be changed using
:func:`chmod`, passing the mode as an integer. Mode values can be
constructed using constants defined in the :mod:`stat` module.  This
example toggles the user's execute permission bit.

.. literalinclude:: pathlib_chmod.py
   :caption:
   :start-after: #end_pymotw_header

The script assumes it has the permissions necessary to modify the mode
of the file when run.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pathlib_chmod.py'))
.. }}}

.. code-block:: none

	$ python3 pathlib_chmod.py
	
	Before: 644
	Adding execute permission
	After: 744

.. {{{end}}}

Deleting
========

There are two methods for removing things from the file system,
depending on the type.  To remove an empty directory, use
:func:`rmdir`.

.. literalinclude:: pathlib_rmdir.py
   :caption:
   :start-after: #end_pymotw_header

A :class:`FileNotFoundError` exception is raised if the
post-conditions are already met and the directory does not exist. It
is also an error to try to remove a directory that is not empty.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pathlib_rmdir.py'))
.. cog.out(run_script(cog.inFile, 'pathlib_rmdir.py', include_prefix=False,
..         ignore_error=True, line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 pathlib_rmdir.py
	
	Removing example_dir

	$ python3 pathlib_rmdir.py
	
	Removing example_dir
	Traceback (most recent call last):
	  File "pathlib_rmdir.py", line 16, in <module>
	    p.rmdir()
	  File ".../lib/python3.5/pathlib.py", line 1262, in rmdir
	    self._accessor.rmdir(self)
	  File ".../lib/python3.5/pathlib.py", line 371, in wrapped
	    return strfunc(str(pathobj), *args)
	FileNotFoundError: [Errno 2] No such file or directory:
	'example_dir'

.. {{{end}}}

For files, symbolic links, and most other path types use
:func:`unlink`.

.. literalinclude:: pathlib_unlink.py
   :caption:
   :start-after: #end_pymotw_header

The user must have permission to remove the file, symbolic link,
socket, or other file system object.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pathlib_unlink.py'))
.. }}}

.. code-block:: none

	$ python3 pathlib_unlink.py
	
	exists before removing: True
	exists after removing: False

.. {{{end}}}

.. rename, replace
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
