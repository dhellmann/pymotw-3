=============================
tarfile -- Tar archive access
=============================

.. module:: tarfile
    :synopsis: Tar archive access

:Purpose: Tar archive access.
:Available In: 2.3 and later

The :mod:`tarfile` module provides read and write access to UNIX tar
archives, including compressed files.  In addition to the POSIX
standards, several GNU tar extensions are supported.  Various UNIX
special file types (hard and soft links, device nodes, etc.) are also
handled.

Testing Tar Files
=================

The :func:`is_tarfile()` function returns a boolean indicating whether
or not the filename passed as an argument refers to a valid tar file.

.. include:: tarfile_is_tarfile.py
    :literal:
    :start-after: #end_pymotw_header

If the file does not exist, :func:`is_tarfile()` raises an
:ref:`IOError <exceptions-IOError>`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tarfile_is_tarfile.py'))
.. }}}

::

	$ python tarfile_is_tarfile.py
	
	          README.txt  False
	         example.tar  True
	     bad_example.tar  False
	        notthere.tar  [Errno 2] No such file or directory: 'notthere.tar'

.. {{{end}}}

Reading Meta-data from an Archive
=================================

Use the :class:`TarFile` class to work directly with a tar archive. It
supports methods for reading data about existing archives as well as
modifying the archives by adding additional files.

To read the names of the files in an existing archive, use
:func:`getnames()`:

.. include:: tarfile_getnames.py
    :literal:
    :start-after: #end_pymotw_header

The return value is a list of strings with the names of the archive
contents:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tarfile_getnames.py'))
.. }}}

::

	$ python tarfile_getnames.py
	
	['README.txt']

.. {{{end}}}

In addition to names, meta-data about the archive members is available
as instances of :class:`TarInfo` objects.  Load the meta-data via
:func:`getmembers()` and :func:`getmember()`.

.. include:: tarfile_getmembers.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tarfile_getmembers.py'))
.. }}}

::

	$ python tarfile_getmembers.py
	
	README.txt
		Modified:	Sun Feb 22 11:13:55 2009
		Mode    :	0644
		Type    :	0
		Size    :	75 bytes
	

.. {{{end}}}


If you know in advance the name of the archive member, you can
retrieve its :class:`TarInfo` object with :func:`getmember()`.

.. include:: tarfile_getmember.py
    :literal:
    :start-after: #end_pymotw_header

If the archive member is not present, :func:`getmember()` raises a
:ref:`KeyError <exceptions-KeyError>`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tarfile_getmember.py'))
.. }}}

::

	$ python tarfile_getmember.py
	
	README.txt is 75 bytes
	ERROR: Did not find notthere.txt in tar archive

.. {{{end}}}

Extracting Files From an Archive
================================

To access the data from an archive member within your program, use the
:func:`extractfile()` method, passing the member's name.

.. include:: tarfile_extractfile.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tarfile_extractfile.py'))
.. }}}

::

	$ python tarfile_extractfile.py
	
	README.txt : The examples for the tarfile module use this file and example.tar as data.
	
	ERROR: Did not find notthere.txt in tar archive

.. {{{end}}}

If you just want to unpack the archive and write the files to the
filesystem, use :func:`extract()` or :func:`extractall()` instead.

.. include:: tarfile_extract.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. outdir = path(cog.inFile).dirname() / 'outdir'
.. outdir.rmtree()
.. cog.out(run_script(cog.inFile, 'tarfile_extract.py'))
.. }}}

::

	$ python tarfile_extract.py
	
	['README.txt']

.. {{{end}}}

.. note:: 

    The standard library documentation includes a note stating that
    :func:`extractall()` is safer than :func:`extract()`, and it
    should be used in most cases.

.. include:: tarfile_extractall.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. outdir = path(cog.inFile).dirname() / 'outdir'
.. outdir.rmtree()
.. cog.out(run_script(cog.inFile, 'tarfile_extractall.py'))
.. }}}

::

	$ python tarfile_extractall.py
	
	['README.txt']

.. {{{end}}}

If you only want to extract certain files from the archive, their
names can be passed to :func:`extractall()`.

.. include:: tarfile_extractall_members.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. outdir = path(cog.inFile).dirname() / 'outdir'
.. outdir.rmtree()
.. cog.out(run_script(cog.inFile, 'tarfile_extractall_members.py'))
.. }}}

::

	$ python tarfile_extractall_members.py
	
	['README.txt']

.. {{{end}}}

Creating New Archives
=====================

To create a new archive, simply open the :class:`TarFile` with a mode
of ``'w'``. Any existing file is truncated and a new archive is
started. To add files, use the :func:`add()` method.

.. include:: tarfile_add.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. outfile = path(cog.inFile).dirname() / 'tarfile_add.tar'
.. outfile.remove()
.. cog.out(run_script(cog.inFile, 'tarfile_add.py'))
.. }}}

::

	$ python tarfile_add.py
	
	creating archive
	adding README.txt
	closing
	
	Contents:
	README.txt

.. {{{end}}}

Using Alternate Archive Member Names
====================================

It is possible to add a file to an archive using a name other than the
original file name, by constructing a :class:`TarInfo` object with an
alternate *arcname* and passing it to :func:`addfile()`.

.. include:: tarfile_addfile.py
    :literal:
    :start-after: #end_pymotw_header

The archive includes only the changed filename:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tarfile_addfile.py'))
.. }}}

::

	$ python tarfile_addfile.py
	
	creating archive
	adding README.txt as RENAMED.txt
	closing
	
	Contents:
	RENAMED.txt

.. {{{end}}}

Writing Data from Sources Other Than Files
==========================================

Sometimes you want to write data to an archive but the data is not in
a file on the filesystem. Rather than writing the data to a file, then
adding that file to the archive, you can use :func:`addfile()` to add
data from an open file-like handle.

.. include:: tarfile_addfile_string.py
    :literal:
    :start-after: #end_pymotw_header

By first constructing a :class:`TarInfo` object ourselves, we can give
the archive member any name we wish.  After setting the size, we can
write the data to the archive using :func:`addfile()` and passing a
:mod:`StringIO` buffer as a source of the data.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tarfile_addfile_string.py'))
.. }}}

::

	$ python tarfile_addfile_string.py
	
	
	Contents:
	made_up_file.txt
	This is the data to write to the archive.

.. {{{end}}}

Appending to Archives
=====================

In addition to creating new archives, it is possible to append to an
existing file. To open a file to append to it, use mode ``'a'``.

.. include:: tarfile_append.py
    :literal:
    :start-after: #end_pymotw_header

The resulting archive ends up with two members:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tarfile_append.py'))
.. }}}

::

	$ python tarfile_append.py
	
	creating archive
	contents: ['README.txt']
	adding index.rst
	contents: ['README.txt', 'index.rst']

.. {{{end}}}

Working with Compressed Archives
================================

Besides regular tar archive files, the :mod:`tarfile` module can work
with archives compressed via the gzip or bzip2 protocols.  To open a
compressed archive, modify the mode string passed to open() to include
``":gz"`` or ``":bz2"``, depending on the compression method you want
to use.

.. include:: tarfile_compression.py
    :literal:
    :start-after: #end_pymotw_header

When opening an existing archive for reading, you can specify
``"r:*"`` to have :mod:`tarfile` determine the compression method to
use automatically.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tarfile_compression.py'))
.. }}}

::

	$ python tarfile_compression.py
	
	FILENAME                       SIZE      
	README.txt                     75        
	tarfile_compression.tar        10240      ['README.txt']
	tarfile_compression.tar.gz     211        ['README.txt']
	tarfile_compression.tar.bz2    188        ['README.txt']

.. {{{end}}}



.. seealso::

    `tarfile <http://docs.python.org/2.7/library/tarfile.html>`_
        The standard library documentation for this module.
    
    `GNU tar manual <http://www.gnu.org/software/tar/manual/html_node/Standard.html>`_
        Documentation of the tar format, including extensions.

    :mod:`zipfile`
        Similar access for ZIP archives.

    :mod:`gzip`
        GNU zip compression

    :mod:`bz2`
        bzip2 compression
