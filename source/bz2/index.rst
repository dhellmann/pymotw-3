==========================
 bz2 -- bzip2 Compression
==========================

.. module:: bz2
    :synopsis: bzip2 compression

:Purpose: bzip2 compression
:Python Version: 2.3 and later

The :mod:`bz2` module is an interface for the bzip2 library, used to
compress data for storage or transmission.  There are three APIs
provided:

- "one shot" compression/decompression functions for operating on a
  blob of data
- iterative compression/decompression objects for working with streams
  of data
- a file-like class that supports reading and writing as with an
  uncompressed file

.. toctree::

   normal

.. only:: bonus

   .. toctree::

      bonus

.. seealso::

    `bz2 <http://docs.python.org/library/bz2.html>`_
        The standard library documentation for this module.

    `bzip2.org <http://www.bzip.org/>`_
        The home page for :command:`bzip2`.

    :mod:`zlib`
        The ``zlib`` module for GNU zip compression.

    :mod:`gzip`
        A file-like interface to GNU zip compressed files.
