===================================
 pydoc --- Online Help for Modules
===================================

.. module:: pydoc
    :synopsis: Online help for modules

:Purpose: Generates help for Python modules and classes from the code.

The ``pydoc`` module imports a Python module and uses the contents
to generate help text at runtime. The output includes docstrings for
any objects that have them, and all of the classes, methods, and
functions of the module are described.

Plain Text Help
===============

Running:

.. code-block:: none

    $ pydoc atexit

    Help on built-in module atexit:
    
    NAME
        atexit - allow programmer to define multiple exit functions
    to be executed upon normal program termination.
    
    DESCRIPTION
        Two public functions, register and unregister, are defined.
    
    FUNCTIONS
        register(...)
            register(func, *args, **kwargs) -> func
    
            Register a function to be executed upon normal program 
    termination
    
                func - function to be called at exit
                args - optional arguments to pass to func
                kwargs - optional keyword arguments to pass to func
    
                func is returned to facilitate usage as a decorator.
    
        unregister(...)
            unregister(func) -> None
    
            Unregister an exit function which was previously 
    registered using
            atexit.register
    
                func - function to be unregistered
    
    FILE
        (built-in)

Produces plaintext help on the console, using a pager program if one
is configured.

HTML Help
=========

``pydoc`` will also generate HTML output, either writing a static
file to a local directory or starting a web server to browse
documentation online.

.. code-block:: none

    $ pydoc -w atexit

Creates ``atexit.html`` in the current directory.

.. code-block:: none

    $ pydoc -p 5000
    Server ready at http://localhost:5000/
    Server commands: [b]rowser, [q]uit
    server> q
    Server stopped

Starts a web server listening at ``http://localhost:5000/``. The
server generates documentation on the fly as you browse. Use the ``b``
command to open a browser window automatically, and ``q`` to stop the
server.

Interactive Help
================

``pydoc`` also adds a function :func:`help` to the ``__builtins__``
so the same information can be accessed from the Python interpreter
prompt.

.. code-block:: none

    $ python
        
    Python 3.5.2 (v3.5.2:4def2a2901a5, Jun 26 2016, 10:47:25)
    [GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
    Type "help", "copyright", "credits" or "license" for more
    information.
    >>> help('atexit')
    Help on module atexit:
    
    NAME
        atexit - allow programmer to define multiple exit functions
    to be executed upon normal program termination.

    ...

.. seealso::

   * :pydoc:`pydoc`

   * :mod:`inspect` -- The ``inspect`` module can be used to retrieve
     the docstrings for an object programmatically.
