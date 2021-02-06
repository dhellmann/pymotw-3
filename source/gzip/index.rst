=======================================
 gzip --- Read and Write GNU zip Files
=======================================

.. module:: gzip
    :synopsis: Read and write gzip files

:Purpose: Read and write gzip files.

The ``gzip`` module provides a file-like interface to GNU zip
files, using :mod:`zlib` to compress and uncompress the data.

Writing Compressed Files
========================

The module-level function ``open()`` creates an instance of the
file-like class ``GzipFile``.  The usual methods for writing and
reading bytes are provided.

.. literalinclude:: gzip_write.py
    :caption:
    :start-after: #end_pymotw_header

To write data into a compressed file, open the file with mode
``'wb'``. This example wraps the ``GzipFile`` with a ``TextIOWrapper``
from the :mod:`io` module to encode Unicode text to bytes suitable for
compression.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gzip_write.py'))
.. }}}

.. code-block:: none

	$ python3 gzip_write.py
	
	application/gzip; charset=binary
	example.txt.gz contains 75 bytes

.. {{{end}}}

Different amounts of compression can be used by passing a
``compresslevel`` argument.  Valid values range from 0 to 9, inclusive.
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
	    0      754793  bc74f5a496ea90620ba3c3b75a9fd04f
	    1        9846  afbc2008176f180124632c8fb32d228f
	    2        8267  8852a3f63cc36719fcd87b8b36e2ac6d
	    3        8227  020279969bf10865118d078096ce89c4
	    4        4167  10e5b548bf264bdb785b60053131c1ff
	    5        4167  67079e678ce367d2fdb1163a566d6a03
	    6        4167  b9e93af66738a2d11d5fc1fc5332180a
	    7        4167  59301172dc98a16ad5bcbfeb14f62ab1
	    8        4167  576eb4e9582707acfef37a9b452a1b3a
	    9        4167  a09f9ca030f414fc4c132dfa259f511b

.. {{{end}}}

A ``GzipFile`` instance also includes a ``writelines()`` method
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
endings or Unicode decoding is performed.

.. literalinclude:: gzip_read.py
    :caption:
    :start-after: #end_pymotw_header

This example reads the file written by ``gzip_write.py`` from the
previous section, using a ``TextIOWrapper`` to decode the text after
it is decompressed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gzip_read.py'))
.. }}}

.. code-block:: none

	$ python3 gzip_read.py
	
	Contents of the example file go here.
	

.. {{{end}}}

While reading a file, it is also possible to seek and read only part
of the data.

.. literalinclude:: gzip_seek.py
    :caption:
    :start-after: #end_pymotw_header

The ``seek()`` position is relative to the *uncompressed* data, so
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

The ``GzipFile`` class can be used to wrap other types of data
streams so they can use compression as well.  This is useful when the
data is being transmitted over a socket or an existing
(already open) file handle.  A :mod:`BytesIO` buffer can also be
used.

.. literalinclude:: gzip_BytesIO.py
    :caption:
    :start-after: #end_pymotw_header

One benefit of using ``GzipFile`` over :mod:`zlib` is that it
supports the file API.  However, when re-reading the previously
compressed data, an explicit length is passed to ``read()``.
Leaving the length off resulted in a CRC error, possibly because
``BytesIO`` returned an empty string before reporting EOF.  When
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
	b'1f8b080084d9ef5e02ff0bc94855284ecc4d55c8c9cc4bd551c82f4b2d5248c
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

   * :mod:`io` -- Building-blocks for creating input and output
     pipelines.
