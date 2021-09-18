=======================================
pydoc -- Online help for Python modules
=======================================

.. module:: pydoc
    :synopsis: Online help for Python modules

:Purpose: Generates help for Python modules and classes from the code.
:Available In: 2.1 and later

The :mod:`pydoc` module imports a Python module and uses the contents
to generate help text at runtime. The output includes docstrings for
any objects that have them, and all of the documentable contents of
the module are described.

Plain Text Help
===============

Running::

    $ pydoc atexit

Produces plaintext help on the console, using your pager if one is
configured.

HTML Help
=========

You can also cause :mod:`pydoc` to generate HTML output, either
writing a static file to a local directory or starting a web server to
browse documentation online.

::

    $ pydoc -w atexit

Creates ``atexit.html`` in the current directory.

::

    $ pydoc -p 5000

Starts a web server listening at http://localhost:5000/. The server
generates documentation as you browse through the available modules.

Interactive Help
================

pydoc also adds a function ``help()`` to the ``__builtins__`` so you
can access the same information from the Python interpreter prompt.

::

    $ python
    Python 2.6.2 (r262:71600, Apr 16 2009, 09:17:39) 
    [GCC 4.0.1 (Apple Computer, Inc. build 5250)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> help('atexit')
    Help on module atexit:

    NAME
        atexit

    FILE
        /Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/atexit.py
    ...

.. seealso::

    `pydoc <http://docs.python.org/2.7/library/pydoc.html>`_
        The standard library documentation for this module.

    :ref:`motw-cli`
        Accessing the Module of the Week articles from the command line.
    
    :ref:`motw-interactive`
        Accessing the Module of the Week articles from the interactive interpreter.
