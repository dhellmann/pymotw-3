======================================
 shutil -- High-level File Operations
======================================

.. module:: shutil
    :synopsis: High-level file operations.

:Purpose: High-level file operations.

The :mod:`shutil` module includes high-level file operations such as
copying and setting permissions.

Copying Files
=============

:func:`copyfile` copies the contents of the source to the
destination and raises :class:`IOError` if it does
not have permission to write to the destination file.  

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

::

	$ python shutil_copyfile.py
	
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

::

	$ python shutil_copyfileobj.py
	
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
.. (path(cog.inFile).parent / 'example').rmtree()
.. cog.out(run_script(cog.inFile, 'shutil_copy.py'))
.. }}}

::

	$ python shutil_copy.py
	
	BEFORE: []
	AFTER: ['shutil_copy.py']

.. {{{end}}}


:func:`copy2` works like :func:`copy`, but includes the access and
modification times in the metadata copied to the new file.

.. literalinclude:: shutil_copy2.py
    :caption:
    :start-after: #end_pymotw_header

The new file has all of the same characteristics as the old version.

.. {{{cog
.. (path(cog.inFile).parent / 'example').rmtree()
.. cog.out(run_script(cog.inFile, 'shutil_copy2.py'))
.. }}}

::

	$ python shutil_copy2.py
	
	SOURCE:
		Mode    : 33188
		Created : Sat Dec  4 10:41:32 2010
		Accessed: Sat Dec  4 17:41:01 2010
		Modified: Sun Nov 14 09:40:36 2010
	DEST:
		Mode    : 33188
		Created : Sat Dec  4 17:41:01 2010
		Accessed: Sat Dec  4 17:41:01 2010
		Modified: Sun Nov 14 09:40:36 2010

.. {{{end}}}


Copying File Metadata
=====================

By default when a new file is created under Unix, it receives
permissions based on the umask of the current user. To copy the
permissions from one file to another, use :func:`copymode`.

.. literalinclude:: shutil_copymode.py
    :caption:
    :start-after: #end_pymotw_header

First, create a file to be modified.

.. literalinclude:: shutil_copymode.sh
    :caption:

Then, run the example script to change the permissions.

.. {{{cog
.. (path(cog.inFile).parent / 'file_to_change.txt').unlink()
.. cog.out(run_script(cog.inFile, 'shutil_copymode.py'))
.. }}}

::

	$ python shutil_copymode.py
	
	BEFORE:
	-r--r--r--  1 dhellmann  dhellmann  7 Dec  4 17:41 file_to_change.txt
	AFTER :
	-rw-r--r--  1 dhellmann  dhellmann  7 Dec  4 17:41 file_to_change.txt

.. {{{end}}}

To copy other metadata about the file use :func:`copystat`.

.. literalinclude:: shutil_copystat.py
    :caption:
    :start-after: #end_pymotw_header

Only the permissions and dates associated with the file are duplicated
with :func:`copystat`.

.. {{{cog
.. (path(cog.inFile).parent / 'file_to_change.txt').unlink()
.. cog.out(run_script(cog.inFile, 'shutil_copystat.py'))
.. }}}

::

	$ python shutil_copystat.py
	
	BEFORE:
		Mode    : 33060
		Created : Sat Dec  4 17:41:01 2010
		Accessed: Sat Dec  4 17:41:01 2010
		Modified: Sat Dec  4 17:41:01 2010
	AFTER:
		Mode    : 33188
		Created : Sat Dec  4 17:41:01 2010
		Accessed: Sat Dec  4 17:41:01 2010
		Modified: Sun Nov 14 09:45:12 2010

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
.. path('/tmp/example').rmtree()
.. cog.out(run_script(cog.inFile, 'shutil_copytree.py'))
.. }}}

::

	$ python shutil_copytree.py
	
	BEFORE:
	ls: /tmp/example: No such file or directory
	
	AFTER:
	total 136
	 8 -rwxr-xr-x   1 dhellmann  wheel   109 Oct 28 07:33 shutil_copymode.sh
	 8 -rw-r--r--   1 dhellmann  wheel  1313 Nov 14 09:39 shutil_rmtree.py
	 8 -rw-r--r--   1 dhellmann  wheel  1300 Nov 14 09:39 shutil_copyfile.py
	 8 -rw-r--r--   1 dhellmann  wheel  1276 Nov 14 09:39 shutil_copy.py
	 8 -rw-r--r--   1 dhellmann  wheel  1140 Nov 14 09:39 __init__.py
	 8 -rw-r--r--   1 dhellmann  wheel  1595 Nov 14 09:40 shutil_copy2.py
	 8 -rw-r--r--   1 dhellmann  wheel  1729 Nov 14 09:45 shutil_copystat.py
	 8 -rw-r--r--   1 dhellmann  wheel     7 Nov 14 09:45 file_to_change.txt
	 8 -rw-r--r--   1 dhellmann  wheel  1324 Nov 14 09:45 shutil_move.py
	 8 -rw-r--r--   1 dhellmann  wheel   419 Nov 27 12:49 shutil_copymode.py
	 8 -rw-r--r--   1 dhellmann  wheel  1331 Dec  1 21:51 shutil_copytree.py
	 8 -rw-r--r--   1 dhellmann  wheel   816 Dec  4 17:39 shutil_copyfileobj.py
	 8 -rw-r--r--   1 dhellmann  wheel     8 Dec  4 17:39 example.out
	24 -rw-r--r--   1 dhellmann  wheel  9767 Dec  4 17:40 index.rst
	 8 -rw-r--r--   1 dhellmann  wheel  1300 Dec  4 17:41 shutil_copyfile.py.copy
	 0 drwxr-xr-x   3 dhellmann  wheel   102 Dec  4 17:41 example
	 0 drwxrwxrwt  18 root       wheel   612 Dec  4 17:41 ..
	 0 drwxr-xr-x  18 dhellmann  wheel   612 Dec  4 17:41 .

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

::

	$ python shutil_rmtree.py
	
	BEFORE:
	total 136
	 8 -rwxr-xr-x   1 dhellmann  wheel   109 Oct 28 07:33 shutil_copymode.sh
	 8 -rw-r--r--   1 dhellmann  wheel  1313 Nov 14 09:39 shutil_rmtree.py
	 8 -rw-r--r--   1 dhellmann  wheel  1300 Nov 14 09:39 shutil_copyfile.py
	 8 -rw-r--r--   1 dhellmann  wheel  1276 Nov 14 09:39 shutil_copy.py
	 8 -rw-r--r--   1 dhellmann  wheel  1140 Nov 14 09:39 __init__.py
	 8 -rw-r--r--   1 dhellmann  wheel  1595 Nov 14 09:40 shutil_copy2.py
	 8 -rw-r--r--   1 dhellmann  wheel  1729 Nov 14 09:45 shutil_copystat.py
	 8 -rw-r--r--   1 dhellmann  wheel     7 Nov 14 09:45 file_to_change.txt
	 8 -rw-r--r--   1 dhellmann  wheel  1324 Nov 14 09:45 shutil_move.py
	 8 -rw-r--r--   1 dhellmann  wheel   419 Nov 27 12:49 shutil_copymode.py
	 8 -rw-r--r--   1 dhellmann  wheel  1331 Dec  1 21:51 shutil_copytree.py
	 8 -rw-r--r--   1 dhellmann  wheel   816 Dec  4 17:39 shutil_copyfileobj.py
	 8 -rw-r--r--   1 dhellmann  wheel     8 Dec  4 17:39 example.out
	24 -rw-r--r--   1 dhellmann  wheel  9767 Dec  4 17:40 index.rst
	 8 -rw-r--r--   1 dhellmann  wheel  1300 Dec  4 17:41 shutil_copyfile.py.copy
	 0 drwxr-xr-x   3 dhellmann  wheel   102 Dec  4 17:41 example
	 0 drwxrwxrwt  18 root       wheel   612 Dec  4 17:41 ..
	 0 drwxr-xr-x  18 dhellmann  wheel   612 Dec  4 17:41 .
	AFTER:
	ls: /tmp/example: No such file or directory

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
.. (path(cog.inFile).parent / 'example').rmtree()
.. d = [ f.unlink() for f in path(cog.inFile).parent.glob('example.*') ]
.. cog.out(run_script(cog.inFile, 'shutil_move.py'))
.. }}}

::

	$ python shutil_move.py
	
	BEFORE:  ['example.txt']
	AFTER :  ['example.out']

.. {{{end}}}


.. seealso::

    `shutil <http://docs.python.org/lib/module-shutil.html>`_
        Standard library documentation for this module.
