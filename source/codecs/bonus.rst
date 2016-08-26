Unicode Data and Network Communication
======================================

Like the standard input and output file descriptors, network sockets
are also byte-streams, and so Unicode data must be encoded into bytes
before it is written to a socket.  This server echos data it receives
back to the sender.

.. include:: codecs_socket_fail.py
   :literal:
   :start-after: #end_pymotw_header

The data could be encoded explicitly before each call to :func:`send`,
but missing one call to :func:`send` would result in an encoding
error.

.. Do not re-run this example every time, since it sometimes generates
.. errors within the thread that distracts from the unicode error.

.. cog.out(run_script(cog.inFile, 'codecs_socket_fail.py', ignore_error=True))

::

	$ python codecs_socket_fail.py
	Traceback (most recent call last):
	  File "codecs_socket_fail.py", line 43, in <module>
	    len_sent = s.send(text)
	UnicodeEncodeError: 'ascii' codec can't encode character 
     u'\u03c0' in position 4: ordinal not in range(128)


Using :func:`makefile` to get a file-like handle for the socket, and
then wrapping that with a stream-based reader or writer, means Unicode
strings will be encoded on the way in to and out of the socket.

.. include:: codecs_socket.py
   :literal:
   :start-after: #end_pymotw_header

This example uses :class:`PassThrough` to show that the data is
encoded before being sent, and the response is decoded after it is
received in the client.

.. Do not re-run this example every time, since it sometimes generates
.. errors within the thread that distracts from the unicode error.

.. cog.out(run_script(cog.inFile, 'codecs_socket.py'))

::

	$ python codecs_socket.py

	Sending : u'pi: \u03c0'
	Writing : 'pi: \xcf\x80'
	Reading : 'pi: \xcf\x80'
	Received: u'pi: \u03c0'

Defining a Custom Encoding
==========================

Since Python comes with a large number of standard codecs already, it
is unlikely that an application will need to define a custom encoder
or decoder.  When it is necessary, though, there are several base
classes in :mod:`codecs` to make the process easier.

The first step is to understand the nature of the transformation
described by the encoding.  These examples will use an "invertcaps"
encoding which converts uppercase letters to lowercase, and lowercase
letters to uppercase.  Here is a simple definition of an encoding
function that performs this transformation on an input string:

.. include:: codecs_invertcaps.py
   :literal:
   :start-after: #end_pymotw_header

In this case, the encoder and decoder are the same function (as with
``ROT-13``).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_invertcaps.py'))
.. }}}

::

	$ python codecs_invertcaps.py
	
	abc.DEF
	ABC.def

.. {{{end}}}

Although it is easy to understand, this implementation is not
efficient, especially for very large text strings.  Fortunately,
:mod:`codecs` includes some helper functions for creating *character
map* based codecs such as invertcaps.  A character map encoding is
made up of two dictionaries.  The *encoding map* converts character
values from the input string to byte values in the output and the
*decoding map* goes the other way.  Create the decoding map first,
and then use :func:`make_encoding_map` to convert it to an encoding
map.  The C functions :func:`charmap_encode` and
:func:`charmap_decode` use the maps to convert their input data
efficiently.

.. include:: codecs_invertcaps_charmap.py
   :literal:
   :start-after: #end_pymotw_header

Although the encoding and decoding maps for invertcaps are the same,
that may not always be the case.  :func:`make_encoding_map` detects
situations where more than one input character is encoded to the same
output byte and replaces the encoding value with ``None`` to mark the
encoding as undefined.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_invertcaps_charmap.py'))
.. }}}

::

	$ python codecs_invertcaps_charmap.py
	
	('ABC.def', 7)
	(u'ABC.def', 7)
	True

.. {{{end}}}

The character map encoder and decoder support all of the standard
error handling methods described earlier, so no extra work is needed
to comply with that part of the API.

.. include:: codecs_invertcaps_error.py
   :literal:
   :start-after: #end_pymotw_header

Because the Unicode code point for ``π`` is not in the encoding map,
the strict error handling mode raises an exception.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_invertcaps_error.py', ignore_error=True, break_lines_at=69))
.. }}}

::

	$ python codecs_invertcaps_error.py
	
	ignore : ('PI: ', 5)
	replace: ('PI: ?', 5)
	strict : 'charmap' codec can't encode character u'\u03c0' in position
	 4: character maps to <undefined>

.. {{{end}}}

After the encoding and decoding maps are defined, a few
additional classes need to be set up, and the encoding should be
registered.  :func:`register` adds a search function to the registry
so that when a user wants to use the encoding :mod:`codecs` can locate
it.  The search function must take a single string argument with the
name of the encoding, and return a :class:`CodecInfo` object if it
knows the encoding, or ``None`` if it does not.

.. include:: codecs_register.py
   :literal:
   :start-after: #end_pymotw_header

Multiple search functions can be registered, and each will be called
in turn until one returns a :class:`CodecInfo` or the list is
exhausted.  The internal search function registered by :mod:`codecs`
knows how to load the standard codecs such as UTF-8 from
:mod:`encodings`, so those names will never be passed to custom search
functions.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_register.py'))
.. }}}

::

	$ python codecs_register.py
	
	UTF-8: <codecs.CodecInfo object for encoding utf-8 at 0x100d0f530>
	search1: Searching for: no-such-encoding
	search2: Searching for: no-such-encoding
	ERROR: unknown encoding: no-such-encoding

.. {{{end}}}

The :class:`CodecInfo` instance returned by the search function tells
:mod:`codecs` how to encode and decode using all of the different
mechanisms supported: stateless, incremental, and stream.
:mod:`codecs` includes base classes to help with setting up a character
map encoding.  This example puts all of the pieces together to
register a search function that returns a :class:`CodecInfo` instance
configured for the invertcaps codec.

.. include:: codecs_invertcaps_register.py
   :literal:
   :start-after: #end_pymotw_header

The stateless encoder/decoder base class is :class:`Codec`.  Override
:func:`encode` and :func:`decode` with the new implementation (in this
case, calling :func:`charmap_encode` and :func:`charmap_decode`
respectively).  Each method must return a tuple containing the
transformed data and the number of the input bytes or characters
consumed.  Conveniently, :func:`charmap_encode` and
:func:`charmap_decode` already return that information.

:class:`IncrementalEncoder` and :class:`IncrementalDecoder` serve as
base classes for the incremental interfaces.  The :func:`encode` and
:func:`decode` methods of the incremental classes are defined in such
a way that they only return the actual transformed data.  Any
information about buffering is maintained as internal state.  The
invertcaps encoding does not need to buffer data (it uses a one-to-one
mapping).  For encodings that produce a different amount of output
depending on the data being processed, such as compression algorithms,
:class:`BufferedIncrementalEncoder` and
:class:`BufferedIncrementalDecoder` are more appropriate base classes,
since they manage the unprocessed portion of the input.

:class:`StreamReader` and :class:`StreamWriter` need :func:`encode`
and :func:`decode` methods, too, and since they are expected to return
the same value as the version from :class:`Codec` multiple
inheritance can be used for the implementation.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'codecs_invertcaps_register.py'))
.. }}}

::

	$ python codecs_invertcaps_register.py
	
	Encoded "abc.DEF" to "ABC.def", consuming 7 characters
	StreamWriter for stdout: ABC.def
	IncrementalDecoder converted "ABC.def" to "abc.DEF"

.. {{{end}}}
