================
 Language Tools
================

In addition to the developer tools covered in an earlier chapter,
Python also includes modules that provide access to its internal
features.  This chapter covers some of the tools for working in
Python, regardless of the application area.

The :mod:`warnings` module is used to report non-fatal conditions or
recoverable errors.  A common example of a warning is the
``DeprecationWarning`` generated when a feature of the standard
library has been superseded by a new class, interface, or module.  Use
``warnings`` to report conditions that may need user attention, but
are not fatal.

Defining a set of classes that conform to a common API can be a
challenge when the API is defined by someone else or uses a lot of
methods.  A common way to work around this problem is to derive all of
the new classes from a common base class, but it is not always obvious
which methods should be overridden and which can fall back on the
default behavior.  Abstract base classes from the :mod:`abc` module
formalize an API by explicitly marking the methods a class must
provide in a way that prevents the class from being instantiated if it
is not completely implemented.  For example, many of Python's
container types have abstract base classes defined in ``abc`` or
:mod:`collections`.

The :mod:`dis` module can be used to disassemble the byte-code version
of a program to understand the steps the interpreter takes to run it.
Looking at disassembled code can be useful when debugging performance
or concurrency issues, since it exposes the atomic operations executed
by the interpreter for each statement in a program.

The :mod:`inspect` module provides introspection support for all
objects in the current process.  That includes imported modules, class
and function definitions, and the objects instantiated from them.
Introspection can be used to generate documentation for source code,
adapt behavior at runtime dynamically, or examine the execution
environment for a program.

.. toctree::
   :maxdepth: 1

   warnings/index
   abc/index
   dis/index
   inspect/index
