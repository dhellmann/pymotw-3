======================
 Modules and Packages
======================

Python's primary extension mechanism uses source code saved to modules
and incorporated into a program through the :command:`import`
statement.  The features that most developers think of as "Python" are
actually implemented as the collection of modules called the Standard
Library, the subject of this book.  Although the import feature is
built into the interpreter itself, there are several modules in the
library related to the import process.

The :mod:`importlib` module exposes the underlying implementation of
the import mechanism used by the interpreter.  It can be used to
import modules dynamically at runtime, instead of using the
:command:`import` statement to load them during start-up.  Dynamically
loading modules is useful when the name of a module that needs to be
imported is not known in advance, such as for plugins or extensions to
an application.

Python packages can include supporting resource files such as
templates, default configuration files, images, and other data along
with source code.  The interface for accessing resource files in a
portable way is implemented in the :mod:`pkgutil` module.  It also
includes support for modifying the import path for a package, so that
the contents can be installed into multiple directories but appear as
part of the same package.

:mod:`zipimport` provides a custom importer for modules and packages
saved to ZIP archives.  It is used to load Python EGG files, for
example, and can also be used as a convenient way to package and
distribute an application.

.. toctree::
   :maxdepth: 1

   importlib/index
   pkgutil/index
   zipimport/index

..
   .. toctree::
       :maxdepth: 1

       imp/index
       zipimport/index
       pkgutil/index

..    importlib/index
..    zipapp/index

