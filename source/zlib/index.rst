==============================
 zlib -- GNU zlib Compression
==============================

.. module:: zlib
    :synopsis: GNU zlib compression library

:Purpose: Low-level access to GNU zlib compression library
:Python Version: 2.5 and later

The :mod:`zlib` module provides a lower-level interface to many of the
functions in the :mod:`zlib` compression library from the GNU project.

Working with Data in Memory
===========================

The simplest way to work with :mod:`zlib` requires holding all of the
data to be compressed or decompressed in memory:

.. include:: zlib_memory.py
    :literal:
    :start-after: #end_pymotw_header

The :func:`compress()` and :func:`decompress()` functions both take a
string argument and return a string.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'zlib_memory.py', break_lines_at=65))
.. }}}

::

	$ python zlib_memory.py
	
	Original     : 26 This is the original text.
	Compressed   : 32 789c0bc9c82c5600a2928c5485fca2ccf4ccbcc41c8592d
	48a123d007f2f097e
	Decompressed : 26 This is the original text.

.. {{{end}}}

The previous example demonstrates that for short text, the compressed
version of a string can be bigger than the uncompressed version.
While the actual results depend on the input data, for short bits of
text it is interesting to observe the compression overhead.

.. include:: zlib_lengths.py
    :literal:
    :start-after: #end_pymotw_header

The ``*`` in the output highlight the lines where the compressed data
takes up more memory than the uncompressed version.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'zlib_lengths.py'))
.. }}}

::

	$ python zlib_lengths.py
	
	      len(data)  len(compressed)
	---------------  ---------------
	              0                8 *
	             26               32 *
	             52               35 
	             78               35 
	            104               36 

.. {{{end}}}

Incremental Compression and Decompression
=========================================

The in-memory approach has drawbacks that make it impractical for
real-world use cases, primarily that the system needs enough memory to
hold both the uncompressed and compressed versions resident in memory
at the same time.  The alternative is to use :class:`Compress` and
:class:`Decompress` objects to manipulate data incrementally, so that
the entire data set does not have to fit into memory.

.. include:: zlib_incremental.py
   :literal:
   :start-after: #end_pymotw_header

This example reads small blocks of data from a plain text file and
passes it to :func:`compress`.  The compressor maintains an internal
buffer of compressed data.  Since the compression algorithm depends on
checksums and minimum block sizes, the compressor may not be ready to
return data each time it receives more input.  If it does not have an
entire compressed block ready, it returns an empty string.  When all
of the data is fed in, the :func:`flush` method forces the compressor
to close the final block and return the rest of the compressed data.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'zlib_incremental.py', break_lines_at=70))
.. }}}

::

	$ python zlib_incremental.py
	
	Compressed: 7801
	buffering...
	buffering...
	buffering...
	buffering...
	buffering...
	Flushed: 55904b6ac4400c44f73e451da0f129b20c2110c85e696b8c40ddedd167ce1
	f7915025a087daa9ef4be8c07e4f21c38962e834b800647435fd3b90747b2810eb9c4b
	bcc13ac123bded6e4bef1c91ee40d3c6580e3ff52aad2e8cb2eb6062dad74a89ca904c
	bb0f2545e0db4b1f2e01955b8c511cb2ac08967d228af1447c8ec72e40c4c714116e60
	cdef171bb6c0feaa255dff1c507c2c4439ec9605b7e0ba9fc54bae39355cb89fd6ebe5
	841d673c7b7bc68a46f575a312eebd220d4b32441bdc1b36ebf0aedef3d57ea4b26dd9
	86dd39af57dfb05d32279de

.. {{{end}}}


Mixed Content Streams
=====================

The :class:`Decompress` class returned by :func:`decompressobj()` can
also be used in situations where compressed and uncompressed data is
mixed together.  

.. include:: zlib_mixed.py
    :literal:
    :start-after: #end_pymotw_header

After decompressing all of the data, the *unused_data* attribute
contains any data not used.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'zlib_mixed.py'))
.. }}}

::

	$ python zlib_mixed.py
	
	Decompressed matches lorem: True
	Unused data matches lorem : True

.. {{{end}}}


Checksums
=========

In addition to compression and decompression functions, :mod:`zlib`
includes two functions for computing checksums of data,
:func:`adler32()` and :func:`crc32()`.  Neither checksum is billed as
cryptographically secure, and they are only intended for use for data
integrity verification.

.. include:: zlib_checksums.py
    :literal:
    :start-after: #end_pymotw_header

Both functions take the same arguments, a string of data and an
optional value to be used as a starting point for the checksum.  They
return a 32-bit signed integer value which can also be passed back on
subsequent calls as a new starting point argument to produce a
*running* checksum.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'zlib_checksums.py'))
.. }}}

::

	$ python zlib_checksums.py
	
	Adler32:   -752715298
	       :    669447099
	CRC-32 :  -1256596780
	       :  -1424888665

.. {{{end}}}

Compressing Network Data
========================
 
The server in the next listing uses the stream compressor to respond
to requests consisting of filenames by writing a compressed version of
the file to the socket used to communicate with the client.  It has
some artificial chunking in place to illustrate the buffering that
occurs when the data passed to :func:`compress()` or
:func:`decompress()` does not result in a complete block of compressed
or uncompressed output.

.. literalinclude:: zlib_server.py
   :lines: 11-72
 
It has some artificial chunking in place to illustrate the buffering
behavior that happens when the data passed to :func:`compress()` or
:func:`decompress()` does not result in a complete block of compressed
or uncompressed output.

.. literalinclude:: zlib_server.py
   :lines: 74-

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
.. cog.out(run_script(cog.inFile, 'zlib_server.py', break_lines_at=69))
.. }}}

::

    $ python zlib_server.py
    
    Client: Contacting server on 127.0.0.1:55085
    Client: sending filename: "lorem.txt"
    Server: client asked for: "lorem.txt"
    Server: RAW "Lorem ipsum dolor sit amet, consectetuer adipiscing elit
    . Donec
    "
    Server: SENDING "7801"
    Server: RAW "egestas, enim et consectetuer ullamcorper, lectus ligula
     rutrum "
    Server: BUFFERING
    Server: RAW "leo, a
    elementum elit tortor eu quam. Duis tincidunt nisi ut ant"
    Server: BUFFERING
    Server: RAW "e. Nulla
    facilisi. Sed tristique eros eu libero. Pellentesque ve"
    Server: BUFFERING
    Server: RAW "l arcu. Vivamus
    purus orci, iaculis ac, suscipit sit amet, pulvi"
    Server: BUFFERING
    Server: RAW "nar eu,
    lacus.
    "
    Server: BUFFERING
    Server: FLUSHING "55904b6ac4400c44f73e451da0f129b20c2110c85e696b8c40d
    dedd167ce1f7915025a087daa9ef4be8c07e4f21c38962e834b800647435fd3b90747
    b2810eb9"
    Server: FLUSHING "c4bbcc13ac123bded6e4bef1c91ee40d3c6580e3ff52aad2e8c
    b2eb6062dad74a89ca904cbb0f2545e0db4b1f2e01955b8c511cb2ac08967d228af14
    47c8ec72"
    Server: FLUSHING "e40c4c714116e60cdef171bb6c0feaa255dff1c507c2c4439ec
    9605b7e0ba9fc54bae39355cb89fd6ebe5841d673c7b7bc68a46f575a312eebd220d4
    b32441bd"
    Server: FLUSHING "c1b36ebf0aedef3d57ea4b26dd986dd39af57dfb05d32279de"
    Client: READ "780155904b6ac4400c44f73e451da0f129b20c2110c85e696b8c40d
    dedd167ce1f7915025a087daa9ef4be8c07e4f21c38962e834b800647435fd3b90747
    b281"
    Client: DECOMPRESSED "Lorem ipsum dolor sit amet, consectetuer "
    Client: READ "0eb9c4bbcc13ac123bded6e4bef1c91ee40d3c6580e3ff52aad2e8c
    b2eb6062dad74a89ca904cbb0f2545e0db4b1f2e01955b8c511cb2ac08967d228af14
    47c8"
    Client: DECOMPRESSED "adipiscing elit. Donec
    egestas, enim et consectetuer ullamcorper, lectus ligula rutrum leo, 
    a
    elementum elit tortor eu quam. Duis ti"
    Client: READ "ec72e40c4c714116e60cdef171bb6c0feaa255dff1c507c2c4439ec
    9605b7e0ba9fc54bae39355cb89fd6ebe5841d673c7b7bc68a46f575a312eebd220d4
    b324"
    Client: DECOMPRESSED "ncidunt nisi ut ante. Nulla
    facilisi. Sed tristique eros eu libero. Pellentesque vel arcu. Vivamu
    s
    purus orci, iacu"
    Client: READ "41bdc1b36ebf0aedef3d57ea4b26dd986dd39af57dfb05d32279de"
    Client: DECOMPRESSED "lis ac, suscipit sit amet, pulvinar eu,
    lacus.
    "
    Client: response matches file contents: True

.. {{{end}}}


.. seealso::

    `zlib <http://docs.python.org/library/zlib.html>`_
        The standard library documentation for this module.

    :mod:`gzip`
        The ``gzip`` module includes a higher level (file-based)
        interface to the zlib library.

    http://www.zlib.net/
        Home page for zlib library.

    http://www.zlib.net/manual.html
        Complete zlib documentation.

    :mod:`bz2`
        The ``bz2`` module provides a similar interface to the bzip2
        compression library.
