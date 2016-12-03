=======================================
 shutil --- High-level File Operations
=======================================

.. module:: shutil
    :synopsis: High-level file operations.

The ``shutil`` module includes high-level file operations such as
copying and archiving.

Copying Files
=============

:func:`copyfile` copies the contents of the source to the destination
and raises :class:`IOError` if it does not have permission to write to
the destination file.

.. literalinclude:: shutil_copyfile.py
    :caption:
    :start-after: #end_pymotw_header

Because the function opens the input file for reading, regardless of
its type, special files (such as Unix device nodes) cannot be copied
as new special files with :func:`copyfile`.

.. {{{cog
.. run_script(cog.inFile, 'rm -rf *.copy', interpreter=None)
.. run_script(cog.inFile, 'rm -rf config.ini', interpreter=None)
.. run_script(cog.inFile, 'rm -rf *~', interpreter=None)
.. run_script(cog.inFile, 'rm -rf *.tar.gz', interpreter=None)
.. cog.out(run_script(cog.inFile, 'shutil_copyfile.py'))
.. }}}

.. code-block:: none

	$ python3 shutil_copyfile.py
	
	BEFORE: ['shutil_copyfile.py']
	AFTER: ['shutil_copyfile.py', 'shutil_copyfile.py.copy']

.. {{{end}}}

The implementation of :func:`copyfile` uses the lower-level function
:func:`copyfileobj`. While the arguments to :func:`copyfile` are
filenames, the arguments to :func:`copyfileobj` are open file
handles. The optional third argument is a buffer length to use for
reading in blocks.

.. literalinclude:: shutil_copyfileobj.py
    :caption:
    :start-after: #end_pymotw_header

The default behavior is to read using large blocks.  Use ``-1`` to
read all of the input at one time or another positive integer to set a
specific block size.  This example uses several different block sizes
to show the effect.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shutil_copyfileobj.py'))
.. }}}

.. code-block:: none

	$ python3 shutil_copyfileobj.py
	
	Default:
	read(16384) bytes
	read(16384) bytes
	
	All at once:
	read(-1) bytes
	read(-1) bytes
	
	Blocks of 256:
	read(256) bytes
	read(256) bytes

.. {{{end}}}

The ``copy()`` function interprets the output name like the Unix
command line tool ``cp``. If the named destination refers to a
directory instead of a file, a new file is created in the directory
using the base name of the source.

.. literalinclude:: shutil_copy.py
    :caption:
    :start-after: #end_pymotw_header

The permissions of the file are copied along with the contents.

.. {{{cog
.. run_script(cog.inFile, 'rm -rf example', interpreter='')
.. cog.out(run_script(cog.inFile, 'shutil_copy.py'))
.. }}}

.. code-block:: none

	$ python3 shutil_copy.py
	
	BEFORE: []
	AFTER : ['example/shutil_copy.py']

.. {{{end}}}


:func:`copy2` works like ``copy()``, but includes the access and
modification times in the metadata copied to the new file.

.. literalinclude:: shutil_copy2.py
    :caption:
    :start-after: #end_pymotw_header

The new file has all of the same characteristics as the old version.

.. {{{cog
.. run_script(cog.inFile, 'rm -rf example', interpreter='')
.. cog.out(run_script(cog.inFile, 'shutil_copy2.py'))
.. }}}

.. code-block:: none

	$ python3 shutil_copy2.py
	
	SOURCE:
		Mode    : 0o100644
		Created : Sat Sep  3 09:51:54 2016
		Accessed: Sat Sep  3 13:10:29 2016
		Modified: Sat Sep  3 09:51:54 2016
	DEST:
		Mode    : 0o100644
		Created : Sat Sep  3 13:10:29 2016
		Accessed: Sat Sep  3 13:10:29 2016
		Modified: Sat Sep  3 09:51:54 2016

.. {{{end}}}

Copying File Metadata
=====================

By default when a new file is created under Unix, it receives
permissions based on the umask of the current user. To copy the
permissions from one file to another, use :func:`copymode`.

.. literalinclude:: shutil_copymode.py
    :caption:
    :start-after: #end_pymotw_header

This example script creates a file to be modified, then uses
:func:`copymode` to duplicate the permissions of the script to the
example file.

.. {{{cog
.. run_script(cog.inFile, 'rm -f file_to_change.txt', interpreter='')
.. cog.out(run_script(cog.inFile, 'shutil_copymode.py'))
.. }}}

.. code-block:: none

	$ python3 shutil_copymode.py
	
	BEFORE: 0o100444
	AFTER : 0o100644

.. {{{end}}}

To copy other metadata about the file use :func:`copystat`.

.. literalinclude:: shutil_copystat.py
    :caption:
    :start-after: #end_pymotw_header

Only the permissions and dates associated with the file are duplicated
with :func:`copystat`.

.. {{{cog
.. run_script(cog.inFile, 'rm -f file_to_change.txt', interpreter='')
.. cog.out(run_script(cog.inFile, 'shutil_copystat.py'))
.. }}}

.. code-block:: none

	$ python3 shutil_copystat.py
	
	BEFORE:
		Mode    : 0o100444
		Created : Sat Sep  3 13:10:30 2016
		Accessed: Sat Sep  3 13:10:30 2016
		Modified: Sat Sep  3 13:10:30 2016
	AFTER:
		Mode    : 0o100644
		Created : Sat Sep  3 13:10:30 2016
		Accessed: Sat Sep  3 13:10:29 2016
		Modified: Sat Sep  3 09:55:22 2016

.. {{{end}}}

.. _shutil-directory-functions:

Working With Directory Trees
============================

``shutil`` includes three functions for working with directory
trees. To copy a directory from one place to another, use
:func:`copytree`. It recurses through the source directory tree,
copying files to the destination. The destination directory must not
exist in advance.

.. literalinclude:: shutil_copytree.py
    :caption:
    :start-after: #end_pymotw_header

The ``symlinks`` argument controls whether symbolic links are copied as
links or as files. The default is to copy the contents to new
files. If the option is true, new symlinks are created within the
destination tree.

.. {{{cog
.. run_script(cog.inFile, 'rm -rf /tmp/example', interpreter='')
.. cog.out(run_script(cog.inFile, 'shutil_copytree.py'))
.. }}}

.. code-block:: none

	$ python3 shutil_copytree.py
	
	BEFORE:
	[]
	
	AFTER:
	['/tmp/example/example',
	 '/tmp/example/example.out',
	 '/tmp/example/file_to_change.txt',
	 '/tmp/example/index.rst',
	 '/tmp/example/shutil_copy.py',
	 '/tmp/example/shutil_copy2.py',
	 '/tmp/example/shutil_copyfile.py',
	 '/tmp/example/shutil_copyfile.py.copy',
	 '/tmp/example/shutil_copyfileobj.py',
	 '/tmp/example/shutil_copymode.py',
	 '/tmp/example/shutil_copystat.py',
	 '/tmp/example/shutil_copytree.py',
	 '/tmp/example/shutil_copytree_verbose.py',
	 '/tmp/example/shutil_disk_usage.py',
	 '/tmp/example/shutil_get_archive_formats.py',
	 '/tmp/example/shutil_get_unpack_formats.py',
	 '/tmp/example/shutil_make_archive.py',
	 '/tmp/example/shutil_move.py',
	 '/tmp/example/shutil_rmtree.py',
	 '/tmp/example/shutil_unpack_archive.py',
	 '/tmp/example/shutil_which.py',
	 '/tmp/example/shutil_which_regular_file.py']

.. {{{end}}}

:func:`copytree` accepts two callable arguments to control its
behavior. The ``ignore`` argument is called with the name of each
directory or subdirectory being copied along with a list of the
contents of the directory. It should return a list of items that
should be copied. The ``copy_function`` argument is called to actually
copy the file.

.. literalinclude:: shutil_copytree_verbose.py
   :caption:
   :start-after: #end_pymotw_header

In the example, :func:`ignore_patterns` is used to create an ignore
function to skip copying Python source files. :func:`verbose_copy`
prints the names of files as they are copied then uses :func:`copy2`,
the default copy function, to make the copies.

.. {{{cog
.. run_script(cog.inFile, 'rm -rf /tmp/example', interpreter='')
.. run_script(cog.inFile, 'rm -rf *.copy', interpreter='')
.. cog.out(run_script(cog.inFile, 'shutil_copytree_verbose.py'))
.. }}}

.. code-block:: none

	$ python3 shutil_copytree_verbose.py
	
	BEFORE:
	[]
	
	copying
	 '../shutil/example.out'
	 to '/tmp/example/example.out'
	copying
	 '../shutil/file_to_change.txt'
	 to '/tmp/example/file_to_change.txt'
	copying
	 '../shutil/index.rst'
	 to '/tmp/example/index.rst'
	
	AFTER:
	['/tmp/example/example',
	 '/tmp/example/example.out',
	 '/tmp/example/file_to_change.txt',
	 '/tmp/example/index.rst']

.. {{{end}}}

To remove a directory and its contents, use :func:`rmtree`.

.. literalinclude:: shutil_rmtree.py
    :caption:
    :start-after: #end_pymotw_header

Errors are raised as exceptions by default, but can be ignored if the
second argument is true, and a special error handler function can be
provided in the third argument.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shutil_rmtree.py'))
.. }}}

.. code-block:: none

	$ python3 shutil_rmtree.py
	
	BEFORE:
	['/tmp/example/example',
	 '/tmp/example/example.out',
	 '/tmp/example/file_to_change.txt',
	 '/tmp/example/index.rst']
	
	AFTER:
	[]

.. {{{end}}}

To move a file or directory from one place to another, use
:func:`move`.

.. literalinclude:: shutil_move.py
    :caption:
    :start-after: #end_pymotw_header

The semantics are similar to those of the Unix command ``mv``. If the
source and destination are within the same file system, the source is
renamed.  Otherwise the source is copied to the destination and then
the source is removed.

.. {{{cog
.. run_script(cog.inFile, 'rm -rf example', interpreter='')
.. run_script(cog.inFile, 'rm -f example*', interpreter='')
.. cog.out(run_script(cog.inFile, 'shutil_move.py'))
.. }}}

.. code-block:: none

	$ python3 shutil_move.py
	
	BEFORE:  ['example.txt']
	AFTER :  ['example.out']

.. {{{end}}}

Finding Files
=============

The :func:`which` function scans a search path looking for a named
file. The typical use case is to find an executable program on the
shell's search path defined in the environment variable ``PATH``.

.. literalinclude:: shutil_which.py
   :caption:
   :start-after: #end_pymotw_header

If no file matching the search parameters can be found, :func:`which`
returns ``None``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shutil_which.py'))
.. }}}

.. code-block:: none

	$ python3 shutil_which.py
	
	/Users/dhellmann/Library/Python/3.5/bin/virtualenv
	/Users/dhellmann/Library/Python/3.5/bin/tox
	None

.. {{{end}}}

:func:`which` takes arguments to filter based on the permissions the
file has, and the search path to examine. The ``path`` argument defaults
to ``os.environ('PATH')``, but can be any string containing directory
names separated by :const:`os.pathsep`. The ``mode`` argument should be
a bitmask matching the permissions of the file. By default the mask
looks for executable files, but the following example uses a readable
bitmask and an alternate search path to find a configuration file.

.. literalinclude:: shutil_which_regular_file.py
   :caption:
   :start-after: #end_pymotw_header

There is still a race condition searching for readable files this way,
because in the time between finding the file and actually trying to
use it, the file can be deleted or its permissions can be changed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'touch config.ini', interpreter='', trailing_newlines=False))
.. cog.out(run_script(cog.inFile, 'shutil_which_regular_file.py', include_prefix=False))
.. }}}

.. code-block:: none

	$ touch config.ini
	$ python3 shutil_which_regular_file.py
	
	./config.ini

.. {{{end}}}

Archives
========

Python's standard library includes many modules for managing archive
files such as :mod:`tarfile` and :mod:`zipfile`. There are also
several higher-level functions for creating and extracting archives in
``shutil``. :func:`get_archive_formats` returns a sequence of names
and descriptions for formats supported on the current system.

.. literalinclude:: shutil_get_archive_formats.py
   :caption:
   :start-after: #end_pymotw_header

The formats supported depend on which modules and underlying libraries
are available, so the output for this example may change based on
where it is run.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shutil_get_archive_formats.py'))
.. }}}

.. code-block:: none

	$ python3 shutil_get_archive_formats.py
	
	bztar: bzip2'ed tar-file
	gztar: gzip'ed tar-file
	tar  : uncompressed tar file
	xztar: xz'ed tar-file
	zip  : ZIP file

.. {{{end}}}

Use :func:`make_archive` to create a new archive file. Its inputs are
designed to best support archiving an entire directory and all of its
contents, recursively. By default it uses the current working
directory, so that all of the files and subdirectories appear at the
top level of the archive. To change that behavior, use the ``root_dir``
argument to move to a new relative position on the filesystem and the
``base_dir`` argument to specify a directory to add to the archive.

.. literalinclude:: shutil_make_archive.py
   :caption:
   :start-after: #end_pymotw_header

This example starts within the source directory for the examples for
``shutil`` and moves up one level in the file system, then adds the
``shutil`` directory to a tar archive compressed with gzip. The
:mod:`logging` module is configured to show messages from
:func:`make_archive` about what it is doing.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shutil_make_archive.py'))
.. }}}

.. code-block:: none

	$ python3 shutil_make_archive.py
	
	Creating archive:
	changing into '..'
	Creating tar archive
	changing back to '...'
	
	Archive contents:
	shutil
	shutil/config.ini
	shutil/example.out
	shutil/file_to_change.txt
	shutil/index.rst
	shutil/shutil_copy.py
	shutil/shutil_copy2.py
	shutil/shutil_copyfile.py
	shutil/shutil_copyfileobj.py
	shutil/shutil_copymode.py
	shutil/shutil_copystat.py
	shutil/shutil_copytree.py
	shutil/shutil_copytree_verbose.py
	shutil/shutil_disk_usage.py
	shutil/shutil_get_archive_formats.py
	shutil/shutil_get_unpack_formats.py
	shutil/shutil_make_archive.py
	shutil/shutil_move.py
	shutil/shutil_rmtree.py
	shutil/shutil_unpack_archive.py
	shutil/shutil_which.py
	shutil/shutil_which_regular_file.py

.. {{{end}}}

``shutil`` maintains a registry of formats that can be unpacked on
the current system, accessible via :func:`get_unpack_formats`.

.. literalinclude:: shutil_get_unpack_formats.py
   :caption:
   :start-after: #end_pymotw_header

This registry is different from the registry for creating archives
because it also includes common file extensions used for each format
so that the function for extracting an archive can guess which format
to use based on the file extension.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shutil_get_unpack_formats.py'))
.. }}}

.. code-block:: none

	$ python3 shutil_get_unpack_formats.py
	
	bztar: bzip2'ed tar-file, names ending in ['.tar.bz2', '.tbz2']
	gztar: gzip'ed tar-file, names ending in ['.tar.gz', '.tgz']
	tar  : uncompressed tar file, names ending in ['.tar']
	xztar: xz'ed tar-file, names ending in ['.tar.xz', '.txz']
	zip  : ZIP file, names ending in ['.zip']

.. {{{end}}}

Extract the archive with :func:`unpack_archive`, passing the archive
file name and optionally the directory where it should be
extracted. If no directory is given, the current directory is used.

.. literalinclude:: shutil_unpack_archive.py
   :caption:
   :start-after: #end_pymotw_header

In this example :func:`unpack_archive` is able to determine the format
of the archive because the filename ends with ``tar.gz``, and that
value is associated with the ``gztar`` format in the unpack format
registry.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shutil_unpack_archive.py'))
.. }}}

.. code-block:: none

	$ python3 shutil_unpack_archive.py
	
	Unpacking archive:
	
	Created:
	shutil
	shutil/config.ini
	shutil/example.out
	shutil/file_to_change.txt
	shutil/index.rst
	shutil/shutil_copy.py
	shutil/shutil_copy2.py
	shutil/shutil_copyfile.py
	shutil/shutil_copyfileobj.py
	shutil/shutil_copymode.py
	shutil/shutil_copystat.py
	shutil/shutil_copytree.py
	shutil/shutil_copytree_verbose.py
	shutil/shutil_disk_usage.py
	shutil/shutil_get_archive_formats.py
	shutil/shutil_get_unpack_formats.py
	shutil/shutil_make_archive.py
	shutil/shutil_move.py
	shutil/shutil_rmtree.py
	shutil/shutil_unpack_archive.py
	shutil/shutil_which.py
	shutil/shutil_which_regular_file.py

.. {{{end}}}

File System Space
=================

It can be useful to examine the local file system to see how much
space is available before performing a long running operation that may
exhaust that space. :func:`disk_usage` returns a tuple with the total
space, the amount currently being used, and the amount remaining free.

.. literalinclude:: shutil_disk_usage.py
   :caption:
   :start-after: #end_pymotw_header

The values returned by :func:`disk_usage` are the number of bytes, so
the example program converts them to more readable units before
printing them.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shutil_disk_usage.py'))
.. }}}

.. code-block:: none

	$ python3 shutil_disk_usage.py
	
	Total: 499.42 GB  465.12 GiB
	Used : 246.68 GB  229.73 GiB
	Free : 252.48 GB  235.14 GiB

.. {{{end}}}



.. seealso::

   * :pydoc:`shutil`

   * :doc:`/compression` -- Modules for dealing with archive and
     compression formats.
