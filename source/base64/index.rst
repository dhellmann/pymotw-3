=========================================
 base64 -- Encode Binary Data with ASCII
=========================================

.. module:: base64
    :synopsis: Encode binary data with ASCII characters.

:Purpose: The base64 module contains functions for translating binary data into a subset of ASCII suitable for transmission using plaintext protocols.
:Python Version: 1.4 and later

The base64, base32, and base16 encodings convert 8 bit bytes to values
with 6, 5, or 4 bits of useful data per byte, allowing non-ASCII bytes
to be encoded as ASCII characters for transmission over protocols that
require plain ASCII, such as SMTP.  The *base* values correspond to
the length of the alphabet used in each encoding.  There are also
URL-safe variations of the original encodings that use slightly
different alphabets.

Base 64 Encoding
================

A basic example of encoding some text looks like this:

.. include:: base64_b64encode.py
    :literal:
    :start-after: #end_pymotw_header

The output shows the 168 bytes of the original source expand to 224
bytes after being encoded.

.. note::

    There are no carriage returns in the encoded data produced by the
    library, but the output has been wrapped artificially to make it
    fit better on the page.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'base64_b64encode.py', break_lines_at=65))
.. }}}

::

	$ python base64_b64encode.py
	
	168 bytes before encoding
	Expect 3 padding bytes
	224 bytes after encoding
	
	CgppbXBvcnQgYmFzZTY0CmltcG9ydCB0ZXh0d3JhcAoKIyBMb2FkIHRoaXMgc291c
	mNlIGZpbGUgYW5kIHN0cmlwIHRoZSBoZWFkZXIuCndpdGggb3BlbihfX2ZpbGVfXy
	wgJ3J0JykgYXMgaW5wdXQ6CiAgICByYXcgPSBpbnB1dC5yZWFkKCkKICAgIGluaXR
	pYWxfZGF0YSA9IHJhdy5zcGxpdCgn

.. {{{end}}}


Base 64 Decoding
================

:func:`b64decode` converts the encoded string back to the original
form by taking four bytes and converting them to the original three, using a
lookup table.

.. include:: base64_b64decode.py
    :literal:
    :start-after: #end_pymotw_header

The encoding process looks at each sequence of 24 bits in the input
(three bytes) and encodes those same 24 bits spread over four bytes in
the output.  The equal signs at the end of the output are padding
inserted because the number of bits in the original string was not
evenly divisible by 24 in this example.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'base64_b64decode.py'))
.. }}}

::

	$ python base64_b64decode.py
	
	Original: This is the data, in the clear.
	Encoded : VGhpcyBpcyB0aGUgZGF0YSwgaW4gdGhlIGNsZWFyLg==
	Decoded : This is the data, in the clear.

.. {{{end}}}

URL-safe Variations
===================

Because the default base64 alphabet may use ``+`` and ``/``, and those
two characters are used in URLs, it is often necessary to use an
alternate encoding with substitutes for those characters.  

.. include:: base64_urlsafe.py
    :literal:
    :start-after: #end_pymotw_header

The ``+`` is replaced with a ``-``, and ``/`` is replaced with
underscore (``_``).  Otherwise, the alphabet is the same.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'base64_urlsafe.py'))
.. }}}

::

	$ python base64_urlsafe.py
	
	Original         : '\xfb\xef'
	Standard encoding: ++8=
	URL-safe encoding: --8=
	
	Original         : '\xff\xff'
	Standard encoding: //8=
	URL-safe encoding: __8=
	

.. {{{end}}}


Other Encodings
===============

Besides base 64, the module provides functions for working with base
32 and base 16 (hex) encoded data.

.. include:: base64_base32.py
    :literal:
    :start-after: #end_pymotw_header

Base 32 output:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'base64_base32.py', break_lines_at=68))
.. }}}

::

	$ python base64_base32.py
	
	Original: This is the data, in the clear.
	Encoded : KRUGS4ZANFZSA5DIMUQGIYLUMEWCA2LOEB2GQZJAMNWGKYLSFY======
	Decoded : This is the data, in the clear.

.. {{{end}}}

The base 16 functions work with the hexadecimal alphabet.

.. include:: base64_base16.py
    :literal:
    :start-after: #end_pymotw_header

Each time the number of encoding bits goes down, the output in the
encoded format takes up more space.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'base64_base16.py', break_lines_at=68))
.. }}}

::

	$ python base64_base16.py
	
	Original: This is the data, in the clear.
	Encoded : 546869732069732074686520646174612C20696E2074686520636C6561
	722E
	Decoded : This is the data, in the clear.

.. {{{end}}}

.. seealso::

    `base64 <http://docs.python.org/library/base64.html>`_
        The standard library documentation for this module.

    :rfc:`3548`
        The Base16, Base32, and Base64 Data Encodings
