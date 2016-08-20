================================
 Data Compression and Archiving
================================

Although modern computer systems have an ever increasing storage
capacity, the growth of data being produced is unrelenting.  Lossless
compression algorithms make up for some of the shortfall in capacity
by trading time spent compressing or decompressing data for the space
needed to store it.  Python includes interfaces to the most popular
compression libraries so it can read and write files interchangeably.

:mod:`zlib` and :mod:`gzip` expose the GNU zip library, and :mod:`bz2`
provides access to the more recent bzip2 format.  Both formats work on
streams of data, without regard to input format, and provide
interfaces for reading and writing compressed files transparently.
Use these modules for compressing a single file or data source.

The standard library also includes modules to manage *archive*
formats, for combining several files into a single file that can be
managed as a unit.  :mod:`tarfile` reads and writes the UNIX tape
archive format, an old standard still widely used today because of its
flexibility.  :mod:`zipfile` works with archives based on the format
popularized by the PC program PKZIP, originally used under MS-DOS and
Windows, but now also used on other platforms because of the
simplicity of its API and portability of the format.

.. toctree::
   :maxdepth: 1

   zlib/index
   gzip/index
   bz2/index
   tarfile/index
   zipfile/index
