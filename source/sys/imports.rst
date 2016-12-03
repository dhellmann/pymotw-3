.. _sys-imports:

===================
Modules and Imports
===================

Most Python programs end up as a combination of several modules with a
main application importing them. Whether using the features of the
standard library or organizing custom code in separate files to make
it easier to maintain, understanding and managing the dependencies for
a program is an important aspect of development. ``sys`` includes
information about the modules available to an application, either as
built-ins or after being imported.  It also defines hooks for
overriding the standard import behavior for special cases.

.. _sys-modules:

Imported Modules
================

:data:`sys.modules` is a dictionary mapping the names of imported
modules to the module object holding the code.

.. literalinclude:: sys_modules.py
    :caption:
    :start-after: #end_pymotw_header

The contents of :data:`sys.modules` change as new modules are imported.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_modules.py'))
.. }}}

.. code-block:: none

	$ python3 sys_modules.py
	
	__main__, _bootlocale, _codecs, _collections_abc,
	_frozen_importlib, _frozen_importlib_external, _imp, _io,
	_locale, _signal, _sre, _stat, _thread, _warnings, _weakref,
	_weakrefset, abc, builtins, codecs, copyreg, encodings,
	encodings.aliases, encodings.latin_1, encodings.utf_8, errno,
	genericpath, io, marshal, os, os.path, posix, posixpath, re,
	site, sre_compile, sre_constants, sre_parse, stat, sys,
	textwrap, zipimport

.. {{{end}}}


Built-in Modules
================

The Python interpreter can be compiled with some C modules built right
in, so they do not need to be distributed as separate shared
libraries. These modules do not appear in the list of imported modules
managed in :data:`sys.modules` because they were not technically
imported. The only way to find the available built-in modules is
through :data:`sys.builtin_module_names`.

.. literalinclude:: sys_builtins.py
    :caption:
    :start-after: #end_pymotw_header

The output of this script will vary, especially if run with a
custom-built version of the interpreter.  This output was created
using a copy of the interpreter installed from the standard python.org
installer for OS X.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_builtins.py'))
.. }}}

.. code-block:: none

	$ python3 sys_builtins.py
	
	_ast, _codecs, _collections, _functools, _imp, _io, _locale,
	_operator, _signal, _sre, _stat, _string, _symtable, _thread,
	_tracemalloc, _warnings, _weakref, atexit, builtins, errno,
	faulthandler, gc, itertools, marshal, posix, pwd, sys, time,
	xxsubtype, zipimport

.. {{{end}}}


.. seealso::

    * `Build Instructions <https://hg.python.org/cpython/file/tip/README>`_ --
      Instructions for building Python, from the README distributed with the source.

.. _sys-path:

Import Path
===========

The search path for modules is managed as a Python list saved in
:data:`sys.path`. The default contents of the path include the directory
of the script used to start the application and the current working
directory.

.. literalinclude:: sys_path_show.py
    :caption:
    :start-after: #end_pymotw_header

The first directory in the search path is the home for the sample
script itself. That is followed by a series of platform-specific paths
where compiled extension modules (written in C) might be installed,
and then the global ``site-packages`` directory is listed last.

.. code-block:: none

    $ python3 sys_path_show.py

    /Users/dhellmann/Documents/PyMOTW/pymotw-3/source/sys
    .../python34.zip
    .../lib/python3.4
    .../lib/python3.4/plat-darwin
    .../python3.4/lib-dynload
    .../lib/python3.4/site-packages


The import search-path list can be modified before starting the
interpreter by setting the shell variable :data:`PYTHONPATH` to a
colon-separated list of directories.

.. code-block:: none

    $ PYTHONPATH=/my/private/site-packages:/my/shared/site-packages \
    > python sys_path_show.py

    /Users/dhellmann/Documents/PyMOTW/pymotw-3/source/sys
    /my/private/site-packages
    /my/shared/site-packages
    .../python34.zip
    .../lib/python3.4
    .../lib/python3.4/plat-darwin
    .../python3.4/lib-dynload
    .../lib/python3.4/site-packages

A program can also modify its path by adding elements to
:data:`sys.path` directly.

.. literalinclude:: sys_path_modify.py
    :caption:
    :start-after: #end_pymotw_header

Reloading an imported module re-imports the file, and uses the same
:class:`module` object to hold the results.  Changing the path between
the initial import and the call to :func:`reload` means a different
module may be loaded the second time.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_path_modify.py'))
.. }}}

.. code-block:: none

	$ python3 sys_path_modify.py
	
	Base directory: .
	Imported example from: ./package_dir_a/example.py
		 This is example A
	Reloaded example from: ./package_dir_b/example.py
		 This is example B

.. {{{end}}}

Custom Importers
================

Modifying the search path lets a programmer control how standard
Python modules are found. But, what if a program needs to import code
from somewhere other than the usual ``.py`` or ``.pyc`` files on the
file system? :pep:`302` solves this problem by introducing the idea of
*import hooks*, which can trap an attempt to find a module on the
search path and take alternative measures to load the code from
somewhere else or apply pre-processing to it.

Custom importers are implemented in two separate phases. The *finder*
is responsible for locating a module and providing a *loader* to
manage the actual import. Custom module finders are added
by appending a factory to the :data:`sys.path_hooks` list. On import,
each part of the path is given to a finder until one claims support
(by not raising :class:`ImportError`). That
finder is then responsible for searching data storage represented by
its path entry for named modules.

.. literalinclude:: sys_path_hooks_noisy.py
    :caption:
    :start-after: #end_pymotw_header

This example illustrates how the finders are instantiated and
queried. The :class:`NoisyImportFinder` raises :class:`ImportError`
when instantiated with a path entry that
does not match its special trigger value, which is obviously not a
real path on the file system. This test prevents the
:class:`NoisyImportFinder` from breaking imports of real modules.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_path_hooks_noisy.py', 
..                    break_lines_at=65, line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 sys_path_hooks_noisy.py
	
	Path hook: <class 'zipimport.zipimporter'>
	Path hook: <function
	FileFinder.path_hook.<locals>.path_hook_for_FileFinder at
	0x101833950>
	Path hook: <class '__main__.NoisyImportFinder'>
	importing target_module
	Checking NoisyImportFinder_PATH_TRIGGER: works
	Looking for 'target_module'
	Import failed: No module named 'target_module'

.. {{{end}}}

Importing from a Shelve
=======================

When the finder locates a module, it is responsible for returning a
*loader* capable of importing that module.  This example illustrates a
custom importer that saves its module contents in a database created
by :mod:`shelve`.

First, a script is used to populate the shelf with a package
containing a sub-module and sub-package.

.. literalinclude:: sys_shelve_importer_create.py
    :caption:
    :start-after: #end_pymotw_header

A real packaging script would read the contents from the file system,
but using hard-coded values is sufficient for a simple example like
this.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_shelve_importer_create.py'))
.. }}}

.. code-block:: none

	$ python3 sys_shelve_importer_create.py
	
	Created /tmp/pymotw_import_example.shelve with:
		 data:README
		 package.__init__
		 package.module1
		 package.subpackage.__init__
		 package.subpackage.module2
		 package.with_error

.. {{{end}}}

The custom importer needs to provide finder and loader classes that
know how to look in a shelf for the source of a module or package.

.. literalinclude:: sys_shelve_importer.py
    :caption:
    :start-after: #end_pymotw_header

Now :class:`ShelveFinder` and :class:`ShelveLoader` can be used to
import code from a shelf. For example, importing the :mod:`package`
just created:

.. literalinclude:: sys_shelve_importer_package.py
    :caption:
    :start-after: #end_pymotw_header

The shelf is added to the import path the first time an import occurs
after the path is modified. The finder recognizes the shelf and
returns a loader, which is used for all imports from that shelf. The
initial package-level import creates a new module object and then uses
``exec`` to run the source loaded from the shelf. It uses the
new module as the namespace so that names defined in the source are
preserved as module-level attributes.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_shelve_importer_package.py'))
.. }}}

.. code-block:: none

	$ python3 sys_shelve_importer_package.py
	
	Import of "package":
	shelf added to import path: /tmp/pymotw_import_example.shelve
	
	looking for 'package'
	  in /tmp/pymotw_import_example.shelve
	  found it as package.__init__
	loading source for 'package' from shelf
	creating a new module object for 'package'
	adding path for package
	execing source...
	package imported
	done
	
	Examine package details:
	  message    : This message is in package.__init__
	  __name__   : package
	  __package__: package
	  __file__   : /tmp/pymotw_import_example.shelve/package
	  __path__   : ['/tmp/pymotw_import_example.shelve']
	  __loader__ : <sys_shelve_importer.ShelveLoader object at 0x101
	c875f8>
	
	Global settings:
	sys.modules entry:
	<module 'package' (<sys_shelve_importer.ShelveLoader object at 0
	x101c875f8>)>

.. {{{end}}}

Custom Package Importing
========================

Loading other modules and sub-packages proceeds in the same way.

.. literalinclude:: sys_shelve_importer_module.py
    :caption:
    :start-after: #end_pymotw_header

The finder receives the entire dotted name of the module to load, and
returns a :class:`ShelveLoader` configured to load modules from the
path entry pointing to the shelf file.  The fully qualified module
name is passed to the loader's :meth:`load_module` method, which
constructs and returns a :class:`module` instance.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_shelve_importer_module.py'))
.. }}}

.. code-block:: none

	$ python3 sys_shelve_importer_module.py
	
	Import of "package.module1":
	shelf added to import path: /tmp/pymotw_import_example.shelve
	
	looking for 'package'
	  in /tmp/pymotw_import_example.shelve
	  found it as package.__init__
	loading source for 'package' from shelf
	creating a new module object for 'package'
	adding path for package
	execing source...
	package imported
	done
	
	looking for 'package.module1'
	  in /tmp/pymotw_import_example.shelve
	  found it as package.module1
	loading source for 'package.module1' from shelf
	creating a new module object for 'package.module1'
	imported as regular module
	execing source...
	package.module1 imported
	done
	
	Examine package.module1 details:
	  message    : This message is in package.module1
	  __name__   : package.module1
	  __package__: package
	  __file__   : /tmp/pymotw_import_example.shelve/package.module1
	  __path__   : /tmp/pymotw_import_example.shelve
	  __loader__ : <sys_shelve_importer.ShelveLoader object at 0x101
	c6bcf8>
	
	Import of "package.subpackage.module2":
	
	looking for 'package.subpackage'
	  in /tmp/pymotw_import_example.shelve
	  found it as package.subpackage.__init__
	loading source for 'package.subpackage' from shelf
	creating a new module object for 'package.subpackage'
	adding path for package
	execing source...
	package.subpackage imported
	done
	
	looking for 'package.subpackage.module2'
	  in /tmp/pymotw_import_example.shelve
	  found it as package.subpackage.module2
	loading source for 'package.subpackage.module2' from shelf
	creating a new module object for 'package.subpackage.module2'
	imported as regular module
	execing source...
	package.subpackage.module2 imported
	done
	
	Examine package.subpackage.module2 details:
	  message    : This message is in package.subpackage.module2
	  __name__   : package.subpackage.module2
	  __package__: package.subpackage
	  __file__   : /tmp/pymotw_import_example.shelve/package.subpack
	age.module2
	  __path__   : /tmp/pymotw_import_example.shelve
	  __loader__ : <sys_shelve_importer.ShelveLoader object at 0x101
	c93828>

.. {{{end}}}

Reloading Modules in a Custom Importer
======================================

Reloading a module is handled slightly differently. Instead of
creating a new module object, the existing object is re-used.

.. literalinclude:: sys_shelve_importer_reload.py
    :caption:
    :start-after: #end_pymotw_header

By re-using the same object, existing references to the module are
preserved even if class or function definitions are modified by the
reload.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_shelve_importer_reload.py'))
.. }}}

.. code-block:: none

	$ python3 sys_shelve_importer_reload.py
	
	First import of "package":
	shelf added to import path: /tmp/pymotw_import_example.shelve
	
	looking for 'package'
	  in /tmp/pymotw_import_example.shelve
	  found it as package.__init__
	loading source for 'package' from shelf
	creating a new module object for 'package'
	adding path for package
	execing source...
	package imported
	done
	
	Reloading "package":
	
	looking for 'package'
	  in /tmp/pymotw_import_example.shelve
	  found it as package.__init__
	loading source for 'package' from shelf
	reusing module from import of 'package'
	adding path for package
	execing source...
	package imported
	done

.. {{{end}}}

Handling Import Errors
======================

When a module cannot be located by any finder, :class:`ImportError`
is raised by the main import code.

.. literalinclude:: sys_shelve_importer_missing.py
    :caption:
    :start-after: #end_pymotw_header

Other errors during the import are propagated.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_shelve_importer_missing.py'))
.. }}}

.. code-block:: none

	$ python3 sys_shelve_importer_missing.py
	
	shelf added to import path: /tmp/pymotw_import_example.shelve
	
	looking for 'package'
	  in /tmp/pymotw_import_example.shelve
	  found it as package.__init__
	loading source for 'package' from shelf
	creating a new module object for 'package'
	adding path for package
	execing source...
	package imported
	done
	
	looking for 'package.module3'
	  in /tmp/pymotw_import_example.shelve
	  not found
	Failed to import: No module named 'package.module3'

.. {{{end}}}


Package Data
============

In addition to defining the API for loading executable Python code,
PEP 302 defines an optional API for retrieving package data
intended for distributing data files, documentation, and other
non-code resources used by a package. By implementing :func:`get_data`,
a loader can allow calling applications to support retrieval of data
associated with the package without considering how the package is
actually installed (especially without assuming that the package is
stored as files on a file system).

.. literalinclude:: sys_shelve_importer_get_data.py
    :caption:
    :start-after: #end_pymotw_header

:func:`get_data` takes a path based on the module or package that owns
the data, and returns the contents of the resource "file" as a byte
string, or raises :class:`IOError` if the resource does not exist.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_shelve_importer_get_data.py', 
..                    ignore_error=True))
.. }}}

.. code-block:: none

	$ python3 sys_shelve_importer_get_data.py
	
	shelf added to import path: /tmp/pymotw_import_example.shelve
	
	looking for 'package'
	  in /tmp/pymotw_import_example.shelve
	  found it as package.__init__
	loading source for 'package' from shelf
	creating a new module object for 'package'
	adding path for package
	execing source...
	package imported
	done
	looking for data
	  in /tmp/pymotw_import_example.shelve
	  for '/tmp/pymotw_import_example.shelve/README'
	
	==============
	package README
	==============
	
	This is the README for ``package``.
	
	looking for data
	  in /tmp/pymotw_import_example.shelve
	  for '/tmp/pymotw_import_example.shelve/foo'
	ERROR: Could not load "foo" 

.. {{{end}}}

.. seealso::

    * :mod:`pkgutil` -- Includes :func:`get_data` for retrieving data
      from a package.

Importer Cache
==============

Searching through all of the hooks each time a module is imported can
become expensive. To save time, :data:`sys.path_importer_cache` is
maintained as a mapping between a path entry and the loader that can
use the value to find modules.

.. literalinclude:: sys_path_importer_cache.py
    :caption:
    :start-after: #end_pymotw_header

A :class:`FileFinder` is used for path locations found on the file
system. Locations on the path not supported by any finder are
associated with a ``None``, since they cannot be used to import
modules. The output below has been truncated due to formatting
constraints.

.. Do not use cog because the output includes virtualenv settings.
.. cog.out(run_script(cog.inFile, 'sys_path_importer_cache.py', break_lines_at=65))

.. cog.out(run_script(cog.inFile, 'sys_path_importer_cache.py'))

.. code-block:: none

	$ python3 sys_path_importer_cache.py
	
	PATH:
	  /Users/dhellmann/Documents/PyMOTW/Python3/pymotw-3/source/sys
	  .../lib/python34.zip
	  .../lib/python3.4
	  .../lib/python3.4/plat-darwin
	  .../lib/python3.4/lib-dynload
	  .../lib/python3.4/site-packages
	
	IMPORTERS:
	  sys_path_importer_cache.py: None
	  .../lib/python3.4/encodings: FileFinder(
          '.../lib/python3.4/encodings')
	  .../lib/python3.4/lib-dynload: FileFinder(
          '.../lib/python3.4/lib-dynload')
	  .../lib/python3.4/lib-dynload: FileFinder(
          '.../lib/python3.4/lib-dynload')
	  .../lib/python3.4/site-packages: FileFinder(
          '.../lib/python3.4/site-packages')
	  .../lib/python3.4: FileFinder(
          '.../lib/python3.4/')
	  .../lib/python3.4/plat-darwin: FileFinder(
          '.../lib/python3.4/plat-darwin')
	  .../lib/python3.4: FileFinder(
          '.../lib/python3.4')
	  .../lib/python34.zip: None
	  .../lib/python3.4/plat-darwin: FileFinder(
          '.../lib/python3.4/plat-darwin')

Meta Path
=========

The :data:`sys.meta_path` further extends the sources of potential
imports by allowing a finder to be searched *before* the regular
:data:`sys.path` is scanned. The API for a finder on the meta-path is
the same as for a regular path. The difference is that the metafinder
is not limited to a single entry in :data:`sys.path` -- it can search
anywhere at all.

.. literalinclude:: sys_meta_path.py
    :caption:
    :start-after: #end_pymotw_header

Each finder on the meta-path is interrogated before :data:`sys.path`
is searched, so there is always an opportunity to have a central
importer load modules without explicitly modifying :data:`sys.path`.
Once the module is "found," the loader API works in the same way as
for regular loaders (although this example is truncated for
simplicity).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_meta_path.py'))
.. }}}

.. code-block:: none

	$ python3 sys_meta_path.py
	
	Creating NoisyMetaImportFinder for foo
	
	looking for 'foo' with path None
	 ... found prefix, returning loader
	loading foo
	
	looking for 'foo.bar' with path ['path-entry-goes-here']
	 ... found prefix, returning loader
	loading foo.bar
	
	looking for 'bar' with path None
	 ... not the right prefix, cannot load

.. {{{end}}}

.. seealso::

    * :mod:`importlib` -- Base classes and other tools for creating
      custom importers.

    * :mod:`zipimport` -- Implements importing Python modules from
      inside ZIP archives.

    * `The Internal Structure of Python Eggs
      <http://setuptools.readthedocs.io/en/latest/formats.html?highlight=egg>`_
      -- setuptools documentation for the egg format

    * `Wheel <http://wheel.readthedocs.org/en/latest/>`_ --
      Documentation for ``wheel`` archive format for installable
      Python code.

    * :pep:`302` -- Import Hooks

    * :pep:`366` -- Main module explicit relative imports

    * :pep:`427` -- The Wheel Binary Package Format 1.0

    * `Import this, that, and the other thing: custom importers
      <http://pyvideo.org/pycon-us-2010/pycon-2010--import-this--that--and-the-other-thin.html>`_ --
      Brett Cannon's PyCon 2010 presentation.
