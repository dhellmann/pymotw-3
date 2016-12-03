======================================================
 sysconfig --- Interpreter Compile-time Configuration
======================================================

.. module:: sysconfig
    :synopsis: Interpreter Compile-time Configuration

:Purpose: Access the configuration settings used to build Python.

The features of ``sysconfig`` have been extracted from
:mod:`distutils` to create a stand-alone module.  It includes
functions for determining the settings used to compile and install the
current interpreter.

Configuration Variables
=======================

Access the build-time configuration settings is provided through two
functions.  :func:`get_config_vars` returns a dictionary mapping the
configuration variable names to values.

.. literalinclude:: sysconfig_get_config_vars.py
   :caption:
   :start-after: #end_pymotw_header

The level of detail available through the ``sysconfig`` API depends
on the platform where a program is running.  On POSIX systems such as
Linux and OS X, the ``Makefile`` used to build the interpreter and
``config.h`` header file generated for the build are parsed and all of
the variables found within are available.  On non-POSIX
systems such as Windows, the settings are limited to a few paths,
filename extensions, and version details.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sysconfig_get_config_vars.py',
..                    line_cleanups=[], line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 sysconfig_get_config_vars.py
	
	Found 665 configuration settings
	
	Some highlights:
	
	 Installation prefixes:
	  prefix=/Library/Frameworks/Python.framework/Versions/3.5
	  exec_prefix=/Library/Frameworks/Python.framework/Versions/3.5
	
	 Version info:
	  py_version=3.5.2
	  py_version_short=3.5
	  py_version_nodot=35
	
	 Base directories:
	  base=/Users/dhellmann/Envs/pymotw35
	  platbase=/Users/dhellmann/Envs/pymotw35
	  userbase=/Users/dhellmann/Library/Python/3.5
	  srcdir=/Library/Frameworks/Python.framework/Versions/3.5/lib/p
	ython3.5/config-3.5m
	
	 Compiler and linker flags:
	  LDFLAGS=-arch i386 -arch x86_64  -g
	  BASECFLAGS=-fno-strict-aliasing -Wsign-compare -fno-common
	-dynamic
	  Py_ENABLE_SHARED=0

.. {{{end}}}

Passing variable names to :func:`get_config_vars` changes the return
value to a :class:`list` created by appending all of the values for
those variables together.

.. literalinclude:: sysconfig_get_config_vars_by_name.py
   :caption:
   :start-after: #end_pymotw_header

This example builds a list of all of the installation base directories
where modules can be found on the current system.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sysconfig_get_config_vars_by_name.py',
..                    line_cleanups=[]))
.. }}}

.. code-block:: none

	$ python3 sysconfig_get_config_vars_by_name.py
	
	Base directories:
	   /Users/dhellmann/Envs/pymotw35
	   /Users/dhellmann/Envs/pymotw35
	   /Users/dhellmann/Library/Python/3.5

.. {{{end}}}

When only a single configuration value is needed, use
:func:`get_config_var` to retrieve it.

.. literalinclude:: sysconfig_get_config_var.py
   :caption:
   :start-after: #end_pymotw_header

If the variable is not found, :func:`get_config_var` returns ``None``
instead of raising an exception.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sysconfig_get_config_var.py'))
.. }}}

.. code-block:: none

	$ python3 sysconfig_get_config_var.py
	
	User base directory: /Users/dhellmann/Library/Python/3.5
	Unknown variable   : None

.. {{{end}}}


Installation Paths
==================

``sysconfig`` is primarily meant to be used by installation and
packaging tools.  As a result, while it provides access to general
configuration settings such as the interpreter version, it is focused
on the information needed to locate parts of the Python distribution
currently installed on a system.  The locations used for installing a
package depend on the *scheme* used.

A scheme is a set of platform-specific default directories organized
based on the platform's packaging standards and guidelines.  There are
different schemes for installing into a site-wide location or a
private directory owned by the user.  The full set of schemes can be
accessed with :func:`get_scheme_names`.

.. literalinclude:: sysconfig_get_scheme_names.py
   :caption:
   :start-after: #end_pymotw_header

There is no concept of a "current scheme" per se.  The default scheme
depends on the platform, and the actual scheme used depends on options
given to the installation program.  If the current system is running a
POSIX-compliant operating system, the default is ``posix_prefix``.
Otherwise the default is the operating system name, as defined by
:data:`os.name`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sysconfig_get_scheme_names.py'))
.. }}}

.. code-block:: none

	$ python3 sysconfig_get_scheme_names.py
	
	nt
	nt_user
	osx_framework_user
	posix_home
	posix_prefix
	posix_user

.. {{{end}}}

Each scheme defines a set of paths used for installing packages.  For
a list of the path names, use :func:`get_path_names`.

.. literalinclude:: sysconfig_get_path_names.py
   :caption:
   :start-after: #end_pymotw_header

Some of the paths may be the same for a given scheme, but installers
should not make any assumptions about what the actual paths are.  Each
name has a particular semantic meaning, so the correct name should be
used to find the path for a given file during installation.  Refer to
:table:`Path Names Used in sysconfig` for a complete list of the path names
and their meaning.

.. table:: Path Names Used in sysconfig

   ===============  ===========
   Name             Description
   ===============  ===========
   ``stdlib``       Standard Python library files, not platform-specific
   ``platstdlib``   Standard Python library files, platform-specific
   ``platlib``      Site-specific, platform-specific files
   ``purelib``      Site-specific, non-platform-specific files
   ``include``      Header files, not platform-specific 
   ``platinclude``  Header files, platform-specific
   ``scripts``      Executable script files
   ``data``         Data files
   ===============  ===========

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sysconfig_get_path_names.py'))
.. }}}

.. code-block:: none

	$ python3 sysconfig_get_path_names.py
	
	stdlib
	platstdlib
	purelib
	platlib
	include
	scripts
	data

.. {{{end}}}

Use :func:`get_paths` to retrieve the actual directories associated
with a scheme.

.. literalinclude:: sysconfig_get_paths.py
   :caption:
   :start-after: #end_pymotw_header

This example shows the difference between the system-wide paths used
for ``posix_prefix`` under a framework build on Mac OS X, and the
user-specific values for ``posix_user``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sysconfig_get_paths.py', line_cleanups=[]))
.. }}}

.. code-block:: none

	$ python3 sysconfig_get_paths.py
	
	posix_prefix
	============
	prefix = /Users/dhellmann/Envs/pymotw35
	
	data
	  .
	include
	  ./include/python3.5m
	platinclude
	  ./include/python3.5m
	platlib
	  ./lib/python3.5/site-packages
	platstdlib
	  ./lib/python3.5
	purelib
	  ./lib/python3.5/site-packages
	scripts
	  ./bin
	stdlib
	  ./lib/python3.5
	
	posix_user
	==========
	prefix = /Users/dhellmann/Library/Python/3.5
	
	data
	  .
	include
	  ./include/python3.5
	platlib
	  ./lib/python3.5/site-packages
	platstdlib
	  ./lib/python3.5
	purelib
	  ./lib/python3.5/site-packages
	scripts
	  ./bin
	stdlib
	  ./lib/python3.5
	

.. {{{end}}}

For an individual path, call :func:`get_path`.

.. literalinclude:: sysconfig_get_path.py
   :caption:
   :start-after: #end_pymotw_header

Using :func:`get_path` is equivalent to saving the value of
:func:`get_paths` and looking up the individual key in the dictionary.
If several paths are needed, :func:`get_paths` is more efficient
because it does not recompute all of the paths each time.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sysconfig_get_path.py', line_cleanups=[]))
.. }}}

.. code-block:: none

	$ python3 sysconfig_get_path.py
	
	posix_prefix
	============
	purelib = /Users/dhellmann/Envs/pymotw35/lib/python3.5/site-pack
	ages
	
	posix_user
	==========
	purelib = /Users/dhellmann/Library/Python/3.5/lib/python3.5/site
	-packages
	

.. {{{end}}}

Python Version and Platform
===========================

While :mod:`sys` includes some basic platform identification (see
:ref:`sys-build-time-info`), it is not specific enough to be used for
installing binary packages because :data:`sys.platform` does not
always include information about hardware architecture, instruction size, or
other values that effect the compatibility of binary libraries.  For a
more precise platform specifier, use :func:`get_platform`.

.. literalinclude:: sysconfig_get_platform.py
   :caption:
   :start-after: #end_pymotw_header

Although this sample output was prepared on an OS X 10.6 system, the
interpreter is compiled for 10.5 compatibility, so that is the version
number included in the platform string.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sysconfig_get_platform.py'))
.. }}}

.. code-block:: none

	$ python3 sysconfig_get_platform.py
	
	macosx-10.6-intel

.. {{{end}}}

As a convenience, the interpreter version from
:data:`sys.version_info` is also available through
:func:`get_python_version` in ``sysconfig``.

.. literalinclude:: sysconfig_get_python_version.py
   :caption:
   :start-after: #end_pymotw_header

:func:`get_python_version` returns a string suitable for use when
building a version-specific path.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sysconfig_get_python_version.py'))
.. }}}

.. code-block:: none

	$ python3 sysconfig_get_python_version.py
	
	sysconfig.get_python_version(): 3.5
	
	sys.version_info:
	  major       : 3
	  minor       : 5
	  micro       : 2
	  releaselevel: final
	  serial      : 0

.. {{{end}}}

.. seealso::

   * :pydoc:`sysconfig`

   * :mod:`distutils` -- ``sysconfig`` used to be part of the
     ``distutils`` package.

   * :mod:`site` -- The ``site`` module describes the paths searched
     when importing in more detail.

   * :mod:`os` -- Includes ``os.name``, the name of the current
     operating system.

   * :mod:`sys` -- Includes other build-time information such as the
     platform.
