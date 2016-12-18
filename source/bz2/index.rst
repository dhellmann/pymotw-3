===========================
 bz2 --- bzip2 Compression
===========================

.. module:: bz2
    :synopsis: bzip2 compression

The ``bz2`` module is an interface for the bzip2 library, used to
compress data for storage or transmission.  There are three APIs
provided:

- "one shot" compression/decompression functions for operating on a
  blob of data
- iterative compression/decompression objects for working with streams
  of data
- a file-like class that supports reading and writing as with an
  uncompressed file

One-shot Operations in Memory
=============================

The simplest way to work with ``bz2`` is to load all of the data to
be compressed or decompressed in memory, and then use
``compress()`` and ``decompress()`` to transform it.

.. literalinclude:: bz2_memory.py
    :caption:
    :start-after: #end_pymotw_header

The compressed data contains non-ASCII characters, so it needs to be
converted to its hexadecimal representation before it can be printed.
In the output from these examples, the hexadecimal version is
reformatted to have at most 40 characters on each line.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'bz2_memory.py'))
.. }}}

.. code-block:: none

	$ python3 bz2_memory.py
	
	Original     : 26 bytes
	b'This is the original text.'
	
	Compressed   : 62 bytes
	b'425a683931415926535916be35a6000002938040'
	b'01040022e59c402000314c000111e93d434da223'
	b'028cf9e73148cae0a0d6ed7f17724538509016be'
	b'35a6'
	
	Decompressed : 26 bytes
	b'This is the original text.'

.. {{{end}}}

For short text, the compressed version can be significantly longer
than the original.  While the actual results depend on the input data,
it is interesting to observe the compression overhead.

.. literalinclude:: bz2_lengths.py
    :caption:
    :start-after: #end_pymotw_header

The output lines ending with ``*`` show the points where the
compressed data is longer than the raw input.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'bz2_lengths.py'))
.. }}}

.. code-block:: none

	$ python3 bz2_lengths.py
	
	      len(data)  len(compressed)
	---------------  ---------------
	              0               14*
	             26               62*
	             52               68*
	             78               70
	            104               72

.. {{{end}}}

Incremental Compression and Decompression
=========================================

The in-memory approach has obvious drawbacks that make it impractical
for real-world use cases.  The alternative is to use ``BZ2Compressor``
and ``BZ2Decompressor`` objects to manipulate data incrementally so that
the entire data set does not have to fit into memory.

.. literalinclude:: bz2_incremental.py
   :caption:
   :start-after: #end_pymotw_header

This example reads small blocks of data from a plain-text file and
passes it to ``compress()``.  The compressor maintains an internal
buffer of compressed data.  Since the compression algorithm depends on
checksums and minimum block sizes, the compressor may not be ready to
return data each time it receives more input.  If it does not have an
entire compressed block ready, it returns an empty string.  When all
of the data is fed in, the ``flush()`` method forces the compressor
to close the final block and return the rest of the compressed data.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'bz2_incremental.py'))
.. }}}

.. code-block:: none

	$ python3 bz2_incremental.py
	
	buffering...
	buffering...
	buffering...
	buffering...
	Flushed: b'425a6839314159265359ba83a48c000014d5800010400504052fa
	7fe003000ba9112793d4ca789068698a0d1a341901a0d53f4d1119a8d4c9e812
	d755a67c10798387682c7ca7b5a3bb75da77755eb81c1cb1ca94c4b6faf209c5
	2a90aaa4d16a4a1b9c167a01c8d9ef32589d831e77df7a5753a398b11660e392
	126fc18a72a1088716cc8dedda5d489da410748531278043d70a8a131c2b8adc
	d6a221bdb8c7ff76b88c1d5342ee48a70a12175074918'

.. {{{end}}}


Mixed Content Streams
=====================

``BZ2Decompressor`` can also be used in situations where
compressed and uncompressed data is mixed together.

.. literalinclude:: bz2_mixed.py
    :caption:
    :start-after: #end_pymotw_header

After decompressing all of the data, the ``unused_data`` attribute
contains any data not used.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'bz2_mixed.py'))
.. }}}

.. code-block:: none

	$ python3 bz2_mixed.py
	
	Decompressed matches lorem: True
	Unused data matches lorem : True

.. {{{end}}}


Writing Compressed Files
========================

``BZ2File`` can be used to write to and read from
bzip2-compressed files using the usual methods for writing and reading
data.

.. literalinclude:: bz2_file_write.py
    :caption:
    :start-after: #end_pymotw_header

To write data into a compressed file, open the file with mode ``'w'``.

.. {{{cog
.. from paver.path import path
.. from paver.easy import sh
.. workdir = path(cog.inFile).dirname()
.. sh("cd %s; rm -f example.bz2" % workdir)
.. cog.out(run_script(cog.inFile, 'bz2_file_write.py'))
.. }}}

.. code-block:: none

	$ python3 bz2_file_write.py
	
	example.bz2: bzip2 compressed data, block size = 900k

.. {{{end}}}


Different compression levels can be used by passing a ``compresslevel``
argument.  Valid values range from ``1`` to ``9``, inclusive.  Lower values
are faster and result in less compression.  Higher values are slower
and compress more, up to a point.

.. literalinclude:: bz2_file_compresslevel.py
    :caption:
    :start-after: #end_pymotw_header

The center column of numbers in the output of the script is the size
in bytes of the files produced.  For this input data, the higher
compression values do not always pay off in decreased storage space
for the same input data.  Results will vary for other inputs.

.. code-block:: none

	$ python3 bz2_file_compresslevel.py

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

A ``BZ2File`` instance also includes a ``writelines()``
method that can be used to write a sequence of strings.

.. literalinclude:: bz2_file_writelines.py
    :caption:
    :start-after: #end_pymotw_header

The lines should end in a newline character, as when writing to a
regular file.

.. {{{cog
.. workdir = path(cog.inFile).dirname()
.. sh("cd %s; rm -f example_lines.txt.bz2" % workdir)
.. cog.out(run_script(cog.inFile, 'bz2_file_writelines.py'))
.. }}}

.. code-block:: none

	$ python3 bz2_file_writelines.py
	
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
read mode (``'r'``). The value returned from ``read()`` will be a
byte string.

.. literalinclude:: bz2_file_read.py
    :caption:
    :start-after: #end_pymotw_header

This example reads the file written by ``bz2_file_write.py`` from the
previous section.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'bz2_file_read.py'))
.. }}}

.. code-block:: none

	$ python3 bz2_file_read.py
	
	Contents of the example file go here.
	

.. {{{end}}}
    
While reading a file, it is also possible to seek, and to read only part
of the data.

.. literalinclude:: bz2_file_seek.py
    :caption:
    :start-after: #end_pymotw_header

The ``seek()`` position is relative to the *uncompressed* data, so
the caller does not need to be aware that the data file is compressed.
This allows a ``BZ2File`` instance to be passed to a function
expecting a regular uncompressed file.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'bz2_file_seek.py'))
.. }}}

.. code-block:: none

	$ python3 bz2_file_seek.py
	
	Entire file:
	b'Contents of the example file go here.\n'
	Starting at position 5 for 10 bytes:
	b'nts of the'
	
	True

.. {{{end}}}

Reading and Writing Unicode Data
================================

The previous examples used ``BZ2File`` directly and managed the
encoding and decoding of Unicode text strings inline with an
``io.TextIOWrapper``, where necessary. These extra steps can be
avoided by using ``bz2.open()``, which sets up an
``io.TextIOWrapper`` to handle the encoding or decoding
automatically.

.. literalinclude:: bz2_unicode.py
   :caption:
   :start-after: #end_pymotw_header

The file handle returned by ``open()`` supports ``seek()``, but
use care because the file pointer moves by *bytes* not *characters*
and may end up in the middle of an encoded character.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'bz2_unicode.py'))
.. }}}

.. code-block:: none

	$ python3 bz2_unicode.py
	
	Full file: Character with an åccent.
	One character: å
	ERROR: failed to decode

.. {{{end}}}



Compressing Network Data
========================

The code in the next example responds to requests consisting of
filenames by writing a compressed version of the file to the socket
used to communicate with the client.  It has some artificial chunking
in place to illustrate the buffering that occurs when the data passed
to ``compress()`` or ``decompress()`` does not result in a
complete block of compressed or uncompressed output.

.. literalinclude:: bz2_server.py
   :caption:
   :lines: 9-52

The main program starts a server in a thread, combining
:mod:`SocketServer` and ``Bz2RequestHandler``.  

.. literalinclude:: bz2_server.py
   :lines: 55-

It then opens a socket to communicate with the server as a client, and
requests the file (defaulting to ``lorem.txt``) which contains:

.. literalinclude:: lorem.txt

.. warning::

    This implementation has obvious security implications.  Do not run
    it on a server on the open Internet or in any environment where
    security might be an issue.

Running ``bz2_server.py`` produces:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'bz2_server.py'))
.. }}}

.. code-block:: none

	$ python3 bz2_server.py
	
	Client: Contacting server on 127.0.0.1:57364
	Client: sending filename: "lorem.txt"
	Server: client asked for: "lorem.txt"
	Server: RAW b'Lorem ipsum dolor sit amet, cons'
	Server: BUFFERING
	Server: RAW b'ectetuer adipiscing elit. Donec\n'
	Server: BUFFERING
	Server: RAW b'egestas, enim et consectetuer ul'
	Server: BUFFERING
	Server: RAW b'lamcorper, lectus ligula rutrum '
	Server: BUFFERING
	Server: RAW b'leo,\na elementum elit tortor eu '
	Server: BUFFERING
	Server: RAW b'quam. Duis tincidunt nisi ut ant'
	Server: BUFFERING
	Server: RAW b'e. Nulla\nfacilisi.\n'
	Server: BUFFERING
	Server: FLUSHING b'425a6839314159265359ba83a48c000014d5800010400
	504052fa7fe003000ba'
	Server: FLUSHING b'9112793d4ca789068698a0d1a341901a0d53f4d1119a8
	d4c9e812d755a67c107'
	Client: READ b'425a6839314159265359ba83a48c000014d58000104005040
	52fa7fe003000ba'
	Server: FLUSHING b'98387682c7ca7b5a3bb75da77755eb81c1cb1ca94c4b6
	faf209c52a90aaa4d16'
	Client: BUFFERING
	Server: FLUSHING b'a4a1b9c167a01c8d9ef32589d831e77df7a5753a398b1
	1660e392126fc18a72a'
	Client: READ b'9112793d4ca789068698a0d1a341901a0d53f4d1119a8d4c9
	e812d755a67c107'
	Server: FLUSHING b'1088716cc8dedda5d489da410748531278043d70a8a13
	1c2b8adcd6a221bdb8c'
	Client: BUFFERING
	Server: FLUSHING b'7ff76b88c1d5342ee48a70a12175074918'
	Client: READ b'98387682c7ca7b5a3bb75da77755eb81c1cb1ca94c4b6faf2
	09c52a90aaa4d16'
	Client: BUFFERING
	Client: READ b'a4a1b9c167a01c8d9ef32589d831e77df7a5753a398b11660
	e392126fc18a72a'
	Client: BUFFERING
	Client: READ b'1088716cc8dedda5d489da410748531278043d70a8a131c2b
	8adcd6a221bdb8c'
	Client: BUFFERING
	Client: READ b'7ff76b88c1d5342ee48a70a12175074918'
	Client: DECOMPRESSED b'Lorem ipsum dolor sit amet, consectetuer 
	adipiscing elit. Donec\negestas, enim et consectetuer ullamcorpe
	r, lectus ligula rutrum leo,\na elementum elit tortor eu quam. D
	uis tincidunt nisi ut ante. Nulla\nfacilisi.\n'
	Client: response matches file contents: True

.. {{{end}}}

.. seealso::

    * :pydoc:`bz2`

    * `bzip2.org <http://www.bzip.org/>`_ -- The home page for
      ``bzip2``.

    * :mod:`zlib` -- The ``zlib`` module for GNU zip compression.

    * :mod:`gzip` -- A file-like interface to GNU zip compressed
      files.

    * :ref:`Porting notes for bz2 <porting-bz2>`
