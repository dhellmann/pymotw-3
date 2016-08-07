======================================
 venv --- Create Virtual Environments
======================================

.. module:: venv
    :synopsis: Create isolated installation and execution contexts.

:Purpose: Create isolated installation and execution contexts.

Python virtual environments, managed by :mod:`venv`, define isolated
environments for installing packages and running programs. Because
each environment has its own interpreter executable and directory for
installing packages it is easy to create environments configured with
various combinations of Python and package versions all on the same
computer.

Creating Environments
=====================

The command line interface to :mod:`venv` depends on how Python was
compiled and installed. The :command:`pyvenv` command is the simplest
interface

.. {{{cog
.. run_script(cog.inFile, 'rm -rf /tmp/testenv', interpreter='')
.. cog.out(run_script(cog.inFile, 'pyvenv /tmp/testenv', interpreter=''))
.. }}}

.. code-block:: none

	$ pyvenv /tmp/testenv
	

.. {{{end}}}

If :command:`pyvenv` is not installed or not on the shell search path,
it is possible to run the :mod:`venv` module using the interpreter's
``-m`` option. The following command has the same effect as the
previous example.

.. code-block:: none

	$ python3 -m venv /tmp/testenv

Contents of a Virtual Environment
=================================

Each virtual environment contains a ``bin`` directory, where the local
interpreter and any executable scripts are installed, an ``include``
directory for files related to building C extensions, and a ``lib``
directory, with a separate ``site-packages`` location for installing
packages.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ls -F /tmp/testenv', interpreter=''))
.. }}}

.. code-block:: none

	$ ls -F /tmp/testenv
	
	bin/
	include/
	lib/
	pyvenv.cfg

.. {{{end}}}

The default ``bin`` directory contains "activation" scripts for
several UNIX shell variants. These can be used to install the virtual
environment on the shell's search path to ensure the shell picks up
programs installed in the environment. It's not necessary to activate
an environment to use programs installed into it, but it can be more
convenient.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ls -F /tmp/testenv/bin', interpreter=''))
.. }}}

.. code-block:: none

	$ ls -F /tmp/testenv/bin
	
	activate
	activate.csh
	activate.fish
	easy_install*
	easy_install-3.5*
	pip*
	pip3*
	pip3.5*
	python@
	python3@
	python3.5@

.. {{{end}}}

On platforms that support them, symbolic links are used rather than
copying the executables like the Python interpreter. In this
environment, :command:`pip` is installed as a local copy but the
interpreter is a symlink.

Finally, the environment includes a ``pyvenv.cfg`` file with settings
describing how the environment is configured and should behave. The
``home`` variable points to the location of the Python interpreter
where :mod:`venv` was run to create the
environment. ``include-system-site-packages`` is a boolean indicating
whether or not the packages installed outside of the virtual
environment, at the system level, should be visible inside the virtual
environment. And ``version`` is the Python version used to create the
environment.

.. Copy the environment config file into a place that works with
.. the sphinx include directive.
.. {{{cog
.. run_script(cog.inFile, 'cp /tmp/testenv/pyvenv.cfg .', interpreter='')
.. }}}
.. {{{end}}}

.. literalinclude:: pyvenv.cfg
   :caption:

.. seealso::

   * :pydoc:`venv`

   * :pep:`405` -- Python Virtual Environments

   * `virtualenv <https://pypi.python.org/pypi/virtualenv>`__ -- A
     version of Python virtual environments that works for Python 2
     and 3.

   * `virtualenvwrapper
     <https://pypi.python.org/pypi/virtualenvwrapper>` __ -- A set of
     shell wrappers for virtualenv to make it easier to manage a large
     number of environments.
