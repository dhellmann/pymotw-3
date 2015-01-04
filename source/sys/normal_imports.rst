.. _sys-modules:

Imported Modules
================

:data:`sys.modules` is a dictionary mapping the names of imported
modules to the module object holding the code.

.. include:: sys_modules.py
    :literal:
    :start-after: #end_pymotw_header

The contents of :data:`sys.modules` change as new modules are imported.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_modules.py'))
.. }}}

::

    $ python sys_modules.py
        
    UserDict, __builtin__, __main__, _abcoll, _codecs, _sre,
    _warnings, abc, codecs, copy_reg, encodings,
    encodings.__builtin__, encodings.aliases, encodings.codecs,
    encodings.encodings, encodings.utf_8, errno, exceptions,
    genericpath, linecache, os, os.path, posix, posixpath, re,
    signal, site, sre_compile, sre_constants, sre_parse, stat,
    string, strop, sys, textwrap, types, warnings, zipimport

.. {{{end}}}


Built-in Modules
================

The Python interpreter can be compiled with some C modules built right
in, so they do not need to be distributed as separate shared
libraries. These modules do not appear in the list of imported modules
managed in :data:`sys.modules` because they were not technically
imported. The only way to find the available built-in modules is
through :data:`sys.builtin_module_names`.

.. include:: sys_builtins.py
    :literal:
    :start-after: #end_pymotw_header

The output of this script will vary, especially if run with a
custom-built version of the interpreter.  This output was created
using a copy of the interpreter installed from the standard python.org
installer for OS X.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_builtins.py'))
.. }}}

::

    $ python sys_builtins.py
    
    __builtin__, __main__, _ast, _codecs, _sre, _symtable, _warnings,
    errno, exceptions, gc, imp, marshal, posix, pwd, signal, sys,
    thread, xxsubtype, zipimport

.. {{{end}}}


.. seealso::

    `Build Instructions <http://svn.python.org/view/python/trunk/README?view=markup>`_
        Instructions for building Python, from the README distributed with the source.

.. _sys-path:

Import Path
===========

The search path for modules is managed as a Python list saved in
:data:`sys.path`. The default contents of the path include the directory
of the script used to start the application and the current working
directory.

.. include:: sys_path_show.py
    :literal:
    :start-after: #end_pymotw_header

The first directory in the search path is the home for the sample
script itself. That is followed by a series of platform-specific paths
where compiled extension modules (written in C) might be installed,
and then the global ``site-packages`` directory is listed last.

::

    $ python sys_path_show.py

    /Users/dhellmann/Documents/PyMOTW/book/PyMOTW/sys
    .../lib/python2.7
    .../lib/python2.7/plat-darwin
    .../lib/python2.7/lib-tk
    .../lib/python2.7/plat-mac
    .../lib/python2.7/plat-mac/lib-scriptpackages
    .../lib/python2.7/site-packages


The import search path list can be modified before starting the
interpreter by setting the shell variable :data:`PYTHONPATH` to a
colon-separated list of directories.

::

    $ PYTHONPATH=/my/private/site-packages:/my/shared/site-packages \
    > python sys_path_show.py

    /Users/dhellmann/Documents/PyMOTW/book/PyMOTW/sys
    /my/private/site-packages
    /my/shared/site-packages
    .../lib/python2.7
    .../lib/python2.7/plat-darwin
    .../lib/python2.7/lib-tk
    .../lib/python2.7/plat-mac
    .../lib/python2.7/plat-mac/lib-scriptpackages
    .../lib/python2.7/site-packages

A program can also modify its path by adding elements to
:data:`sys.path` directly.

.. include:: sys_path_modify.py
    :literal:
    :start-after: #end_pymotw_header

Reloading an imported module re-imports the file, and uses the same
:class:`module` object to hold the results.  Changing the path between
the initial import and the call to :func:`reload` means a different
module may be loaded the second time.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_path_modify.py'))
.. }}}

::

    $ python sys_path_modify.py
    
    Base directory: .
    Imported example from: ./package_dir_a/example.pyc
        This is example A
    Reloaded example from: ./package_dir_b/example.pyc
        This is example B

.. {{{end}}}
