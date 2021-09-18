=====================================
shutil -- High-level file operations.
=====================================

.. module:: shutil
    :synopsis: High-level file operations.

:Purpose: High-level file operations.
:Available In: 1.4 and later

The :mod:`shutil` module includes high-level file operations such as
copying, setting permissions, etc.

Copying Files
=============

:func:`copyfile()` copies the contents of the source to the
destination. Raises :ref:`IOError <exceptions-IOError>` if you do not
have permission to write to the destination file.  Because the
function opens the input file for reading, regardless of its type,
special files cannot be copied as new special files with
:func:`copyfile()`.

.. include:: shutil_copyfile.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. run_script(cog.inFile, 'rm -rf *.copy', interpreter=None)
.. cog.out(run_script(cog.inFile, 'shutil_copyfile.py'))
.. }}}

::

	$ python shutil_copyfile.py
	
	BEFORE: ['shutil_copyfile.py']
	AFTER: ['shutil_copyfile.py', 'shutil_copyfile.py.copy']

.. {{{end}}}


:func:`copyfile()` is written using the lower-level function
:func:`copyfileobj()`. While the arguments to :func:`copyfile()` are
file names, the arguments to :func:`copyfileobj()` are open file
handles. The optional third argument is a buffer length to use for
reading in chunks (by default, the entire file is read at one time).

.. include:: shutil_copyfileobj.py
    :literal:
    :start-after: #end_pymotw_header

The default behavior is to read using large blocks.  Use ``-1`` to
read all of the input at one time or another positive integer to set
your own block size.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shutil_copyfileobj.py'))
.. }}}

::

	$ python shutil_copyfileobj.py
	
	Default:
	read(16384) => Lorem ipsum dolor sit amet, consectetuer adipiscing elit. 
	Vestibulum aliquam mollis dolor. Donec vulputate nunc ut diam. 
	Ut rutrum mi vel sem. Vestibulum ante ipsum.
	read(16384) => 
	
	All at once:
	read(-1) => Lorem ipsum dolor sit amet, consectetuer adipiscing elit. 
	Vestibulum aliquam mollis dolor. Donec vulputate nunc ut diam. 
	Ut rutrum mi vel sem. Vestibulum ante ipsum.
	read(-1) => 
	
	Blocks of 20:
	read(20) => Lorem ipsum dolor si
	read(20) => t amet, consectetuer
	read(20) =>  adipiscing elit. 
	V
	read(20) => estibulum aliquam mo
	read(20) => llis dolor. Donec vu
	read(20) => lputate nunc ut diam
	read(20) => . 
	Ut rutrum mi vel 
	read(20) => sem. Vestibulum ante
	read(20) =>  ipsum.
	read(20) => 

.. {{{end}}}


The :func:`copy()` function interprets the output name like the Unix
command line tool ``cp``. If the named destination refers to a
directory instead of a file, a new file is created in the directory
using the base name of the source. The permissions of the file are
copied along with the contents.

.. include:: shutil_copy.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. (path(cog.inFile).parent / 'example').rmtree()
.. cog.out(run_script(cog.inFile, 'shutil_copy.py'))
.. }}}

::

	$ python shutil_copy.py
	
	BEFORE: []
	AFTER: ['shutil_copy.py']

.. {{{end}}}


:func:`copy2()` works like :func:`copy()`, but includes the access and
modification times in the meta-data copied to the new file.

.. include:: shutil_copy2.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. (path(cog.inFile).parent / 'example').rmtree()
.. cog.out(run_script(cog.inFile, 'shutil_copy2.py'))
.. }}}

::

	$ python shutil_copy2.py
	
	SOURCE:
		Mode    : 33188
		Created : Sat Jul 16 12:28:43 2011
		Accessed: Thu Feb 21 06:36:54 2013
		Modified: Sat Feb 19 19:18:23 2011
	DEST:
		Mode    : 33188
		Created : Thu Feb 21 06:36:54 2013
		Accessed: Thu Feb 21 06:36:54 2013
		Modified: Sat Feb 19 19:18:23 2011

.. {{{end}}}


Copying File Meta-data
======================

By default when a new file is created under Unix, it receives
permissions based on the umask of the current user. To copy the
permissions from one file to another, use :func:`copymode()`.

.. include:: shutil_copymode.py
    :literal:
    :start-after: #end_pymotw_header

First, create a file to be modified:

.. include:: shutil_copymode.sh
    :literal:

Then run the example script to change the permissions.

.. {{{cog
.. (path(cog.inFile).parent / 'file_to_change.txt').unlink()
.. cog.out(run_script(cog.inFile, 'shutil_copymode.py'))
.. }}}

::

	$ python shutil_copymode.py
	
	BEFORE: -r--r--r--  1 dhellmann  dhellmann  7 Feb 21 06:36 file_to_change.txt
	AFTER : -rw-r--r--  1 dhellmann  dhellmann  7 Feb 21 06:36 file_to_change.txt

.. {{{end}}}

To copy other meta-data about the file (permissions, last access time,
and last modified time), use :func:`copystat()`.

.. include:: shutil_copystat.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. (path(cog.inFile).parent / 'file_to_change.txt').unlink()
.. cog.out(run_script(cog.inFile, 'shutil_copystat.py'))
.. }}}

::

	$ python shutil_copystat.py
	
	BEFORE:
		Mode    : 33060
		Created : Thu Feb 21 06:36:54 2013
		Accessed: Thu Feb 21 06:36:54 2013
		Modified: Thu Feb 21 06:36:54 2013
	AFTER :
		Mode    : 33188
		Created : Thu Feb 21 06:36:54 2013
		Accessed: Thu Feb 21 06:36:54 2013
		Modified: Sat Feb 19 19:18:23 2011

.. {{{end}}}

Working With Directory Trees
============================

:mod:`shutil` includes 3 functions for working with directory
trees. To copy a directory from one place to another, use
:func:`copytree()`. It recurses through the source directory tree,
copying files to the destination. The destination directory must not
exist in advance. The *symlinks* argument controls whether symbolic
links are copied as links or as files. The default is to copy the
contents to new files. If the option is true, new symlinks are created
within the destination tree.

.. note::

  The documentation for :func:`copytree()` says it should be
  considered a sample implementation, rather than a tool. You may want
  to copy the implementation and make it more robust, or add features
  like a progress meter.

.. include:: shutil_copytree.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shutil_copytree.py'))
.. }}}

::

	$ python shutil_copytree.py
	
	BEFORE:
	ls: /tmp/example: No such file or directory
	AFTER:
	total 8
	8 -rw-r--r--   1 dhellmann  wheel  1595 Feb 19  2011 shutil_copy2.py
	0 drwxrwxrwt  19 root       wheel   646 Feb 21 06:36 ..
	0 drwxr-xr-x   3 dhellmann  wheel   102 Feb 21 06:36 .

.. {{{end}}}

To remove a directory and its contents, use :func:`rmtree()`. Errors
are raised as exceptions by default, but can be ignored if the second
argument is true, and a special error handler function can be provided
in the third argument.

.. include:: shutil_rmtree.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shutil_rmtree.py'))
.. }}}

::

	$ python shutil_rmtree.py
	
	BEFORE:
	total 8
	8 -rw-r--r--   1 dhellmann  wheel  1595 Feb 19  2011 shutil_copy2.py
	0 drwxrwxrwt  19 root       wheel   646 Feb 21 06:36 ..
	0 drwxr-xr-x   3 dhellmann  wheel   102 Feb 21 06:36 .
	AFTER:
	ls: /tmp/example: No such file or directory

.. {{{end}}}

To move a file or directory from one place to another, use
:func:`move()`. The semantics are similar to those of the Unix command
``mv``. If the source and destination are within the same filesystem,
the source is simply renamed.  Otherwise the source is copied to the
destination and then the source is removed.

.. include:: shutil_move.py
    :literal:
    :start-after: #end_pymotw_header

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

    `shutil <https://docs.python.org/2/library/shutil.html>`_
        Standard library documentation for this module.

    :ref:`article-file-access`
        Other utilities for working with files.
