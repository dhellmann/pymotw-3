==========================================
 base64 --- Encode Binary Data with ASCII
==========================================

.. module:: base64
    :synopsis: Encode binary data with ASCII characters.

The ``base64`` module contains functions for translating binary
data into a subset of ASCII suitable for transmission using plaintext
protocols. The base64, base32, base16, and base85 encodings convert 8
bit bytes to values that fit inside the ASCII range of printable
characters, trading more bits to represent the data for compatibility
with systems that only support ASCII data, such as SMTP.  The *base*
values correspond to the length of the alphabet used in each encoding.
There are also URL-safe variations of the original encodings that use
slightly different alphabets.

Base 64 Encoding
================

This is a basic example of encoding some text.

.. literalinclude:: base64_b64encode.py
    :caption:
    :start-after: #end_pymotw_header

The input must be a byte string, so the unicode string is first
encoded to UTF-8. The output shows the 185 bytes of the UTF-8 source
expand to 248 bytes after being encoded.

.. note::

    There are no carriage returns in the encoded data produced by the
    library, but the output has been wrapped artificially to make it
    fit better on the page.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'base64_b64encode.py'))
.. }}}

.. code-block:: none

	$ python3 base64_b64encode.py
	
	185 bytes before encoding
	Expect 1 padding bytes
	248 bytes after encoding
	
	b'CgppbXBvcnQgYmFzZTY0CmltcG9ydCB0ZXh0d3JhcAoKIyBMb2FkIHRoaXMgc2
	91cmNlIGZpbGUgYW5kIHN0cmlwIHRoZSBoZWFkZXIuCndpdGggb3BlbihfX2ZpbG
	VfXywgJ3InLCBlbmNvZGluZz0ndXRmLTgnKSBhcyBpbnB1dDoKICAgIHJhdyA9IG
	lucHV0LnJlYWQoKQogICAgaW5pdGlhbF9kYXRhID0gcmF3LnNwbGl0KCc='

.. {{{end}}}


Base 64 Decoding
================

:func:`b64decode` converts an encoded string back to the original
form by taking four bytes and converting them to the original three, using a
lookup table.

.. literalinclude:: base64_b64decode.py
    :caption:
    :start-after: #end_pymotw_header

The encoding process looks at each sequence of 24 bits in the input
(three bytes) and encodes those same 24 bits spread over four bytes in
the output.  The equal signs at the end of the output are padding
inserted because the number of bits in the original string was not
evenly divisible by 24, in this example.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'base64_b64decode.py'))
.. }}}

.. code-block:: none

	$ python3 base64_b64decode.py
	
	Encoded : b'VGhpcyBpcyB0aGUgZGF0YSwgaW4gdGhlIGNsZWFyLg=='
	Decoded : b'This is the data, in the clear.'

.. {{{end}}}

The value returned from :func:`b64decode` is a byte string. If the
contents are known to be text, the byte string can be converted to a
unicode object. However, the point of using base 64 encoding is to be
able to transmit binary data, and so it is not always safe to assume
that the decoded value is text.

URL-safe Variations
===================

Because the default base64 alphabet may use ``+`` and ``/``, and those
two characters are used in URLs, it is often necessary to use an
alternate encoding with substitutes for those characters.

.. literalinclude:: base64_urlsafe.py
    :caption:
    :start-after: #end_pymotw_header

The ``+`` is replaced with a ``-``, and ``/`` is replaced with
underscore (``_``).  Otherwise, the alphabet is the same.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'base64_urlsafe.py'))
.. }}}

.. code-block:: none

	$ python3 base64_urlsafe.py
	
	Original         : b'\xfb\xef'
	Standard encoding: b'++8='
	URL-safe encoding: b'--8='
	
	Original         : b'\xff\xff'
	Standard encoding: b'//8='
	URL-safe encoding: b'__8='
	

.. {{{end}}}


Other Encodings
===============

Besides Base64, the module provides functions for working with Base85,
Base32, and Base16 (hex) encoded data.

.. literalinclude:: base64_base32.py
    :caption:
    :start-after: #end_pymotw_header

The Base32 alphabet includes the 26 uppercase letters from the ASCII
set and the digits 2 through 7.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'base64_base32.py'))
.. }}}

.. code-block:: none

	$ python3 base64_base32.py
	
	Original: b'This is the data, in the clear.'
	Encoded : b'KRUGS4ZANFZSA5DIMUQGIYLUMEWCA2LOEB2GQZJAMNWGKYLSFY==
	===='
	Decoded : b'This is the data, in the clear.'

.. {{{end}}}

The Base16 functions work with the hexadecimal alphabet.

.. literalinclude:: base64_base16.py
    :caption:
    :start-after: #end_pymotw_header

Each time the number of encoding bits goes down, the output in the
encoded format takes up more space.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'base64_base16.py'))
.. }}}

.. code-block:: none

	$ python3 base64_base16.py
	
	Original: b'This is the data, in the clear.'
	Encoded : b'546869732069732074686520646174612C20696E207468652063
	6C6561722E'
	Decoded : b'This is the data, in the clear.'

.. {{{end}}}

The Base85 functions use an expanded alphabet that is more
space-efficient than base 64.

.. literalinclude:: base64_base85.py
   :caption:
   :start-after: #end_pymotw_header

There are several Base85 encodings and different variations are used
in Mercurial, git, and the PDF file format. Python includes two
implementations, :func:`b85encode` implements the version used in Git
and Mercurial while :func:`a85encode` implements the Ascii85 variant
used by PDF files.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'base64_base85.py'))
.. }}}

.. code-block:: none

	$ python3 base64_base85.py
	
	Original    : 31 bytes b'This is the data, in the clear.'
	b64 Encoded : 44 bytes b'VGhpcyBpcyB0aGUgZGF0YSwgaW4gdGhlIGNsZWF
	yLg=='
	b85 Encoded : 39 bytes b'RA^~)AZc?TbZBKDWMOn+EFfuaAarPDAY*K0VR9}
	'
	a85 Encoded : 39 bytes b'<+oue+DGm>FD,5.A79Rg/0JYE+EV:.+Cf5!@<*t
	'

.. {{{end}}}

.. seealso::

    * :pydoc:`base64`

    * :rfc:`3548` -- The Base16, Base32, and Base64 Data Encodings

    * :rfc:`1924` -- A Compact Representation of IPv6 Addresses
      (suggests base-85 encoding for IPv6 network addresses)

    * `Ascii85 <https://en.wikipedia.org/wiki/Ascii85>`__

    * :ref:`Porting notes for base64 <porting-base64>`
