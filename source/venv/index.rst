======================================
 venv --- Create Virtual Environments
======================================

.. module:: venv
    :synopsis: Create isolated installation and execution contexts.

:Purpose: Create isolated installation and execution contexts.

Python virtual environments, managed by ``venv``, are set up for
installing packages and running programs in a way that isolates them
from other packages installed on the rest of the system. Because each
environment has its own interpreter executable and directory for
installing packages, it is easy to create environments configured with
various combinations of Python and package versions all on the same
computer.

Creating Environments
=====================

The command line interface to ``venv`` depends on how Python was
compiled and installed. The ``pyvenv`` command is the simplest
interface

.. {{{cog
.. run_script(cog.inFile, 'rm -rf /tmp/demoenv', interpreter='')
.. cog.out(run_script(cog.inFile, 'pyvenv /tmp/demoenv', interpreter=''))
.. }}}

.. code-block:: none

	$ pyvenv /tmp/demoenv
	

.. {{{end}}}

If ``pyvenv`` is not installed or not on the shell search path,
it is possible to run the ``venv`` module using the interpreter's
``-m`` option. The following command has the same effect as the
previous example.

.. code-block:: none

	$ python3 -m venv /tmp/demoenv

Contents of a Virtual Environment
=================================

Each virtual environment contains a ``bin`` directory, where the local
interpreter and any executable scripts are installed, an ``include``
directory for files related to building C extensions, and a ``lib``
directory, with a separate ``site-packages`` location for installing
packages.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ls -F /tmp/demoenv', interpreter=''))
.. }}}

.. code-block:: none

	$ ls -F /tmp/demoenv
	
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
.. cog.out(run_script(cog.inFile, 'ls -F /tmp/demoenv/bin', interpreter=''))
.. }}}

.. code-block:: none

	$ ls -F /tmp/demoenv/bin
	
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
environment, ``pip`` is installed as a local copy but the
interpreter is a symlink.

Finally, the environment includes a ``pyvenv.cfg`` file with settings
describing how the environment is configured and should behave. The
``home`` variable points to the location of the Python interpreter
where ``venv`` was run to create the
environment. ``include-system-site-packages`` is a boolean indicating
whether or not the packages installed outside of the virtual
environment, at the system level, should be visible inside the virtual
environment. And ``version`` is the Python version used to create the
environment.

.. Copy the environment config file into a place that works with
.. the sphinx include directive.
.. {{{cog
.. run_script(cog.inFile, 'cp /tmp/demoenv/pyvenv.cfg .', interpreter='')
.. }}}
.. {{{end}}}

.. literalinclude:: pyvenv.cfg
   :caption:
   :language: none

A virtual environment is more useful with tools like ``pip``
and :mod:`setuptools` available to install other packages, so
``pyvenv`` installs them by default. To create a bare
environment without these tools, pass ``--without-pip`` on the command
line.

Using Virtual Environments
==========================

Virtual environments are commonly used to run different versions of
programs or to test a given version of a program with different
versions of its dependencies. For example, before upgrading from one
version of Sphinx to another, it is useful to test the input
documentation files using both the old and new versions. To start,
create two virtual environments.

.. {{{cog
.. # Remove previous run.
.. run_script(cog.inFile, 'rm -rf /tmp/sphinx1', interpreter='')
.. run_script(cog.inFile, 'rm -rf /tmp/sphinx2', interpreter='')
.. cog.out(run_script(cog.inFile, 'pyvenv /tmp/sphinx1', interpreter=''))
.. cog.out(run_script(cog.inFile, 'pyvenv /tmp/sphinx2', interpreter='', include_prefix=False))
.. # Upgrade pip to avoid warnings.
.. run_script(cog.inFile, '/tmp/sphinx1/bin/pip install -U pip', interpreter='')
.. run_script(cog.inFile, '/tmp/sphinx2/bin/pip install -U pip', interpreter='')
.. }}}

.. code-block:: none

	$ pyvenv /tmp/sphinx1
	

	$ pyvenv /tmp/sphinx2
	

.. {{{end}}}

The install the versions of the tools to test.

.. {{{cog
.. cog.out(run_script(cog.inFile, '/tmp/sphinx1/bin/pip install Sphinx==1.3.6',
..                    interpreter='', line_break_mode='wrap'))
.. cog.out(run_script(cog.inFile, '/tmp/sphinx2/bin/pip install Sphinx==1.4.4',
..                    interpreter='', include_prefix=False, line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ /tmp/sphinx1/bin/pip install Sphinx==1.3.6
	
	Collecting Sphinx==1.3.6
	  Using cached Sphinx-1.3.6-py2.py3-none-any.whl
	Collecting Jinja2>=2.3 (from Sphinx==1.3.6)
	  Using cached Jinja2-2.8-py2.py3-none-any.whl
	Collecting Pygments>=2.0 (from Sphinx==1.3.6)
	  Using cached Pygments-2.1.3-py2.py3-none-any.whl
	Collecting babel!=2.0,>=1.3 (from Sphinx==1.3.6)
	  Using cached Babel-2.3.4-py2.py3-none-any.whl
	Collecting snowballstemmer>=1.1 (from Sphinx==1.3.6)
	  Using cached snowballstemmer-1.2.1-py2.py3-none-any.whl
	Collecting alabaster<0.8,>=0.7 (from Sphinx==1.3.6)
	  Using cached alabaster-0.7.9-py2.py3-none-any.whl
	Collecting six>=1.4 (from Sphinx==1.3.6)
	  Using cached six-1.10.0-py2.py3-none-any.whl
	Collecting sphinx-rtd-theme<2.0,>=0.1 (from Sphinx==1.3.6)
	  Using cached sphinx_rtd_theme-0.1.9-py3-none-any.whl
	Collecting docutils>=0.11 (from Sphinx==1.3.6)
	Collecting MarkupSafe (from Jinja2>=2.3->Sphinx==1.3.6)
	  Using cached MarkupSafe-0.23.tar.gz
	Collecting pytz>=0a (from babel!=2.0,>=1.3->Sphinx==1.3.6)
	  Using cached pytz-2016.6.1-py2.py3-none-any.whl
	Installing collected packages: MarkupSafe, Jinja2, Pygments,
	pytz, babel, snowballstemmer, alabaster, six, sphinx-rtd-theme,
	docutils, Sphinx
	  Running setup.py install for MarkupSafe: started
	    Running setup.py install for MarkupSafe: finished with
	status 'done'
	Successfully installed Jinja2-2.8 MarkupSafe-0.23 Pygments-2.1.3
	Sphinx-1.3.6 alabaster-0.7.9 babel-2.3.4 docutils-0.12
	pytz-2016.6.1 six-1.10.0 snowballstemmer-1.2.1 sphinx-rtd-
	theme-0.1.9

	$ /tmp/sphinx2/bin/pip install Sphinx==1.4.4
	
	Collecting Sphinx==1.4.4
	  Using cached Sphinx-1.4.4-py2.py3-none-any.whl
	Collecting Jinja2>=2.3 (from Sphinx==1.4.4)
	  Using cached Jinja2-2.8-py2.py3-none-any.whl
	Collecting imagesize (from Sphinx==1.4.4)
	  Using cached imagesize-0.7.1-py2.py3-none-any.whl
	Collecting Pygments>=2.0 (from Sphinx==1.4.4)
	  Using cached Pygments-2.1.3-py2.py3-none-any.whl
	Collecting babel!=2.0,>=1.3 (from Sphinx==1.4.4)
	  Using cached Babel-2.3.4-py2.py3-none-any.whl
	Collecting snowballstemmer>=1.1 (from Sphinx==1.4.4)
	  Using cached snowballstemmer-1.2.1-py2.py3-none-any.whl
	Collecting alabaster<0.8,>=0.7 (from Sphinx==1.4.4)
	  Using cached alabaster-0.7.9-py2.py3-none-any.whl
	Collecting six>=1.4 (from Sphinx==1.4.4)
	  Using cached six-1.10.0-py2.py3-none-any.whl
	Collecting docutils>=0.11 (from Sphinx==1.4.4)
	Collecting MarkupSafe (from Jinja2>=2.3->Sphinx==1.4.4)
	  Using cached MarkupSafe-0.23.tar.gz
	Collecting pytz>=0a (from babel!=2.0,>=1.3->Sphinx==1.4.4)
	  Using cached pytz-2016.6.1-py2.py3-none-any.whl
	Installing collected packages: MarkupSafe, Jinja2, imagesize,
	Pygments, pytz, babel, snowballstemmer, alabaster, six,
	docutils, Sphinx
	  Running setup.py install for MarkupSafe: started
	    Running setup.py install for MarkupSafe: finished with
	status 'done'
	Successfully installed Jinja2-2.8 MarkupSafe-0.23 Pygments-2.1.3
	Sphinx-1.4.4 alabaster-0.7.9 babel-2.3.4 docutils-0.12
	imagesize-0.7.1 pytz-2016.6.1 six-1.10.0 snowballstemmer-1.2.1

.. {{{end}}}

Then it is possible to run the different versions of Sphinx from the
virtual environments separately, to test them with the same input
files.

.. {{{cog
.. cog.out(run_script(cog.inFile, '/tmp/sphinx1/bin/sphinx-build --version', interpreter=''))
.. cog.out(run_script(cog.inFile, '/tmp/sphinx2/bin/sphinx-build --version', interpreter='', include_prefix=False))
.. }}}

.. code-block:: none

	$ /tmp/sphinx1/bin/sphinx-build --version
	
	Sphinx (sphinx-build) 1.3.6

	$ /tmp/sphinx2/bin/sphinx-build --version
	
	Sphinx (sphinx-build) 1.4.4

.. {{{end}}}


.. seealso::

   * :pydoc:`venv`

   * :pep:`405` -- Python Virtual Environments

   * `virtualenv <https://pypi.python.org/pypi/virtualenv>`__ -- A
     version of Python virtual environments that works for Python 2
     and 3.

   * `virtualenvwrapper
     <https://pypi.python.org/pypi/virtualenvwrapper>`__ -- A set of
     shell wrappers for virtualenv to make it easier to manage a large
     number of environments.

   * `Sphinx <http://www.sphinx-doc.org/en/stable/>`__ -- Tool for
     converting reStructuredText input files to HTML, LaTeX, and other
     formats for consumption.
