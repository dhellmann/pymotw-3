===============================
 zipfile -- ZIP Archive Access
===============================

.. module:: zipfile
    :synopsis: ZIP archive access

:Purpose: Read and write ZIP archive files.
:Python Version: 1.6 and later

The :mod:`zipfile` module can be used to manipulate ZIP archive files,
the format popularized by the PC program PKZIP.

Testing ZIP Files
=================

The :func:`is_zipfile()` function returns a boolean indicating whether
or not the filename passed as an argument refers to a valid ZIP
archive.

.. include:: zipfile_is_zipfile.py
    :literal:
    :start-after: #end_pymotw_header

If the file does not exist at all, :func:`is_zipfile()` returns
:const:`False`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'zipfile_is_zipfile.py'))
.. }}}

::

	$ python zipfile_is_zipfile.py

	     README.txt  False
	    example.zip  True
	bad_example.zip  False
	   notthere.zip  False

.. {{{end}}}

Reading Metadata from an Archive
================================

Use the :class:`ZipFile` class to work directly with a ZIP archive. It
supports methods for reading data about existing archives as well as
modifying the archives by adding additional files.  

.. include:: zipfile_namelist.py
    :literal:
    :start-after: #end_pymotw_header

The :func:`namelist` method returns the names of the files in an
existing archive.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'zipfile_namelist.py'))
.. }}}

::

	$ python zipfile_namelist.py

	['README.txt']

.. {{{end}}}

The list of names is only part of the information available from the
archive, though. To access all of the metadata about the ZIP
contents, use the :func:`infolist()` or :func:`getinfo()` methods.

.. include:: zipfile_infolist.py
    :literal:
    :start-after: #end_pymotw_header

There are additional fields other than those printed here, but
deciphering the values into anything useful requires careful reading
of the *PKZIP Application Note* with the ZIP file specification.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'zipfile_infolist.py'))
.. }}}

::

	$ python zipfile_infolist.py

	README.txt
		Comment     : 
		Modified    : 2010-11-15 06:48:02
		System      : Unix
		ZIP version : 30
		Compressed  : 65 bytes
		Uncompressed: 76 bytes
	

.. {{{end}}}

If the name of the archive member is known in advance, its
:class:`ZipInfo` object can be retrieved directly with
:func:`getinfo()`.

.. include:: zipfile_getinfo.py
    :literal:
    :start-after: #end_pymotw_header

If the archive member is not present, :func:`getinfo()` raises a
:class:`KeyError`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'zipfile_getinfo.py'))
.. }}}

::

	$ python zipfile_getinfo.py

	README.txt is 76 bytes
	ERROR: Did not find notthere.txt in zip file

.. {{{end}}}

Extracting Archived Files From an Archive
=========================================

To access the data from an archive member, use the :func:`read()`
method, passing the member's name.

.. include:: zipfile_read.py
    :literal:
    :start-after: #end_pymotw_header

The data is automatically decompressed, if necessary.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'zipfile_read.py'))
.. }}}

::

	$ python zipfile_read.py

	README.txt :
	The examples for the zipfile module use 
	this file and example.zip as data.
	
	
	ERROR: Did not find notthere.txt in zip file
	

.. {{{end}}}

Creating New Archives
=====================

To create a new archive, instantiate the :class:`ZipFile` with
a mode of ``'w'``.  Any existing file is truncated and a new archive
is started. To add files, use the :func:`write()` method.

.. include:: zipfile_write.py
    :literal:
    :start-after: #end_pymotw_header

By default, the contents of the archive are not compressed.

.. {{{cog
.. (path(cog.inFile).dirname() / 'zipfile_write.zip').unlink()
.. cog.out(run_script(cog.inFile, 'zipfile_write.py'))
.. }}}

::

	$ python zipfile_write.py

	creating archive
	adding README.txt
	
	README.txt
		Comment     : 
		Modified    : 2010-11-15 06:48:00
		System      : Unix
		ZIP version : 20
		Compressed  : 76 bytes
		Uncompressed: 76 bytes
	

.. {{{end}}}


To add compression, the :mod:`zlib` module is required. If :mod:`zlib`
is available, the compression mode for individual files or for the
archive as a whole can be set using :const:`zipfile.ZIP_DEFLATED`. The
default compression mode is :const:`zipfile.ZIP_STORED`, which adds
the input data to the archive without compressing it.

.. include:: zipfile_write_compression.py
    :literal:
    :start-after: #end_pymotw_header

This time, the archive member is compressed.

.. {{{cog
.. (path(cog.inFile).dirname() / 'zipfile_write_compression.zip').unlink()
.. cog.out(run_script(cog.inFile, 'zipfile_write_compression.py'))
.. }}}

::

	$ python zipfile_write_compression.py

	creating archive
	adding README.txt with compression mode deflated
	
	README.txt
		Comment     : 
		Modified    : 2010-11-15 06:48:00
		System      : Unix
		ZIP version : 20
		Compressed  : 65 bytes
		Uncompressed: 76 bytes
	

.. {{{end}}}


Using Alternate Archive Member Names
====================================

Pass an *arcname* value to :func:`write()` to add a file to an archive
using a name other than the original filename.

.. include:: zipfile_write_arcname.py
    :literal:
    :start-after: #end_pymotw_header

There is no sign of the original filename in the archive.

.. {{{cog
.. (path(cog.inFile).dirname() / 'zipfile_write_arcname.zip').unlink()
.. cog.out(run_script(cog.inFile, 'zipfile_write_arcname.py'))
.. }}}

::

	$ python zipfile_write_arcname.py

	NOT_README.txt
		Comment     : 
		Modified    : 2010-11-15 06:48:00
		System      : Unix
		ZIP version : 20
		Compressed  : 76 bytes
		Uncompressed: 76 bytes
	

.. {{{end}}}


Writing Data from Sources Other Than Files
==========================================

Sometimes it is necessary to write to a ZIP archive using data that
did not come from an existing file. Rather than writing the data to a
file, then adding that file to the ZIP archive, use the
:func:`writestr()` method to add a string of bytes to the archive
directly.

.. include:: zipfile_writestr.py
    :literal:
    :start-after: #end_pymotw_header


In this case, the *compress_type* argument to :class:`ZipFile` was
used to compress the data, since :func:`writestr()` does not take
an argument to specify the compression.

.. {{{cog
.. (path(cog.inFile).dirname() / 'zipfile_writestr.zip').unlink()
.. cog.out(run_script(cog.inFile, 'zipfile_writestr.py'))
.. }}}

::

	$ python zipfile_writestr.py

	from_string.txt
		Comment     : 
		Modified    : 2010-11-28 13:48:46
		System      : Unix
		ZIP version : 20
		Compressed  : 36 bytes
		Uncompressed: 34 bytes
	
	This data did not exist in a file.

.. {{{end}}}

Writing with a ZipInfo Instance
===============================

Normally, the modification date is computed when a file or string is
added to the archive.  A :class:`ZipInfo` instance can be passed to
:func:`writestr` to define the modification date and other metadata.

.. include:: zipfile_writestr_zipinfo.py
    :literal:
    :start-after: #end_pymotw_header

In this example, the modified time is set to the current time, the
data is compressed, and false value for *create_system* is used.  A
simple comment is also associated with the new file.

.. {{{cog
.. (path(cog.inFile).dirname() / 'zipfile_writestr_zipinfo.zip').unlink()
.. cog.out(run_script(cog.inFile, 'zipfile_writestr_zipinfo.py'))
.. }}}

::

	$ python zipfile_writestr_zipinfo.py

	from_string.txt
		Comment     : Remarks go here
		Modified    : 2010-11-28 13:48:46
		System      : Windows
		ZIP version : 20
		Compressed  : 36 bytes
		Uncompressed: 34 bytes
	

.. {{{end}}}

Appending to Files
==================

In addition to creating new archives, it is possible to append to an
existing archive or add an archive at the end of an existing file
(such as a ``.exe`` file for a self-extracting archive). To open a
file to append to it, use mode ``'a'``.

.. include:: zipfile_append.py
    :literal:
    :start-after: #end_pymotw_header

The resulting archive contains two members:

.. {{{cog
.. (path(cog.inFile).dirname() / 'zipfile_append.zip').unlink()
.. cog.out(run_script(cog.inFile, 'zipfile_append.py'))
.. }}}

::

	$ python zipfile_append.py

	creating archive
	
	README.txt
		Comment     : 
		Modified    : 2010-11-15 06:48:00
		System      : Unix
		ZIP version : 20
		Compressed  : 76 bytes
		Uncompressed: 76 bytes
	
	appending to the archive
	
	README.txt
		Comment     : 
		Modified    : 2010-11-15 06:48:00
		System      : Unix
		ZIP version : 20
		Compressed  : 76 bytes
		Uncompressed: 76 bytes
	
	README2.txt
		Comment     : 
		Modified    : 2010-11-15 06:48:00
		System      : Unix
		ZIP version : 20
		Compressed  : 76 bytes
		Uncompressed: 76 bytes
	

.. {{{end}}}

Python ZIP Archives
===================

Python can import modules from inside ZIP archives using
:mod:`zipimport`, if those archives appear in :data:`sys.path`. The
:class:`PyZipFile` class can be used to construct a module suitable
for use in this way. The extra method :func:`writepy()` tells
:class:`PyZipFile` to scan a directory for ``.py`` files and add the
corresponding ``.pyo`` or ``.pyc`` file to the archive. If neither
compiled form exists, a ``.pyc`` file is created and added.

.. include:: zipfile_pyzipfile.py
    :literal:
    :start-after: #end_pymotw_header

With the debug attribute of the :class:`PyZipFile` set to ``3``,
verbose debugging is enabled and output is produced as it compiles
each ``.py`` file it finds.

.. {{{cog
.. (path(cog.inFile).dirname() / 'zipfile_pyzipfile.zip').unlink()
.. cog.out(run_script(cog.inFile, 'zipfile_pyzipfile.py'))
.. }}}

::

	$ python zipfile_pyzipfile.py

	Adding python files
	Adding package in . as .
	Adding ./__init__.pyc
	Adding ./zipfile_append.pyc
	Adding ./zipfile_getinfo.pyc
	Adding ./zipfile_infolist.pyc
	Compiling ./zipfile_is_zipfile.py
	Adding ./zipfile_is_zipfile.pyc
	Adding ./zipfile_namelist.pyc
	Adding ./zipfile_printdir.pyc
	Adding ./zipfile_pyzipfile.pyc
	Adding ./zipfile_read.pyc
	Adding ./zipfile_write.pyc
	Adding ./zipfile_write_arcname.pyc
	Adding ./zipfile_write_compression.pyc
	Adding ./zipfile_writestr.pyc
	Adding ./zipfile_writestr_zipinfo.pyc
	__init__.pyc
	zipfile_append.pyc
	zipfile_getinfo.pyc
	zipfile_infolist.pyc
	zipfile_is_zipfile.pyc
	zipfile_namelist.pyc
	zipfile_printdir.pyc
	zipfile_pyzipfile.pyc
	zipfile_read.pyc
	zipfile_write.pyc
	zipfile_write_arcname.pyc
	zipfile_write_compression.pyc
	zipfile_writestr.pyc
	zipfile_writestr_zipinfo.pyc
	
	Imported from: pyzipfile.zip/zipfile_pyzipfile.pyc

.. {{{end}}}

Limitations
===========

The :mod:`zipfile` module does not support ZIP files with appended
comments, or multi-disk archives. It does support ZIP files larger
than 4 GB that use the ZIP64 extensions.

.. seealso::

    `zipfile <http://docs.python.org/library/zipfile.html>`_
        The standard library documentation for this module.

    :mod:`zlib`
        ZIP compression library

    :mod:`tarfile`
        Read and write tar archives

    :mod:`zipimport`
        Import Python modules from ZIP archive.

    `PKZIP Application Note`_
        Official specification for the ZIP archive format.

.. _PKZIP Application Note: http://www.pkware.com/documents/casestudies/APPNOTE.TXT
