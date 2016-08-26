============================================================
 os.path --- Platform-independent Manipulation of Filenames
============================================================

.. module:: os.path
    :synopsis: Platform-independent manipulation of filenames.

:Purpose: Parse, build, test, and otherwise work on filenames and paths.

Writing code to work with files on multiple platforms is easy using
the functions included in the :mod:`os.path` module. Even programs not
intended to be ported between platforms should use :mod:`os.path` for
reliable filename parsing.

Parsing Paths
=============

The first set of functions in :mod:`os.path` can be used to parse
strings representing filenames into their component parts. It is
important to realize that these functions do not depend on the paths
actually existing; they operate solely on the strings.

Path parsing depends on a few variable defined in :mod:`os`:

* :const:`os.sep` - The separator between portions of the path (e.g.,
  "``/``" or "``\``").

* :const:`os.extsep` - The separator between a filename and the file
  "extension" (e.g., "``.``").

* :const:`os.pardir` - The path component that means traverse the
  directory tree up one level (e.g., "``..``").

* :const:`os.curdir` - The path component that refers to the current
  directory (e.g., "``.``").

The :func:`split` function breaks the path into two separate parts and
returns a :class:`tuple` with the results. The second element of the
:class:`tuple` is the last component of the path, and the first element is
everything that comes before it.

.. literalinclude:: ospath_split.py
    :caption:
    :start-after: #end_pymotw_header

When the input argument ends in :const:`os.sep`, the "last element" of
the path is an empty string.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ospath_split.py'))
.. }}}

.. code-block:: none

	$ python3 ospath_split.py
	
	 '/one/two/three' : ('/one/two', 'three')
	'/one/two/three/' : ('/one/two/three', '')
	              '/' : ('/', '')
	              '.' : ('', '.')
	               '' : ('', '')

.. {{{end}}}

The :func:`basename` function returns a value equivalent to the second
part of the :func:`split` value.

.. literalinclude:: ospath_basename.py
    :caption:
    :start-after: #end_pymotw_header

The full path is stripped down to the last element, whether that
refers to a file or directory.  If the path ends in the directory
separator (:const:`os.sep`), the base portion is considered to be
empty.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ospath_basename.py'))
.. }}}

.. code-block:: none

	$ python3 ospath_basename.py
	
	 '/one/two/three' : 'three'
	'/one/two/three/' : ''
	              '/' : ''
	              '.' : '.'
	               '' : ''

.. {{{end}}}

The :func:`dirname` function returns the first part of the split path:

.. literalinclude:: ospath_dirname.py
    :caption:
    :start-after: #end_pymotw_header

Combining the results of :func:`basename` with :func:`dirname` gives
the original path.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ospath_dirname.py'))
.. }}}

.. code-block:: none

	$ python3 ospath_dirname.py
	
	 '/one/two/three' : '/one/two'
	'/one/two/three/' : '/one/two/three'
	              '/' : '/'
	              '.' : ''
	               '' : ''

.. {{{end}}}

:func:`splitext` works like :func:`split`, but divides the path on the
extension separator, rather than the directory separator.

.. literalinclude:: ospath_splitext.py
    :caption:
    :start-after: #end_pymotw_header

Only the last occurrence of :const:`os.extsep` is used when looking
for the extension, so if a filename has multiple extensions
the results of splitting it leaves part of the extension on the
prefix.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ospath_splitext.py'))
.. }}}

.. code-block:: none

	$ python3 ospath_splitext.py
	
	       'filename.txt' : ('filename', '.txt')
	           'filename' : ('filename', '')
	'/path/to/filename.txt' : ('/path/to/filename', '.txt')
	                  '/' : ('/', '')
	                   '' : ('', '')
	  'my-archive.tar.gz' : ('my-archive.tar', '.gz')
	      'no-extension.' : ('no-extension', '.')

.. {{{end}}}

:func:`commonprefix` takes a list of paths as an argument and returns
a single string that represents a common prefix present in all of the
paths. The value may represent a path that does not actually exist,
and the path separator is not included in the consideration, so the
prefix might not stop on a separator boundary.

.. literalinclude:: ospath_commonprefix.py
    :caption:
    :start-after: #end_pymotw_header

In this example, the common prefix string is ``/one/two/three``, even
though one path does not include a directory named ``three``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ospath_commonprefix.py'))
.. }}}

.. code-block:: none

	$ python3 ospath_commonprefix.py
	
	PATH: /one/two/three/four
	PATH: /one/two/threefold
	PATH: /one/two/three/
	
	PREFIX: /one/two/three

.. {{{end}}}

Building Paths
==============

Besides taking existing paths apart, it is frequently necessary to
build paths from other strings.  To combine several path components
into a single value, use :func:`join`:

.. literalinclude:: ospath_join.py
    :caption:
    :start-after: #end_pymotw_header

If any argument to join begins with :const:`os.sep`, all of the
previous arguments are discarded and the new one becomes the beginning
of the return value.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ospath_join.py'))
.. }}}

.. code-block:: none

	$ python3 ospath_join.py
	
	('one', 'two', 'three') : 'one/two/three'
	('/', 'one', 'two', 'three') : '/one/two/three'
	('/one', '/two', '/three') : '/three'

.. {{{end}}}

It is also possible to work with paths that include "variable" components
that can be expanded automatically. For example, :func:`expanduser`
converts the tilde (``~``) character to the name of a user's home
directory.

.. literalinclude:: ospath_expanduser.py
    :caption:
    :start-after: #end_pymotw_header

If the user's home directory cannot be found, the string is returned
unchanged, as with ``~nosuchuser`` in this example.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ospath_expanduser.py'))
.. }}}

.. code-block:: none

	$ python3 ospath_expanduser.py
	
	           ~ : /Users/dhellmann
	  ~dhellmann : /Users/dhellmann
	 ~nosuchuser : ~nosuchuser

.. {{{end}}}

:func:`expandvars` is more general, and expands any shell environment
variables present in the path.

.. literalinclude:: ospath_expandvars.py
    :caption:
    :start-after: #end_pymotw_header

No validation is performed to ensure that the variable value results
in the name of a file that already exists.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ospath_expandvars.py'))
.. }}}

.. code-block:: none

	$ python3 ospath_expandvars.py
	
	/path/to/VALUE

.. {{{end}}}

Normalizing Paths
=================

Paths assembled from separate strings using :func:`join` or with
embedded variables might end up with extra separators or relative path
components. Use :func:`normpath` to clean them up:

.. literalinclude:: ospath_normpath.py
    :caption:
    :start-after: #end_pymotw_header

Path segments made up of :const:`os.curdir` and :const:`os.pardir` are
evaluated and collapsed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ospath_normpath.py'))
.. }}}

.. code-block:: none

	$ python3 ospath_normpath.py
	
	     one//two//three : one/two/three
	   one/./two/./three : one/two/three
	one/../alt/two/three : alt/two/three

.. {{{end}}}

To convert a relative path to an absolute filename, use
:func:`abspath`.

.. literalinclude:: ospath_abspath.py
    :caption:
    :start-after: #end_pymotw_header

The result is a complete path, starting at the top of the file system
tree.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ospath_abspath.py'))
.. }}}

.. code-block:: none

	$ python3 ospath_abspath.py
	
	                  '.' : '/private/tmp'
	                 '..' : '/private'
	    './one/two/three' : '/private/tmp/one/two/three'
	   '../one/two/three' : '/private/one/two/three'

.. {{{end}}}

File Times
==========

Besides working with paths, :mod:`os.path` includes functions for
retrieving file properties, similar to the ones returned by
:func:`os.stat`:

.. literalinclude:: ospath_properties.py
    :caption:
    :start-after: #end_pymotw_header

:func:`os.path.getatime` returns the access time,
:func:`os.path.getmtime` returns the modification time, and
:func:`os.path.getctime` returns the creation time.
:func:`os.path.getsize` returns the amount of data in the file,
represented in bytes.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ospath_properties.py'))
.. }}}

.. code-block:: none

	$ python3 ospath_properties.py
	
	File         : ospath_properties.py
	Access time  : Fri Aug 26 16:13:04 2016
	Modified time: Fri Aug 26 15:50:48 2016
	Change time  : Fri Aug 26 15:50:49 2016
	Size         : 481

.. {{{end}}}

Testing Files
=============

When a program encounters a path name, it often needs to know whether
the path refers to a file, directory, or symlink and whether it
exists.  :mod:`os.path` includes functions for testing all of these
conditions.

.. literalinclude:: ospath_tests.py
    :caption:
    :start-after: #end_pymotw_header

All of the test functions return boolean values.

.. {{{cog
.. run_script(cog.inFile, 'rm -f broken_link', interpreter='')
.. cog.out(run_script(cog.inFile, 'ln -s /does/not/exist broken_link', interpreter='', trailing_newlines=False))
.. cog.out(run_script(cog.inFile, 'ospath_tests.py', include_prefix=False))
.. }}}

.. code-block:: none

	$ ln -s /does/not/exist broken_link
	$ python3 ospath_tests.py
	
	File        : 'ospath_tests.py'
	Absolute    : False
	Is File?    : True
	Is Dir?     : False
	Is Link?    : False
	Mountpoint? : False
	Exists?     : True
	Link Exists?: True
	
	File        : ''
	Absolute    : False
	Is File?    : False
	Is Dir?     : False
	Is Link?    : False
	Mountpoint? : False
	Exists?     : False
	Link Exists?: False
	
	File        : '/'
	Absolute    : True
	Is File?    : False
	Is Dir?     : True
	Is Link?    : False
	Mountpoint? : True
	Exists?     : True
	Link Exists?: True
	
	File        : './broken_link'
	Absolute    : False
	Is File?    : False
	Is Dir?     : False
	Is Link?    : True
	Mountpoint? : False
	Exists?     : False
	Link Exists?: True
	

.. {{{end}}}


.. seealso::

    `os.path <http://docs.python.org/lib/module-os.path.html>`_
        Standard library documentation for this module.

    :mod:`os`
        The ``os`` module is a parent of ``os.path``.

    :mod:`time`
        The time module includes functions to convert between the
        representation used by the time property functions in
        ``os.path`` and easy-to-read strings.
