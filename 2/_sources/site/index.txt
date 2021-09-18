===============================
site -- Site-wide configuration
===============================

.. module:: site
    :synopsis: Site-wide configuration

The :mod:`site` module handles site-specific configuration, especially
the :ref:`import path <sys-path>`.

Import Path
===========

:mod:`site` is automatically imported each time the interpreter starts
up.  On import, it extends :ref:`sys.path <sys-path>` with
site-specific names constructed by combining the prefix values
:ref:`sys.prefix <sys-prefix>` and :ref:`sys.exec_prefix <sys-prefix>`
with several suffixes.  The prefix values used are saved in the
module-level variable ``PREFIXES`` for reference later.  Under
Windows, the suffixes are an empty string and ``lib/site-packages``.
For Unix-like platforms, the values are
``lib/python$version/site-packages`` and ``lib/site-python``.

.. include:: site_import_path.py
   :literal:
   :start-after: #end_pymotw_header

Each of the paths resulting from the combinations is tested, and those
that exist are added to :ref:`sys.path <sys-path>`.

::
    
    $ python site_import_path.py 
    Path prefixes:
       /Library/Frameworks/Python.framework/Versions/2.7
       /Library/Frameworks/Python.framework/Versions/2.7
    
    /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages
       exists: True
      in path: True
    /Library/Frameworks/Python.framework/Versions/2.7/lib/site-python
       exists: False
      in path: False

User Directories
================

In addition to the global site-packages paths, :mod:`site` is
responsible for adding the user-specific locations to the import path.
The user-specific paths are all based on the ``USER_BASE`` directory,
which usually located in a part of the filesystem owned (and writable)
by the current user.  Inside the ``USER_BASE`` is a site-packages
directory, with the path accessible as ``USER_SITE``.

.. include:: site_user_base.py
   :literal:
   :start-after: #end_pymotw_header

The ``USER_SITE`` path name is created using the same
platform-specific values described above.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'site_user_base.py'))
.. }}}

::

	$ python site_user_base.py
	
	Base: /Users/dhellmann/.local
	Site: /Users/dhellmann/.local/lib/python2.7/site-packages

.. {{{end}}}

The user base directory can be set through the ``PYTHONUSERBASE``
environment variable, and has platform-specific defaults
(``~/Python$version/site-packages`` for Windows and ``~/.local`` for
non-Windows).  

You can check the ``USER_BASE`` value from outside of your Python
program by running :mod:`site` from the command line.  :mod:`site`
will give you the name of the directory whether or not it exists, but
it is only added to the import path when it does.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m site --user-base'))
.. cog.out(run_script(cog.inFile, '-m site --user-site', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'PYTHONUSERBASE=/tmp/$USER python -m site --user-base', interpreter=None, include_prefix=False))
.. cog.out(run_script(cog.inFile, 'PYTHONUSERBASE=/tmp/$USER python -m site --user-site', interpreter=None, include_prefix=False))
.. }}}

::

	$ python -m site --user-base
	

	$ python -m site --user-site
	

	$ PYTHONUSERBASE=/tmp/$USER python -m site --user-base
	

	$ PYTHONUSERBASE=/tmp/$USER python -m site --user-site
	

.. {{{end}}}

The user directory is disabled under some circumstances that would
pose security issues.  For example, if the process is running with a
different effective user or group id than the actual user that started
it.  Your application can check the setting by examining
``ENABLE_USER_SITE``.

.. include:: site_enable_user_site.py
   :literal:
   :start-after: #end_pymotw_header

The user directory can also be explicitly disabled on the command line
with :option:`-s`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'site_enable_user_site.py'))
.. cog.out(run_script(cog.inFile, '-s site_enable_user_site.py', include_prefix=False))
.. }}}

::

	$ python site_enable_user_site.py
	
	Flag   : True
	Meaning: Enabled

	$ python -s site_enable_user_site.py
	
	Flag   : False
	Meaning: Disabled by command-line option

.. {{{end}}}

Path Configuration Files
========================

As paths are added to the import path, they are also scanned for *path
configuration files*.  A path configuration file is a plain text file
with the extension ``.pth``.  Each line in the file can take one of
four forms:

1. A full or relative path to another location that should be added to
   the import path.
2. A Python statement to be executed.  All such lines must begin with
   an ``import`` statement.
3. Blank lines are ignored.
4. A line starting with ``#`` is treated as a comment and ignored.

Path configuration files can be used to extend the import path to look
in locations that would not have been added automatically.  For
example, Distribute_ adds a path to ``easy-install.pth`` when it
installs a package in "develop" mode using ``python setup.py
develop``.

The function for extending ``sys.path`` is public, so we can use it in
example programs to show how the path configuration files work.  Given
a directory ``with_modules`` containing the file ``mymodule.py`` with
this ``print`` statement showing how the module was imported:

.. include:: with_modules/mymodule.py
   :literal:
   :start-after: #end_pymotw_header

This script shows how :func:`addsitedir()` extends the import path so
the interpreter can find the desired module.

.. include:: site_addsitedir.py
   :literal:
   :start-after: #end_pymotw_header

After the directory containing the module is added to ``sys.path``,
the script can import :mod:`mymodule` without issue.

.. {{{cog
.. (path(cog.inFile).dirname() / 'with_modules/mymodule.pyc').unlink()
.. cog.out(run_script(cog.inFile, 'site_addsitedir.py with_modules'))
.. }}}

::

	$ python site_addsitedir.py with_modules
	
	Could not import mymodule: No module named mymodule
	
	New paths:
	   /Users/dhellmann/Documents/PyMOTW/src/PyMOTW/site/with_modules
	
	Loaded mymodule from with_modules/mymodule.py

.. {{{end}}}

If the directory given to :func:`addsitedir()` includes any files
matching the pattern ``*.pth``, they are loaded as path configuration
files.  For example, if we create ``with_pth/pymotw.pth`` containing:

.. literalinclude:: with_pth/pymotw.pth

and copy ``mymodule.py`` to ``with_pth/subdir/mymodule.py``, then we
can import it by adding ``with_pth`` as a site directory, even though
the module is not in that directory.

.. {{{cog
.. (path(cog.inFile).dirname() / 'with_pth/subdir/mymodule.pyc').unlink()
.. cog.out(run_script(cog.inFile, 'site_addsitedir.py with_pth'))
.. }}}

::

	$ python site_addsitedir.py with_pth
	
	Could not import mymodule: No module named mymodule
	
	New paths:
	   /Users/dhellmann/Documents/PyMOTW/src/PyMOTW/site/with_pth
	   /Users/dhellmann/Documents/PyMOTW/src/PyMOTW/site/with_pth/subdir
	
	Loaded mymodule from with_pth/subdir/mymodule.py

.. {{{end}}}

If a site directory contains multiple ``.pth`` files, they are
processed in alphabetical order.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ls -F with_multiple_pth', interpreter=None))
.. cog.out(run_script(cog.inFile, 'cat with_multiple_pth/a.pth', interpreter=None, include_prefix=False))
.. cog.out(run_script(cog.inFile, 'cat with_multiple_pth/b.pth', interpreter=None, include_prefix=False))
.. }}}

::

	$ ls -F with_multiple_pth
	
	a.pth
	b.pth
	from_a/
	from_b/

	$ cat with_multiple_pth/a.pth
	
	./from_a

	$ cat with_multiple_pth/b.pth
	
	./from_b

.. {{{end}}}

In this case, the module is found in ``with_multiple_pth/from_a``
because ``a.pth`` is read before ``b.pth``.

.. {{{cog
.. (path(cog.inFile).dirname() / 'with_multiple_pth/from_a/mymodule.pyc').unlink()
.. cog.out(run_script(cog.inFile, 'site_addsitedir.py with_multiple_pth'))
.. }}}

::

	$ python site_addsitedir.py with_multiple_pth
	
	Could not import mymodule: No module named mymodule
	
	New paths:
	   /Users/dhellmann/Documents/PyMOTW/src/PyMOTW/site/with_multiple_pth
	   /Users/dhellmann/Documents/PyMOTW/src/PyMOTW/site/with_multiple_pth/from_a
	   /Users/dhellmann/Documents/PyMOTW/src/PyMOTW/site/with_multiple_pth/from_b
	
	Loaded mymodule from with_multiple_pth/from_a/mymodule.py

.. {{{end}}}


.. module:: sitecustomize
    :synopsis: Site-specific configuration

sitecustomize
=============

The :mod:`site` module is also responsible for loading site-wide
customization defined by the local site owner in a
:mod:`sitecustomize` module.  Uses for :mod:`sitecustomize` include
extending the import path and `enabling coverage
<http://nedbatchelder.com/blog/201001/running_code_at_python_startup.html>`__,
profiling, or other development tools.

For example, this ``sitecustomize.py`` script extends the import path
with a directory based on the current platform.  The platform-specific
path in ``/opt/python`` is added to the import path, so any packages
installed there can be imported.  A system like this is useful for
sharing packages containing compiled extension modules between hosts
on a network via a shared filesystem.  Only the ``sitecustomize.py``
script needs to be installed on each host, and the other packages can
be accessed from the file server.

.. include:: with_sitecustomize/sitecustomize.py
   :literal:
   :start-after: #end_pymotw_header

A simple script can be used to show that ``sitecustomize.py`` is
imported before Python starts running your own code.

.. include:: with_sitecustomize/site_sitecustomize.py
   :literal:
   :start-after: #end_pymotw_header

Since :mod:`sitecustomize` is meant for system-wide configuration, it
should be installed somewere in the default path (usally in the
``site-packages`` directory).  This example sets ``PYTHONPATH``
explicitly to ensure the module is picked up.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'PYTHONPATH=with_sitecustomize python with_sitecustomize/site_sitecustomize.py', interpreter=None))
.. }}}

::

	$ PYTHONPATH=with_sitecustomize python with_sitecustomize/site_sitecusto\
	mize.py
	
	Loading sitecustomize.py
	Adding new path /opt/python/2.7/Darwin-11.4.2-x86_64-i386-64bit
	Running main program
	End of path: /opt/python/2.7/Darwin-11.4.2-x86_64-i386-64bit

.. {{{end}}}

.. module:: usercustomize
    :synopsis: User-specific configuration

usercustomize
=============

Similar to :mod:`sitecustomize`, the :mod:`usercustomize` module can
be used to set up user-specific settings each time the interpreter
starts up.  :mod:`usercustomize` is loaded after :mod:`sitecustomize`,
so site-wide customizations can be overridden.

In environments where a user's home directory is shared on several
servers running different operating systems or versions, the standard
user directory mechanism may not work for user-specific installations
of packages.  In these cases, platform-specific directory tree can be
used instead.

.. include:: with_usercustomize/usercustomize.py
   :literal:
   :start-after: #end_pymotw_header

Another simple script, similar to the one used for
:mod:`sitecustomize`, can be used to show that ``usercustomize.py`` is
imported before Python starts running your own code.

.. include:: with_usercustomize/site_usercustomize.py
   :literal:
   :start-after: #end_pymotw_header

Since :mod:`usercustomize` is meant for user-specific configuration
for a user, it should be installed somewhere in the user's default
path, but not on the site-wide path. The default ``USER_BASE``
directory is a good location.  This example sets ``PYTHONPATH``
explicitly to ensure the module is picked up.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'PYTHONPATH=with_usercustomize python with_usercustomize/site_usercustomize.py', interpreter=None))
.. }}}

::

	$ PYTHONPATH=with_usercustomize python with_usercustomize/site_usercusto\
	mize.py
	
	Loading usercustomize.py
	Adding new path /Users/dhellmann/python/2.7/Darwin-11.4.2-x86_64-i386-64bit
	Running main program
	End of path: /Users/dhellmann/python/2.7/Darwin-11.4.2-x86_64-i386-64bit

.. {{{end}}}

When the user site directory feature is disabled, :mod:`usercustomize`
is not imported, whether it is located in the user site directory or
elsewhere.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'PYTHONPATH=with_usercustomize python -s with_usercustomize/site_usercustomize.py', interpreter=None))
.. }}}

::

	$ PYTHONPATH=with_usercustomize python -s with_usercustomize/site_usercu\
	stomize.py
	
	Running main program
	End of path: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages

.. {{{end}}}


Disabling site
==============

To maintain backwards-compatibility with versions of Python from
before the automatic import was added, the interpreter accepts an
:option:`-S` option.

::

    $ python -S site_import_path.py 
    Path prefixes:
       sys.prefix     : /Library/Frameworks/Python.framework/Versions/2.7
       sys.exec_prefix: /Library/Frameworks/Python.framework/Versions/2.7
    
    /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages
       exists: True
      in path: False
    /Library/Frameworks/Python.framework/Versions/2.7/lib/site-python
       exists: False
      in path: False

.. seealso::

    `site <http://docs.python.org/2.7/library/site.html>`_
        The standard library documentation for this module.

    :ref:`sys-imports`
        Description of how the import path defined in :mod:`sys` works.

    `Running code at Python startup <http://nedbatchelder.com/blog/201001/running_code_at_python_startup.html>`__
        Post from Ned Batchelder discussing ways to cause the Python
        interpreter to run your custom initialization code before
        starting the main program execution.

.. _Distribute: http://packages.python.org/distribute
