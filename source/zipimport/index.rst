.. _zipimport-ref:

==================================================
 zipimport --- Load Python Code from ZIP Archives
==================================================

.. module:: zipimport
    :synopsis: Load Python code from ZIP archives.

:Purpose: Import Python modules saved as members of ZIP archives.

The :mod:`zipimport` module implements the :class:`zipimporter` class,
which can be used to find and load Python modules inside ZIP
archives. The :class:`zipimporter` supports the "import hooks" API
specified in PEP 302; this is how Python Eggs work.

It is not usually necessary to use the :mod:`zipimport` module
directly, since it is possible to import directly from a ZIP archive
as long as that archive appears in :data:`sys.path`. However, it is
instructive to study how the importer API can be used, to learn the
features available and understand how module importing works.  Knowing
how the ZIP importer works will also help debug issues that may come
up when distributing applications packaged as ZIP archives created
with :class:`zipfile.PyZipFile`.

Example
=======

These examples reuse some of the code from the discussion of
:mod:`zipfile` to create an example ZIP archive containing a few
Python modules.

.. literalinclude:: zipimport_make_example.py
   :caption:
   :start-after: #end_pymotw_header

Run ``zipimport_make_example.py`` before any of the rest of the
examples to create a ZIP archive containing all of the modules in the
example directory, along with some test data needed for the examples
in this section.

.. {{{cog
.. # clean up pyc files in case the interpreter version has
.. # changed since the last build
.. workdir = path(cog.inFile).dirname()
.. print('removing *.pyc')
.. sh("find %s -name '*.pyc' | xargs rm" % workdir)
.. print('removing __pycache__')
.. sh("rm -rf %s" % (workdir / '__pycache__'))
.. print('removing example_package/__pycache__')
.. sh("rm -rf %s" % (workdir / 'example_package/__pycache__'))
.. unlink(workdir / 'zipimport_example.zip')
.. cog.out(run_script(cog.inFile, 'zipimport_make_example.py'))
.. }}}

::

	$ python3 zipimport_make_example.py
	
	__init__.pyc
	example_package/__init__.pyc
	zipimport_find_module.pyc
	zipimport_get_code.pyc
	zipimport_get_data.pyc
	zipimport_get_data_nozip.pyc
	zipimport_get_data_zip.pyc
	zipimport_get_source.pyc
	zipimport_is_package.pyc
	zipimport_load_module.pyc
	zipimport_make_example.pyc
	zipimport_get_source.py
	example_package/README.txt

.. {{{end}}}


Finding a Module
================

Given the full name of a module, :func:`find_module()` will try to
locate that module inside the ZIP archive.

.. literalinclude:: zipimport_find_module.py
   :caption:
   :start-after: #end_pymotw_header

If the module is found, the :class:`zipimporter` instance is
returned. Otherwise, ``None`` is returned.

.. {{{cog
.. (path(cog.inFile).parent / 'zipimport_example.zip').unlink()
.. run_script(cog.inFile, 'zipimport_make_example.py')
.. cog.out(run_script(cog.inFile, 'zipimport_find_module.py', line_break_mode='wrap'))
.. }}}

::

	$ python3 zipimport_find_module.py
	
	zipimport_find_module : <zipimporter object
	"zipimport_example.zip">
	not_there : None

.. {{{end}}}

Accessing Code
==============

The :func:`get_code()` method loads the code object for a module from
the archive.

.. literalinclude:: zipimport_get_code.py
   :caption:
   :start-after: #end_pymotw_header

The code object is not the same as a :class:`module` object, but is
used to create one.

.. {{{cog
.. (path(cog.inFile).parent / 'zipimport_example.zip').unlink()
.. run_script(cog.inFile, 'zipimport_make_example.py')
.. cog.out(run_script(cog.inFile, 'zipimport_get_code.py', 
..                    break_lines_at=65, line_break_mode='wrap'))
.. }}}

::

	$ python3 zipimport_get_code.py
	
	<code object <module> at 0x101253810, file
	"./zipimport_get_code.py", line 6>

.. {{{end}}}

To load the code as a usable module, use :func:`load_module()`
instead.

.. literalinclude:: zipimport_load_module.py
   :caption:
   :start-after: #end_pymotw_header

The result is a module object configured as though the code had been
loaded from a regular import.

.. {{{cog
.. (path(cog.inFile).parent / 'zipimport_example.zip').unlink()
.. run_script(cog.inFile, 'zipimport_make_example.py')
.. cog.out(run_script(cog.inFile, 'zipimport_load_module.py', 
..                    break_lines_at=65, line_break_mode='wrap'))
.. }}}

::

	$ python3 zipimport_load_module.py
	
	<code object <module> at 0x1012b48a0, file
	"./zipimport_get_code.py", line 6>
	Name   : zipimport_get_code
	Loader : <zipimporter object "zipimport_example.zip">
	Code   : <code object <module> at 0x1012b48a0, file
	"./zipimport_get_code.py", line 6>

.. {{{end}}}

Source
======

As with the :mod:`inspect` module, it is possible to retrieve the
source code for a module from the ZIP archive, if the archive includes
the source. In the case of the example, only
``zipimport_get_source.py`` is added to ``zipimport_example.zip`` (the
rest of the modules are just added as the ``.pyc`` files).

.. literalinclude:: zipimport_get_source.py
   :caption:
   :start-after: #end_pymotw_header

If the source for a module is not available, :func:`get_source()`
returns ``None``.

.. {{{cog
.. (path(cog.inFile).parent / 'zipimport_example.zip').unlink()
.. run_script(cog.inFile, 'zipimport_make_example.py')
.. cog.out(run_script(cog.inFile, 'zipimport_get_source.py', 
..                    break_lines_at=65, line_break_mode='truncate'))
.. }}}

::

	$ python3 zipimport_get_source.py
	
	=================================================================
	zipimport_get_code
	=================================================================
	None
	
	=================================================================
	zipimport_get_source
	=================================================================
	#!/usr/bin/env python3
	#
	# Copyright 2007 Doug Hellmann.
	#
	"""Retrieving the source code for a module within a zip archive.
	"""
	#end_pymotw_header
	
	import zipimport
	
	modules = [
	    'zipimport_get_code',
	    'zipimport_get_source',
	]
	
	importer = zipimport.zipimporter('zipimport_example.zip')
	for module_name in modules:
	    source = importer.get_source(module_name)
	    print('=' * 80)
	    print(module_name)
	    print('=' * 80)
	    print(source)
	    print()
	
	

.. {{{end}}}

Packages
========

To determine if a name refers to a package instead of a regular module, use
:func:`is_package()`.

.. literalinclude:: zipimport_is_package.py
   :caption:
   :start-after: #end_pymotw_header

In this case, ``zipimport_is_package`` came from a module and the
``example_package`` is a package.

.. {{{cog
.. (path(cog.inFile).parent / 'zipimport_example.zip').unlink()
.. run_script(cog.inFile, 'zipimport_make_example.py')
.. cog.out(run_script(cog.inFile, 'zipimport_is_package.py'))
.. }}}

::

	$ python3 zipimport_is_package.py
	
	zipimport_is_package False
	example_package True

.. {{{end}}}

Data
====

There are times when source modules or packages need to be distributed
with non-code data. Images, configuration files, default data, and
test fixtures are just a few examples of this. Frequently, the module
:attr:`__path__` or :attr:`__file__` attributes are used to find these
data files relative to where the code is installed.

For example, with a "normal" module, the file system path can be
constructed from the :attr:`__file__` attribute of the imported
package like this:

.. literalinclude:: zipimport_get_data_nozip.py
   :caption:
   :start-after: #end_pymotw_header

The output will depend on where the sample code is located on the
file system.

.. {{{cog
.. (path(cog.inFile).parent / 'zipimport_example.zip').unlink()
.. run_script(cog.inFile, 'zipimport_make_example.py')
.. cog.out(run_script(cog.inFile, 'zipimport_get_data_nozip.py'))
.. }}}

::

	$ python3 zipimport_get_data_nozip.py
	
	example_package/README.txt :
	This file represents sample data which could be embedded in the
	ZIP archive.  You could include a configuration file, images, or
	any other sort of noncode data.
	

.. {{{end}}}

If the ``example_package`` is imported from the ZIP archive instead of
the file system, using :attr:`__file__` does not work:

.. literalinclude:: zipimport_get_data_zip.py
   :caption:
   :start-after: #end_pymotw_header

The :attr:`__file__` of the package refers to the ZIP archive, and not
a directory, so building up the path to the ``README.txt`` file gives
the wrong value.

.. {{{cog
.. (path(cog.inFile).parent / 'zipimport_example.zip').unlink()
.. run_script(cog.inFile, 'zipimport_make_example.py')
.. cog.out(run_script(cog.inFile, 'zipimport_get_data_zip.py', ignore_error=True,
..                    break_lines_at=65, line_break_mode='wrap'))
.. }}}

::

	$ python3 zipimport_get_data_zip.py
	
	zipimport_example.zip/example_package/__init__.pyc
	zipimport_example.zip/example_package/README.txt :
	Traceback (most recent call last):
	  File "zipimport_get_data_zip.py", line 20, in <module>
	    print(open(data_filename, 'rt').read())
	NotADirectoryError: [Errno 20] Not a directory:
	'zipimport_example.zip/example_package/README.txt'

.. {{{end}}}

A more reliable way to retrieve the file is to use the
:func:`get_data()` method. The :class:`zipimporter` instance that
loaded the module can be accessed through the :attr:`__loader__`
attribute of the imported module:

.. literalinclude:: zipimport_get_data.py
   :caption:
   :start-after: #end_pymotw_header

:func:`pkgutil.get_data` uses this interface to access data from
within a package. The value returned is a byte string, which needs to
be decoded to a unicode string before printing.

.. {{{cog
.. (path(cog.inFile).parent / 'zipimport_example.zip').unlink()
.. run_script(cog.inFile, 'zipimport_make_example.py')
.. cog.out(run_script(cog.inFile, 'zipimport_get_data.py'))
.. }}}

::

	$ python3 zipimport_get_data.py
	
	zipimport_example.zip/example_package/__init__.pyc
	This file represents sample data which could be embedded in the
	ZIP archive.  You could include a configuration file, images, or
	any other sort of noncode data.
	

.. {{{end}}}

The ``__loader__`` is not set for modules not imported via
:mod:`zipimport`.

.. seealso::

   * :pydoc:`zipimport`

   * :ref:`Porting notes for zipimport <porting-zipimport>`

   * :mod:`imp` -- Other import-related functions.

   * :mod:`pkgutil` -- Provides a more generic interface to
     :func:`get_data`.

   * :mod:`zipfile` -- Read and write ZIP archive files.

   * :pep:`302` -- New Import Hooks
