================================
 tarfile --- Tar Archive Access
================================

.. module:: tarfile
    :synopsis: Tar archive access

The ``tarfile`` module provides read and write access to Unix tar
archives, including compressed files.  In addition to the POSIX
standards, several GNU tar extensions are supported.  Unix special
file types such as hard and soft links, and device nodes are also
handled.

.. note::

  Although ``tarfile`` implements a Unix format, it can be used to
  create and read tar archives under Microsoft Windows, too.

Testing Tar Files
=================

The :func:`is_tarfile` function returns a boolean indicating whether
or not the filename passed as an argument refers to a valid tar archive.

.. literalinclude:: tarfile_is_tarfile.py
    :caption:
    :start-after: #end_pymotw_header

If the file does not exist, :func:`is_tarfile` raises an
:class:`IOError`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tarfile_is_tarfile.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 tarfile_is_tarfile.py
	
	     README.txt  False
	    example.tar  True
	bad_example.tar  False
	   notthere.tar  [Errno 2] No such file or directory:
	'notthere.tar'

.. {{{end}}}

Reading Metadata from an Archive
================================

Use the :class:`TarFile` class to work directly with a tar archive. It
supports methods for reading data about existing archives as well as
modifying the archives by adding additional files.

To read the names of the files in an existing archive, use
:func:`getnames`.

.. literalinclude:: tarfile_getnames.py
    :caption:
    :start-after: #end_pymotw_header

The return value is a list of strings with the names of the archive
contents.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tarfile_getnames.py'))
.. }}}

.. code-block:: none

	$ python3 tarfile_getnames.py
	
	['index.rst', 'README.txt']

.. {{{end}}}

In addition to names, metadata about the archive members is available
as instances of :class:`TarInfo` objects.

.. literalinclude:: tarfile_getmembers.py
    :caption:
    :start-after: #end_pymotw_header

Load the metadata via :func:`getmembers` and :func:`getmember`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tarfile_getmembers.py'))
.. }}}

.. code-block:: none

	$ python3 tarfile_getmembers.py
	
	index.rst
		Modified:	 Fri Aug 19 16:27:54 2016
		Mode    :	 0o644
		Type    :	 b'0'
		Size    :	 9878 bytes
	
	README.txt
		Modified:	 Fri Aug 19 16:27:54 2016
		Mode    :	 0o644
		Type    :	 b'0'
		Size    :	 75 bytes
	

.. {{{end}}}


If the name of the archive member is known in advance, its
:class:`TarInfo` object can be retrieved with :func:`getmember`.

.. literalinclude:: tarfile_getmember.py
    :caption:
    :start-after: #end_pymotw_header

If the archive member is not present, :func:`getmember` raises a
:class:`KeyError`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tarfile_getmember.py'))
.. }}}

.. code-block:: none

	$ python3 tarfile_getmember.py
	
	README.txt is 75 bytes
	ERROR: Did not find notthere.txt in tar archive

.. {{{end}}}

Extracting Files from an Archive
================================

To access the data from an archive member within a program, use the
:func:`extractfile` method, passing the member's name.

.. literalinclude:: tarfile_extractfile.py
    :caption:
    :start-after: #end_pymotw_header

The return value is a file-like object from which the contents of the
archive member can be read.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tarfile_extractfile.py'))
.. }}}

.. code-block:: none

	$ python3 tarfile_extractfile.py
	
	README.txt :
	The examples for the tarfile module use this file and
	example.tar as data.
	
	ERROR: Did not find notthere.txt in tar archive

.. {{{end}}}

To unpack the archive and write the files to the file system, use
:func:`extract` or :func:`extractall` instead.

.. literalinclude:: tarfile_extract.py
    :caption:
    :start-after: #end_pymotw_header

The member or members are read from the archive and written to the
file system, starting in the directory named in the arguments.

.. {{{cog
.. outdir = path(cog.inFile).dirname() / 'outdir'
.. outdir.rmtree()
.. cog.out(run_script(cog.inFile, 'tarfile_extract.py'))
.. }}}

.. code-block:: none

	$ python3 tarfile_extract.py
	
	['README.txt']

.. {{{end}}}

The standard library documentation includes a note stating that
:func:`extractall` is safer than :func:`extract`, especially for
working with streaming data where rewinding to read an earlier part of
the input is not possible, and it should be used in most cases.

.. literalinclude:: tarfile_extractall.py
    :caption:
    :start-after: #end_pymotw_header

With :func:`extractall`, the first argument is the name of the
directory where the files should be written.

.. {{{cog
.. outdir = path(cog.inFile).dirname() / 'outdir'
.. outdir.rmtree()
.. cog.out(run_script(cog.inFile, 'tarfile_extractall.py'))
.. }}}

.. code-block:: none

	$ python3 tarfile_extractall.py
	
	['README.txt', 'index.rst']

.. {{{end}}}

To extract specific files from the archive, pass their names or
:class:`TarInfo` metadata containers to :func:`extractall`.

.. literalinclude:: tarfile_extractall_members.py
    :caption:
    :start-after: #end_pymotw_header

When a ``members`` list is provided, only the named files are extracted.

.. {{{cog
.. outdir = path(cog.inFile).dirname() / 'outdir'
.. outdir.rmtree()
.. cog.out(run_script(cog.inFile, 'tarfile_extractall_members.py'))
.. }}}

.. code-block:: none

	$ python3 tarfile_extractall_members.py
	
	['README.txt']

.. {{{end}}}

Creating New Archives
=====================

To create a new archive, open the :class:`TarFile` with a mode of
``'w'``.

.. literalinclude:: tarfile_add.py
    :caption:
    :start-after: #end_pymotw_header

Any existing file is truncated and a new archive is started. To add
files, use the :func:`add` method.

.. {{{cog
.. outfile = path(cog.inFile).dirname() / 'tarfile_add.tar'
.. outfile.remove()
.. cog.out(run_script(cog.inFile, 'tarfile_add.py'))
.. }}}

.. code-block:: none

	$ python3 tarfile_add.py
	
	creating archive
	adding README.txt
	
	Contents:
	README.txt

.. {{{end}}}

Using Alternate Archive Member Names
====================================

It is possible to add a file to an archive using a name other than the
original filename by constructing a :class:`TarInfo` object with an
alternate ``arcname`` and passing it to :func:`addfile`.

.. literalinclude:: tarfile_addfile.py
    :caption:
    :start-after: #end_pymotw_header

The archive includes only the changed filename:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tarfile_addfile.py'))
.. }}}

.. code-block:: none

	$ python3 tarfile_addfile.py
	
	creating archive
	adding README.txt as RENAMED.txt
	
	Contents:
	RENAMED.txt

.. {{{end}}}

Writing Data from Sources Other Than Files
==========================================

Sometimes it is necessary to write data into an archive directly from
memory.  Rather than writing the data to a file, then adding that file
to the archive, you can use :func:`addfile` to add data from an open
file-like handle that returns bytes.

.. literalinclude:: tarfile_addfile_string.py
    :caption:
    :start-after: #end_pymotw_header

By first constructing a :class:`TarInfo` object, the archive member
can be given any name desired.  After setting the size, the data is
written to the archive using :func:`addfile` and a :mod:`BytesIO`
buffer as a source of the data.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tarfile_addfile_string.py'))
.. }}}

.. code-block:: none

	$ python3 tarfile_addfile_string.py
	
	Contents:
	made_up_file.txt
	This is the data to write to the archive.

.. {{{end}}}

Appending to Archives
=====================

In addition to creating new archives, it is possible to append to an
existing file by using mode ``'a'``.

.. literalinclude:: tarfile_append.py
    :caption:
    :start-after: #end_pymotw_header

The resulting archive ends up with two members:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tarfile_append.py'))
.. }}}

.. code-block:: none

	$ python3 tarfile_append.py
	
	creating archive
	contents:
	['README.txt']
	adding index.rst
	contents:
	['README.txt', 'index.rst']

.. {{{end}}}

Working with Compressed Archives
================================

Besides regular tar archive files, the ``tarfile`` module can work
with archives compressed via the gzip or bzip2 protocols.  To open a
compressed archive, modify the mode string passed to :func:`open` to
include ``":gz"`` or ``":bz2"``, depending on the desired compression
method.

.. literalinclude:: tarfile_compression.py
    :caption:
    :start-after: #end_pymotw_header

When opening an existing archive for reading, specify ``"r:*"`` to
have ``tarfile`` determine the compression method to use
automatically.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'tarfile_compression.py'))
.. }}}

.. code-block:: none

	$ python3 tarfile_compression.py
	
	FILENAME                       SIZE      
	README.txt                     75        
	tarfile_compression.tar        10240      ['README.txt']
	tarfile_compression.tar.gz     213        ['README.txt']
	tarfile_compression.tar.bz2    199        ['README.txt']

.. {{{end}}}

.. seealso::

   * :pydoc:`tarfile`

   * `GNU tar manual
     <http://www.gnu.org/software/tar/manual/html_node/Standard.html>`__
     -- Documentation of the tar format, including extensions.

   * :mod:`zipfile` -- Similar access for ZIP archives.

   * :mod:`gzip` -- GNU zip compression

   * :mod:`bz2` -- bzip2 compression
