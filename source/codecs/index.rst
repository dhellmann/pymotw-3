========================================
 codecs -- String Encoding and Decoding
========================================

.. module:: codecs
    :synopsis: String encoding and decoding.

:Purpose: Encoders and decoders for converting text between different representations.
:Python Version: 2.1 and later

The :mod:`codecs` module provides stream and file interfaces for
transcoding data.  It is most commonly used to work with Unicode text,
but other encodings are also available for other purposes.

.. toctree::

   normal

.. only:: bonus

   .. toctree:: 

      bonus

.. seealso::

    `codecs <http://docs.python.org/library/codecs.html>`_
        The standard library documentation for this module.

    :mod:`locale`
        Accessing and managing the localization-based configuration
        settings and behaviors.

    :mod:`io`
        The ``io`` module includes file and stream wrappers that
        handle encoding and decoding, too.

    :mod:`SocketServer`
        For a more detailed example of an echo server, see the
        ``SocketServer`` module.

    :mod:`encodings`
        Package in the standard library containing the encoder/decoder
        implementations provided by Python.

    :pep:`100`
        Python Unicode Integration PEP.

    `Unicode HOWTO`_
        The official guide for using Unicode with Python 2.x.

    `Python Unicode Objects <http://effbot.org/zone/unicode-objects.htm>`_
        Fredrik Lundh's article about using non-ASCII character sets
        in Python 2.0.

    `How to Use UTF-8 with Python <http://evanjones.ca/python-utf8.html>`_
        Evan Jones' quick guide to working with Unicode, including XML
        data and the Byte-Order Marker.

    `On the Goodness of Unicode <http://www.tbray.org/ongoing/When/200x/2003/04/06/Unicode>`_
        Introduction to internationalization and Unicode by Tim Bray.

    `On Character Strings <http://www.tbray.org/ongoing/When/200x/2003/04/13/Strings>`_
        A look at the history of string processing in programming
        languages, by Tim Bray.

    `Characters vs. Bytes <http://www.tbray.org/ongoing/When/200x/2003/04/26/UTF>`_
        Part one of Tim Bray's "essay on modern character string
        processing for computer programmers."  This installment covers
        in-memory representation of text in formats other than ASCII
        bytes.

    `Endianness <http://en.wikipedia.org/wiki/Endianness>`_
        Explanation of endianness in Wikipedia.

    `W3C XML Entity Definitions for Characters <http://www.w3.org/TR/xml-entity-names/>`__
        Specification for XML representations of character references
        that cannot be represented in an encoding.

.. _Unicode HOWTO: http://docs.python.org/howto/unicode
