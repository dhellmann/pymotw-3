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

.. code-block:: none

	$ python3 gzip_write.py
	
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

.. code-block:: none

	$ python3 gzip_compresslevel.py
	
	Level  Size        Checksum
	-----  ----------  ---------------------------------
	data       754688  e4c0f9433723971563f08a458715119c
	    1        9839  5aa0436a5f6d7c4a334ff52d6530b664
	    2        8260  dcebb0d734880f83888e40579d3fd4ab
	    3        8221  b3f36797921e51f22c9fb621d28134f3
	    4        4160  125ea38d71fa55f16bbec8dd8a5e9621
	    5        4160  e7a72a8554e08621809a81f5e615201e
	    6        4160  29dbf8a6ccf3ec4ba180bd22fdd72c7f
	    7        4160  87c5b410583eac8ec6d8d4f62e28c0cb
	    8        4160  ad8bd69395a75eaf2bbbfcf135cb699a
	    9        4160  0d55d6ea1881244258861f1d91987646

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

.. code-block:: none

	$ python3 gzip_writelines.py
	
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

.. code-block:: none

	$ python3 gzip_read.py
	
	b'Contents of the example file go here.\n'

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

.. code-block:: none

	$ python3 gzip_seek.py
	
	Entire file:
	b'Contents of the example file go here.\n'
	Starting at position 5 for 10 bytes:
	b'nts of the'
	
	True

.. {{{end}}}


Working with Streams
====================

The :class:`GzipFile` class can be used to wrap other types of data
streams so they can use compression as well.  This is useful when the
data is being transmitted over a socket or an existing
(already open) file handle.  A :mod:`BytesIO` buffer can also be
used.

.. literalinclude:: gzip_BytesIO.py
    :caption:
    :start-after: #end_pymotw_header

One benefit of using :class:`GzipFile` over :mod:`zlib` is that it
supports the file API.  However, when re-reading the previously
compressed data, an explicit length is passed to :func:`read`.
Leaving the length off resulted in a CRC error, possibly because
:class:`BytesIO` returned an empty string before reporting EOF.  When
working with streams of compressed data, either prefix the data with
an integer representing the actual amount of data to be read or use
the incremental decompression API in :mod:`zlib`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gzip_BytesIO.py', break_lines_at=65))
.. }}}

.. code-block:: none

	$ python3 gzip_BytesIO.py
	
	UNCOMPRESSED: 300
	b'The same line, over and over.\nThe same line, over and over.\nT
	he same line, over and over.\nThe same line, over and over.\nThe 
	same line, over and over.\nThe same line, over and over.\nThe sam
	e line, over and over.\nThe same line, over and over.\nThe same l
	ine, over and over.\nThe same line, over and over.\n'
	COMPRESSED: 51
	b'1f8b0800d867a75702ff0bc94855284ecc4d55c8c9cc4bd551c82f4b2d5248c
	c4b0133f4b8424665916401d3e717802c010000'
	
	REREAD: 300
	b'The same line, over and over.\nThe same line, over and over.\nT
	he same line, over and over.\nThe same line, over and over.\nThe 
	same line, over and over.\nThe same line, over and over.\nThe sam
	e line, over and over.\nThe same line, over and over.\nThe same l
	ine, over and over.\nThe same line, over and over.\n'

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
