Unicode Primer
==============

CPython 2.x supports two types of strings for working with text data.
Old-style :class:`str` instances use a single 8-bit byte to represent
each character of the string using its ASCII code.  In contrast,
:class:`unicode` strings are managed internally as a sequence of
Unicode *code points*.  The code point values are saved as a sequence
of 2 or 4 bytes each, depending on the options given when Python was
compiled.  Both :class:`unicode` and :class:`str` are derived from a
common base class, and support a similar API.

When :class:`unicode` strings are output, they are encoded using one
of several standard schemes so that the sequence of bytes can be
reconstructed as the same string of text later.  The bytes of the encoded
value are not necessarily the same as the code point values, and the
encoding defines a way to translate between the two sets of values.
Reading Unicode data also requires knowing the encoding so that the
incoming bytes can be converted to the internal representation used by
the :class:`unicode` class.

The most common encodings for Western languages are ``UTF-8`` and
``UTF-16``, which use sequences of one and two byte values
respectively to represent each code point.  Other encodings can be more
efficient for storing languages where most of the characters are
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
of the input byte string, then insert a space between every *nbytes*
bytes before returning the value.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_to_hex.py'))
.. }}}

::

	$ python codecs_to_hex.py
	
	61 62 63 64 65 66
	6162 6364 6566

.. {{{end}}}

The first encoding example begins by printing the text ``'pi: π'``
using the raw representation of the :class:`unicode` class.  The ``π``
character is replaced with the expression for its Unicode code point,
``\u03c0``.  The next two lines encode the string as UTF-8 and UTF-16
respectively, and show the hexadecimal values resulting from the
encoding.

.. literalinclude:: codecs_encodings.py
   :caption:
   :start-after: #end_pymotw_header

The result of encoding a :class:`unicode` string is a :class:`str`
object.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_encodings.py'))
.. }}}

::

	$ python codecs_encodings.py
	
	Raw   : u'pi: \u03c0'
	UTF-8 : 70 69 3a 20 cf 80
	UTF-16: fffe 7000 6900 3a00 2000 c003

.. {{{end}}}

Given a sequence of encoded bytes as a :class:`str` instance, the
:func:`decode` method translates them to code points and returns the
sequence as a :class:`unicode` instance.

.. literalinclude:: codecs_decode.py
   :caption:
   :start-after: #end_pymotw_header

The choice of encoding used does not change the output type.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_decode.py'))
.. }}}

::

	$ python codecs_decode.py
	
	Original : u'pi: \u03c0'
	Encoded  : 70 69 3a 20 cf 80 <type 'str'>
	Decoded  : u'pi: \u03c0' <type 'unicode'>

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
:mod:`codecs` provides classes that manage the data encoding and
decoding, so applications do not have to do that work.

The simplest interface provided by :mod:`codecs` is a replacement for
the built-in :func:`open` function.  The new version works just like
the built-in, but adds two new arguments to specify the encoding and
desired error handling technique.

.. literalinclude:: codecs_open_write.py
   :caption:
   :start-after: #end_pymotw_header

This example starts with a :class:`unicode` string with the code point
for π and saves the text to a file using an encoding specified on the
command line.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_open_write.py utf-8'))
.. cog.out(run_script(cog.inFile, 'codecs_open_write.py utf-16', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'codecs_open_write.py utf-32', include_prefix=False))
.. }}}

::

	$ python codecs_open_write.py utf-8
	
	Writing to utf-8.txt
	File contents:
	70 69 3a 20 cf 80

	$ python codecs_open_write.py utf-16
	
	Writing to utf-16.txt
	File contents:
	fffe 7000 6900 3a00 2000 c003

	$ python codecs_open_write.py utf-32
	
	Writing to utf-32.txt
	File contents:
	fffe0000 70000000 69000000 3a000000 20000000 c0030000

.. {{{end}}}

Reading the data with :func:`open` is straightforward, with one catch:
the encoding must be known in advance, in order to set up the decoder
correctly.  Some data formats, such as XML, specify the encoding as
part of the file, but usually it is up to the application to manage.
:mod:`codecs` simply takes the encoding as an argument and assumes it
is correct.

.. literalinclude:: codecs_open_read.py
   :caption:
   :start-after: #end_pymotw_header

This example reads the files created by the previous program, and
prints the representation of the resulting :class:`unicode` object to
the console.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_open_read.py utf-8'))
.. cog.out(run_script(cog.inFile, 'codecs_open_read.py utf-16', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'codecs_open_read.py utf-32', include_prefix=False))
.. }}}

::

	$ python codecs_open_read.py utf-8
	
	Reading from utf-8.txt
	u'pi: \u03c0'

	$ python codecs_open_read.py utf-16
	
	Reading from utf-16.txt
	u'pi: \u03c0'

	$ python codecs_open_read.py utf-32
	
	Reading from utf-32.txt
	u'pi: \u03c0'

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
used to indicate the byte order.  :mod:`codecs` defines constants for
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

::

	$ python codecs_bom.py
	
	BOM          : fffe
	BOM_BE       : feff
	BOM_LE       : fffe
	BOM_UTF8     : efbb bf
	BOM_UTF16    : fffe
	BOM_UTF16_BE : feff
	BOM_UTF16_LE : fffe
	BOM_UTF32    : fffe 0000
	BOM_UTF32_BE : 0000 feff
	BOM_UTF32_LE : fffe 0000

.. {{{end}}}

Byte ordering is detected and handled automatically by the decoders in
:mod:`codecs`, but an explicit ordering can be specified when
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

::

	$ python codecs_bom_create_file.py
	
	Native order  : fffe
	Selected order: feff
	utf_16_be     : 0070 0069 003a 0020 03c0

.. {{{end}}}

``codecs_bom_detection.py`` does not specify a byte order when opening
the file, so the decoder uses the BOM value in the first two bytes of
the file to determine it.

.. literalinclude:: codecs_bom_detection.py
   :caption:
   :start-after: #end_pymotw_header

Since the first two bytes of the file are used for byte order
detection, they are not included in the data returned by :func:`read`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_bom_detection.py'))
.. }}}

::

	$ python codecs_bom_detection.py
	
	Raw    : feff 0070 0069 003a 0020 03c0
	Decoded: u'pi: \u03c0'

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

:mod:`codecs` uses the same five error handling options that are
provided by the :func:`encode` method of :class:`unicode` and the
:func:`decode` method of :class:`str`, listed in :table:`Codec Error
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
:class:`UnicodeEncodeError` when writing Unicode data to an ASCII
output stream, such as a regular file or :data:`sys.stdout`.  This
sample program can be used to experiment with the different error
handling modes.

.. literalinclude:: codecs_encode_error.py
   :caption:
   :start-after: #end_pymotw_header

While ``strict`` mode is safest for ensuring an application explicitly
sets the correct encoding for all I/O operations, it can lead to
program crashes when an exception is raised.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_encode_error.py strict', break_lines_at=69))
.. }}}

::

	$ python codecs_encode_error.py strict
	
	ERROR: 'ascii' codec can't encode character u'\u03c0' in position 4: 
	ordinal not in range(128)

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

::

	$ python codecs_encode_error.py replace
	
	File contents: 'pi: ?'

.. {{{end}}}

To skip over problem data entirely, use ``ignore``.  Any data that
cannot be encoded is discarded.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_encode_error.py ignore'))
.. }}}

::

	$ python codecs_encode_error.py ignore
	
	File contents: 'pi: '

.. {{{end}}}

There are two lossless error handling options, both of which replace
the character with an alternate representation defined by a standard
separate from the encoding.  ``xmlcharrefreplace`` uses an XML
character reference as a substitute (the list of character references
is specified in the W3C document *XML Entity Definitions for Characters*).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_encode_error.py xmlcharrefreplace'))
.. }}}

::

	$ python codecs_encode_error.py xmlcharrefreplace
	
	File contents: 'pi: &#960;'

.. {{{end}}}

The other lossless error handling scheme is ``backslashreplace``, which
produces an output format like the value returned when :func:`repr` of
a :class:`unicode` object is printed.  Unicode characters are replaced
with ``\u`` followed by the hexadecimal value of the code point.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_encode_error.py backslashreplace'))
.. }}}

::

	$ python codecs_encode_error.py backslashreplace
	
	File contents: 'pi: \\u03c0'

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
:class:`UnicodeDecodeError` results from trying to convert part of the
UTF-16 BOM to a character using the UTF-8 decoder.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_decode_error.py strict', break_lines_at=66))
.. }}}

::

	$ python codecs_decode_error.py strict
	
	Original     : u'pi: \u03c0'
	File contents: ff fe 70 00 69 00 3a 00 20 00 c0 03
	ERROR: 'utf8' codec can't decode byte 0xff in position 0: invalid 
	start byte

.. {{{end}}}

Switching to ``ignore`` causes the decoder to skip over the invalid
bytes.  The result is still not quite what is expected, though, since
it includes embedded null bytes.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_decode_error.py ignore'))
.. }}}

::

	$ python codecs_decode_error.py ignore
	
	Original     : u'pi: \u03c0'
	File contents: ff fe 70 00 69 00 3a 00 20 00 c0 03
	Read         : u'p\x00i\x00:\x00 \x00\x03'

.. {{{end}}}

In ``replace`` mode invalid bytes are replaced with ``\uFFFD``, the
official Unicode replacement character, which looks like a diamond
with a black background containing a white question mark.

.. |?| unicode:: 0xFFFD

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_decode_error.py replace'))
.. }}}

::

	$ python codecs_decode_error.py replace
	
	Original     : u'pi: \u03c0'
	File contents: ff fe 70 00 69 00 3a 00 20 00 c0 03
	Read         : u'\ufffd\ufffdp\x00i\x00:\x00 \x00\ufffd\x03'

.. {{{end}}}

Standard Input and Output Streams
=================================

The most common cause of :class:`UnicodeEncodeError` exceptions is
code that tries to print :class:`unicode` data to the console or a
Unix pipeline when :data:`sys.stdout` is not configured with an
encoding.

.. literalinclude:: codecs_stdout.py
   :caption:
   :start-after: #end_pymotw_header

Problems with the default encoding of the standard I/O channels can be
difficult to debug because the program frequently works as expected when the
output goes to the console, but causes an encoding error when it is used
as part of a pipeline and the output includes Unicode characters
outside of the ASCII range.  This difference in behavior is caused by
Python's initialization code, which sets the default encoding for each
standard I/O channel *only if* the channel is connected to a terminal
(:func:`isatty` returns ``True``).  If there is no terminal, Python
assumes the program will configure the encoding explicitly, and leaves
the I/O channel alone.

.. Do not use cog, since it never has a TTY.

::

	$ python codecs_stdout.py 

	Default encoding: utf-8
	TTY: True
	pi: π

	$ python codecs_stdout.py | cat -

	Default encoding: None
	TTY: False
	Traceback (most recent call last):
	  File "codecs_stdout.py", line 18, in <module>
	    print text
	UnicodeEncodeError: 'ascii' codec can't encode character 
     u'\u03c0' in position 4: ordinal not in range(128)

To explicitly set the encoding on the standard output channel, use
:func:`getwriter` to get a stream encoder class for a specific
encoding.  Instantiate the class, passing ``sys.stdout`` as the only
argument.

.. literalinclude:: codecs_stdout_wrapped.py
   :caption:
   :start-after: #end_pymotw_header

Writing to the wrapped version of ``sys.stdout`` passes the Unicode
text through an encoder before sending the encoded bytes to stdout.
Replacing ``sys.stdout`` means that any code used by an application
that prints to standard output will be able to take advantage of the
encoding writer.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_stdout_wrapped.py'))
.. }}}

::

	$ python codecs_stdout_wrapped.py
	
	Via write: pi: π
	Via print: pi: π

.. {{{end}}}

The next problem to solve is how to know which encoding should be
used.  The proper encoding varies based on location, language, and
user or system configuration, so hard-coding a fixed value is not a
good idea.  It would also be annoying for a user to need to pass
explicit arguments to every program setting the input and output
encodings.  Fortunately, there is a global way to get a reasonable
default encoding using :mod:`locale`.

.. literalinclude:: codecs_stdout_locale.py
   :caption:
   :start-after: #end_pymotw_header

The function :func:`locale.getdefaultlocale` returns the language and
preferred encoding based on the system and user configuration settings
in a form that can be used with :func:`getwriter`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_stdout_locale.py'))
.. }}}

::

	$ python codecs_stdout_locale.py
	
	Locale encoding    : UTF8
	With wrapped stdout: pi: π

.. {{{end}}}

The encoding also needs to be set up when working with
:data:`sys.stdin`.  Use :func:`getreader` to get a reader capable of
decoding the input bytes.

.. literalinclude:: codecs_stdin.py
   :caption:
   :start-after: #end_pymotw_header

Reading from the wrapped handle returns :class:`unicode` objects
instead of :class:`str` instances.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_stdout_locale.py | python codecs_stdin.py'))
.. }}}

::

	$ python codecs_stdout_locale.py | python codecs_stdin.py
	
	From stdin:
	u'Locale encoding    : UTF8\nWith wrapped stdout: pi: \u03c0\n'

.. {{{end}}}

Encoding Translation
====================

Although most applications will work with :class:`unicode` data
internally, decoding or encoding it as part of an I/O operation, there
are times when changing a file's encoding without holding on to that
intermediate data format is useful.  :func:`EncodedFile` takes an open
file handle using one encoding and wraps it with a class that
translates the data to another encoding as the I/O occurs.

.. literalinclude:: codecs_encodedfile.py
   :caption:
   :start-after: #end_pymotw_header

This example shows reading from and writing to separate handles
returned by :func:`EncodedFile`.  No matter whether the handle is used
for reading or writing, the *file_encoding* always refers to the
encoding in use by the open file handle passed as the first argument,
and *data_encoding* value refers to the encoding in use by the data
passing through the :func:`read` and :func:`write` calls.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_encodedfile.py'))
.. }}}

::

	$ python codecs_encodedfile.py
	
	Start as UTF-8   : 70 69 3a 20 cf 80
	Encoded to UTF-16: fffe 7000 6900 3a00 2000 c003
	Back to UTF-8    : 70 69 3a 20 cf 80

.. {{{end}}}


Non-Unicode Encodings
=====================

Although most of the earlier examples use Unicode encodings,
:mod:`codecs` can be used for many other data translations.  For
example, Python includes codecs for working with base-64, bzip2,
ROT-13, ZIP, and other data formats.

.. literalinclude:: codecs_rot13.py
   :caption:
   :start-after: #end_pymotw_header

Any transformation that can be expressed as a function taking a single
input argument and returning a byte or Unicode string can be
registered as a codec.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_rot13.py'))
.. }}}

::

	$ python codecs_rot13.py
	
	Original: abcdefghijklmnopqrstuvwxyz
	ROT-13  : nopqrstuvwxyzabcdefghijklm

.. {{{end}}}

Using :mod:`codecs` to wrap a data stream provides a simpler interface
than working directly with :mod:`zlib`.

.. literalinclude:: codecs_zlib.py
   :caption:
   :start-after: #end_pymotw_header

Not all of the compression or encoding systems support reading a
portion of the data through the stream interface using
:func:`readline` or :func:`read` because they need to find the end of
a compressed segment to expand it.  If a program cannot hold the
entire uncompressed data set in memory, use the incremental access
features of the compression library, instead of :mod:`codecs`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_zlib.py'))
.. }}}

::

	$ python codecs_zlib.py
	
	Original length : 1350
	ZIP compressed  : 48
	Read first line : 'abcdefghijklmnopqrstuvwxyz\n'
	Uncompressed    : 1350
	Same            : True

.. {{{end}}}

Incremental Encoding
====================

Some of the encodings provided, especially ``bz2`` and ``zlib``, may
dramatically change the length of the data stream as they work on it.
For large data sets, these encodings operate better incrementally,
working on one small chunk of data at a time.  The
:class:`IncrementalEncoder` and :class:`IncrementalDecoder` API is
designed for this purpose.

.. literalinclude:: codecs_incremental_bz2.py
   :caption:
   :start-after: #end_pymotw_header

Each time data is passed to the encoder or decoder its internal state
is updated.  When the state is consistent (as defined by the codec),
data is returned and the state resets.  Until that point, calls to
:func:`encode` or :func:`decode` will not return any data.  When the
last bit of data is passed in, the argument *final* should be set to
``True`` so the codec knows to flush any remaining buffered data.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_incremental_bz2.py', break_lines_at=69))
.. }}}

::

	$ python codecs_incremental_bz2.py
	
	Text length : 27
	Repetitions : 50
	Expected len: 1350
	
	Encoding:.................................................
	Encoded : 99 bytes
	
	Total encoded length: 99
	
	Decoding:............................................................
	............................
	Decoded : 1350 characters
	Decoding:..........
	
	Total uncompressed length: 1350

.. {{{end}}}
