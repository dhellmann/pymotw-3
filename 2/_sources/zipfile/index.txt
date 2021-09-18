===========================================
zipfile -- Read and write ZIP archive files
===========================================

.. module:: zipfile
    :synopsis: Read and write ZIP archive files.

:Purpose: Read and write ZIP archive files.
:Available In: 1.6 and later

The :mod:`zipfile` module can be used to manipulate ZIP archive files.

Limitations
===========

The :mod:`zipfile` module does not support ZIP files with appended
comments, or multi-disk ZIP files. It does support ZIP files larger
than 4 GB that use the ZIP64 extensions.

Testing ZIP Files
=================

The :func:`is_zipfile()` function returns a boolean indicating whether
or not the filename passed as an argument refers to a valid ZIP file.

.. include:: zipfile_is_zipfile.py
    :literal:
    :start-after: #end_pymotw_header

Notice that if the file does not exist at all, :func:`is_zipfile()`
returns False.

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

Reading Meta-data from a ZIP Archive
====================================

Use the :class:`ZipFile` class to work directly with a ZIP archive. It
supports methods for reading data about existing archives as well as
modifying the archives by adding additional files.

To read the names of the files in an existing archive, use
:func:`namelist()`:

.. include:: zipfile_namelist.py
    :literal:
    :start-after: #end_pymotw_header

The return value is a list of strings with the names of the archive
contents:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'zipfile_namelist.py'))
.. }}}

::

	$ python zipfile_namelist.py
	
	['README.txt']

.. {{{end}}}

The list of names is only part of the information available from the
archive, though. To access all of the meta-data about the ZIP
contents, use the :func:`infolist()` or :func:`getinfo()` methods.

.. include:: zipfile_infolist.py
    :literal:
    :start-after: #end_pymotw_header

There are additional fields other than those printed here, but
deciphering the values into anything useful requires careful reading
of the `PKZIP Application Note`_ with the ZIP file specification.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'zipfile_infolist.py'))
.. }}}

::

	$ python zipfile_infolist.py
	
	README.txt
		Comment:	
		Modified:	2007-12-16 10:08:52
		System:		3 (0 = Windows, 3 = Unix)
		ZIP version:	23
		Compressed:	63 bytes
		Uncompressed:	75 bytes
	

.. {{{end}}}

If you know in advance the name of the archive member, you can
retrieve its :class:`ZipInfo` object with :func:`getinfo()`.

.. include:: zipfile_getinfo.py
    :literal:
    :start-after: #end_pymotw_header

If the archive member is not present, :func:`getinfo()` raises a
:ref:`KeyError <exceptions-KeyError>`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'zipfile_getinfo.py'))
.. }}}

::

	$ python zipfile_getinfo.py
	
	README.txt is 75 bytes
	ERROR: Did not find notthere.txt in zip file

.. {{{end}}}

Extracting Archived Files From a ZIP Archive
============================================

To access the data from an archive member, use the :func:`read()`
method, passing the member's name.

.. include:: zipfile_read.py
    :literal:
    :start-after: #end_pymotw_header

The data is automatically decompressed for you, if necessary.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'zipfile_read.py'))
.. }}}

::

	$ python zipfile_read.py
	
	README.txt :
	'The examples for the zipfile module use this file and example.zip as data.\n'
	
	ERROR: Did not find notthere.txt in zip file
	

.. {{{end}}}

Creating New Archives
=====================

To create a new archive, simple instantiate the :class:`ZipFile` with
a mode of ``'w'``.  Any existing file is truncated and a new archive
is started. To add files, use the :func:`write()` method.

.. include:: zipfile_write.py
    :literal:
    :start-after: #end_pymotw_header

By default, the contents of the archive are not compressed:

::

    $ python zipfile_write.py
    creating archive
    adding README.txt
    closing

    README.txt
            Comment:
            Modified:       2007-12-16 10:08:50
            System:         3 (0 = Windows, 3 = Unix)
            ZIP version:    20
            Compressed:     75 bytes
            Uncompressed:   75 bytes

To add compression, the :mod:`zlib` module is required. If :mod:`zlib`
is available, you can set the compression mode for individual files or
for the archive as a whole using ``zipfile.ZIP_DEFLATED``. The default
compression mode is ``zipfile.ZIP_STORED``.

.. include:: zipfile_write_compression.py
    :literal:
    :start-after: #end_pymotw_header

This time the archive member is compressed:

::

    $ python zipfile_write_compression.py 
    creating archive
    adding README.txt with compression mode deflated
    closing

    README.txt
            Comment:
            Modified:       2007-12-16 10:08:50
            System:         3 (0 = Windows, 3 = Unix)
            ZIP version:    20
            Compressed:     63 bytes
            Uncompressed:   75 bytes


Using Alternate Archive Member Names
====================================

It is easy to add a file to an archive using a name other than the original
file name, by passing the arcname argument to :func:`write()`.

.. include:: zipfile_write_arcname.py
    :literal:
    :start-after: #end_pymotw_header

There is no sign of the original filename in the archive:

::

    $ python zipfile_write_arcname.py 
    NOT_README.txt
            Comment:
            Modified:       2007-12-16 10:08:50
            System:         3 (0 = Windows, 3 = Unix)
            ZIP version:    20
            Compressed:     75 bytes
            Uncompressed:   75 bytes

Writing Data from Sources Other Than Files
==========================================

Sometimes it is necessary to write to a ZIP archive using data that
did not come from an existing file. Rather than writing the data to a
file, then adding that file to the ZIP archive, you can use the
:func:`writestr()` method to add a string of bytes to the archive
directly.

.. include:: zipfile_writestr.py
    :literal:
    :start-after: #end_pymotw_header


In this case, I used the compress argument to :class:`ZipFile` to
compress the data, since :func:`writestr()` does not take compress as
an argument.

::

    $ python zipfile_writestr.py
    from_string.txt
            Comment:
            Modified:       2007-12-16 11:38:14
            System:         3 (0 = Windows, 3 = Unix)
            ZIP version:    20
            Compressed:     62 bytes
            Uncompressed:   68 bytes

This data did not exist in a file before being added to the ZIP file

Writing with a ZipInfo Instance
===============================

Normally, the modification date is computed for you when you add a
file or string to the archive. When using :func:`writestr()`, you can
also pass a :class:`ZipInfo` instance to define the modification date
and other meta-data yourself.

.. include:: zipfile_writestr_zipinfo.py
    :literal:
    :start-after: #end_pymotw_header

In this example, I set the modified time to the current time, compress the
data, provide a false value for ``create_system``, and add a comment.

::

    $ python zipfile_writestr_zipinfo.py
    from_string.txt
            Comment:        Remarks go here
            Modified:       2007-12-16 11:44:14
            System:         0 (0 = Windows, 3 = Unix)
            ZIP version:    20
            Compressed:     62 bytes
            Uncompressed:   68 bytes

Appending to Files
==================

In addition to creating new archives, it is possible to append to an
existing archive or add an archive at the end of an existing file
(such as a .exe file for a self-extracting archive). To open a file to
append to it, use mode ``'a'``.

.. include:: zipfile_append.py
    :literal:
    :start-after: #end_pymotw_header

The resulting archive ends up with 2 members:

::

    $ python zipfile_append.py 
    creating archive

    README.txt
            Comment:
            Modified:       2007-12-16 10:08:50
            System:         3 (0 = Windows, 3 = Unix)
            ZIP version:    20
            Compressed:     75 bytes
            Uncompressed:   75 bytes

    appending to the archive

    README.txt
            Comment:
            Modified:       2007-12-16 10:08:50
            System:         3 (0 = Windows, 3 = Unix)
            ZIP version:    20
            Compressed:     75 bytes
            Uncompressed:   75 bytes

    README2.txt
            Comment:
            Modified:       2007-12-16 10:08:50
            System:         3 (0 = Windows, 3 = Unix)
            ZIP version:    20
            Compressed:     75 bytes
            Uncompressed:   75 bytes

Python ZIP Archives
===================

Since version 2.3 Python has had the ability to :ref:`import modules
from inside ZIP archives <zipimport-ref>` if those archives appear in
:ref:`sys.path <sys-path>`. The :class:`PyZipFile` class can be used
to construct a module suitable for use in this way. When you use the
extra method :func:`writepy()`, :class:`PyZipFile` scans a directory
for ``.py`` files and adds the corresponding ``.pyo`` or ``.pyc`` file
to the archive. If neither compiled form exists, a ``.pyc`` file is
created and added.

.. include:: zipfile_pyzipfile.py
    :literal:
    :start-after: #end_pymotw_header

With the debug attribute of the :class:`PyZipFile` set to 3, verbose
debugging is enabled and you can observe as it compiles each ``.py``
file it finds.

::

    $ python zipfile_pyzipfile.py
    Adding python files
    Adding package in . as .
    Compiling ./__init__.py
    Adding ./__init__.pyc
    Compiling ./zipfile_append.py
    Adding ./zipfile_append.pyc
    Compiling ./zipfile_getinfo.py
    Adding ./zipfile_getinfo.pyc
    Compiling ./zipfile_infolist.py
    Adding ./zipfile_infolist.pyc
    Compiling ./zipfile_is_zipfile.py
    Adding ./zipfile_is_zipfile.pyc
    Compiling ./zipfile_namelist.py
    Adding ./zipfile_namelist.pyc
    Compiling ./zipfile_printdir.py
    Adding ./zipfile_printdir.pyc
    Compiling ./zipfile_pyzipfile.py
    Adding ./zipfile_pyzipfile.pyc
    Compiling ./zipfile_read.py
    Adding ./zipfile_read.pyc
    Compiling ./zipfile_write.py
    Adding ./zipfile_write.pyc
    Compiling ./zipfile_write_arcname.py
    Adding ./zipfile_write_arcname.pyc
    Compiling ./zipfile_write_compression.py
    Adding ./zipfile_write_compression.pyc
    Compiling ./zipfile_writestr.py
    Adding ./zipfile_writestr.pyc
    Compiling ./zipfile_writestr_zipinfo.py
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
    
    Imported from: zipfile_pyzipfile.zip/zipfile_pyzipfile.pyc

.. seealso::

    `zipfile <http://docs.python.org/2.7/library/zipfile.html>`_
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
