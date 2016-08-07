=======================================
 gzip --- Read and Write GNU zip Files
=======================================

.. module:: gzip
    :synopsis: Read and write gzip files

:Purpose: Read and write gzip files.

The :mod:`gzip` module provides a file-like interface to GNU zip
files, using :mod:`zlib` to compress and uncompress the data.

Writing Compressed Files
========================

The module-level function :func:`open` creates an instance of the
file-like class :class:`GzipFile`.  The usual methods for writing and
reading data are provided.

.. literalinclude:: gzip_write.py
    :caption:
    :start-after: #end_pymotw_header

To write data into a compressed file, open the file with mode ``'w'``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gzip_write.py'))
.. }}}

::

	$ python gzip_write.py

	application/x-gzip; charset=binary
	example.txt.gz contains 68 bytes

.. {{{end}}}

Different amounts of compression can be used by passing a
*compresslevel* argument.  Valid values range from 1 to 9, inclusive.
Lower values are faster and result in less compression.  Higher values
are slower and compress more, up to a point.

.. literalinclude:: gzip_compresslevel.py
    :caption:
    :start-after: #end_pymotw_header

The center column of numbers in the output shows the size in bytes of
the files produced by compressing the input.  For this input data, the
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
	    1        9839  3fbd996cd4d63acc70047fb62646f2ba
	    2        8260  427bf6183d4518bcd05611d4f114a07c
	    3        8221  078331b777a11572583e3fdaa120b845
	    4        4160  f73c478ffcba30bfe0b1d08d0f597394
	    5        4160  022d920880e24c1895219a31105a89c8
	    6        4160  45ba520d6af45e279a56bb9c67294b82
	    7        4160  9a834b8a2c649d4b8d509cb12cc580e2
	    8        4160  c1aafc7d7d58cba4ef21dfce6fd1f443
	    9        4160  78039211f5777f9f34cf770c2eaafc6d

.. {{{end}}}

A :class:`GzipFile` instance also includes a :func:`writelines` method
that can be used to write a sequence of strings.

.. literalinclude:: gzip_writelines.py
    :caption:
    :start-after: #end_pymotw_header

As with a regular file, the input lines need to include a newline
character.

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

To read data back from previously compressed files, open the file with
binary read mode (``'rb'``) so no text-based translation of line
endings is performed.

.. literalinclude:: gzip_read.py
    :caption:
    :start-after: #end_pymotw_header

This example reads the file written by ``gzip_write.py`` from the
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

.. literalinclude:: gzip_seek.py
    :caption:
    :start-after: #end_pymotw_header

The :func:`seek` position is relative to the *uncompressed* data, so
the caller does not need to know that the data file is compressed.

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

The :class:`GzipFile` class can be used to wrap other types of data
streams so they can use compression as well.  This is useful when the
data is being transmitted over a socket or an existing
(already open) file handle.  A :mod:`StringIO` buffer can also be
used.

.. literalinclude:: gzip_StringIO.py
    :caption:
    :start-after: #end_pymotw_header

One benefit of using :class:`GzipFile` over :mod:`zlib` is that it
supports the file API.  However, when re-reading the previously
compressed data, an explicit length is passed to :func:`read`.
Leaving the length off resulted in a CRC error, possibly because
:class:`StringIO` returned an empty string before reporting EOF.  When
working with streams of compressed data, either prefix the data with
an integer representing the actual amount of data to be read or use
the incremental decompression API in :mod:`zlib`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gzip_StringIO.py', break_lines_at=65))
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
	1f8b08001f96f24c02ff0bc94855284ecc4d55c8c9cc4bd551c82f4b2d5248cc4
	b0133f4b8424665916401d3e717802c010000
	
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

   * :pydoc:`gzip`

   * :mod:`zlib` -- The ``zlib`` module is a lower-level interface to
     gzip compression.

   * :mod:`zipfile` -- The ``zipfile`` module gives access to ZIP
     archives.

   * :mod:`bz2` -- The ``bz2`` module uses the bzip2 compression
     format.

   * :mod:`tarfile` -- The ``tarfile`` module includes built-in
     support for reading compressed tar archives.
