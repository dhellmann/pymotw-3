==========================
 mmap -- Memory-map files
==========================

.. module:: mmap
    :synopsis: Memory-map files

:Purpose: Memory-map files instead of reading the contents directly.
:Available In: 2.1 and later

Memory-mapping a file uses the operating system virtual memory system
to access the data on the filesystem directly, instead of using normal
I/O functions.  Memory-mapping typically improves I/O performance
because it does not involve a separate system call for each access and
it does not require copying data between buffers -- the memory is
accessed directly.

Memory-mapped files can be treated as mutable strings or file-like
objects, depending on your need. A mapped file supports the expected
file API methods, such as :func:`close`, :func:`flush`, :func:`read`,
:func:`readline`, :func:`seek`, :func:`tell`, and :func:`write`. It
also supports the string API, with features such as slicing and
methods like :func:`find`.

All of the examples use the text file ``lorem.txt``, containing a bit
of Lorem Ipsum. For reference, the text of the file is:

.. include:: lorem.txt
    :literal:

.. note::

  There are differences in the arguments and behaviors for
  :func:`mmap` between Unix and Windows, which are not discussed
  below. For more details, refer to the standard library
  documentation.

Reading
=======

Use the :func:`mmap` function to create a memory-mapped file.  The
first argument is a file descriptor, either from the :func:`fileno`
method of a :class:`file` object or from :func:`os.open`. The caller
is responsible for opening the file before invoking :func:`mmap`, and
closing it after it is no longer needed.

The second argument to :func:`mmap` is a size in bytes for the portion
of the file to map. If the value is ``0``, the entire file is
mapped. If the size is larger than the current size of the file, the
file is extended.

.. note::

  You cannot create a zero-length mapping under Windows. 

An optional keyword argument, *access*, is supported by both
platforms. Use :const:`ACCESS_READ` for read-only access,
:const:`ACCESS_WRITE` for write-through (assignments to the memory go
directly to the file), or :const:`ACCESS_COPY` for copy-on-write
(assignments to memory are not written to the file).

.. include:: mmap_read.py
    :literal:
    :start-after: #end_pymotw_header

The file pointer tracks the last byte accessed through a slice
operation.  In this example, the pointer moves ahead 10 bytes after
the first read.  It is then reset to the beginning of the file by the
slice operation, and moved ahead 10 bytes again by the slice.  After
the slice operation, calling :func:`read` again gives the bytes 11-20
in the file.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'mmap_read.py'))
.. }}}

::

	$ python mmap_read.py
	
	First 10 bytes via read : Lorem ipsu
	First 10 bytes via slice: Lorem ipsu
	2nd   10 bytes via read : m dolor si

.. {{{end}}}

Writing
=======

To set up the memory mapped file to receive updates, start by opening
it for appending with mode ``'r+'`` (not ``'w'``) before mapping
it. Then use any of the API method that change the data
(:func:`write`, assignment to a slice, etc.).

Here's an example using the default access mode of
:const:`ACCESS_WRITE` and assigning to a slice to modify part of a
line in place:

.. include:: mmap_write_slice.py
    :literal:
    :start-after: #end_pymotw_header

The word "consectetuer" is replaced in the middle of the first line:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'mmap_write_slice.py'))
.. }}}

::

	$ python mmap_write_slice.py
	
	Looking for    : consectetuer
	Replacing with : reutetcesnoc
	Before: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec
	After : Lorem ipsum dolor sit amet, reutetcesnoc adipiscing elit. Donec

.. {{{end}}}

ACCESS_COPY Mode
----------------

Using the access setting :const:`ACCESS_COPY` does not write changes
to the file on disk.

.. include:: mmap_write_copy.py
    :literal:
    :start-after: #end_pymotw_header

It is necessary to rewind the file handle in this example separately
from the mmap handle because the internal state of the two objects is
maintained separately.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'mmap_write_copy.py'))
.. }}}

::

	$ python mmap_write_copy.py
	
	Memory Before: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec
	File Before  : Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec
	
	Memory After : Lorem ipsum dolor sit amet, reutetcesnoc adipiscing elit. Donec
	File After   : Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec

.. {{{end}}}

Regular Expressions
===================

Since a memory mapped file can act like a string, it can be used with
other modules that operate on strings, such as regular
expressions. This example finds all of the sentences with "nulla" in
them.

.. include:: mmap_regex.py
    :literal:
    :start-after: #end_pymotw_header

Because the pattern includes two groups, the return value from
:func:`findall` is a sequence of tuples. The :command:`print`
statement pulls out the sentence match and replaces newlines with
spaces so the result prints on a single line.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'mmap_regex.py'))
.. }}}

::

	$ python mmap_regex.py
	
	Nulla facilisi.
	Nulla feugiat augue eleifend nulla.

.. {{{end}}}


.. seealso::

    `mmap <https://docs.python.org/2/library/mmap.html>`_
        Standard library documentation for this module.

    :mod:`os`
        The os module.

    :mod:`contextlib`
        Use the :func:`closing` function to create a context manager
        for a memory mapped file.

    :mod:`re`
        Regular expressions.
