===============================
 zlib --- GNU zlib Compression
===============================

.. module:: zlib
    :synopsis: GNU zlib compression library

:Purpose: Low-level access to GNU zlib compression library

The :mod:`zlib` module provides a lower-level interface to many of the
functions in the :mod:`zlib` compression library from the GNU project.

Working with Data in Memory
===========================

The simplest way to work with :mod:`zlib` requires holding all of the
data to be compressed or decompressed in memory.

.. literalinclude:: zlib_memory.py
    :caption:
    :start-after: #end_pymotw_header

The :func:`compress` and :func:`decompress` functions both take a
byte sequence argument and return a byte sequence.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'zlib_memory.py'))
.. }}}

.. code-block:: none

	$ python3 zlib_memory.py
	
	Original     : 26 b'This is the original text.'
	Compressed   : 32 b'789c0bc9c82c5600a2928c5485fca2ccf4ccbcc41c85
	92d48a123d007f2f097e'
	Decompressed : 26 b'This is the original text.'

.. {{{end}}}

The previous example demonstrates that the compressed version of small
amounts of data can be larger than the uncompressed version.  While
the actual results depend on the input data, it is interesting to
observe the compression overhead for small data sets

.. literalinclude:: zlib_lengths.py
    :caption:
    :start-after: #end_pymotw_header

The ``*`` in the output highlight the lines where the compressed data
takes up more memory than the uncompressed version.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'zlib_lengths.py'))
.. }}}

.. code-block:: none

	$ python3 zlib_lengths.py
	
	      len(data)  len(compressed)
	---------------  ---------------
	              0                8 *
	             26               32 *
	             52               35 
	             78               35 
	            104               36 

.. {{{end}}}

:mod:`zlib` supports several different compression levels, allowing a
balance between computational cost and the amount of space
reduction. The default compression level,
:data:`zlib.Z_DEFAULT_COMPRESSION` is ``-1`` and corresponds to a
hard-coded value that compromises between performance and compression
outcome. This currently corresponds to level ``6``.

.. literalinclude:: zlib_compresslevel.py
   :caption:
   :start-after: #end_pymotw_header

A level of 0 means no compression at all. A level of 9 requires the
most computation and produces the smallest output. As this example
shows, the same size reduction may be achieved with multiple
compression levels for a given input.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'zlib_compresslevel.py'))
.. }}}

.. code-block:: none

	$ python3 zlib_compresslevel.py
	
	Level   Size
	-----   ----
	    0  20491
	    1    172
	    2    172
	    3    172
	    4     98
	    5     98
	    6     98
	    7     98
	    8     98
	    9     98

.. {{{end}}}


Incremental Compression and Decompression
=========================================

The in-memory approach has drawbacks that make it impractical for
real-world use cases, primarily that the system needs enough memory to
hold both the uncompressed and compressed versions resident in memory
at the same time.  The alternative is to use :class:`Compress` and
:class:`Decompress` objects to manipulate data incrementally, so that
the entire data set does not have to fit into memory.

.. literalinclude:: zlib_incremental.py
   :caption:
   :start-after: #end_pymotw_header

This example reads small blocks of data from a plain text file and
passes it to :func:`compress`.  The compressor maintains an internal
buffer of compressed data.  Since the compression algorithm depends on
checksums and minimum block sizes, the compressor may not be ready to
return data each time it receives more input.  If it does not have an
entire compressed block ready, it returns an empty byte string.  When
all of the data is fed in, the :func:`flush` method forces the
compressor to close the final block and return the rest of the
compressed data.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'zlib_incremental.py'))
.. }}}

.. code-block:: none

	$ python3 zlib_incremental.py
	
	Compressed: b'7801'
	buffering...
	buffering...
	buffering...
	buffering...
	buffering...
	Flushed: b'55904b6ac4400c44f73e451da0f129b20c2110c85e696b8c40dde
	dd167ce1f7915025a087daa9ef4be8c07e4f21c38962e834b800647435fd3b90
	747b2810eb9c4bbcc13ac123bded6e4bef1c91ee40d3c6580e3ff52aad2e8cb2
	eb6062dad74a89ca904cbb0f2545e0db4b1f2e01955b8c511cb2ac08967d228a
	f1447c8ec72e40c4c714116e60cdef171bb6c0feaa255dff1c507c2c4439ec96
	05b7e0ba9fc54bae39355cb89fd6ebe5841d673c7b7bc68a46f575a312eebd22
	0d4b32441bdc1b36ebf0aedef3d57ea4b26dd986dd39af57dfb05d32279de'

.. {{{end}}}

Mixed Content Streams
=====================

The :class:`Decompress` class returned by :func:`decompressobj` can
also be used in situations where compressed and uncompressed data is
mixed together.

.. literalinclude:: zlib_mixed.py
    :caption:
    :start-after: #end_pymotw_header

After decompressing all of the data, the *unused_data* attribute
contains any data not used.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'zlib_mixed.py'))
.. }}}

.. code-block:: none

	$ python3 zlib_mixed.py
	
	Decompressed matches lorem: True
	Unused data matches lorem : True

.. {{{end}}}

Checksums
=========

In addition to compression and decompression functions, :mod:`zlib`
includes two functions for computing checksums of data,
:func:`adler32` and :func:`crc32`.  Neither checksum is
cryptographically secure, and they are only intended for use for data
integrity verification.

.. literalinclude:: zlib_checksums.py
    :caption:
    :start-after: #end_pymotw_header

Both functions take the same arguments, a byte string containing the
data and an optional value to be used as a starting point for the
checksum.  They return a 32-bit signed integer value which can also be
passed back on subsequent calls as a new starting point argument to
produce a *running* checksum.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'zlib_checksums.py'))
.. }}}

.. code-block:: none

	$ python3 zlib_checksums.py
	
	Adler32:   3542251998
	       :    669447099
	CRC-32 :   3038370516
	       :   2870078631

.. {{{end}}}

Compressing Network Data
========================

The server in the next listing uses the stream compressor to respond
to requests consisting of filenames by writing a compressed version of
the file to the socket used to communicate with the client.

.. literalinclude:: zlib_server.py
   :caption:
   :start-after: #end_pymotw_header

It has some artificial chunking in place to illustrate the buffering
behavior that happens when the data passed to :func:`compress` or
:func:`decompress` does not result in a complete block of compressed
or uncompressed output.

The client connects to the socket and requests a file.  Then it loops,
receiving blocks of compressed data.  Since a block may not contain
enough information to decompress it entirely, the remainder of any
data received earlier is combined with the new data and passed to the
decompressor.  As the data is decompressed, it is appended to a
buffer, which is compared against the file contents at the end of the
processing loop.

.. warning::

    This server has obvious security implications.  Do not run it on a
    system on the open Internet or in any environment where security
    might be an issue.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'zlib_server.py'))
.. }}}

.. code-block:: none

	$ python3 zlib_server.py
	
	Client: Contacting server on 127.0.0.1:53658
	Client: sending filename: 'lorem.txt'
	Server: client asked for: 'lorem.txt'
	Server: RAW b'Lorem ipsum dolor sit amet, consectetuer adipiscin
	g elit. Donec\n'
	Server: SENDING b'7801'
	Server: RAW b'egestas, enim et consectetuer ullamcorper, lectus 
	ligula rutrum '
	Server: BUFFERING
	Server: RAW b'leo, a\nelementum elit tortor eu quam. Duis tincid
	unt nisi ut ant'
	Server: BUFFERING
	Server: RAW b'e. Nulla\nfacilisi. Sed tristique eros eu libero. 
	Pellentesque ve'
	Server: BUFFERING
	Server: RAW b'l arcu. Vivamus\npurus orci, iaculis ac, suscipit 
	sit amet, pulvi'
	Client: READ b'7801'
	Client: BUFFERING
	Server: BUFFERING
	Server: RAW b'nar eu,\nlacus.\n'
	Server: BUFFERING
	Server: FLUSHING b'55904b6ac4400c44f73e451da0f129b20c2110c85e696
	b8c40ddedd167ce1f7915025a087daa9ef4be8c07e4f21c38962e834b8006474
	35fd3b90747b2810eb9'
	Server: FLUSHING b'c4bbcc13ac123bded6e4bef1c91ee40d3c6580e3ff52a
	ad2e8cb2eb6062dad74a89ca904cbb0f2545e0db4b1f2e01955b8c511cb2ac08
	967d228af1447c8ec72'
	Client: READ b'55904b6ac4400c44f73e451da0f129b20c2110c85e696b8c4
	0ddedd167ce1f7915025a087daa9ef4be8c07e4f21c38962e834b800647435fd
	3b90747b2810eb9'
	Server: FLUSHING b'e40c4c714116e60cdef171bb6c0feaa255dff1c507c2c
	4439ec9605b7e0ba9fc54bae39355cb89fd6ebe5841d673c7b7bc68a46f575a3
	12eebd220d4b32441bd'
	Client: DECOMPRESSED b'Lorem ipsum dolor sit amet, consectetuer 
	adi'
	Client: READ b'c4bbcc13ac123bded6e4bef1c91ee40d3c6580e3ff52aad2e
	8cb2eb6062dad74a89ca904cbb0f2545e0db4b1f2e01955b8c511cb2ac08967d
	228af1447c8ec72'
	Client: DECOMPRESSED b'piscing elit. Donec\negestas, enim et con
	sectetuer ullamcorper, lectus ligula rutrum leo, a\nelementum el
	it tortor eu quam. Duis tinci'
	Client: READ b'e40c4c714116e60cdef171bb6c0feaa255dff1c507c2c4439
	ec9605b7e0ba9fc54bae39355cb89fd6ebe5841d673c7b7bc68a46f575a312ee
	bd220d4b32441bd'
	Client: DECOMPRESSED b'dunt nisi ut ante. Nulla\nfacilisi. Sed t
	ristique eros eu libero. Pellentesque vel arcu. Vivamus\npurus o
	rci, iaculis ac'
	Server: FLUSHING b'c1b36ebf0aedef3d57ea4b26dd986dd39af57dfb05d32
	279de'
	Client: READ b'c1b36ebf0aedef3d57ea4b26dd986dd39af57dfb05d32279d
	e'
	Client: DECOMPRESSED b', suscipit sit amet, pulvinar eu,\nlacus.
	\n'
	Client: response matches file contents: True

.. {{{end}}}


.. seealso::

   * :pydoc:`zlib`

   * :mod:`gzip` -- The ``gzip`` module includes a higher level
     (file-based) interface to the zlib library.

   * http://www.zlib.net/ -- Home page for zlib library.

   * http://www.zlib.net/manual.html -- Complete zlib documentation.

   * :mod:`bz2` -- The ``bz2`` module provides a similar interface to
     the bzip2 compression library.
