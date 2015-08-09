One-shot Operations in Memory
=============================

The simplest way to work with :mod:`bz2` is to load all of the data to
be compressed or decompressed in memory, and then use
:func:`compress()` and :func:`decompress()` to transform it.

.. include:: bz2_memory.py
    :literal:
    :start-after: #end_pymotw_header

The compressed data contains non-ASCII characters, so it needs to be
converted to its hexadecimal representation before it can be printed.
In the output from these examples, the hexadecimal version is
reformatted to have at most 40 characters on each line.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'bz2_memory.py'))
.. }}}

::

	$ python bz2_memory.py
	
	Original     : 26 bytes
	This is the original text.
	
	Compressed   : 62 bytes
	425a683931415926535916be35a6000002938040
	01040022e59c402000314c000111e93d434da223
	028cf9e73148cae0a0d6ed7f17724538509016be
	35a6
	
	Decompressed : 26 bytes
	This is the original text.

.. {{{end}}}

For short text, the compressed version can be significantly longer
than the original.  While the actual results depend on the input data,
it is interesting to observe the compression overhead.

.. include:: bz2_lengths.py
    :literal:
    :start-after: #end_pymotw_header

The output lines ending with ``*`` show the points where the
compressed data is longer than the raw input.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'bz2_lengths.py'))
.. }}}

::

	$ python bz2_lengths.py
	
	      len(data)  len(compressed)
	---------------  ---------------
	              0               14 *
	             26               62 *
	             52               68 *
	             78               70 
	            104               72 

.. {{{end}}}

Incremental Compression and Decompression
=========================================

The in-memory approach has obvious drawbacks that make it impractical
for real-world use cases.  The alternative is to use :class:`BZ2Compressor`
and :class:`BZ2Decompressor` objects to manipulate data incrementally, so that
the entire data set does not have to fit into memory.

.. include:: bz2_incremental.py
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
.. cog.out(run_script(cog.inFile, 'bz2_incremental.py', break_lines_at=70))
.. }}}

::

	$ python bz2_incremental.py
	
	buffering...
	buffering...
	buffering...
	buffering...
	Flushed: 425a6839314159265359ba83a48c000014d5800010400504052fa7fe00300
	0ba9112793d4ca789068698a0d1a341901a0d53f4d1119a8d4c9e812d755a67c107983
	87682c7ca7b5a3bb75da77755eb81c1cb1ca94c4b6faf209c52a90aaa4d16a4a1b9c16
	7a01c8d9ef32589d831e77df7a5753a398b11660e392126fc18a72a1088716cc8dedda
	5d489da410748531278043d70a8a131c2b8adcd6a221bdb8c7ff76b88c1d5342ee48a7
	0a12175074918

.. {{{end}}}


Mixed Content Streams
=====================

:class:`BZ2Decompressor` can also be used in situations where
compressed and uncompressed data is mixed together.  

.. include:: bz2_mixed.py
    :literal:
    :start-after: #end_pymotw_header

After decompressing all of the data, the *unused_data* attribute
contains any data not used.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'bz2_mixed.py'))
.. }}}

::

	$ python bz2_mixed.py
	
	Decompressed matches lorem: True
	Unused data matches lorem : True

.. {{{end}}}


Writing Compressed Files
========================

:class:`BZ2File` can be used to write to and read from
bzip2-compressed files using the usual methods for writing and reading
data.  

.. include:: bz2_file_write.py
    :literal:
    :start-after: #end_pymotw_header

To write data into a compressed file, open the file with mode ``'w'``.

.. {{{cog
.. workdir = path(cog.inFile).dirname()
.. sh("cd %s; rm -f example.bz2" % workdir)
.. cog.out(run_script(cog.inFile, 'bz2_file_write.py'))
.. }}}

::

	$ python bz2_file_write.py
	
	example.bz2: bzip2 compressed data, block size = 900k

.. {{{end}}}


Different compression levels can be used by passing a *compresslevel*
argument.  Valid values range from ``1`` to ``9``, inclusive.  Lower values
are faster and result in less compression.  Higher values are slower
and compress more, up to a point.

.. include:: bz2_file_compresslevel.py
    :literal:
    :start-after: #end_pymotw_header

The center column of numbers in the output of the script is the size
in bytes of the files produced.  For this input data, the higher
compression values do not always pay off in decreased storage space
for the same input data.  Results will vary for other inputs.

::

	$ python bz2_file_compresslevel.py

	3018243926 8771 compress-level-1.bz2
	1942389165 4949 compress-level-2.bz2
	2596054176 3708 compress-level-3.bz2
	1491394456 2705 compress-level-4.bz2
	1425874420 2705 compress-level-5.bz2
	2232840816 2574 compress-level-6.bz2
	447681641 2394 compress-level-7.bz2
	3699654768 1137 compress-level-8.bz2
	3103658384 1137 compress-level-9.bz2
	Input contains 754688 bytes

A :class:`BZ2File` instance also includes a :func:`writelines()`
method that can be used to write a sequence of strings.

.. include:: bz2_file_writelines.py
    :literal:
    :start-after: #end_pymotw_header

The lines should end in a newline character, like when writing to a
regular file.

.. {{{cog
.. workdir = path(cog.inFile).dirname()
.. sh("cd %s; rm -f example_lines.txt.bz2" % workdir)
.. cog.out(run_script(cog.inFile, 'bz2_file_writelines.py'))
.. }}}

::

	$ python bz2_file_writelines.py
	
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


Reading Compressed Files
========================

To read data back from previously compressed files, open the file with
binary read mode (``'rb'``) so no text-based translation of line
endings is performed.

.. include:: bz2_file_read.py
    :literal:
    :start-after: #end_pymotw_header

This example reads the file written by ``bz2_file_write.py`` from the
previous section.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'bz2_file_read.py'))
.. }}}

::

	$ python bz2_file_read.py
	
	Contents of the example file go here.
	

.. {{{end}}}
    
While reading a file, it is also possible to seek, and to read only part
of the data.

.. include:: bz2_file_seek.py
    :literal:
    :start-after: #end_pymotw_header

The :func:`seek()` position is relative to the *uncompressed* data, so
the caller does not even need to be aware that the data file is
compressed.  This allows a :class:`BZ2File` instance to be passed to a
function expecting a regular uncompressed file.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'bz2_file_seek.py'))
.. }}}

::

	$ python bz2_file_seek.py
	
	Entire file:
	Contents of the example file go here.
	
	Starting at position 5 for 10 bytes:
	nts of the
	
	True

.. {{{end}}}
