=================================
 Outside of the Standard Library
=================================

Although the Python standard library is extensive, there is also a
robust ecosystem of modules provided by third-party developers and
available from the `Python Package Index`_. This appendix describes
some of these modules, and the situations when you might want to use
them to supplement or even replace the standard library.

Text
====

The :mod:`string` module includes a very basic template tool. Many web
frameworks include more powerful template tools, but Jinja2_ and Mako_
are popular standalone alternatives. Both support looping and
conditional control structures as well as other features for combining
data with a template to produce text output.

.. _Jinja2: http://jinja.pocoo.org
.. _Mako: http://docs.makotemplates.org/en/latest/

The :mod:`re` module includes functions for searching and parsing text
using formally described patterns called regular expressions. It is
not the only way to parse text, though.

The PLY_ package supports building parsers in the style of the GNU
tools lexx and yacc, commonly used for building language compilers. By
providing inputs describing the valid tokens, a grammar, and actions
to take when each are encountered, it is possible to build fully
functional compilers and interpreters, as well as more straightforward
data parsers.

PyParsing_ is a another tool for building parsers. The inputs are
instances of classes that can be chained together using operators and
method calls to build up a grammar.

Finally, NLTK_ is a package for processing natural language text --
human languages instead of computer languages. It supports parsing
sentences into parts of speech, finding the root form of words, and
basic semantic processing.

.. _PLY: http://www.dabeaz.com/ply/
.. _PyParsing: http://pyparsing.wikispaces.com
.. _NLTK: http://www.nltk.org

Algorithms
==========

The :mod:`functools` module includes some tools for creating
decorators, functions that wrap other functions to change how they
behave. The wrapt_ package goes further than ``functools.wrap()`` to
ensure that a decorator is constructed properly and works for all
edge-cases.

.. _wrapt: http://wrapt.readthedocs.org/

Dates and Times
===============

The :mod:`time` and :mod:`datetime` modules provide functions and
classes for manipulating time and date values. Both include functions
for parsing strings to turn them into internal representations. The
dateutil_ package includes a more flexible parser that makes it easier
to build robust applications that are more forgiving of different
input formats.

The :mod:`datetime` module includes a timezone-aware class for
representing a specific time on a specific day. It does not, however,
include a full timezone database. The pytz_ package does provide such
a database. It is distributed separately from the standard library
because it is maintained by other authors and it is updated frequently
when timezone and daylight savings time values are changed by the
political institutions that control them.

.. _dateutil: https://dateutil.readthedocs.io/
.. _pytz: http://pythonhosted.org/pytz/

Mathematics
===========

The :mod:`math` module contains fast implementations of advanced
mathematical functions. NumPy_ expands the set of functions supported
to include linear algebra and Fourier transform functions. It also
includes a fast multi-dimensional array implementation, improving on
the version in :mod:`array`.

.. _NumPy: http://www.numpy.org

Data Persistence and Exchange
=============================

The examples in the :mod:`sqlite3` section run SQL statements directly
and work with low-level data structures. For large applications, it is
often desirable to map classes to tables in the database using an
*object relational mapper* or ORM. The sqlalchemy_ ORM library
provides APIs for associating classes with tables, building queries,
and connecting to different types of production-grade relational
databases.

The lxml_ package wraps the libxml2 and libxslt libraries to create an
alternative to the XML parser in
:mod:`xml.etree.ElementTree`. Developers familiar with using those
libraries from other languages may find lxml easier to adopt in
Python.

The defusedxml_ package contains fixes for "`Billion Laughs`_" and
other entity expansion denial of service vulnerabilities in Python's
XML libraries and makes working with untrusted XML safer than using
the standard library alone.

.. _sqlalchemy: http://www.sqlalchemy.org
.. _lxml: http://lxml.de
.. _Billion Laughs: http://en.wikipedia.org/wiki/Billion_laughs
.. _defusedxml: https://pypi.python.org/pypi/defusedxml

Cryptography
============

The team building the cryptography_ package says "Our goal is for it
to be your 'cryptographic standard library'." The cryptography package
exposes high-level APIs to make it easy to add cryptographic features
to applications and the package is actively maintained with frequent
releases to address vulnerabilities in the underlying libraries such
as OpenSSL.

.. _cryptography: https://cryptography.io/en/latest/

Concurrency with Processes, Threads, and Coroutines
===================================================

The event loop built into :mod:`asyncio` is a reference implementation
based on the abstract API defined by the module. It is possible to
replace the event loop with a library such as uvloop_, which gives
better performance in exchange for adding extra application
dependencies.

The curio_ package is another concurrency package similar to asyncio
but with a smaller API that treats everything as a coroutine and does
not support callbacks in the way asyncio does.

The Twisted_ library provides an extensible framework for Python
programming, with special focus on event-based network programming and
multiprotocol integration. It is mature, robust, and well-documented.

.. _curio: https://github.com/dabeaz/curio
.. _uvloop: http://uvloop.readthedocs.io
.. _Twisted: https://twistedmatrix.com/

The Internet
============

The requests_ package is a very popular replacement for
:mod:`urllib.request`. It provides a consistent API for working with
remote resources addressable via HTTP, includes robust SSL support,
and can use connection pooling for better performance in
multi-threaded applications. It also provides features that make it
well suited for accessing REST APIs, such as built-in JSON parsing.

Python's :mod:`html` module includes a basic parser for well-formed
HTML data. However, real world data is rarely well structured, making
parsing it problematic. The BeautifulSoup_ and PyQuery_ libraries are
alternatives to :mod:`html` that are more robust in the face of messy
data. Both define APIs for parsing, modifying, and constructing HTML.

.. _requests: http://docs.python-requests.org/
.. _BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/
.. _PyQuery: http://pyquery.rtfd.org/

The built-in :mod:`http.server` package includes base classes for
creating simple HTTP servers from scratch. It does not offer much
support beyond that for building web-based applications, though. The
Django_ and Pyramid_ packages are two popular web application
frameworks that provide more support for advanced features like
request parsing, URL routing, and cookie handling.

.. _Django: http://www.djangoproject.com/
.. _Pyramid: https://trypyramid.com/

Many existing libraries do not work with :mod:`asyncio` because they
do not integrate with the event loop. A new set of libraries such as
aiohttp_ is being created to fill this gap as part of the `aio-libs`_
project.

.. _aiohttp: http://aiohttp.readthedocs.io/
.. _aio-libs: https://github.com/aio-libs

Email
=====

The API for :mod:`imaplib` is relatively low-level, requiring the
caller to understand the IMAP protocol to build queries and parse
results. The imapclient_ package provides a higher-level API that is
easier to work with for building applications that need to manipulate
IMAP mailboxes.

.. _imapclient: http://imapclient.freshfoo.com/

Application Building Blocks
===========================

The two standard library modules for building command line interfaces,
:mod:`argparse` and :mod:`getopt`, both separate the definition of
command line arguments from their parsing and value
processing. Alternatively, click_ (the "Command Line Interface
Construction Kit"), works by defining command processing functions and
then associating option and prompt definitions with those commands
using decorators.

cliff_ ("Command Line Interface Formulation Framework") provides a set
of base classes for defining commands and a plugin system for
extending applications with multiple sub-commands that can be
distributed in separate packages. It uses :mod:`argparse` to build the
help text and argument parser, so the command line processing is
familiar.

The docopt_ package reverses the typical flow by asking the developer
to write the help text for a program, which it then parses to
understand the sub-commands, valid combinations of options, and
sub-commands.

For interactive terminal-based programs, `prompt_toolkit`_ includes
advanced features like color support, syntax highlighting, input
editing, mouse support, and searchable history. It can be used to
build command-oriented programs with a prompt loop like the :mod:`cmd`
module, or full-screen applications like text editors.

While INI files such as used by :mod:`configparser` continue to be
popular for application configuration, the YAML_ file format is also
very popular. YAML provides many of the data structure features of
JSON in a format that is easier for people to read. The PyYAML_
library provides access to a YAML parser and serializer.

.. _click: http://click.pocoo.org
.. _cliff: http://docs.openstack.org/developer/cliff/
.. _docopt: http://docopt.org
.. _prompt_toolkit: http://python-prompt-toolkit.readthedocs.io/en/stable/
.. _YAML: http://yaml.org
.. _PyYAML: http://pyyaml.org

Developer Tools
===============

The standard library module :mod:`venv` is new in Python 3. For
similar application isolation under both Python 2 and 3, use
virtualenv_.

The fixtures_ package provides several test resource management
classes tailor made to work with the ``addCleanup()`` method of test
cases from the :mod:`unittest` module. The provided fixture classes
can manage loggers, environment variables, temporary files, and more
in a consistent and safe way that ensures each test case is completely
isolated from others in the suite.

.. _virtualenv: https://virtualenv.pypa.io/
.. _fixtures: https://pypi.python.org/pypi/fixtures

The :mod:`distutils` module in the standard library for packaging
Python modules for distribution and reuse is deprecated. The
replacement, setuptools_, is packaged separately from the standard
library to make it easier to deliver new versions frequently. The API
for setuptools includes tools for building the list of files to
include in a package. There are extensions to automatically build the
list from the set of files managed by a version control system. For
example, using `setuptools-git`_ with source in a git_ repository
causes all of the tracked files to be included in the package by
default. After a package is built, the twine_ application will upload
it to the package index to be shared with other developers.

.. _setuptools: http://pythonhosted.org/setuptools/
.. _setuptools-git: https://pypi.python.org/pypi/setuptools-git
.. _git: https://git-scm.com
.. _twine: https://pypi.python.org/pypi/twine

Tools like :mod:`tabnanny` are good at finding common formatting
mistakes in Python code. The `Python Code Quality Authority`_
maintains an extensive range of more advanced *static analysis tools*,
including tools that enforce style guidelines, find common programming
errors, and even help avoid excessive complexity.

.. _Python Code Quality Authority: http://meta.pycqa.org/en/latest/

.. seealso::

   * `Python Package Index`_ or PyPI -- The site for finding and
     downloading extension modules distributed separately from the
     Python runtime.

.. _Python Package Index: https://pypi.python.org/pypi
