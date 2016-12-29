=========================================
 codecs --- String Encoding and Decoding
=========================================

.. module:: codecs
    :synopsis: String encoding and decoding.

:Purpose: Encoders and decoders for converting text between different
          representations.

The ``codecs`` module provides stream and file interfaces for
transcoding data.  It is most commonly used to work with Unicode text,
but other encodings are also available for other purposes.

Unicode Primer
==============

CPython 3.x differentiates between *text* and *byte* strings.
``bytes`` instances use a sequence of 8-bit byte values.  In
contrast, ``str`` strings are managed internally as a sequence of
Unicode *code points*.  The code point values are saved as a sequence
of 2 or 4 bytes each, depending on the options given when Python was
compiled.

When ``str`` values are output, they are encoded using one of
several standard schemes so that the sequence of bytes can be
reconstructed as the same string of text later.  The bytes of the
encoded value are not necessarily the same as the code point values,
and the encoding defines a way to translate between the two sets of
values.  Reading Unicode data also requires knowing the encoding so
that the incoming bytes can be converted to the internal
representation used by the ``unicode`` class.

The most common encodings for Western languages are ``UTF-8`` and
``UTF-16``, which use sequences of one and two byte values
respectively to represent each code point.  Other encodings can be
more efficient for storing languages where most of the characters are
represented by code points that do not fit into two bytes.

.. seealso::

  For more introductory information about Unicode, refer to the list
  of references at the end of this section.  The *Python Unicode
  HOWTO* is especially helpful.

Encodings
---------

The best way to understand encodings is to look at the different
series of bytes produced by encoding the same string in different
ways.  The following examples use this function to format the byte
string to make it easier to read.

.. literalinclude:: codecs_to_hex.py
   :caption:
   :start-after: #end_pymotw_header

The function uses :mod:`binascii` to get a hexadecimal representation
of the input byte string, then insert a space between every ``nbytes``
bytes before returning the value.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_to_hex.py'))
.. }}}

.. code-block:: none

	$ python3 codecs_to_hex.py
	
	b'61 62 63 64 65 66'
	b'6162 6364 6566'

.. {{{end}}}

The first encoding example begins by printing the text ``'pi: π'``
using the raw representation of the ``unicode`` class, followed
by the name of each character from the Unicode database.  The next two
lines encode the string as UTF-8 and UTF-16 respectively, and show the
hexadecimal values resulting from the encoding.

.. literalinclude:: codecs_encodings.py
   :caption:
   :start-after: #end_pymotw_header

The result of encoding a ``str`` is a ``bytes`` object.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_encodings.py'))
.. }}}

.. code-block:: none

	$ python3 codecs_encodings.py
	
	Raw   : 'pi: π'
	  'p': LATIN SMALL LETTER P
	  'i': LATIN SMALL LETTER I
	  ':': COLON
	  ' ': SPACE
	  'π': GREEK SMALL LETTER PI
	UTF-8 : b'70 69 3a 20 cf 80'
	UTF-16: b'fffe 7000 6900 3a00 2000 c003'

.. {{{end}}}

Given a sequence of encoded bytes as a ``bytes`` instance, the
``decode()`` method translates them to code points and returns the
sequence as a ``str`` instance.

.. literalinclude:: codecs_decode.py
   :caption:
   :start-after: #end_pymotw_header

The choice of encoding used does not change the output type.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_decode.py'))
.. }}}

.. code-block:: none

	$ python3 codecs_decode.py
	
	Original : 'pi: π'
	Encoded  : b'70 69 3a 20 cf 80' <class 'bytes'>
	Decoded  : 'pi: π' <class 'str'>

.. {{{end}}}

.. note::

  The default encoding is set during the interpreter start-up process,
  when :mod:`site` is loaded.  Refer to the
  :ref:`sys-unicode-defaults` section from the discussion of
  :mod:`sys` for a description of the default encoding settings.

Working with Files
==================

Encoding and decoding strings is especially important when dealing
with I/O operations.  Whether writing to a file, socket, or other
stream, the data must use the proper encoding.  In general, all text
data needs to be decoded from its byte representation as it is read,
and encoded from the internal values to a specific representation as
it is written.  A program can explicitly encode and decode data, but
depending on the encoding used it can be non-trivial to determine
whether enough bytes have been read in order to fully decode the data.
``codecs`` provides classes that manage the data encoding and
decoding, so applications do not have to do that work.

The simplest interface provided by ``codecs`` is an alternative to
the built-in ``open()`` function.  The new version works just like
the built-in, but adds two new arguments to specify the encoding and
desired error handling technique.

.. literalinclude:: codecs_open_write.py
   :caption:
   :start-after: #end_pymotw_header

This example starts with a ``unicode`` string with the code point
for π and saves the text to a file using an encoding specified on the
command line.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_open_write.py utf-8'))
.. cog.out(run_script(cog.inFile, 'codecs_open_write.py utf-16', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'codecs_open_write.py utf-32', include_prefix=False))
.. }}}

.. code-block:: none

	$ python3 codecs_open_write.py utf-8
	
	Writing to utf-8.txt
	File contents:
	b'70 69 3a 20 cf 80'

	$ python3 codecs_open_write.py utf-16
	
	Writing to utf-16.txt
	File contents:
	b'fffe 7000 6900 3a00 2000 c003'

	$ python3 codecs_open_write.py utf-32
	
	Writing to utf-32.txt
	File contents:
	b'fffe0000 70000000 69000000 3a000000 20000000 c0030000'

.. {{{end}}}

Reading the data with ``open()`` is straightforward, with one catch:
the encoding must be known in advance, in order to set up the decoder
correctly.  Some data formats, such as XML, specify the encoding as
part of the file, but usually it is up to the application to manage.
``codecs`` simply takes the encoding as an argument and assumes it
is correct.

.. literalinclude:: codecs_open_read.py
   :caption:
   :start-after: #end_pymotw_header

This example reads the files created by the previous program, and
prints the representation of the resulting ``unicode`` object to
the console.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_open_read.py utf-8'))
.. cog.out(run_script(cog.inFile, 'codecs_open_read.py utf-16', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'codecs_open_read.py utf-32', include_prefix=False))
.. }}}

.. code-block:: none

	$ python3 codecs_open_read.py utf-8
	
	Reading from utf-8.txt
	'pi: π'

	$ python3 codecs_open_read.py utf-16
	
	Reading from utf-16.txt
	'pi: π'

	$ python3 codecs_open_read.py utf-32
	
	Reading from utf-32.txt
	'pi: π'

.. {{{end}}}

Byte Order
==========

Multi-byte encodings such as UTF-16 and UTF-32 pose a problem when
transferring the data between different computer systems, either by
copying the file directly or with network communication.  Different
systems use different ordering of the high and low order bytes.  This
characteristic of the data, known as its *endianness*, depends on
factors such as the hardware architecture and choices made by the
operating system and application developer.  There is not always a way
to know in advance what byte order to use for a given set of data, so
the multi-byte encodings include a *byte-order marker* (BOM) as the
first few bytes of encoded output.  For example, UTF-16 is defined in
such a way that 0xFFFE and 0xFEFF are not valid characters, and can be
used to indicate the byte order.  ``codecs`` defines constants for
the byte order markers used by UTF-16 and UTF-32.

.. literalinclude:: codecs_bom.py
   :caption:
   :start-after: #end_pymotw_header

``BOM``, ``BOM_UTF16``, and ``BOM_UTF32`` are automatically set to the
appropriate big-endian or little-endian values depending on the
current system's native byte order.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_bom.py'))
.. }}}

.. code-block:: none

	$ python3 codecs_bom.py
	
	BOM          : b'fffe'
	BOM_BE       : b'feff'
	BOM_LE       : b'fffe'
	BOM_UTF8     : b'efbb bf'
	BOM_UTF16    : b'fffe'
	BOM_UTF16_BE : b'feff'
	BOM_UTF16_LE : b'fffe'
	BOM_UTF32    : b'fffe 0000'
	BOM_UTF32_BE : b'0000 feff'
	BOM_UTF32_LE : b'fffe 0000'

.. {{{end}}}

Byte ordering is detected and handled automatically by the decoders in
``codecs``, but an explicit ordering can be specified when
encoding.

.. literalinclude:: codecs_bom_create_file.py
   :caption:
   :start-after: #end_pymotw_header

``codecs_bom_create_file.py`` figures out the native byte ordering,
then uses the alternate form explicitly so the next example can
demonstrate auto-detection while reading.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_bom_create_file.py'))
.. }}}

.. code-block:: none

	$ python3 codecs_bom_create_file.py
	
	Native order  : b'fffe'
	Selected order: b'feff'
	utf_16_be     : b'0070 0069 003a 0020 03c0'

.. {{{end}}}

``codecs_bom_detection.py`` does not specify a byte order when opening
the file, so the decoder uses the BOM value in the first two bytes of
the file to determine it.

.. literalinclude:: codecs_bom_detection.py
   :caption:
   :start-after: #end_pymotw_header

Since the first two bytes of the file are used for byte order
detection, they are not included in the data returned by ``read()``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_bom_detection.py'))
.. }}}

.. code-block:: none

	$ python3 codecs_bom_detection.py
	
	Raw    : b'feff 0070 0069 003a 0020 03c0'
	Decoded: 'pi: π'

.. {{{end}}}

Error Handling
==============

The previous sections pointed out the need to know the encoding being
used when reading and writing Unicode files.  Setting the encoding
correctly is important for two reasons.  If the encoding is configured
incorrectly while reading from a file, the data will be interpreted
wrong and may be corrupted or simply fail to decode.  Not all Unicode
characters can be represented in all encodings, so if the wrong
encoding is used while writing then an error will be generated and
data may be lost.

``codecs`` uses the same five error handling options that are
provided by the ``encode()`` method of ``str`` and the
``decode()`` method of ``bytes``, listed in :table:`Codec Error
Handling Modes`.

.. table:: Codec Error Handling Modes

   =====================   ===========
   Error Mode              Description
   =====================   ===========
   ``strict``              Raises an exception if the data cannot be converted.
   ``replace``             Substitutes a special marker character for data that cannot be encoded.
   ``ignore``              Skips the data.
   ``xmlcharrefreplace``   XML character (encoding only)
   ``backslashreplace``    escape sequence (encoding only)
   =====================   ===========

Encoding Errors
---------------

The most common error condition is receiving a
``UnicodeEncodeError`` when writing Unicode data to an ASCII
output stream, such as a regular file or ``sys.stdout``.  This
sample program can be used to experiment with the different error
handling modes.

.. literalinclude:: codecs_encode_error.py
   :caption:
   :start-after: #end_pymotw_header

While ``strict`` mode is safest for ensuring an application explicitly
sets the correct encoding for all I/O operations, it can lead to
program crashes when an exception is raised.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_encode_error.py strict', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 codecs_encode_error.py strict
	
	ERROR: 'ascii' codec can't encode character '\u03c0' in position
	4: ordinal not in range(128)

.. {{{end}}}

Some of the other error modes are more flexible.  For example,
``replace`` ensures that no error is raised, at the expense of
possibly losing data that cannot be converted to the requested
encoding.  The Unicode character for pi still cannot be encoded in
ASCII, but instead of raising an exception the character is replaced
with ``?`` in the output.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_encode_error.py replace'))
.. }}}

.. code-block:: none

	$ python3 codecs_encode_error.py replace
	
	File contents: b'pi: ?'

.. {{{end}}}

To skip over problem data entirely, use ``ignore``.  Any data that
cannot be encoded is discarded.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_encode_error.py ignore'))
.. }}}

.. code-block:: none

	$ python3 codecs_encode_error.py ignore
	
	File contents: b'pi: '

.. {{{end}}}

There are two lossless error handling options, both of which replace
the character with an alternate representation defined by a standard
separate from the encoding.  ``xmlcharrefreplace`` uses an XML
character reference as a substitute (the list of character references
is specified in the W3C document *XML Entity Definitions for Characters*).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_encode_error.py xmlcharrefreplace'))
.. }}}

.. code-block:: none

	$ python3 codecs_encode_error.py xmlcharrefreplace
	
	File contents: b'pi: &#960;'

.. {{{end}}}

The other lossless error handling scheme is ``backslashreplace``, which
produces an output format like the value returned when ``repr()`` of
a ``unicode`` object is printed.  Unicode characters are replaced
with ``\u`` followed by the hexadecimal value of the code point.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_encode_error.py backslashreplace'))
.. }}}

.. code-block:: none

	$ python3 codecs_encode_error.py backslashreplace
	
	File contents: b'pi: \\u03c0'

.. {{{end}}}


Decoding Errors
---------------

It is also possible to see errors when decoding data, especially if
the wrong encoding is used.

.. literalinclude:: codecs_decode_error.py
   :caption:
   :start-after: #end_pymotw_header

As with encoding, ``strict`` error handling mode raises an exception
if the byte stream cannot be properly decoded.  In this case, a
``UnicodeDecodeError`` results from trying to convert part of the
UTF-16 BOM to a character using the UTF-8 decoder.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_decode_error.py strict', break_lines_at=66))
.. }}}

.. code-block:: none

	$ python3 codecs_decode_error.py strict
	
	Original     : 'pi: π'
	File contents: b'ff fe 70 00 69 00 3a 00 20 00 c0 03'
	ERROR: 'utf-8' codec can't decode byte 0xff in position 0: invalid
	 start byte

.. {{{end}}}

Switching to ``ignore`` causes the decoder to skip over the invalid
bytes.  The result is still not quite what is expected, though, since
it includes embedded null bytes.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_decode_error.py ignore'))
.. }}}

.. code-block:: none

	$ python3 codecs_decode_error.py ignore
	
	Original     : 'pi: π'
	File contents: b'ff fe 70 00 69 00 3a 00 20 00 c0 03'
	Read         : 'p\x00i\x00:\x00 \x00\x03'

.. {{{end}}}

In ``replace`` mode invalid bytes are replaced with ``\uFFFD``, the
official Unicode replacement character, which looks like a diamond
with a black background containing a white question mark.

.. |?| unicode:: 0xFFFD

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_decode_error.py replace'))
.. }}}

.. code-block:: none

	$ python3 codecs_decode_error.py replace
	
	Original     : 'pi: π'
	File contents: b'ff fe 70 00 69 00 3a 00 20 00 c0 03'
	Read         : '��p\x00i\x00:\x00 \x00�\x03'

.. {{{end}}}

Encoding Translation
====================

Although most applications will work with ``str`` data
internally, decoding or encoding it as part of an I/O operation, there
are times when changing a file's encoding without holding on to that
intermediate data format is useful.  ``EncodedFile()`` takes an open
file handle using one encoding and wraps it with a class that
translates the data to another encoding as the I/O occurs.

.. literalinclude:: codecs_encodedfile.py
   :caption:
   :start-after: #end_pymotw_header

This example shows reading from and writing to separate handles
returned by ``EncodedFile()``.  No matter whether the handle is used
for reading or writing, the ``file_encoding`` always refers to the
encoding in use by the open file handle passed as the first argument,
and ``data_encoding`` value refers to the encoding in use by the data
passing through the ``read()`` and ``write()`` calls.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_encodedfile.py'))
.. }}}

.. code-block:: none

	$ python3 codecs_encodedfile.py
	
	Start as UTF-8   : b'70 69 3a 20 cf 80'
	Encoded to UTF-16: b'fffe 7000 6900 3a00 2000 c003'
	Back to UTF-8    : b'70 69 3a 20 cf 80'

.. {{{end}}}


Non-Unicode Encodings
=====================

Although most of the earlier examples use Unicode encodings,
``codecs`` can be used for many other data translations.  For
example, Python includes codecs for working with base-64, bzip2,
ROT-13, ZIP, and other data formats.

.. literalinclude:: codecs_rot13.py
   :caption:
   :start-after: #end_pymotw_header

Any transformation that can be expressed as a function taking a single
input argument and returning a byte or Unicode string can be
registered as a codec. For the ``'rot_13'`` codec, the input should be
a Unicode string and the output will also be a Unicode string.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_rot13.py'))
.. }}}

.. code-block:: none

	$ python3 codecs_rot13.py
	
	Original: abcdefghijklmnopqrstuvwxyz
	ROT-13  : nopqrstuvwxyzabcdefghijklm

.. {{{end}}}

Using ``codecs`` to wrap a data stream provides a simpler interface
than working directly with :mod:`zlib`.

.. literalinclude:: codecs_zlib.py
   :caption:
   :start-after: #end_pymotw_header

Not all of the compression or encoding systems support reading a
portion of the data through the stream interface using
``readline()`` or ``read()`` because they need to find the end of
a compressed segment to expand it.  If a program cannot hold the
entire uncompressed data set in memory, use the incremental access
features of the compression library, instead of ``codecs``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_zlib.py'))
.. }}}

.. code-block:: none

	$ python3 codecs_zlib.py
	
	Original length : 1350
	ZIP compressed  : 48
	Read first line : b'abcdefghijklmnopqrstuvwxyz\n'
	Uncompressed    : 1350
	Same            : True

.. {{{end}}}

Incremental Encoding
====================

Some of the encodings provided, especially ``bz2`` and ``zlib``, may
dramatically change the length of the data stream as they work on it.
For large data sets, these encodings operate better incrementally,
working on one small chunk of data at a time.  The
``IncrementalEncoder`` and ``IncrementalDecoder`` API is
designed for this purpose.

.. literalinclude:: codecs_incremental_bz2.py
   :caption:
   :start-after: #end_pymotw_header

Each time data is passed to the encoder or decoder its internal state
is updated.  When the state is consistent (as defined by the codec),
data is returned and the state resets.  Until that point, calls to
``encode()`` or ``decode()`` will not return any data.  When the
last bit of data is passed in, the argument ``final`` should be set to
``True`` so the codec knows to flush any remaining buffered data.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_incremental_bz2.py'))
.. }}}

.. code-block:: none

	$ python3 codecs_incremental_bz2.py
	
	Text length : 27
	Repetitions : 50
	Expected len: 1350
	
	Encoding: .................................................
	Encoded : 99 bytes
	
	Total encoded length: 99
	
	Decoding: ......................................................
	..................................
	Decoded : 1350 characters
	Decoding: ..........
	
	Total uncompressed length: 1350

.. {{{end}}}

Unicode Data and Network Communication
======================================

Uetwork sockets are byte-streams, and unlike the standard input and
output streams they do not support encoding by default. That means
programs that want to send or receive Unicode data over the network
must encode into bytes before it is written to a socket.  This server
echos data it receives back to the sender.

.. literalinclude:: codecs_socket_fail.py
   :caption:
   :start-after: #end_pymotw_header

The data could be encoded explicitly before each call to ``send()``,
but missing one call to ``send()`` would result in an encoding
error.

.. Do not re-run this example every time, since it sometimes generates
.. errors within the thread that distracts from the unicode error.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_socket_fail.py', ignore_error=True))
.. }}}

.. code-block:: none

	$ python3 codecs_socket_fail.py
	
	Traceback (most recent call last):
	  File "codecs_socket_fail.py", line 43, in <module>
	    len_sent = s.send(text)
	TypeError: a bytes-like object is required, not 'str'

.. {{{end}}}

Using ``makefile()`` to get a file-like handle for the socket, and
then wrapping that with a stream-based reader or writer, means Unicode
strings will be encoded on the way in to and out of the socket.

.. literalinclude:: codecs_socket.py
   :caption:
   :start-after: #end_pymotw_header

This example uses ``PassThrough`` to show that the data is
encoded before being sent, and the response is decoded after it is
received in the client.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_socket.py'))
.. }}}

.. code-block:: none

	$ python3 codecs_socket.py
	
	Sending : 'pi: π'
	Writing : b'pi: \xcf\x80'
	Reading :
	b'pi: \xcf\x80'
	Reading :
	b''
	Received: 'pi: π'

.. {{{end}}}

Defining a Custom Encoding
==========================

Since Python comes with a large number of standard codecs already, it
is unlikely that an application will need to define a custom encoder
or decoder.  When it is necessary, though, there are several base
classes in ``codecs`` to make the process easier.

The first step is to understand the nature of the transformation
described by the encoding.  These examples will use an "invertcaps"
encoding which converts uppercase letters to lowercase, and lowercase
letters to uppercase.  Here is a simple definition of an encoding
function that performs this transformation on an input string.

.. literalinclude:: codecs_invertcaps.py
   :caption:
   :start-after: #end_pymotw_header

In this case, the encoder and decoder are the same function (as is
also the case with ``ROT-13``).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_invertcaps.py'))
.. }}}

.. code-block:: none

	$ python3 codecs_invertcaps.py
	
	abcDEF
	ABCdef

.. {{{end}}}

Although it is easy to understand, this implementation is not
efficient, especially for very large text strings.  Fortunately,
``codecs`` includes some helper functions for creating *character
map* based codecs such as invertcaps.  A character map encoding is
made up of two dictionaries.  The *encoding map* converts character
values from the input string to byte values in the output and the
*decoding map* goes the other way.  Create the decoding map first,
and then use ``make_encoding_map()`` to convert it to an encoding
map.  The C functions ``charmap_encode()`` and
``charmap_decode()`` use the maps to convert their input data
efficiently.

.. literalinclude:: codecs_invertcaps_charmap.py
   :caption:
   :start-after: #end_pymotw_header

Although the encoding and decoding maps for invertcaps are the same,
that may not always be the case.  ``make_encoding_map()`` detects
situations where more than one input character is encoded to the same
output byte and replaces the encoding value with ``None`` to mark the
encoding as undefined.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_invertcaps_charmap.py'))
.. }}}

.. code-block:: none

	$ python3 codecs_invertcaps_charmap.py
	
	(b'ABCdef', 6)
	('ABCdef', 6)
	True

.. {{{end}}}

The character map encoder and decoder support all of the standard
error handling methods described earlier, so no extra work is needed
to comply with that part of the API.

.. literalinclude:: codecs_invertcaps_error.py
   :caption:
   :start-after: #end_pymotw_header

Because the Unicode code point for ``π`` is not in the encoding map,
the strict error handling mode raises an exception.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_invertcaps_error.py', ignore_error=True, line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 codecs_invertcaps_error.py
	
	ignore : (b'PI: ', 5)
	replace: (b'PI: ?', 5)
	strict : 'charmap' codec can't encode character '\u03c0' in
	position 4: character maps to <undefined>

.. {{{end}}}

After the encoding and decoding maps are defined, a few
additional classes need to be set up, and the encoding should be
registered.  ``register()`` adds a search function to the registry
so that when a user wants to use the encoding ``codecs`` can locate
it.  The search function must take a single string argument with the
name of the encoding, and return a ``CodecInfo`` object if it
knows the encoding, or ``None`` if it does not.

.. literalinclude:: codecs_register.py
   :caption:
   :start-after: #end_pymotw_header

Multiple search functions can be registered, and each will be called
in turn until one returns a ``CodecInfo`` or the list is
exhausted.  The internal search function registered by ``codecs``
knows how to load the standard codecs such as UTF-8 from
:mod:`encodings`, so those names will never be passed to custom search
functions.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_register.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 codecs_register.py
	
	UTF-8: <codecs.CodecInfo object for encoding utf-8 at
	0x1019773a8>
	search1: Searching for: no-such-encoding
	search2: Searching for: no-such-encoding
	ERROR: unknown encoding: no-such-encoding

.. {{{end}}}

The ``CodecInfo`` instance returned by the search function tells
``codecs`` how to encode and decode using all of the different
mechanisms supported: stateless, incremental, and stream.
``codecs`` includes base classes to help with setting up a character
map encoding.  This example puts all of the pieces together to
register a search function that returns a ``CodecInfo`` instance
configured for the invertcaps codec.

.. literalinclude:: codecs_invertcaps_register.py
   :caption:
   :start-after: #end_pymotw_header

The stateless encoder/decoder base class is ``Codec``.  Override
``encode()`` and ``decode()`` with the new implementation (in this
case, calling ``charmap_encode()`` and ``charmap_decode()``
respectively).  Each method must return a tuple containing the
transformed data and the number of the input bytes or characters
consumed.  Conveniently, ``charmap_encode()`` and
``charmap_decode()`` already return that information.

``IncrementalEncoder`` and ``IncrementalDecoder`` serve as
base classes for the incremental interfaces.  The ``encode()`` and
``decode()`` methods of the incremental classes are defined in such
a way that they only return the actual transformed data.  Any
information about buffering is maintained as internal state.  The
invertcaps encoding does not need to buffer data (it uses a one-to-one
mapping).  For encodings that produce a different amount of output
depending on the data being processed, such as compression algorithms,
``BufferedIncrementalEncoder`` and
``BufferedIncrementalDecoder`` are more appropriate base classes,
since they manage the unprocessed portion of the input.

``StreamReader`` and ``StreamWriter`` need ``encode()``
and ``decode()`` methods, too, and since they are expected to return
the same value as the version from ``Codec`` multiple
inheritance can be used for the implementation.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_invertcaps_register.py'))
.. }}}

.. code-block:: none

	$ python3 codecs_invertcaps_register.py
	
	Encoded "abcDEF" to "b'ABCdef'", consuming 6 characters
	StreamWriter for io buffer: 
	  writing "abcDEF"
	  buffer contents:  b'ABCdef'
	IncrementalDecoder converted b'ABCdef' to 'abcDEF'

.. {{{end}}}


.. seealso::

   * :pydoc:`codecs`

   * :mod:`locale` -- Accessing and managing the localization-based
     configuration settings and behaviors.

   * :mod:`io` -- The ``io`` module includes file and stream wrappers
     that handle encoding and decoding, too.

   * :mod:`socketserver` -- For a more detailed example of an echo
     server, see the ``socketserver`` module.

   * :mod:`encodings` -- Package in the standard library containing
     the encoder/decoder implementations provided by Python.

   * :pep:`100` -- Python Unicode Integration PEP.

   * `Unicode HOWTO`_ -- The official guide for using Unicode with Python.

   * `Text vs. Data Instead of Unicode vs. 8-bit
     <https://docs.python.org/3.0/whatsnew/3.0.html#text-vs-data-instead-of-unicode-vs-8-bit>`__
     -- Section of the "What's New" article for Python 3.0 covering
     the text handling changes.

   * `Python Unicode Objects
     <http://effbot.org/zone/unicode-objects.htm>`_ -- Fredrik Lundh's
     article about using non-ASCII character sets in Python 2.0.

   * `How to Use UTF-8 with Python
     <http://evanjones.ca/python-utf8.html>`__ -- Evan Jones' quick
     guide to working with Unicode, including XML data and the
     Byte-Order Marker.

   * `On the Goodness of Unicode
     <http://www.tbray.org/ongoing/When/200x/2003/04/06/Unicode>`__ --
     Introduction to internationalization and Unicode by Tim Bray.

   * `On Character Strings
     <http://www.tbray.org/ongoing/When/200x/2003/04/13/Strings>`__ --
     A look at the history of string processing in programming
     languages, by Tim Bray.

   * `Characters vs. Bytes
     <http://www.tbray.org/ongoing/When/200x/2003/04/26/UTF>`__ --
     Part one of Tim Bray's "essay on modern character string
     processing for computer programmers."  This installment covers
     in-memory representation of text in formats other than ASCII
     bytes.

   * `Endianness <https://en.wikipedia.org/wiki/Endianness>`__ --
     Explanation of endianness in Wikipedia.

   * `W3C XML Entity Definitions for Characters
     <http://www.w3.org/TR/xml-entity-names/>`__ -- Specification for
     XML representations of character references that cannot be
     represented in an encoding.

.. _Unicode HOWTO: https://docs.python.org/3/howto/unicode.html
