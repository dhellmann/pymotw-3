=================
 The File System
=================

Python's standard library includes a large range of tools for working
with files on the file system, building and parsing filenames, and
examining file contents.

The first step in working with files is to determine the name of the
file to work on.  Python represents filenames as simple strings, but
provides tools for building them from standard, platform-independent,
components in :mod:`os.path`.

The :mod:`pathlib` module provides an object-oriented API for working
with file system paths. Using it instead of :mod:`os.path` provides
some conveniences because it operates at a higher level of
abstraction.

List the contents of a directory with :func:`listdir()` from
:mod:`os`, or use :mod:`glob` to build a list of filenames from a
pattern.

The file name pattern matching used by :mod:`glob` is also exposed
directly through :mod:`fnmatch` so it can be used in other contexts.

After the name of the file is identified, other characteristics, such
as permissions or the file size, can be checked using
:func:`os.stat()` and the constants in :mod:`stat`.

When an application needs random access to files, :mod:`linecache`
makes it easy to read lines by their line number.  The contents of the
file are maintained in a cache, so be careful of memory consumption.

:mod:`tempfile` is useful for cases that need to create scratch files
to hold data temporarily, or before moving it to a permanent location.
It provides classes to create temporary files and directories safely
and securely.  Names are guaranteed to be unique, and include random
components so they are not easily guessable.

Frequently, programs need to work on files as a whole, without regard
to their content.  The :mod:`shutil` module includes high-level file
operations such as copying files and directories, and setting
permissions.

The :mod:`filecmp` module compares files and directories by looking at
the bytes they contain, but without any special knowledge about their
format.

The built-in :class:`file` class can be used to read and write files
visible on local file systems.  A program's performance can suffer when
it accesses large files through the :func:`read` and :func:`write`
interfaces, though, since they both involve copying the data
multiple times as it is moved from the disk to memory the application
can see.  Using :mod:`mmap` tells the operating system to use its virtual
memory subsystem to map a file's contents directly into memory accessible
by a program, avoiding a copy step between the operating system and the
internal buffer for the :class:`file` object.

Text data using characters not available in ASCII is usually saved in
a Unicode data format.  Since the standard :class:`file` handle
assumes each byte of a text file represents one character, reading
Unicode text with multi-byte encodings requires extra processing.  The
:mod:`codecs` module handles the encoding and decoding automatically,
so that in many cases a non-ASCII file can be used without any other
changes to the program.

For testing code that depends on reading or writing data from files,
:mod:`StringIO` provides an in-memory stream object that behaves like
a file, but does not reside on disk.

.. toctree::
    :maxdepth: 1

    os.path/index
    pathlib/index
    glob/index
    fnmatch/index
    linecache/index
    filecmp/index
    mmap/index
    codecs/index

..
    ospath/index
    glob
    fnmatch/index
    pathlib/index
    linecache/index
    * tempfile/index
    * shutil/index
    filecmp/index
    mmap/index
    codecs/index
    * StringIO/index (replace with io)
