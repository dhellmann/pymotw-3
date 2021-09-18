========================
bz2 -- bzip2 compression
========================

.. module:: bz2
    :synopsis: bzip2 compression

:Purpose: bzip2 compression
:Available In: 2.3 and later

The :mod:`bz2` module is an interface for the bzip2 library, used to
compress data for storage or transmission.  There are three APIs
provided:

- "one shot" compression/decompression functions for operating on a blob of data
- iterative compression/decompression objects for working with streams of data
- a file-like class that supports reading and writing as with an uncompressed file

One-shot Operations in Memory
=============================

The simplest way to work with bz2 requires holding all of the data to
be compressed or decompressed in memory, and then using
:func:`compress()` and :func:`decompress()`.

.. include:: bz2_memory.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'bz2_memory.py'))
.. }}}

::

	$ python bz2_memory.py
	
	Original     : 26 This is the original text.
	Compressed   : 62 425a683931415926535916be35a600000293804001040022e59c402000314c000111e93d434da223028cf9e73148cae0a0d6ed7f17724538509016be35a6
	Decompressed : 26 This is the original text.

.. {{{end}}}

Notice that for short text, the compressed version can be
significantly longer.  While the actual results depend on the input
data, for short bits of text it is interesting to observe the
compression overhead.

.. include:: bz2_lengths.py
    :literal:
    :start-after: #end_pymotw_header

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
	            130               77 
	            156               77 
	            182               73 
	            208               75 
	            234               80 
	            260               80 
	            286               81 
	            312               80 
	            338               81 
	            364               81 
	            390               76 
	            416               78 
	            442               84 
	            468               84 
	            494               87 

.. {{{end}}}


Working with Streams
====================

The in-memory approach is not practical for real-world use cases,
since you rarely want to hold both the entire compressed and
uncompressed data sets in memory at the same time.  The alternative is
to use :class:`BZ2Compressor` and :class:`BZ2Decompressor` objects to
work with streams of data, so that the entire data set does not have
to fit into memory.

The simple server below responds to requests consisting of filenames
by writing a compressed version of the file to the socket used to
communicate with the client.  It has some artificial chunking in place
to illustrate the buffering behavior that happens when the data passed
to :func:`compress()` or :func:`decompress()` doesn't result in a
complete block of compressed or uncompressed output.

.. warning::

    This implementation has obvious security implications.  Do not run
    it on a server on the open internet or in any environment where
    security might be an issue.

.. include:: bz2_server.py
    :literal:
    :start-after: #end_pymotw_header

::

    $ python bz2_server.py
    Client: Contacting server on 127.0.0.1:54092
    Client: sending filename: "lorem.txt"
    Server: client asked for: "lorem.txt"
    Server: RAW "Lorem ipsum dolor sit amet, cons"
    Server: BUFFERING
    Server: RAW "ectetuer adipiscing elit. Donec
    "
    Server: BUFFERING
    Server: RAW "egestas, enim et consectetuer ul"
    Server: BUFFERING
    Server: RAW "lamcorper, lectus ligula rutrum "
    Server: BUFFERING
    Server: RAW "leo, a
    elementum elit tortor eu "
    Server: BUFFERING
    Server: RAW "quam. Duis tincidunt nisi ut ant"
    Server: BUFFERING
    Server: RAW "e. Nulla
    facilisi. Sed tristique"
    Server: BUFFERING
    Server: RAW " eros eu libero. Pellentesque ve"
    Server: BUFFERING
    Server: RAW "l arcu. Vivamus
    purus orci, iacu"
    Server: BUFFERING
    Server: RAW "lis ac, suscipit sit amet, pulvi"
    Server: BUFFERING
    Server: RAW "nar eu,
    lacus. Praesent placerat"
    Server: BUFFERING
    Server: RAW " tortor sed nisl. Nunc blandit d"
    Server: BUFFERING
    Server: RAW "iam egestas
    dui. Pellentesque ha"
    Server: BUFFERING
    Server: RAW "bitant morbi tristique senectus "
    Server: BUFFERING
    Server: RAW "et netus et
    malesuada fames ac t"
    Server: BUFFERING
    Server: RAW "urpis egestas. Aliquam viverra f"
    Server: BUFFERING
    Server: RAW "ringilla
    leo. Nulla feugiat augu"
    Server: BUFFERING
    Server: RAW "e eleifend nulla. Vivamus mauris"
    Server: BUFFERING
    Server: RAW ". Vivamus sed
    mauris in nibh pla"
    Server: BUFFERING
    Server: RAW "cerat egestas. Suspendisse poten"
    Server: BUFFERING
    Server: RAW "ti. Mauris massa. Ut
    eget velit "
    Server: BUFFERING
    Server: RAW "auctor tortor blandit sollicitud"
    Server: BUFFERING
    Server: RAW "in. Suspendisse imperdiet
    justo."
    Server: BUFFERING
    Server: RAW "
    "
    Server: BUFFERING
    Server: FLUSHING "425a68393141592653590fd264ff00004357800010400524074b003ff7ff0040"
    Server: FLUSHING "01dd936c1834269926d4d13d232640341a986935343534f5000018d311846980"
    Client: READ "425a68393141592653590fd264ff00004357800010400524074b003ff7ff0040"
    Server: FLUSHING "0001299084530d35434f51ea1ea13fce3df02cb7cde200b67bb8fca353727a30"
    Client: BUFFERING
    Server: FLUSHING "fe67cdcdd2307c455a3964fad491e9350de1a66b9458a40876613e7575a9d2de"
    Client: READ "01dd936c1834269926d4d13d232640341a986935343534f5000018d311846980"
    Server: FLUSHING "db28ab492d5893b99616ebae68b8a61294a48ba5d0a6c428f59ad9eb72e0c40f"
    Client: BUFFERING
    Server: FLUSHING "f449c4f64c35ad8a27caa2bbd9e35214df63183393aa35919a4f1573615c6ae3"
    Client: READ "0001299084530d35434f51ea1ea13fce3df02cb7cde200b67bb8fca353727a30"
    Server: FLUSHING "611f18917467ad690abb4cb67a3a5f1fd36c2511d105836a0fed317be03702ba"
    Client: BUFFERING
    Server: FLUSHING "394984c68a595d1cc2f5219a1ada69b6d6863cf5bd925f36626046d68c3a9921"
    Client: READ "fe67cdcdd2307c455a3964fad491e9350de1a66b9458a40876613e7575a9d2de"
    Server: FLUSHING "3103445c9d2438d03b5a675dfdc74e3bed98e8b72dec76c923afa395eb5ce61b"
    Client: BUFFERING
    Server: FLUSHING "50cfc0ccaaa726b293a50edc28b551261dd09a24aba682972bc75f1fae4c4765"
    Client: READ "db28ab492d5893b99616ebae68b8a61294a48ba5d0a6c428f59ad9eb72e0c40f"
    Server: FLUSHING "f3b7eeea36e771e577350970dab4baf07750ccf96494df9e63a9454b7133be1d"
    Client: BUFFERING
    Server: FLUSHING "ee330da50a869eea59f73319b18959262860897dafdc965ac4b79944c4cc3341"
    Client: READ "f449c4f64c35ad8a27caa2bbd9e35214df63183393aa35919a4f1573615c6ae3"
    Server: FLUSHING "5b23816d45912c8860f40ea930646fc8adbc48040cbb6cd4fc222f8c66d58256"
    Client: BUFFERING
    Server: FLUSHING "d508d8eb4f43986b9203e13f8bb9229c284807e9327f80"
    Client: READ "611f18917467ad690abb4cb67a3a5f1fd36c2511d105836a0fed317be03702ba"
    Client: BUFFERING
    Client: READ "394984c68a595d1cc2f5219a1ada69b6d6863cf5bd925f36626046d68c3a9921"
    Client: BUFFERING
    Client: READ "3103445c9d2438d03b5a675dfdc74e3bed98e8b72dec76c923afa395eb5ce61b"
    Client: BUFFERING
    Client: READ "50cfc0ccaaa726b293a50edc28b551261dd09a24aba682972bc75f1fae4c4765"
    Client: BUFFERING
    Client: READ "f3b7eeea36e771e577350970dab4baf07750ccf96494df9e63a9454b7133be1d"
    Client: BUFFERING
    Client: READ "ee330da50a869eea59f73319b18959262860897dafdc965ac4b79944c4cc3341"
    Client: BUFFERING
    Client: READ "5b23816d45912c8860f40ea930646fc8adbc48040cbb6cd4fc222f8c66d58256"
    Client: BUFFERING
    Client: READ "d508d8eb4f43986b9203e13f8bb9229c284807e9327f80"
    Client: DECOMPRESSED "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec
    egestas, enim et consectetuer ullamcorper, lectus ligula rutrum leo, a
    elementum elit tortor eu quam. Duis tincidunt nisi ut ante. Nulla
    facilisi. Sed tristique eros eu libero. Pellentesque vel arcu. Vivamus
    purus orci, iaculis ac, suscipit sit amet, pulvinar eu,
    lacus. Praesent placerat tortor sed nisl. Nunc blandit diam egestas
    dui. Pellentesque habitant morbi tristique senectus et netus et
    malesuada fames ac turpis egestas. Aliquam viverra fringilla
    leo. Nulla feugiat augue eleifend nulla. Vivamus mauris. Vivamus sed
    mauris in nibh placerat egestas. Suspendisse potenti. Mauris massa. Ut
    eget velit auctor tortor blandit sollicitudin. Suspendisse imperdiet
    justo.
    "
    Client: response matches file contents: True


Mixed Content Streams
=====================

:class:`BZ2Decompressor` can also be used in situations where
compressed and uncompressed data is mixed together.  After
decompressing all of the data, the *unused_data* attribute contains
any data not used.

.. include:: bz2_mixed.py
    :literal:
    :start-after: #end_pymotw_header

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
data.  To write data into a compressed file, open the file with mode
``'w'``.

.. include:: bz2_file_write.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. workdir = path(cog.inFile).dirname()
.. sh("cd %s; rm -f example.txt.bzw" % workdir)
.. cog.out(run_script(cog.inFile, 'bz2_file_write.py'))
.. }}}

::

	$ python bz2_file_write.py
	
	example.txt.bz2: bzip2 compressed data, block size = 900k

.. {{{end}}}


Different compression levels can be used by passing a *compresslevel*
argument.  Valid values range from 1 to 9, inclusive.  Lower values
are faster and result in less compression.  Higher values are slower
and compress more, up to a point.

.. include:: bz2_file_compresslevel.py
    :literal:
    :start-after: #end_pymotw_header

The center column of numbers in the output of the script is the size
in bytes of the files produced.  As you see, for this input data, the
higher compression values do not always pay off in decreased storage
space for the same input data.  Results will vary for other inputs.

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

To read data back from previously compressed files, simply open the
file with mode ``'r'``.

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
    
While reading a file, it is also possible to seek and read only part
of the data.

.. include:: bz2_file_seek.py
    :literal:
    :start-after: #end_pymotw_header

The :func:`seek()` position is relative to the *uncompressed* data, so the
caller does not even need to know that the data file is compressed.

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


.. seealso::

    `bz2 <http://docs.python.org/2.7/library/bz2.html>`_
        The standard library documentation for this module.

    `bzip2.org <http://www.bzip.org/>`_
        The home page for bzip2.

    :mod:`zlib`
        The zlib module for GNU zip compression.

    :mod:`gzip`
        A file-like interface to GNU zip compressed files.

    :mod:`SocketServer`
        Base classes for creating your own network servers.
