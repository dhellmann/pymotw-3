============================================
imp -- Interface to module import mechanism.
============================================

.. module:: imp
    :synopsis: Interface to module import mechanism.

:Purpose: 
    The imp module exposes the implementation of Python's import statement.
:Available In: At least 2.2.1

The imp module includes functions that expose part of the underlying
implementation of Python's import mechanism for loading code in packages and
modules. It is one access point to importing modules dynamically, and useful
in some cases where you don't know the name of the module you need to import
when you write your code (e.g., for plugins or extensions to an application).

Example Package
===============

The examples below use a package called "example" with ``__init__.py``:

.. include:: example/__init__.py
    :literal:
    :start-after: #end_pymotw_header

and module called submodule containing:

.. include:: example/submodule.py
    :literal:
    :start-after: #end_pymotw_header

Watch for the text from the print statements in the sample output when
the package or module are imported.

Module Types
============

Python supports several styles of modules. Each requires its own handling when
opening the module and adding it to the namespace. Some of the supported types
and those parameters can be listed by the ``get_suffixes()`` function.

.. include:: imp_get_suffixes.py
    :literal:
    :start-after: #end_pymotw_header

``get_suffixes()`` returns a sequence of tuples containing the file
extension, mode to use for opening the file, and a type code from a
constant defined in the module. This table is incomplete, because some
of the importable module or package types do not correspond to single
files.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'imp_get_suffixes.py'))
.. }}}

::

	$ python imp_get_suffixes.py
	
	 Extension       Mode       Type
	--------------------------------
	       .so         rb  extension
	 module.so         rb  extension
	       .py          U     source
	      .pyc         rb   compiled

.. {{{end}}}

Finding Modules
===============

The first step to loading a module is finding it. ``find_module()``
scans the import search path looking for a package or module with the
given name. It returns an open file handle (if appropriate for the
type), filename where the module was found, and "description" (a tuple
such as those returned by ``get_suffixes()``).

.. include:: imp_find_module.py
    :literal:
    :start-after: #end_pymotw_header

``find_module()`` does not pay attention to dotted package names
("example.submodule"), so the caller has to take care to pass the
correct path for any nested modules. That means that when importing
the submodule from the package, you need to give a path that points to
the package directory for ``find_module()`` to locate the module
you're looking for.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'imp_find_module.py'))
.. }}}

::

	$ python imp_find_module.py
	
	Package:
	package /Users/dhellmann/Documents/PyMOTW/src/PyMOTW/imp/example
	
	Sub-module:
	source /Users/dhellmann/Documents/PyMOTW/src/PyMOTW/imp/example/submodule.py

.. {{{end}}}

If ``find_module()`` cannot locate the module, it raises an
:ref:`ImportError <exceptions-ImportError>`.

.. include:: imp_find_module_error.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'imp_find_module_error.py'))
.. }}}

::

	$ python imp_find_module_error.py
	
	ImportError: No module named no_such_module

.. {{{end}}}

Loading Modules
===============

Once you have found the module, use ``load_module()`` to actually
import it.  ``load_module()`` takes the full dotted path module name
and the values returned by ``find_module()`` (the open file handle,
filename, and description tuple).

.. include:: imp_load_module.py
    :literal:
    :start-after: #end_pymotw_header

``load_module()`` creates a new module object with the name given,
loads the code for it, and adds it to :ref:`sys.modules
<sys-modules>`.

.. Do not use cog for this example because the path changes.

::

	$ python imp_load_module.py
	Importing example package
	Package: <module 'example' from '/Users/dhellmann/Documents/PyMOTW/trunk/PyMOTW/imp/example/__init__.py'>
	Importing submodule
	Sub-module: <module 'example.module' from '/Users/dhellmann/Documents/PyMOTW/trunk/PyMOTW/imp/example/submodule.py'>

If you call ``load_module()`` for a module which has already been
imported, the effect is like calling ``reload()`` on the existing
module object.

.. include:: imp_load_module_reload.py
    :literal:
    :start-after: #end_pymotw_header

Instead of a creating a new module, the contents of the existing
module are simply replaced.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'imp_load_module_reload.py'))
.. }}}

::

	$ python imp_load_module_reload.py
	
	0 (not in sys.modules) Importing example package
	1 (have in sys.modules) Importing example package

.. {{{end}}}

.. seealso::

    `imp <http://docs.python.org/2.7/library/imp.html>`_
        The standard library documentation for this module.
        
    :ref:`sys-imports`
        Import hooks, the module search path, and other related machinery.

    :mod:`inspect`
        Load information from a module programmatically.

    :pep:`302`
        New import hooks.

    :pep:`369`
        Post import hooks.
