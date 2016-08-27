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



.. pure vs. concrete
.. examples of windows paths

.. sorting, hashing

.. slash operator for combining segments
.. joinpath() method for same
.. parts attribute for parsing
.. parents attribute for moving up the tree
.. parent attribute for looking at containing directory
.. name attribute for final component
.. suffix attribute for getting the extension
.. stem attribute for the base name

.. match

.. relative_to
.. with_name
.. with_suffix

.. cwd class method
.. home class method

.. stat
.. chmod, group, owner
.. exists
.. expanduser
.. glob, rglob

.. is_dir, is_file, is_symlink, is_socket, is_fifo, is_block_device, is_char_device

.. iterdir

.. mkdir, rmdir
.. rename, replace

.. open
.. read_bytes, write_bytes
.. read_text, write_text

.. symlink_to
.. touch
.. unlink


.. seealso::

   * :pydoc:`pathlib`

   * :mod:`os.path` -- Platform-independent manipulation of filenames

   * :pep:`428` -- The pathlib module
