=========================================
 importlib --- Python's Import Mechanism
=========================================

.. module:: importlib
    :synopsis: Interface to module import mechanism.

:Purpose: The importlib module exposes the implementation of Python's
          import statement.

The ``importlib`` module includes functions that implement Python's
import mechanism for loading code in packages and modules. It is one
access point to importing modules dynamically, and useful in some
cases where the name of the module that needs to be imported is
unknown when the code is written (for example, for plugins or
extensions to an application).

Example Package
===============

The examples in this section use a package called ``example`` with
``__init__.py``.

.. literalinclude:: example/__init__.py
    :caption:
    :start-after: #end_pymotw_header

The package also contains ``submodule.py``.

.. literalinclude:: example/submodule.py
    :caption:
    :start-after: #end_pymotw_header

Watch for the text from the ``print()`` calls in the sample output
when the package or module are imported.

Module Types
============

Python supports several styles of modules. Each requires its own
handling when opening the module and adding it to the namespace, and
support for the formats varies by platform.  For example, under
Microsoft Windows, shared libraries are loaded from files with
extensions ``.dll`` or ``.pyd``, instead of ``.so``.  The extensions
for C modules may also change when using a debug build of the
interpreter instead of a normal release build, since they can be
compiled with debug information included as well.  If a C extension
library or other module is not loading as expected, use the constants
defined in ``importlib.machinery`` to find the supported types for
the current platform, and the parameters for loading them.

.. literalinclude:: importlib_suffixes.py
    :caption:
    :start-after: #end_pymotw_header

The return value is a sequence of tuples containing the file
extension, mode to use for opening the file containing the module, and
a type code from a constant defined in the module. This table is
incomplete, because some of the importable module or package types do
not correspond to single files.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'importlib_suffixes.py'))
.. }}}

.. code-block:: none

	$ python3 importlib_suffixes.py
	
	Source:     ['.py']
	Debug:      ['.pyc']
	Optimized:  ['.pyc']
	Bytecode:   ['.pyc']
	Extension:  ['.cpython-36m-darwin.so', '.abi3.so', '.so']

.. {{{end}}}

Importing Modules
=================

The high level API in ``importlib`` makes it simple to import a
module given an absolute or relative name.  When using a relative
module name, specify the package containing the module as a separate
argument.

.. literalinclude:: importlib_import_module.py
   :caption:
   :start-after: #end_pymotw_header

The return value from ``import_module()`` is the module object that
was created by the import.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'importlib_import_module.py'))
.. }}}

.. code-block:: none

	$ python3 importlib_import_module.py
	
	Importing example package
	Importing submodule
	<module 'example.submodule' from '.../example/submodule.py'>
	<module 'example.submodule' from '.../example/submodule.py'>
	True

.. {{{end}}}

If the module cannot be imported, ``import_module()`` raises
``ImportError``.

.. literalinclude:: importlib_import_module_error.py
   :caption:
   :start-after: #end_pymotw_header

The error message includes the name of the missing module.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'importlib_import_module_error.py'))
.. }}}

.. code-block:: none

	$ python3 importlib_import_module_error.py
	
	Importing example package
	Error: No module named 'example.nosuchmodule'

.. {{{end}}}

To reload an existing module, use ``reload()``.

.. literalinclude:: importlib_reload.py
   :caption:
   :start-after: #end_pymotw_header

The return value from ``reload()`` is the new module. Depending on
which type of loader was used, it may be the same module instance.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'importlib_reload.py'))
.. }}}

.. code-block:: none

	$ python3 importlib_reload.py
	
	Importing example package
	Importing submodule
	<module 'example.submodule' from '.../example/submodule.py'>
	Importing submodule
	True

.. {{{end}}}

Loaders
=======

The lower-level API in ``importlib`` provides access to the loader
objects, as described in :ref:`sys-imports` from the section on the
``sys`` module. To get a loader for a module, use
``find_loader()``. Then to retrieve the module, use the loader's
``load_module()`` method.

.. literalinclude:: importlib_find_loader.py
   :caption:
   :start-after: #end_pymotw_header

This example loads the top level of the ``example`` package.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'importlib_find_loader.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 importlib_find_loader.py
	
	Loader: <_frozen_importlib_external.SourceFileLoader object at
	0x101fe1828>
	Importing example package
	Module: <module 'example' from '.../example/__init__.py'>

.. {{{end}}}

Submodules within packages need to be loaded separately using the path
from the package. In the following example, the package is loaded
first and then its path is passed to ``find_loader()`` to create a
loader capable of loading the submodule.

.. literalinclude:: importlib_submodule.py
   :caption:
   :start-after: #end_pymotw_header

Unlike with ``import_module()``, the name of the submodule should be
given without any relative path prefix, since the loader will already
be constrained by the package's path.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'importlib_submodule.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 importlib_submodule.py
	
	Importing example package
	Loader: <_frozen_importlib_external.SourceFileLoader object at
	0x101fe1f28>
	Importing submodule
	Module: <module 'submodule' from '.../example/submodule.py'>

.. {{{end}}}

.. seealso::

   * :pydoc:`importlib`

   * :ref:`sys-imports` -- Import hooks, the module search path, and
     other related machinery in the ``sys`` module.

   * :mod:`inspect` -- Load information from a module
     programmatically.

   * :pep:`302` -- New import hooks.

   * :pep:`369` -- Post import hooks.

   * :pep:`488` -- Elimination of PYO files.
