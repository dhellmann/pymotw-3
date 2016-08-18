:tocdepth: 2

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

New Modules
===========

Python 3 includes a number of new modules, providing features not
present in Python 2.

:mod:`asyncio`
  Asynchronous I/O, event loop, and other concurrency tools.

Renamed Modules
===============

Many standard library modules were renamed between Python 2 and 3 as
part of :pep:`3108` (*Standard Library Reorganization*). All of the
new module names use consistent lower case, and some have been moved
into packages to better organize related modules. Often, code using
these modules can be updated to work with Python 3 just by fixing the
import statements. A complete list of the renames can be found in the
dictionary ``lib2to3.fixes.fix_imports.MAPPING`` (the keys are the
Python 2 name and the values are the Python 3 name).

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
.. for old, new in sorted(MAPPING.items(), key=lambda x: x[0].lower()):
..   if new.startswith('_'):
..     continue
..   cog.out("   ``{}``, :mod:`{}`\n".format(old, new))
.. cog.out("\n")
.. }}}

.. csv-table:: Renamed Modules
   :header: "Python 2 Name", "Python 3 Name"

   ``__builtin__``, :mod:`builtins`
   ``_winreg``, :mod:`winreg`
   ``BaseHTTPServer``, :mod:`http.server`
   ``CGIHTTPServer``, :mod:`http.server`
   ``commands``, :mod:`subprocess`
   ``ConfigParser``, :mod:`configparser`
   ``Cookie``, :mod:`http.cookies`
   ``cookielib``, :mod:`http.cookiejar`
   ``copy_reg``, :mod:`copyreg`
   ``cPickle``, :mod:`pickle`
   ``cStringIO``, :mod:`io`
   ``dbhash``, :mod:`dbm.bsd`
   ``dbm``, :mod:`dbm.ndbm`
   ``Dialog``, :mod:`tkinter.dialog`
   ``DocXMLRPCServer``, :mod:`xmlrpc.server`
   ``dumbdbm``, :mod:`dbm.dumb`
   ``FileDialog``, :mod:`tkinter.filedialog`
   ``gdbm``, :mod:`dbm.gnu`
   ``htmlentitydefs``, :mod:`html.entities`
   ``HTMLParser``, :mod:`html.parser`
   ``httplib``, :mod:`http.client`
   ``Queue``, :mod:`queue`
   ``repr``, :mod:`reprlib`
   ``robotparser``, :mod:`urllib.robotparser`
   ``ScrolledText``, :mod:`tkinter.scrolledtext`
   ``SimpleDialog``, :mod:`tkinter.simpledialog`
   ``SimpleHTTPServer``, :mod:`http.server`
   ``SimpleXMLRPCServer``, :mod:`xmlrpc.server`
   ``SocketServer``, :mod:`socketserver`
   ``StringIO``, :mod:`io`
   ``Tix``, :mod:`tkinter.tix`
   ``tkColorChooser``, :mod:`tkinter.colorchooser`
   ``tkCommonDialog``, :mod:`tkinter.commondialog`
   ``Tkconstants``, :mod:`tkinter.constants`
   ``Tkdnd``, :mod:`tkinter.dnd`
   ``tkFileDialog``, :mod:`tkinter.filedialog`
   ``tkFont``, :mod:`tkinter.font`
   ``Tkinter``, :mod:`tkinter`
   ``tkMessageBox``, :mod:`tkinter.messagebox`
   ``tkSimpleDialog``, :mod:`tkinter.simpledialog`
   ``ttk``, :mod:`tkinter.ttk`
   ``urlparse``, :mod:`urllib.parse`
   ``UserList``, :mod:`collections`
   ``UserString``, :mod:`collections`
   ``xmlrpclib``, :mod:`xmlrpc.client`

.. {{{end}}}

.. seealso::

   * The six_ package is useful for writing code that runs under both
     Python 2 and 3. In particular, the ``six.moves`` module allows
     your code to import renamed modules using a single import
     statement, automatically redirecting the import to the correct
     version of the name depending on the version of Python.

   * :pep:`3108` -- Standard Library Reorganization

.. _six: http://pythonhosted.org/six/

Removed Modules
===============

.. index::
   single: porting; removed modules

These modules are either no longer present at all, or have had their
features merged into other existing modules.

bsddb
-----

The :mod:`bsddb` and :mod:`dbm.bsd` modules have been
removed. Bindings for Berkeley DB are now maintained `outside of the
standard library <https://pypi.python.org/pypi/bsddb3>`__ as
``bsddb3``.

commands
--------

.. index::
   pair: porting; subprocess

The :mod:`commands` module was deprecated in Python 2.6 and removed
in Python 3.0. See :mod:`subprocess` instead.

compiler
--------

.. index::
   pair: porting; ast

The :mod:`compiler` module has been removed. See :mod:`ast` instead.

.. _porting-decimal:

decimal
-------

.. index::
   pair: porting; decimal

Python 3.3 incorporated a C implementation of :mod:`decimal` based on
``libmpdec``. This change improved performance, but also includes some
API changes and behavior differences from the pure-Python
implementation. See `the Python 3.3 release notes
<https://docs.python.org/3.3/whatsnew/3.3.html#decimal>`__ for
details.

dircache
--------

The :mod:`dircache` module has been removed, without a replacement.

EasyDialogs
-----------

.. index::
   pair: porting; tkinter

The :mod:`EasyDialogs` module has been removed. See :mod:`tkinter`
instead.

exceptions
----------

The :mod:`exceptions` module has been removed because all of the
exceptions defined there are available as built-in classes.

htmllib
-------

.. index::
   pair: porting; html.parser

The :mod:`htmllib` module has been removed. See :mod:`html.parser`
instead.

md5
---

.. index::
   pair: porting; hashlib

The implementation of the MD5 message digest algorithm has moved to
:mod:`hashlib`.

mimetools, MimeWriter, mimify, multifile, and rfc822
----------------------------------------------------

.. index::
   pair: porting; email

The :mod:`mimetools`, :mod:`MimeWriter`, :mod:`mimify`,
:mod:`multifile`, and :mod:`rfc822` modules have been removed. See
:mod:`email` instead.

popen2
------

.. index::
   pair: porting; subprocess

The :mod:`popen2` module has been removed. See :mod:`subprocess`
instead.

posixfile
---------

.. index::
   pair: porting; io

The :mod:`posixfile` module has been removed. See :mod:`io` instead.

.. _porting-re:

re
--

.. index::
   pair: porting; re

The :const:`UNICODE` flag represents the default behavior. To restore
the ASCII-specific behavior from Python 2, use the :const:`ASCII`
flag.


sets
----

The :mod:`sets` module was deprecated in Python 2.6 and removed in
Python 3.0. Use the built-in types :class:`set` and
:class:`orderedset` instead.

sha
---

.. index::
   pair: porting; hashlib

The implementation of the SHA-1 message digest algorithm has moved
to :mod:`hashlib`.

sre
---

.. index::
   pair: porting; re

The :mod:`sre` module was deprecated in Python 2.5 and removed in
Python 3.0. Use :mod:`re` instead.

statvfs
-------

.. index::
   pair: porting; os

The :mod:`statvfs` module was deprecated in Python 2.6 and removed
in Python 3.0. See :func:`os.statvfs` in the :mod:`os` module
instead.

.. _porting-string:

string
------

.. index::
   pair: porting; string

All functions from the :mod:`string` module that are also methods of
:class:`str` objects have been removed.

The constants :data:`letters`, :data:`lowercase`, and
:data:`uppercase` have been removed. The new constants with similar
names are limited to the ASCII character set.

The :func:`maketrans` function has been replaced by methods on
:class:`str`, :class:`bytes`, and :class:`bytearray` to clarify which
input types are supported by each translation table.

.. _porting-struct:

struct
------

.. index::
   pair: porting; struct

:func:`struct.pack` now only supports byte strings when using the
``s`` string pack code, and no longer implicitly encodes string
objects to UTF-8 (:pyissue:`10783`).


thread
------

.. index::
   pair: porting; threading

The :mod:`thread` module has been removed.  Use the higher-level API
in :mod:`threading` instead.

.. _porting-time:

time
----

.. index::
   pair: porting; time

:func:`time.asctime` and :func:`time.ctime` have been reimplemented to
not use the system functions of the same time to allow larger years to
be used. :func:`time.ctime` now supports years from 1900 through
:data:`maxint`, although for values higher than ``9999`` the output
string is longer than the standard 24 characters to allow for the
extra year digits (:pyissue:`8013`).

user
----

.. index::
   pair: porting; site

The :mod:`user` module was deprecated in Python 2.6 and removed in
Python 3.0. See user-customization features provided by the
:mod:`site` module instead.

Deprecated Modules
==================

.. index::
   single: porting; deprecated modules

These modules are still present in the standard library, but are
deprecated and should not be used in new Python 3 programs.

asyncore and asynchat
---------------------

.. index::
   pair: porting; asyncore
   pair: porting; asynchat

Asynchronous I/O and protocol handlers.

See :mod:`asyncio` instead.

formatter
---------

.. index::
   pair: porting; formatter

Generic output formatter and device interface.

See :pyissue:`18716` for details.

imp
---

.. index::
   pair: porting; imp
   pair: porting; importlib

Access the implementation of the import statement.

See :mod:`importlib` instead.

optparse
--------

.. index::
   pair: porting; optparse
   pair: porting; argparse

Command-line option parsing library.

The API for :mod:`argparse` is similar to the one provided by
:mod:`optparse`, and in many cases :mod:`argparse` can be used as a
straightforward replacement by updating the names of the classes and
methods used.


Summary of Changes to Modules
=============================

.. index::
   single: porting; changed modules

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

.. _porting-itertools:

itertools
---------

.. index::
   pair: porting; itertools

The functions :func:`imap`, :func:`izip`, and :func:`ifilter` have
been replaced with versions of the built-in functions that return
iterables instead of :class:`list` objects (:func:`map`, :func:`zip`,
and :func:`filter:` respectively).

The function :func:`ifilterfalse` has been renamed
:func:`filterfalse`.

.. _porting-locale:

locale
------

.. index::
   pair: porting; locale

The normalized version of the name of the UTF-8 encoding has changed
from "UTF8" to "UTF-8" because Mac OS X and OpenBSD do not support the
use of "UTF8" (:pyissue:`10154` and :pyissue:`10090`).


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

.. _porting-operator:

operator
--------

.. index::
   pair: porting; operator

The :func:`div` function has been removed. Use either :func:`floordiv`
or :func:`truediv`, depending on the desired semantics.

The :func:`repeat` function is removed. Use :func:`mul` instead.

The functions :func:`getslice`, :func:`setslice`, and :func:`delslice`
are removed. Use :func:`getitem`, :func:`setitem`, and :func:`delitem`
with slice indexes instead.

The function :func:`isCallable` has been removed. Use the abstract
base class :class:`collections.Callable` instead.

.. code-block:: python

   isinstance(obj, collections.Callable)

The type checking functions :func:`isMappingType`,
:func:`isSequenceType`, and :func:`isNumberType` have been
removed. Use the relevant abstract base classes from
:mod:`collections` or :mod:`numbers` instead.

.. code-block:: python

   isinstance(obj, collections.Mapping)
   isinstance(obj, collections.Sequence)
   isinstance(obj, numbers.Number)

The :func:`sequenceIncludes` function has been removed. Use
:func:`contains` instead.

.. _porting-os:

os
--

.. index::
   pair: porting; os

The functions :func:`popen2`, :func:`popen3`, and :func:`popen4` have
been removed.  :func:`popen` is still present but deprecated and emits
warnings if used.  Code using these functions should be rewritten to
use :mod:`subprocess` instead to be more portable across operating
systems.

The functions :func:`os.tmpnam`, :func:`os.tempnam` and
:func:`os.tmpfile` have been removed. Use the :mod:`tempfile` module
instead.

The function :func:`os.stat_float_times` is deprecated
(:pyissue:`14711`).

:func:`os.unsetenv` no longer ignores errors (:pyissue:`13415`).

.. _porting-pdb:

pdb
---

.. index::
   pair: porting; pdb

The ``print`` command alias has been removed so that it does not
shadow the ``print()`` function (:pyissue:`18764`). The ``p`` shortcut
is retained.

.. _porting-pickle:

pickle
------

.. index::
   pair: porting; pickle

The C implementation of the pickle module from Python 2 has been moved
to a new module that is automatically used to replace the Python
implementation when possible. The old import idiom of

::

    try:
       import cPickle as pickle
    except:
       import pickle

can be replaced with

::

    import pickle

Interoperability between Python 2.x and 3.x has been improved for
pickled data using the level 2 protocol or lower to resolve an issue
introduced when a large number of standard library modules were
renamed during the transition to Python 3. Because pickled data
includes references to class and type names, and those names changed,
it was difficult to exchange pickled data between Python 2 and 3
programs. Now for data pickled using protocol level 2 or older, the
old names of the classes are automatically used when writing to and
reading from a pickle stream.

This behavior is available by default, and can be turned off using the
``fix_imports`` option. This change improves the situation, but does
not eliminate incompatibilities entirely. In particular, it is
possible that data pickled under Python 3.1 can't be read under Python
3.0. To ensure maximum portability between Python 3 applications, use
protocol level 3, which does not include this compatibility feature.

The default protocol version has changed from ``0``, the
human-readable version, to ``3``, the binary format with the best
interoperability when shared between Python 3 applications.

Byte string data written to a pickle by a Python 2.x application is
decoded when it is read back to create a Unicode string object. The
encoding for the transformation defaults to ASCII, and can be changed
by passing values to the :class:`Unpickler`.

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

.. _porting-uuid:

uuid
----

.. index::
   pair: porting; uuid

:func:`uuid.getnode` now uses the ``PATH`` environment variable to
find programs that can report the MAC address of the host under UNIX
(:pyissue:`19855`). It falls back to looking in ``/sbin`` and
``/usr/sbin`` if no program is found on the search path. This search
behavior may give different results than with earlier versions of
Python if alternate versions of programs like ``netstat``,
``ifconfig``, ``ip``, and ``arp`` are present and produce different
output.

.. _porting-whichdb:

whichdb
-------

.. index::
   pair: porting; whichdb

The functionality of ``whichdb`` has moved to the :mod:`dbm` module.

.. _porting-xml.etree.ElementTree:

xml.etree.ElementTree
---------------------

.. index::
   pair: porting; xml.etree.ElementTree

:class:`XMLTreeBuilder` has been renamed :class:`TreeBuilder`, and the
API has undergone several changes.

:func:`ElementTree.getchildren` has been deprecated. Use
``list(elem)`` to build a list of the children.

:func:`ElementTree.getiterator` has been deprecated. Use :func:`iter`
to create an iterator using the normal iterator protocol
instead.

When parsing fails, rather than raising
:class:`xml.parsers.expat.ExpatError`, :class:`XMLParser` now raises
:class:`xml.etree.ElementTree.ParseError`.

.. _porting-zipimport:

zipimport
---------

.. index::
   pair: porting; zipimport

The data returned from :func:`get_data` is a byte string, and needs to
be decoded before being used as a unicode string.
