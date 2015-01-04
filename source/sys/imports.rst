.. _sys-imports:

===================
Modules and Imports
===================

Most Python programs end up as a combination of several modules with a
main application importing them. Whether using the features of the
standard library, or organizing custom code in separate files to make
it easier to maintain, understanding and managing the dependencies for
a program is an important aspect of development. :mod:`sys` includes
information about the modules available to an application, either as
built-ins or after being imported.  It also defines hooks for
overriding the standard import behavior for special cases.

.. toctree::

   normal_imports

.. only:: bonus

   .. toctree:: 

      bonus_imports

.. seealso::

    :mod:`imp`
        The imp module provides tools used by importers.

    :mod:`importlib`
        Base classes and other tools for creating custom importers.
        
    `The Quick Guide to Python Eggs <http://peak.telecommunity.com/DevCenter/PythonEggs>`_
        PEAK documentation for working with EGGs.
        
    `Python 3 stdlib module "importlib" <http://docs.python.org/py3k/library/importlib.html>`_
        Python 3.x includes abstract base classes that makes it easier
        to create custom importers.

    .. only:: bonus

       :pep:`302`
           Import Hooks

       :mod:`zipimport`
           Implements importing Python modules from inside ZIP archives.
        
       `Import this, that, and the other thing: custom importers <http://us.pycon.org/2010/conference/talks/?filter=core>`_
           Brett Cannon's PyCon 2010 presentation.
