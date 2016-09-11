==================================
 pydoc -- Online Help for Modules
==================================

.. module:: pydoc
    :synopsis: Online help for modules

:Purpose: Generates help for Python modules and classes from the code.

The :mod:`pydoc` module imports a Python module and uses the contents
to generate help text at runtime. The output includes docstrings for
any objects that have them, and all of the classes, methods, and
functions of the module are described.

Plain Text Help
===============

Running::

    $ pydoc atexit

Produces plaintext help on the console, using a pager program if one
is configured.

HTML Help
=========

:mod:`pydoc` will also generate HTML output, either writing a static
file to a local directory or starting a web server to browse
documentation online.

::

    $ pydoc -w atexit

Creates ``atexit.html`` in the current directory.

::

    $ pydoc -p 5000

Starts a web server listening at ``http://localhost:5000/``. The server
generates documentation on the fly as you browse.

Interactive Help
================

:mod:`pydoc` also adds a function :func:`help` to the ``__builtins__``
so the same information can be accessed from the Python interpreter
prompt.

::

    $ python
        
    Python 2.7 (r27:82508, Jul  3 2010, 21:12:11) 
    [GCC 4.0.1 (Apple Inc. build 5493)] on darwin
    Type "help", "copyright", "credits" or "license" for more 
    information.
    >>> help('atexit')
    Help on module atexit:
    
    NAME
        atexit

    ...    

.. seealso::

    `pydoc <http://docs.python.org/library/pydoc.html>`_
        The standard library documentation for this module.

    :mod:`inspect`
        The ``inspect`` module can be used to retrieve the docstrings
        for an object programmatically.
