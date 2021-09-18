====================================
gzip -- Read and write GNU zip files
====================================

.. module:: gzip
    :synopsis: Read and write gzip files

:Purpose: Read and write gzip files.
:Available In: 1.5.2 and later

The gzip module provides a file-like interface to GNU zip files, using
:mod:`zlib` to compress and uncompress the data.

Writing Compressed Files
========================

The module-level function ``open()`` creates an instance of the
file-like class GzipFile.  The usual methods for writing and reading
data are provided.  To write data into a compressed file, open the
file with mode ``'w'``.

.. include:: gzip_write.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gzip_write.py'))
.. }}}

::

	$ python gzip_write.py
	
	application/x-gzip; charset=binary
	example.txt.gz contains 68 bytes of compressed data

.. {{{end}}}

Different amounts of compression can be used by passing a
*compresslevel* argument.  Valid values range from 1 to 9, inclusive.
Lower values are faster and result in less compression.  Higher values
are slower and compress more, up to a point.

.. include:: gzip_compresslevel.py
    :literal:
    :start-after: #end_pymotw_header

The center column of numbers in the output of the script is the size
in bytes of the files produced.  As you see, for this input data, the
higher compression values do not necessarily pay off in decreased
storage space.  Results will vary, depending on the input data.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gzip_compresslevel.py'))
.. }}}

::

	$ python gzip_compresslevel.py
	
	Level  Size        Checksum
	-----  ----------  ---------------------------------
	data       754688  e4c0f9433723971563f08a458715119c
	    1        9839  9a7d983796832f354f8ed980d8f9490b
	    2        8260  bfc400197e9fc1ee6d8fcf23055362b2
	    3        8221  63a50795cf7e203339236233f473e23b
	    4        4160  c3d7f661a98895a20e22b1c97e02a02a
	    5        4160  800a904ede7007dacf7e6313d044a9c9
	    6        4160  8904134bbd7e2f4cc87dbda39093835b
	    7        4160  724bd069062b2adb0739d3ab427b8729
	    8        4160  61504720d0e524d2b32689a3409d978d
	    9        4160  538734caa5e4558c7da7c19ca2620573

.. {{{end}}}


A GzipFile instance also includes a ``writelines()`` method that can
be used to write a sequence of strings.

.. include:: gzip_writelines.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gzip_writelines.py'))
.. }}}

::

	$ python gzip_writelines.py
	
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.

.. {{{end}}}


Reading Compressed Data
=======================

To read data back from previously compressed files, simply open the
file with mode ``'r'``.

.. include:: gzip_read.py
    :literal:
    :start-after: #end_pymotw_header

This example reads  the file  written by  ``gzip_write.py``  from the
previous section.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gzip_read.py'))
.. }}}

::

	$ python gzip_read.py
	
	Contents of the example file go here.
	

.. {{{end}}}
    
While reading a file, it is also possible to seek and read only part
of the data.

.. include:: gzip_seek.py
    :literal:
    :start-after: #end_pymotw_header

The ``seek()`` position is relative to the *uncompressed* data, so the
caller does not even need to know that the data file is compressed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gzip_seek.py'))
.. }}}

::

	$ python gzip_seek.py
	
	Entire file:
	Contents of the example file go here.
	
	Starting at position 5 for 10 bytes:
	nts of the
	
	True

.. {{{end}}}


Working with Streams
====================

When working with a data stream instead of a file, use the GzipFile
class directly to compress or uncompress it.  This is useful when the
data is being transmitted over a socket or from read an existing
(already open) file handle.  A StringIO buffer can also be used.

.. include:: gzip_StringIO.py
    :literal:
    :start-after: #end_pymotw_header

.. note::

    When re-reading the previously compressed data, I pass an explicit length to
    ``read()``.  Leaving the length off resulted in a CRC error, possibly because
    StringIO returned an empty string before reporting EOF.  If you are
    working with streams of compressed data, you may want to prefix the data with
    an integer representing the actual amount of data to be read.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gzip_StringIO.py'))
.. }}}

::

	$ python gzip_StringIO.py
	
	UNCOMPRESSED: 300
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.
	
	COMPRESSED: 51
	1f8b08009706265102ff0bc94855284ecc4d55c8c9cc4bd551c82f4b2d5248cc4b0133f4b8424665916401d3e717802c010000
	
	RE-READ: 300
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.
	The same line, over and over.
	

.. {{{end}}}


.. seealso::

    `gzip <http://docs.python.org/2.7/library/gzip.html>`_
        The standard library documentation for this module.

    :mod:`zlib`
        The zlib module is a lower-level interface to gzip compression.

    :mod:`zipfile`
        The zipfile module gives access to ZIP archives.

    :mod:`bz2`
        The bz2 module uses the bzip2 compression format.

    :mod:`tarfile`
        The tarfile module includes built-in support for reading compressed tar archives.
