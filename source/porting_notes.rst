  ..
     Snippets
     --------
     pyissue - builds reference to a python bug
     porting - starts new section
     mod - builds reference to a module

=============
Porting Notes
=============

This section includes notes and tips for updating from Python 2 to
Python 3, including summaries of and references for the changes in
each module.

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


Changes in Modules Between Python 2 and 3
=========================================

.. _porting-atexit:

atexit
------

When :mod:`atexit` was updated to include a C implementation
(:pyissue:`1680961`), a regression was introduced in the error
handling logic that caused only the summary of the exception to be
shown, without the traceback. This regression was fixed in Python 3.3
(:pyissue:`18776`).


