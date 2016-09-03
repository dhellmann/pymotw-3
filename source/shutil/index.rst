=======================================
 shutil --- High-level File Operations
=======================================

.. module:: shutil
    :synopsis: High-level file operations.

:Purpose: High-level file operations.

The :mod:`shutil` module includes high-level file operations such as
copying and setting permissions.

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

The :func:`copy` function interprets the output name like the Unix
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


:func:`copy2` works like :func:`copy`, but includes the access and
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
		Accessed: Sat Sep  3 10:33:33 2016
		Modified: Sat Sep  3 09:51:54 2016
	DEST:
		Mode    : 0o100644
		Created : Sat Sep  3 10:33:33 2016
		Accessed: Sat Sep  3 10:33:33 2016
		Modified: Sat Sep  3 09:51:54 2016

.. {{{end}}}

Copying File Metadata
=====================

By default when a new file is created under UNIX, it receives
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
		Created : Sat Sep  3 10:33:33 2016
		Accessed: Sat Sep  3 10:33:33 2016
		Modified: Sat Sep  3 10:33:33 2016
	AFTER:
		Mode    : 0o100644
		Created : Sat Sep  3 10:33:33 2016
		Accessed: Sat Sep  3 10:33:33 2016
		Modified: Sat Sep  3 09:55:22 2016

.. {{{end}}}

.. _shutil-directory-functions:

Working With Directory Trees
============================

:mod:`shutil` includes three functions for working with directory
trees. To copy a directory from one place to another, use
:func:`copytree`. It recurses through the source directory tree,
copying files to the destination. The destination directory must not
exist in advance.

.. note::

  The documentation for :func:`copytree` says it should be
  considered a sample implementation, rather than a tool.  Consider
  starting with the current implementation and making it more robust,
  or adding features like a progress meter, before using it.

.. literalinclude:: shutil_copytree.py
    :caption:
    :start-after: #end_pymotw_header

The *symlinks* argument controls whether symbolic links are copied as
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
	 '/tmp/example/shutil_disk_usage.py',
	 '/tmp/example/shutil_move.py',
	 '/tmp/example/shutil_rmtree.py']

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
	 '/tmp/example/index.rst',
	 '/tmp/example/shutil_copy.py',
	 '/tmp/example/shutil_copy2.py',
	 '/tmp/example/shutil_copyfile.py',
	 '/tmp/example/shutil_copyfile.py.copy',
	 '/tmp/example/shutil_copyfileobj.py',
	 '/tmp/example/shutil_copymode.py',
	 '/tmp/example/shutil_copystat.py',
	 '/tmp/example/shutil_copytree.py',
	 '/tmp/example/shutil_disk_usage.py',
	 '/tmp/example/shutil_move.py',
	 '/tmp/example/shutil_rmtree.py']
	
	AFTER:
	[]

.. {{{end}}}

To move a file or directory from one place to another, use
:func:`move`.

.. literalinclude:: shutil_move.py
    :caption:
    :start-after: #end_pymotw_header

The semantics are similar to those of the Unix command :command:`mv`. If the
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
	Used : 246.62 GB  229.68 GiB
	Free : 252.54 GB  235.20 GiB

.. {{{end}}}



.. seealso::

   * :pydoc:`shutil`
