  ..
     Snippets
     --------
     pyissue - builds reference to a python bug
     porting - starts new section
     mod - builds reference to a module

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
* `What's New In Python 3.5 <https://docs.python.org/3.5/whatsnew/3.5.html>`__

For more information about porting to Python 3, refer to

* `Porting Python 2 Code to Python 3
  <https://docs.python.org/3/howto/pyporting.html>`__ on
  ``docs.python.org``.
* `Porting to Python 3 <http://python3porting.com/>`__, by Lennart
  Regebro.
* The `python-porting
  <http://mail.python.org/mailman/listinfo/python-porting>`__ mailing
  list.

Renamed Modules
===============

Many standard library modules were renamed between Python 2 and 3 as
part of :pep:`3108` (*Standard Library Reorganization*). All of the
new module names use consistent lower case, and some have been moved
into packages to better organize related modules. A complete list of
the renames can be found in the dictionary
``lib2to3.fixes.fix_imports.MAPPING`` (the keys are the Python 2 name
and the values are the Python 3 name).

.. index::
   single: porting; renamed modules
   single: renamed modules

.. Build the rename table directive dynamically.
..
.. {{{cog
.. from lib2to3.fixes.fix_imports import MAPPING
.. cog.out("\n")
.. cog.out(".. csv-table:: Renamed Modules\n")
.. cog.out('   :header: "Python 2 Name", "Python 3 Name"\n')
.. cog.out("\n")
.. for old, new in sorted(MAPPING.items()):
..   cog.out("   {}, {}\n".format(old, new))
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

   * :pep:`3108` -- Standard Library Reorganization

.. _six: http://pythonhosted.org/six/

New Modules
===========

asyncio
  Asynchronous I/O, event loop, and other concurrency tools.

Deprecated Modules
==================

These modules are still present in the standard library, but are
deprecated and should not be used in new Python 3 programs.

.. index::
   pair: porting; asyncore
   pair: porting; asynchat

asyncore and asynchat
  Asynchronous I/O and protocol handlers.

  See :mod:`asyncio` instead.

.. index::
   pair: porting; formatter

formatter
  Generic output formatter and device interface.

.. index::
   pair: porting; imp

imp
  Access the implementation of the import statement.

.. index::
   pair: porting; optparse

optparse
  Command-line option parsing library.

  The API for :mod:`argparse` is similar to the one provided by
  :mod:`optparse`, and in many cases :mod:`argparse` can be used as a
  straightforward replacement by updating the names of the classes and
  methods used.


Summary of Changes to Modules
=============================

.. _porting-abc:

abc
---

.. index::
   pair: porting; abc

The :func:`abstractproperty`, :func:`abstractclassmethod`, and
:func:`abstractstaticmethod` decorators are deprecated. Combining
:func:`abstractmethod` with the :func:`property`, :func:`classmethod`,
and :func:`staticmethod` decorators works as expected
(:pyissue:`11610`).

.. _porting-dbm:
.. _porting-anydbm:

anydbm
------

.. index::
   pair: porting; anydbm
   pair: porting; dbm

The ``anydbm`` module has been renamed :mod:`dbm` in Python 3.

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

.. _porting-array:

array
-----

.. index::
   pair: porting; array

The ``'c'`` type used for character bytes in early version of Python 2
has been removed. Use ``'b'`` or ``'B'`` for bytes instead.

The ``'u'`` type for characters from unicode strings has been
deprecated and will be removed in Python 4.0.

The methods :func:`tostring` and :func:`fromstring` have been renamed
:func:`tobytes` and :func:`frombytes` to remove ambiguity
(:pyissue:`8990`).

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

.. _porting-base64:

base64
------

.. index::
   pair: porting; base64

The :func:`encodestring` and :func:`decodestring` have been renamed
:func:`encodebytes` and :func:`decodebytes` respectively. The old
names still work as aliases, but are deprecated (:pyissue:`3613`).

Two new encodings using 85-character alphabets have been
added. :func:`b85encode` implements an encoding used in Mercurial and
git, while :func:`a85encode` implements the Ascii85 format used by PDF
files (:pyissue:`17618`).

.. _porting-bz2:

bz2
---

.. index::
   pair: porting; bz2

:class:`BZ2File` instances now support the context manager protocol,
and do not need to be wrapped with :func:`contextlib.closing`.

.. _porting-contextlib:

contextlib
----------

.. index::
   pair: porting; contextlib

:func:`contextlib.nested` has been removed. Pass multiple context
managers to the same ``with`` statement instead.

.. _porting-collections:

collections
-----------

.. index::
   pair: porting; collections

The abstract base classes formerly defined in :mod:`collections` moved
to :mod:`collections.abc`, with backwards-compatibility imports in
:mod:`collections`, for now (:pyissue:`11085`).

.. _porting-configparser:

configparser
------------

.. index::
   pair: porting; configparser

The old ``ConfigParser`` module has been renamed to
:mod:`configparser`.

The old :class:`ConfigParser` class was removed in favor of
:class:`SafeConfigParser` which has in turn been renamed to
:class:`ConfigParser`. The deprecated interpolation behavior is
available via :class:`LegacyInterpolation`.

The :func:`read` method now supports an ``encoding`` argument, so it
is no longer necessary to use :mod:`codecs` to read configuration
files with Unicode values in them.

Using the old :class:`RawConfigParser` is discouraged. New projects
should use ``ConfigParser(interpolation=None)`` instead to achieve the
same behavior.

.. _porting-csv:

csv
---

.. index::
   pair: porting; csv

Instead of using the :func:`next` method of a reader directly, use the
built-in :func:`next` function to invoke the iterator properly.

.. _porting-datetime:

datetime
--------

.. index::
   pair: porting; datetime

Starting with Python 3.3, equality comparisons between naive and
timezone-aware :class:`datetime` instances return ``False`` instead of
raising :class:`TypeError` (:pyissue:`15006`).

Prior to Python 3.5, a :class:`datetime.time` object representing
midnight evaluated to ``False`` when converted to a Boolean. This
behavior has been removed in Python 3.5 (:pyissue:`13936`).

.. _porting-fractions:

fractions
---------

.. index::
   pair: porting; fractions

The :func:`from_float` and :func:`from_decimal` class methods are no
longer needed. Floating point and :class:`Decimal` values can be
passed directly to the :class:`Fraction` constructor.

.. _porting-gettext:

gettext
-------

.. index::
   pair: porting; gettext

All of the translation functions in :mod:`gettext` assume unicode
input and output, and the unicode variants such as :func:`ugettext`
have been removed.


.. _porting-glob:

glob
----

.. index::
   pair: porting; glob

The new function :func:`escape` implements a work-around for searching
for files with meta-characters in the name (:pyissue:`8402`).

.. _porting-imaplib:

imaplib
-------

.. index::
   pair: porting; imaplib

Under Python 3, :mod:`imaplib` returns byte-strings encoded as
UTF-8. There is support for accepting unicode strings and encoding
them automatically as outgoing commands are sent or as the username
and password for logging in to the server.


.. _porting-mailbox:

mailbox
-------

.. index::
   pair: porting; mailbox

mailbox reads and writes mailbox files in binary mode, relying on the
email package to parse messages.  StringIO and text file input is
deprecated (:pyissue:`9124`).

.. _porting-mmap:

mmap
----

.. index::
   pair: porting; mmap

Values returned from read APIs are byte strings, and need to be
decoded before being treated as text.

.. _porting-pdb:

pdb
---

.. index::
   pair: porting; pdb

The ``print`` command alias has been removed so that it does not
shadow the ``print()`` function (:pyissue:`18764`). The ``p`` shortcut
is retained.

.. _porting-pipes:

pipes
-----

.. index::
   pair: porting; pipes

:func:`pipes.quote` has moved to :mod:`shlex` (:pyissue:`9723`).

.. _porting-random:

random
------

.. index::
   pair: porting; random

The function ``jumpahead()`` was removed in Python 3.0.


.. _porting-shelve:

shelve
------

.. index::
   pair: porting; shelve

The default output format for :mod:`shelve` may create a file with a
``.db`` extension added to the name given to :func:`shelve.open`.

.. _porting-socketserver:

socketserver
------------

.. index::
   pair: porting; socketserver

The :mod:`socketserver` module was named ``SocketServer`` under
Python 2.


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

The variable :data:`sys.version_info` is now a :py:class:`namedtuple`
instance with attributes ``major``, ``minor``, ``micro``,
``releaselevel``, and ``serial`` (:pyissue:`4285`).

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

.. _porting-threading:

threading
---------

.. index::
   pair: porting; threading
   pair: porting; thread

The ``thread`` module is deprecated in favor of the API in
:mod:`threading`.

The debugging features of :mod:`threading`, including the "verbose"
argument has been removed from the APIs (:pyissue:`13550`).

Older implementations of :mod:`threading` used factory functions for
some of the classes because they were implemented in C as extension
types and could not be subclassed. That limitation of the language has
been removed, and so many of the old factory functions have been
converted to standard classes, which allow subclassing
(:pyissue:`10968`).

The public symbols exported from :mod:`threading` have been renamed to
be :pep:`8` compliant. The old names are retained for backwards
compatibility, but they will be removed in a future release.

.. _porting-UserDict:
.. _porting-UserList:
.. _porting-UserString:

UserDict, UserList, and UserString
----------------------------------

.. index::
   pair: porting; UserDict
   pair: porting; UserList
   pair: porting; UserString

The UserDict, UserList, and UserString classes have been moved out of
their own modules into the :mod:`collections` module. :class:`dict`,
:class:`list`, and :class:`str` can be subclassed directly, but the
classes in :mod:`collections` may make implementing the subclass
simpler because the content of the container is available directly
through an instance attribute. The abstract classes in
:mod:`collections.abc` are also useful for creating custom containers
that follow the APIs of the built-in types.

.. _porting-whichdb:

whichdb
-------

.. index::
   pair: porting; whichdb

The functionality of ``whichdb`` has moved to the :mod:`dbm` module.
