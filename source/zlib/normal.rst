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
