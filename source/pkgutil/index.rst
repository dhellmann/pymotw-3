===============================
 pkgutil --- Package Utilities
===============================

.. module:: pkgutil
    :synopsis: Package utilities

:Purpose: Add to the module search path for a specific package and
          work with resources included in a package.

The :mod:`pkgutil` module includes functions for changing the import
rules for Python packages and for loading non-code resources from
files distributed within a package.

Package Import Paths
====================

The :func:`extend_path` function is used to modify the search path and
change the way sub-modules are imported from within a package so that
several different directories can be combined as though they are one.
This can be used to override installed versions of packages with
development versions, or to combine platform-specific and shared
modules into a single package namespace.

The most common way to call :func:`extend_path` is by adding these two
lines to the ``__init__.py`` inside the package:

.. code-block:: none

    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)

:func:`extend_path` scans ``sys.path`` for directories that include a
subdirectory named for the package given as the second argument.  The
list of directories is combined with the path value passed as the
first argument and returned as a single list, suitable for use as the
package import path.

An example package called :mod:`demopkg` includes two files,
``__init__.py`` and ``shared.py``.  The ``__init__.py`` file in
``demopkg1`` contains :command:`print` statements to show the search
path before and after it is modified, to highlight the difference.

.. literalinclude:: demopkg1/__init__.py
   :caption:
   :start-after: #end_pymotw_header

The ``extension`` directory, with add-on features for :mod:`demopkg`,
contains three more source files. There is an ``__init__.py`` at each
directory level, and a ``not_shared.py``.

.. {{{cog
.. cog.out(run_script(cog.inFile, "find extension -name '*.py'", interpreter=''))
.. }}}

.. code-block:: none

	$ find extension -name '*.py'
	
	extension/__init__.py
	extension/demopkg1/__init__.py
	extension/demopkg1/not_shared.py

.. {{{end}}}

This simple test program imports the :mod:`demopkg1` package.

.. literalinclude:: pkgutil_extend_path.py
   :caption:
   :start-after: #end_pymotw_header

When this test program is run directly from the command line, the
:mod:`not_shared` module is not found.

.. note::

  The full file system paths in these examples have been shortened to
  emphasize the parts that change.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pkgutil_extend_path.py'))
.. }}}

.. code-block:: none

	$ python3 pkgutil_extend_path.py
	
	demopkg1.__path__ before:
	['.../demopkg1']
	
	demopkg1.__path__ after:
	['.../demopkg1']
	
	demopkg1           : .../demopkg1/__init__.py
	demopkg1.shared    : .../demopkg1/shared.py
	demopkg1.not_shared: Not found (No module named 'demopkg1.not_sh
	ared')

.. {{{end}}}

However, if the ``extension`` directory is added to the
:data:`PYTHONPATH` and the program is run again, different results are
produced.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'PYTHONPATH=extension python3 pkgutil_extend_path.py', interpreter=None))
.. }}}

.. code-block:: none

	$ PYTHONPATH=extension python3 pkgutil_extend_path.py
	
	demopkg1.__path__ before:
	['.../demopkg1']
	
	demopkg1.__path__ after:
	['.../demopkg1',
	 '.../extension/demopkg1']
	
	demopkg1           : .../demopkg1/__init__.py
	demopkg1.shared    : .../demopkg1/shared.py
	demopkg1.not_shared: .../extension/demopkg1/not_shared.py

.. {{{end}}}

The version of :mod:`demopkg1` inside the ``extension`` directory has
been added to the search path, so the :mod:`not_shared` module is
found there.

Extending the path in this manner is useful for combining
platform-specific versions of packages with common packages,
especially if the platform-specific versions include C extension
modules.

Development Versions of Packages
================================

While developing enhancements to a project, it is common to need to
test changes to an installed package. Replacing the installed copy
with a development version may be a bad idea, since it is not
necessarily correct and other tools on the system are likely to depend
on the installed package.

A completely separate copy of the package could be configured in a
development environment using :command:`virtualenv` or :mod:`venv`,
but for small modifications the overhead of setting up a virtual
environment with all of the dependencies may be excessive.

Another option is to use :mod:`pkgutil` to modify the module search
path for modules that belong to the package under development. In this
case, however, the path must be reversed so development version
overrides the installed version.

Given a package :mod:`demopkg2` containing an ``__init__.py`` and
``overloaded.py``, with the function under development located in
``demopkg2/overloaded.py``. The installed version contains

.. literalinclude:: demopkg2/overloaded.py
   :caption:
   :start-after: #end_pymotw_header

and ``demopkg2/__init__.py`` contains

.. literalinclude:: demopkg2/__init__.py
   :caption:
   :start-after: #end_pymotw_header

:func:`reverse` is used to ensure that any directories added to the
search path by :mod:`pkgutil` are scanned for imports *before* the
default location.

This program imports :mod:`demopkg2.overloaded` and calls :func:`func`:

.. literalinclude:: pkgutil_devel.py
   :caption:
   :start-after: #end_pymotw_header

Running it without any special path treatment produces output from the
installed version of :func:`func`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pkgutil_devel.py'))
.. }}}

.. code-block:: none

	$ python3 pkgutil_devel.py
	
	demopkg2           : .../demopkg2/__init__.py
	demopkg2.overloaded: .../demopkg2/overloaded.py
	
	This is the installed version of func().

.. {{{end}}}

A development directory containing

.. {{{cog
.. cog.out(run_script(cog.inFile, "find develop/demopkg2 -name '*.py'", interpreter=None))
.. }}}

.. code-block:: none

	$ find develop/demopkg2 -name '*.py'
	
	develop/demopkg2/__init__.py
	develop/demopkg2/overloaded.py

.. {{{end}}}

and a modified version of :mod:`overloaded`

.. literalinclude:: develop/demopkg2/overloaded.py
   :caption:
   :start-after: #end_pymotw_header

will be loaded when the test program is run with the ``develop``
directory in the search path.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'PYTHONPATH=develop python3 pkgutil_devel.py', interpreter=None))
.. }}}

.. code-block:: none

	$ PYTHONPATH=develop python3 pkgutil_devel.py
	
	demopkg2           : .../demopkg2/__init__.py
	demopkg2.overloaded: .../develop/demopkg2/overloaded.py
	
	This is the development version of func().

.. {{{end}}}

Managing Paths with PKG Files
=============================

The first example illustrated how to extend the search path using
extra directories included in the :data:`PYTHONPATH`. It is also
possible to add to the search path using ``*.pkg`` files containing
directory names. PKG files are similar to the PTH files used by the
:mod:`site` module. They can contain directory names, one per line, to
be added to the search path for the package.

Another way to structure the platform-specific portions of the
application from the first example is to use a separate directory for
each operating system, and include a ``.pkg`` file to extend the
search path.

This example uses the same :mod:`demopkg1` files, and also includes
the following files:

.. {{{cog
.. sh("find . -name __pycache__ | xargs rm -rf")
.. cog.out(run_script(cog.inFile, "find os_* -type f", interpreter=None))
.. }}}

.. code-block:: none

	$ find os_* -type f
	
	os_one/demopkg1/__init__.py
	os_one/demopkg1/not_shared.py
	os_one/demopkg1.pkg
	os_two/demopkg1/__init__.py
	os_two/demopkg1/not_shared.py
	os_two/demopkg1.pkg

.. {{{end}}}

The PKG files are named ``demopkg1.pkg`` to match the package
being extended.  They both contain::

    demopkg

This demo program shows the version of the module being imported.

.. literalinclude:: pkgutil_os_specific.py
   :caption:
   :start-after: #end_pymotw_header

A simple wrapper script can be used to switch between the two
packages.

.. literalinclude:: with_os.sh
   :caption:
   :language: bash

And when run with ``"one"`` or ``"two"`` as the arguments, the path is
adjusted:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'one', interpreter='./with_os.sh'))
.. cog.out(run_script(cog.inFile, 'two', interpreter='./with_os.sh', include_prefix=False))
.. }}}

.. code-block:: none

	$ ./with_os.sh one
	
	PYTHONPATH=os_one
	
	demopkg1.__path__ before:
	['.../demopkg1']
	
	demopkg1.__path__ after:
	['.../demopkg1',
	 '.../os_one/demopkg1',
	 'demopkg']
	
	demopkg1: .../demopkg1/__init__.py
	demopkg1.shared: .../demopkg1/shared.py
	demopkg1.not_shared: .../os_one/demopkg1/not_shared.py

	$ ./with_os.sh two
	
	PYTHONPATH=os_two
	
	demopkg1.__path__ before:
	['.../demopkg1']
	
	demopkg1.__path__ after:
	['.../demopkg1',
	 '.../os_two/demopkg1',
	 'demopkg']
	
	demopkg1: .../demopkg1/__init__.py
	demopkg1.shared: .../demopkg1/shared.py
	demopkg1.not_shared: .../os_two/demopkg1/not_shared.py

.. {{{end}}}

PKG files can appear anywhere in the normal search path, so a
single PKG file in the current working directory could also be
used to include a development tree.

Nested Packages
===============

For nested packages, it is only necessary to modify the path of the top-level
package. For example, with this directory structure

.. {{{cog
.. cog.out(run_script(cog.inFile, "find nested -name '*.py'", interpreter=None))
.. }}}

.. code-block:: none

	$ find nested -name '*.py'
	
	nested/__init__.py
	nested/second/__init__.py
	nested/second/deep.py
	nested/shallow.py

.. {{{end}}}

Where ``nested/__init__.py`` contains

.. literalinclude:: nested/__init__.py
   :caption:
   :start-after: #end_pymotw_header

and a development tree like

.. {{{cog
.. cog.out(run_script(cog.inFile, "find develop/nested -name '*.py'", interpreter=None))
.. }}}

.. code-block:: none

	$ find develop/nested -name '*.py'
	
	develop/nested/__init__.py
	develop/nested/second/__init__.py
	develop/nested/second/deep.py
	develop/nested/shallow.py

.. {{{end}}}

Both the :mod:`shallow` and :mod:`deep` modules contain a simple
function to print out a message indicating whether or not they come
from the installed or development version.

This test program exercises the new packages.

.. literalinclude:: pkgutil_nested.py
   :caption:
   :start-after: #end_pymotw_header

When ``pkgutil_nested.py`` is run without any path manipulation, the
installed version of both modules are used.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pkgutil_nested.py'))
.. }}}

.. code-block:: none

	$ python3 pkgutil_nested.py
	
	nested.shallow: .../nested/shallow.py
	This func() comes from the installed version of nested.shallow
	
	nested.second.deep: .../nested/second/deep.py
	This func() comes from the installed version of nested.second.de
	ep

.. {{{end}}}

When the ``develop`` directory is added to the path, the development
version of both functions override the installed versions.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'PYTHONPATH=develop python3 pkgutil_nested.py', interpreter=None))
.. }}}

.. code-block:: none

	$ PYTHONPATH=develop python3 pkgutil_nested.py
	
	nested.shallow: .../develop/nested/shallow.py
	This func() comes from the development version of nested.shallow
	
	nested.second.deep: .../develop/nested/second/deep.py
	This func() comes from the development version of nested.second.
	deep

.. {{{end}}}

Package Data
============

In addition to code, Python packages can contain data files such as
templates, default configuration files, images, and other supporting
files used by the code in the package.  The :func:`get_data` function
gives access to the data in the files in a format-agnostic way, so it
does not matter if the package is distributed as an EGG, part of a
frozen binary, or regular files on the file system.

With a package :mod:`pkgwithdata` containing a ``templates`` directory

.. {{{cog
.. cog.out(run_script(cog.inFile, 'find pkgwithdata -type f', interpreter=None))
.. }}}

.. code-block:: none

	$ find pkgwithdata -type f
	
	pkgwithdata/__init__.py
	pkgwithdata/templates/base.html

.. {{{end}}}

The file ``pkgwithdata/templates/base.html`` contains a simple HTML
template.

.. literalinclude:: pkgwithdata/templates/base.html
   :caption:
   :language: html

This program uses :func:`get_data` to retrieve the template contents
and print them out.

.. literalinclude:: pkgutil_get_data.py
   :caption:
   :start-after: #end_pymotw_header

The arguments to :func:`get_data` are the dotted name of the package,
and a filename relative to the top of the package.  The return value
is a byte sequence, so it is decoded from UTF-8 before being printed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pkgutil_get_data.py'))
.. }}}

.. code-block:: none

	$ python3 pkgutil_get_data.py
	
	<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
	<html> <head>
	<title>PyMOTW Template</title>
	</head>
	
	<body>
	<h1>Example Template</h1>
	
	<p>This is a sample data file.</p>
	
	</body>
	</html>

.. {{{end}}}

:func:`get_data` is distribution format-agnostic because it uses the
import hooks defined in :pep:`302` to access the package contents.
Any loader that provides the hooks can be used, including the ZIP
archive importer in :mod:`zipfile`.

.. literalinclude:: pkgutil_get_data_zip.py
   :caption:
   :start-after: #end_pymotw_header

This example uses :func:`PyZipFile.writepy` to create a ZIP archive
containing a copy of the :mod:`pkgwithdata` package, including a
renamed version of the template file.  It then adds the ZIP archive to
the import path before using :mod:`pkgutil` to load the template and
print it.  Refer to the discussion of :mod:`zipfile` for more details
about using :func:`writepy`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pkgutil_get_data_zip.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 pkgutil_get_data_zip.py
	
	Loading pkgwithdata from
	pkgwithdatainzip.zip/pkgwithdata/__init__.pyc
	
	Template:
	<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
	<html> <head>
	<title>PyMOTW Template</title>
	</head>
	
	<body>
	<h1>Example Template</h1>
	
	<p>This is a sample data file.</p>
	
	</body>
	</html>

.. {{{end}}}


.. seealso::

   * :pydoc:`pkgutil`

   * `virtualenv`_ -- Ian Bicking's virtual environment script.

   * :mod:`distutils` -- Packaging tools from Python standard library.

   * `setuptools`_ -- Next-generation packaging tools.

   * :pep:`302` -- Import Hooks

   * :mod:`zipfile` -- Create importable ZIP archives.

   * :mod:`zipimport` -- Importer for packages in ZIP archives.

.. _virtualenv: http://pypi.python.org/pypi/virtualenv

.. _setuptools: https://setuptools.readthedocs.io/en/latest/
