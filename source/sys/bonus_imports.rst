Custom Importers
================

Modifying the search path lets a programmer control how standard
Python modules are found, but what if a program needs to import code
from somewhere other than the usual ``.py`` or ``.pyc`` files on the
file system? PEP 302 solves this problem by introducing the idea of
*import hooks* that can trap an attempt to find a module on the search
path and take alternative measures to load the code from somewhere
else or apply pre-processing to it.

Custom importers are implemented in two separate phases. The *finder*
is responsible for locating a module and providing a *loader* to
manage the actual import. Custom module finders are added
by appending a factory to the :data:`sys.path_hooks` list. On import,
each part of the path is given to a finder until one claims support
(by not raising :class:`ImportError`). That
finder is then responsible for searching data storage represented by
its path entry for named modules.

.. include:: sys_path_hooks_noisy.py
    :literal:
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

::

    $ python sys_path_hooks_noisy.py
    
    Checking NoisyImportFinder_PATH_TRIGGER: works
    Looking for "target_module"
    Checking /Users/dhellmann/Documents/PyMOTW/book/PyMOTW/sys:
     wrong finder
    Import failed: No module named target_module

.. {{{end}}}

Importing from a Shelve
=======================

When the finder locates a module, it is responsible for returning a
*loader* capable of importing that module.  This example illustrates a
custom importer that saves its module contents in a database created
by :mod:`shelve`.

First, a script is used to populate the shelf with a package
containing a sub-module and sub-package.

.. include:: sys_shelve_importer_create.py
    :literal:
    :start-after: #end_pymotw_header

A real packaging script would read the contents from the file system,
but using hard-coded values is sufficient for a simple example like
this.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_shelve_importer_create.py'))
.. }}}

::

    $ python sys_shelve_importer_create.py
    
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

.. include:: sys_shelve_importer.py
    :literal:
    :start-after: #end_pymotw_header

Now :class:`ShelveFinder` and :class:`ShelveLoader` can be used to
import code from a shelf. For example, importing the :mod:`package`
just created:

.. include:: sys_shelve_importer_package.py
    :literal:
    :start-after: #end_pymotw_header

The shelf is added to the import path the first time an import occurs
after the path is modified. The finder recognizes the shelf and
returns a loader, which is used for all imports from that shelf. The
initial package-level import creates a new module object and then uses
:command:`exec` to run the source loaded from the shelf, using the new
module as the namespace so that names defined in the source are
preserved as module-level attributes.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_shelve_importer_package.py', break_lines_at=74))
.. }}}

::

    $ python sys_shelve_importer_package.py
    
    Import of "package":
    shelf added to import path: /tmp/pymotw_import_example.shelve
    
    looking for "package"
      in /tmp/pymotw_import_example.shelve
      found it as package.__init__
    loading source for "package" from shelf
    creating a new module object for "package"
    adding path for package
    execing source...
    package imported
    done
    
    Examine package details:
      message    : This message is in package.__init__
      __name__   : package
      __package__: 
      __file__   : /tmp/pymotw_import_example.shelve/package
      __path__   : ['/tmp/pymotw_import_example.shelve']
      __loader__ : <sys_shelve_importer.ShelveLoader object at 0x1006d42d0>
    
    Global settings:
    sys.modules entry:
    <module 'package' from '/tmp/pymotw_import_example.shelve/package'>

.. {{{end}}}

Custom Package Importing
========================

Loading other modules and sub-packages proceeds in the same way.

.. include:: sys_shelve_importer_module.py
    :literal:
    :start-after: #end_pymotw_header

The finder receives the entire dotted name of the module to load, and
returns a :class:`ShelveLoader` configured to load modules from the
path entry pointing to the shelf file.  The fully qualified module
name is passed to the loader's :meth:`load_module` method, which
constructs and returns a :class:`module` instance.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_shelve_importer_module.py', break_lines_at=70))
.. }}}

::

    $ python sys_shelve_importer_module.py
    
    Import of "package.module1":
    shelf added to import path: /tmp/pymotw_import_example.shelve
    
    looking for "package"
      in /tmp/pymotw_import_example.shelve
      found it as package.__init__
    loading source for "package" from shelf
    creating a new module object for "package"
    adding path for package
    execing source...
    package imported
    done
    
    looking for "package.module1"
      in /tmp/pymotw_import_example.shelve
      found it as package.module1
    loading source for "package.module1" from shelf
    creating a new module object for "package.module1"
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
      __loader__ : <sys_shelve_importer.ShelveLoader object at 0x1006d42d0
    >
    
    Import of "package.subpackage.module2":
    
    looking for "package.subpackage"
      in /tmp/pymotw_import_example.shelve
      found it as package.subpackage.__init__
    loading source for "package.subpackage" from shelf
    creating a new module object for "package.subpackage"
    adding path for package
    execing source...
    package.subpackage imported
    done
    
    looking for "package.subpackage.module2"
      in /tmp/pymotw_import_example.shelve
      found it as package.subpackage.module2
    loading source for "package.subpackage.module2" from shelf
    creating a new module object for "package.subpackage.module2"
    imported as regular module
    execing source...
    package.subpackage.module2 imported
    done
    
    Examine package.subpackage.module2 details:
      message    : This message is in package.subpackage.module2
      __name__   : package.subpackage.module2
      __package__: package.subpackage
      __file__   : /tmp/pymotw_import_example.shelve/package.subpackage.mo
    dule2
      __path__   : /tmp/pymotw_import_example.shelve
      __loader__ : <sys_shelve_importer.ShelveLoader object at 0x1006d4390
    >

.. {{{end}}}

Reloading Modules in a Custom Importer
======================================

Reloading a module is handled slightly differently. Instead of
creating a new module object, the existing module is re-used.

.. include:: sys_shelve_importer_reload.py
    :literal:
    :start-after: #end_pymotw_header

By re-using the same object, existing references to the module are
preserved even if class or function definitions are modified by the
reload.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_shelve_importer_reload.py', break_lines_at=74))
.. }}}

::

    $ python sys_shelve_importer_reload.py
    
    First import of "package":
    shelf added to import path: /tmp/pymotw_import_example.shelve
    
    looking for "package"
      in /tmp/pymotw_import_example.shelve
      found it as package.__init__
    loading source for "package" from shelf
    creating a new module object for "package"
    adding path for package
    execing source...
    package imported
    done
    
    Reloading "package":
    
    looking for "package"
      in /tmp/pymotw_import_example.shelve
      found it as package.__init__
    loading source for "package" from shelf
    reusing existing module from import of "package"
    adding path for package
    execing source...
    package imported
    done

.. {{{end}}}

Handling Import Errors
======================

When a module cannot be located by any finder, :class:`ImportError`
is raised by the main import code.

.. include:: sys_shelve_importer_missing.py
    :literal:
    :start-after: #end_pymotw_header

Other errors during the import are propagated.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_shelve_importer_missing.py', break_lines_at=74))
.. }}}

::

    $ python sys_shelve_importer_missing.py
    
    shelf added to import path: /tmp/pymotw_import_example.shelve
    
    looking for "package"
      in /tmp/pymotw_import_example.shelve
      found it as package.__init__
    loading source for "package" from shelf
    creating a new module object for "package"
    adding path for package
    execing source...
    package imported
    done
    
    looking for "package.module3"
      in /tmp/pymotw_import_example.shelve
      not found
    Failed to import: No module named module3

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

.. include:: sys_shelve_importer_get_data.py
    :literal:
    :start-after: #end_pymotw_header

:func:`get_data` takes a path based on the module or package that owns
the data, and returns the contents of the resource "file" as a string,
or raises :class:`IOError` if the resource does not
exist.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_shelve_importer_get_data.py', 
..                    ignore_error=True, break_lines_at=74))
.. }}}

::

    $ python sys_shelve_importer_get_data.py
    
    shelf added to import path: /tmp/pymotw_import_example.shelve
    
    looking for "package"
      in /tmp/pymotw_import_example.shelve
      found it as package.__init__
    loading source for "package" from shelf
    creating a new module object for "package"
    adding path for package
    execing source...
    package imported
    done
    looking for data
      in /tmp/pymotw_import_example.shelve
      for "/tmp/pymotw_import_example.shelve/README"
    
    ==============
    package README
    ==============
    
    This is the README for ``package``.
    
    looking for data
      in /tmp/pymotw_import_example.shelve
      for "/tmp/pymotw_import_example.shelve/foo"
    ERROR: Could not load "foo" 

.. {{{end}}}

.. seealso::

    :mod:`pkgutil`
        Includes :func:`get_data` for retrieving data from a package.

Importer Cache
==============

Searching through all of the hooks each time a module is imported can
become expensive. To save time, :data:`sys.path_importer_cache` is
maintained as a mapping between a path entry and the loader that can
use the value to find modules.

.. include:: sys_path_importer_cache.py
    :literal:
    :start-after: #end_pymotw_header

A cache value of ``None`` means to use the default file system
loader. Directories on the path that do not exist are associated with
an :class:`imp.NullImporter` instance, since they cannot be used to
import modules. In the example output, several
:class:`zipimport.zipimporter` instances are used to manage EGG files
found on the path.

.. NOT RUNNING
.. cog.out(run_script(cog.inFile, 'sys_path_importer_cache.py', break_lines_at=74))

::

    $ python sys_path_importer_cache.py
            
    PATH:
      /Users/dhellmann/Documents/PyMOTW/book/PyMOTW/sys
      .../lib/python2.7/site-packages/distribute-0.6.10-py2.7.egg
      .../lib/python2.7/site-packages/pip-0.7.2-py2.7.egg
      .../lib/python27.zip
      .../lib/python2.7
      .../lib/python2.7/plat-darwin
      .../lib/python2.7/plat-mac
      .../lib/python2.7/plat-mac/lib-scriptpackages
      .../lib/python2.7/lib-tk
      .../lib/python2.7/lib-old
      .../lib/python2.7/lib-dynload
      .../lib/python2.7/site-packages
        
    IMPORTERS:
      sys_path_importer_cache.py: <imp.NullImporter object at 0x100d02080>
      .../lib/python27.zip: <imp.NullImporter object at 0x100d02030>
      .../lib/python2.7/lib-dynload: None
      .../lib/python2.7/encodings: None
      .../lib/python2.7: None
      .../lib/python2.7/lib-old: None
      .../lib/python2.7/site-packages: None
      .../lib/python2.7/plat-darwin: None
      .../lib/python2.7/: None
      .../lib/python2.7/plat-mac/lib-scriptpackages: None
      .../lib/python2.7/plat-mac: None
      .../lib/python2.7/site-packages/pip-0.7.2-py2.7.egg: None
      .../lib/python2.7/lib-tk: None
      .../lib/python2.7/site-packages/distribute-0.6.10-py2.7.egg: None

Meta Path
=========

The :data:`sys.meta_path` further extends the sources of potential
imports by allowing a finder to be searched *before* the regular
:data:`sys.path` is scanned. The API for a finder on the meta-path is
the same as for a regular path. The difference is that the meta-finder
is not limited to a single entry in :data:`sys.path`, it can search
anywhere at all.

.. include:: sys_meta_path.py
    :literal:
    :start-after: #end_pymotw_header

Each finder on the meta-path is interrogated before :data:`sys.path`
is searched, so there is always an opportunity to have a central
importer load modules without explicitly modifying :data:`sys.path`.
Once the module is "found", the loader API works in the same way as
for regular loaders (although this example is truncated for
simplicity).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_meta_path.py'))
.. }}}

::

    $ python sys_meta_path.py
    
    Creating NoisyMetaImportFinder for foo
    
    looking for "foo" with path "None"
     ... found prefix, returning loader
    loading foo
    
    looking for "foo.bar" with path "['path-entry-goes-here']"
     ... found prefix, returning loader
    loading foo.bar
    
    looking for "bar" with path "None"
     ... not the right prefix, cannot load

.. {{{end}}}
