==================================
 imp -- Python's Import Mechanism
==================================

.. module:: imp
    :synopsis: Interface to module import mechanism.

:Purpose: 
    The imp module exposes the implementation of Python's import statement.

The :mod:`imp` module includes functions that expose part of the
underlying implementation of Python's import mechanism for loading
code in packages and modules. It is one access point to importing
modules dynamically, and useful in some cases where the name of the
module that needs to be imported is unknown when the code is
written (e.g., for plugins or extensions to an application).

Example Package
===============

The examples in this section use a package called :mod:`example` with
``__init__.py``:

.. literalinclude:: example/__init__.py
    :caption:
    :start-after: #end_pymotw_header

and module called :mod:`submodule` containing:

.. literalinclude:: example/submodule.py
    :caption:
    :start-after: #end_pymotw_header

Watch for the text from the :command:`print` statements in the sample
output when the package or module are imported.

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
library or other module is not loading as expected, use
:func:`get_suffixes` to print a list of the supported types for the
current platform, and the parameters for loading them.

.. literalinclude:: imp_get_suffixes.py
    :caption:
    :start-after: #end_pymotw_header

The return value is a sequence of tuples containing the file
extension, mode to use for opening the file containing the module, and
a type code from a constant defined in the module. This table is
incomplete, because some of the importable module or package types do
not correspond to single files.  

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

The first step to loading a module is finding it. :func:`find_module`
scans the import search path looking for a package or module with the
given name. It returns an open file handle (if appropriate for the
type), filename where the module was found, and "description" (a tuple
such as those returned by :func:`get_suffixes`).

.. literalinclude:: imp_find_module.py
    :caption:
    :start-after: #end_pymotw_header

:func:`find_module` does not process dotted names
(``example.submodule``), so the caller has to take care to pass the
correct path for any nested modules. That means that when importing
the nested module from the package, give a path that points to the
package directory for :func:`find_module` to locate a module within
the package.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'imp_find_module.py'))
.. }}}

::

	$ python imp_find_module.py
	
	Package:
	package ./example
	
	Sub-module:
	source ./example/submodule.py

.. {{{end}}}

If :func:`find_module` cannot locate the module, it raises an
:class:`ImportError`.

.. literalinclude:: imp_find_module_error.py
    :caption:
    :start-after: #end_pymotw_header

The error message includes the name of the missing module.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'imp_find_module_error.py'))
.. }}}

::

	$ python imp_find_module_error.py
	
	ImportError: No module named no_such_module

.. {{{end}}}

Loading Modules
===============

After the module is found, use :func:`load_module` to actually
import it.  :func:`load_module` takes the full dotted path module name
and the values returned by :func:`find_module` (the open file handle,
filename, and description tuple).

.. literalinclude:: imp_load_module.py
    :caption:
    :start-after: #end_pymotw_header

:func:`load_module` creates a new module object with the name given,
loads the code for it, and adds it to :data:`sys.modules`.

.. NOT RUNNING
.. cog.out(run_script(cog.inFile, 'imp_load_module.py', 
..                    break_lines_at=70, line_break_mode='wrap'))

::

    $ python imp_load_module.py
    
    Importing example package
    Package: <module 'example' from '/Users/dhellmann/Documents/
    PyMOTW/book/PyMOTW/imp/example/__init__.pyc'>
    Importing submodule
    Sub-module: <module 'example.submodule' from '/Users/dhellmann/
    Documents/PyMOTW/book/PyMOTW/imp/example/submodule.pyc'>


If :func:`load_module` is called for a module that has already been
imported, the effect is like calling :func:`reload` on the existing
module object.

.. literalinclude:: imp_load_module_reload.py
    :caption:
    :start-after: #end_pymotw_header

Instead of a creating a new module, the contents of the existing
module are replaced.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'imp_load_module_reload.py'))
.. }}}

::

	$ python imp_load_module_reload.py
	
	0 (not in sys.modules) Importing example package
	1 (have in sys.modules) Importing example package

.. {{{end}}}

.. seealso::

    `imp <http://docs.python.org/library/imp.html>`_
        The standard library documentation for this module.
        
    :ref:`sys-imports`
        Import hooks, the module search path, and other related
        machinery in the :mod:`sys` module.

    :mod:`inspect`
        Load information from a module programmatically.

    :pep:`302`
        New import hooks.

    :pep:`369`
        Post import hooks.
