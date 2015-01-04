Install Location
================

The path to the actual interpreter program is available in
:const:`sys.executable` on all systems for which having a path to the
interpreter makes sense.  This can be useful for ensuring that the
correct interpreter is being used, and also gives clues about paths
that might be set based on the interpreter location.

:const:`sys.prefix` refers to the parent directory of the interpreter
installation.  It usually includes ``bin`` and ``lib`` directories for
executables and installed modules, respectively.

.. include:: sys_locations.py
    :literal:
    :start-after: #end_pymotw_header

This example output was produced on a Mac running a framework build
installed from python.org.

::

    $ python sys_locations.py
        
    Interpreter executable: /Library/Frameworks/Python.framework/
    Versions/2.7/Resources/Python.app/Contents/MacOS/Python
    Installation prefix   : /Library/Frameworks/Python.framework/
    Versions/2.7
