  ..
     Snippets
     --------
     pyissue - builds reference to a python bug
     porting - starts new section
     mod - builds reference to a module

.. spelling::

   Lennart
   Regebro

===============
 Porting Notes
===============

This section includes notes and tips for updating from Python 2 to
Python 3, including summaries of and references for the changes in
each module.

References
==========

The notes in this section are based on the "What's New" documents
prepared by the Python development team and release manager for each
release.

* `What's New In Python 3.0 <https://docs.python.org/3.0/whatsnew/3.0.html>`__
* `What's New In Python 3.1 <https://docs.python.org/3.1/whatsnew/3.1.html>`__
* `What's New In Python 3.2 <https://docs.python.org/3.2/whatsnew/3.2.html>`__
* `What's New In Python 3.3 <https://docs.python.org/3.3/whatsnew/3.3.html>`__
* `What's New In Python 3.4 <https://docs.python.org/3.4/whatsnew/3.4.html>`__

For more information about porting to Python 3, refer to

* `Porting Python 2 Code to Python 3
  <https://docs.python.org/3/howto/pyporting.html>`__ on
  docs.python.org.
* `Porting to Python 3 <http://python3porting.com/>`__, by Lennart
  Regebro.
* The `python-porting
  <http://mail.python.org/mailman/listinfo/python-porting>`__ mailing
  list.

Renamed Modules
===============

Many standard library modules were renamed between Python 2 and 3. All
of the new module names use consistent lower case, and some have been
moved into packages to better organize related modules. A complete
list of the renames can be found in the dictionary
``lib2to3.fixes.fix_imports.MAPPING`` (the keys are the Python 2 name
and the values are the Python 3 name).

.. Build the rename table directive dynamically.
..
.. {{{cog
.. from lib2to3.fixes.fix_imports import MAPPING
.. cog.out("\n")
.. cog.out(".. csv-table:: Renamed Modules\n")
.. cog.out('   :header: "Python 2 Name", "Python 3 Name"\n')
.. cog.out("\n")
.. for old, new in sorted(MAPPING.items()):
..   cog.out("   %s, %s\n" % (old, new))
.. cog.out("\n")
.. }}}

.. csv-table:: Renamed Modules
   :header: "Python 2 Name", "Python 3 Name"

   BaseHTTPServer, http.server
   CGIHTTPServer, http.server
   ConfigParser, configparser
   Cookie, http.cookies
   Dialog, tkinter.dialog
   DocXMLRPCServer, xmlrpc.server
   FileDialog, tkinter.filedialog
   HTMLParser, html.parser
   Queue, queue
   ScrolledText, tkinter.scrolledtext
   SimpleDialog, tkinter.simpledialog
   SimpleHTTPServer, http.server
   SimpleXMLRPCServer, xmlrpc.server
   SocketServer, socketserver
   StringIO, io
   Tix, tkinter.tix
   Tkconstants, tkinter.constants
   Tkdnd, tkinter.dnd
   Tkinter, tkinter
   UserList, collections
   UserString, collections
   __builtin__, builtins
   _winreg, winreg
   cPickle, pickle
   cStringIO, io
   commands, subprocess
   cookielib, http.cookiejar
   copy_reg, copyreg
   dbhash, dbm.bsd
   dbm, dbm.ndbm
   dumbdbm, dbm.dumb
   dummy_thread, _dummy_thread
   gdbm, dbm.gnu
   htmlentitydefs, html.entities
   httplib, http.client
   markupbase, _markupbase
   repr, reprlib
   robotparser, urllib.robotparser
   thread, _thread
   tkColorChooser, tkinter.colorchooser
   tkCommonDialog, tkinter.commondialog
   tkFileDialog, tkinter.filedialog
   tkFont, tkinter.font
   tkMessageBox, tkinter.messagebox
   tkSimpleDialog, tkinter.simpledialog
   ttk, tkinter.ttk
   urlparse, urllib.parse
   xmlrpclib, xmlrpc.client

.. {{{end}}}

.. seealso::

   * The six_ package is useful for writing code that runs under both
     Python 2 and 3. In particular, the ``six.moves`` module allows
     your code to import renamed modules using a single import
     statement, automatically redirecting the import to the correct
     version of the name depending on the version of Python.

.. _six: http://pythonhosted.org/six/

New Modules
===========



Deprecated Modules
==================

These modules are still present in the standard library, but are
deprecated and should not be used in new Python 3 programs.

formatter
  Generic output formatter and device interface.

imp
  Access the implementation of the import statement.

optparse
  Command-line option parsing library.

  The API for :mod:`argparse` is similar to the one provided by
  :mod:`optparse`, and in many cases :mod:`argparse` can be used as a
  straightforward replacement by updating the names of the classes and
  methods used.


Summary of Changes to Modules
=============================

.. _porting-argparse:

argparse
--------

.. index::
   pair: porting; argparse

The ``version`` argument to :class:`ArgumentParser` has been removed
in favor of a special ``action`` type (:pyissue:`13248`).

Replace::

  parser = argparse.ArgumentParser(version='1.0')

with something like::

  parser = argparse.ArgumentParser(version='1.0')
  parser.add_argument('--version', action='version',
                      version='%(prog)s 1.0')

The option name and version format string can be modified to suit the
needs of the application.

In Python 3.4, the version action was changed to print the version
string to stdout instead of stderr (:pyissue:`18920`).

.. _porting-atexit:

atexit
------

.. index::
   pair: porting; atexit

When :mod:`atexit` was updated to include a C implementation
(:pyissue:`1680961`), a regression was introduced in the error
handling logic that caused only the summary of the exception to be
shown, without the traceback. This regression was fixed in Python 3.3
(:pyissue:`18776`).

.. _porting-shelve:

shelve
------

The default output format for :mod:`shelve` may create a file with a
``.db`` extension added to the name given to :func:`shelve.open`.

.. _porting-sys:

sys
---

.. index::
   pair: porting; sys

.. Patch #1680961

The variable :data:`sys.exitfunc` is no longer checked for a clean-up
action to be run when a program exits. Use :mod:`atexit` instead.

The variable :data:`sys.subversion` is no longer defined.

Flags :data:`sys.flags.py3k_warning`,
:data:`sys.flags.division_warning`, :data:`sys.flags.division_new`,
:data:`sys.flags.tabcheck`, and :data:`sys.flags.unicode` are no
longer defined.

The variable :data:`sys.maxint` is no longer defined, use
:data:`sys.maxsize` instead. See :pep:`237` (Unifying Long Integers
and Integers).

The global exception tracking variables :data:`sys.exc_type`,
:data:`sys.exc_value`, and :data:`sys.exc_traceback` have been
removed. The function :func:`sys.exc_clear` has also been removed.

.. issue 4285

The variable :data:`sys.version_info` is now a :py:class:`namedtuple`
instance with attributes ``major``, ``minor``, ``micro``,
``releaselevel``, and ``serial``.

.. http://mail.python.org/pipermail/python-dev/2009-October/093321.html

The "check interval" feature, controlling the number of opcodes to
execute before allowing a thread context switch has been replaced with
an absolute time value instead, managed with
:func:`sys.setswitchinterval`. The old functions for managing the
check interval, :func:`sys.getcheckinterval` and
:func:`sys.setcheckinterval`, are deprecated.

.. https://docs.python.org/3.3/whatsnew/3.3.html#visible-changes

The :data:`sys.meta_path` and :data:`sys.path_hooks` variables now
expose all of the path finders and entry hooks for importing
modules. In earlier versions, only finders and hooks explicitly added
to the path were exposed, and the C import used values in its
implementation that could not be modified from the outside.

For Linux systems, :data:`sys.platform` no longer includes the version
number. The value is now just ``linux`` and not ``linux2`` or
``linux3``.
