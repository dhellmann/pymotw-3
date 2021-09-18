===============================
About Python Module of the Week
===============================

PyMOTW is a series of blog posts written by `Doug Hellmann
<http://www.doughellmann.com/>`_.  It was started as a way to build
the habit of writing something on a regular basis.  The focus of the
series is building a set of example code for the modules in the
`Python <http://www.python.org/>`_ standard library.

See the project home page at http://pymotw.com/ for
updates and the latest release.  Source code is available from
https://github.com/dhellmann/pymotw.

Complete documentation for the standard library can be found on the
Python web site at http://docs.python.org/library/.

Tools
=====

The source text for PyMOTW is reStructuredText_
and the HTML and PDF output are
created using Sphinx_.

.. _reStructuredText: http://docutils.sourceforge.net/

.. _Sphinx: http://sphinx.pocoo.org/

The output from all the example programs has been generated with
CPython (see below for version) and inserted into the text using
cog_. 

.. _cog: http://nedbatchelder.com/code/cog/

.. {{{cog
.. cog.out(run_script(cog.inFile, '-V'))
.. }}}

::

	$ python -V
	
	Python 2.7.8

.. {{{end}}}

.. warning::

  Some of the features described here may not be available in earlier
  versions of the standard library. When in doubt, refer to the
  documentation for the version of Python you are using.


Subscribe
=========

As new articles are written, they are posted to my blog
(http://blog.doughellmann.com/).  Updates are available by RSS from
http://feeds.doughellmann.com/PyMOTW and `email
<http://feedburner.google.com/fb/a/mailverify?uri=PyMOTW&amp;loc=en_US>`_.

.. _motw-cli:

The motw Command Line Interface
===============================

PyMOTW includes a command line program, ``motw``, to make it even
easier to access the examples while you are developing. Simply run
``motw module`` to open the local copy of the HTML text for the named
module. There are also options to view the articles in different
formats (see the ``-h`` output for details).

Usage: ``motw [options] <module_name>``

Options:

-h, --help  show this help message and exit
-t, --text  Print plain-text version of help to stdout
-w, --web   Open HTML version of help from web
--html      Open HTML version of help from installed file

.. _motw-interactive:

Using PyMOTW with the Interactive Interpreter
=============================================

PyMOTW articles are at your fingertips while you're working with the
Python interactive interpreter.  Importing ``PyMOTW`` adds the
function ``motw()`` to the ``__builtins__`` namespace.  Run
``motw(module)`` to see the help for an imported module.  Enclose the
name in quotes for a module that you haven't already imported.

::

    $ python
    Python 2.6.2 (r262:71600, Apr 16 2009, 09:17:39) 
    [GCC 4.0.1 (Apple Computer, Inc. build 5250)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import PyMOTW
    >>> motw('atexit')
    
    atexit -- Call functions when a program is closing down
    *******************************************************
    ...

.. _translations:

Translations and Other Versions
===============================

`Chinese <http://www.vbarter.cn/pymotw/>`_

  Junjie Cai (蔡俊杰) and Yan Sheng (盛艳) have started a google code
  project called PyMOTWCN (http://code.google.com/p/pymotwcn/) and
  posted the completed translations at http://www.vbarter.cn/pymotw/.

`German <http://schoenian-online.de/pymotw.html>`_

  Ralf Schönian is translating PyMOTW into German, following an
  alphabetical order.  The results are available on his web site,
  http://schoenian-online.de/pymotw.html.  Ralf is an active member of
  the `pyCologne
  <http://wiki.python.de/User_Group_K%C3%B6ln?action=show&redirect=pyCologne>`_
  user group in Germany and author of pyVoc, the open source
  English/German vocabulary trainer (http://code.google.com/p/pyvoc/).

`Italian <http://robyp.x10host.com/>`_

  Roberto Pauletto is working on an Italian translation at
  http://robyp.x10host.com/.  Roberto creates Windows applications
  with C# by day, and tinkers with Linux and Python at home.  He has
  recently moved to Python from Perl for all of his
  system-administration scripting.

`Spanish <http://denklab.org/articles/category/pymotw/>`_

  `Ernesto Rico Schmidt <http://denklab.org/>`_ provides a Spanish
  translation that follows the English version posts. Ernesto is in
  Bolivia, and is translating these examples as a way to contribute to
  the members of the `Bolivian Free Software
  <http://www.softwarelibre.org.bo/>`_ community who use Python.  The
  full list of articles available in Spanish can be found at
  http://denklab.org/articles/category/pymotw/, and there is an `RSS
  feed <http://denklab.org/feeds/articles/category/pymotw/>`_.

`Japanese <http://ja.pymotw.com/>`_

  `Tetsuya Morimoto <http://d.hatena.ne.jp/t2y-1979/>`_ is creating a
  Japanese translation. Tetsuya has used Python for 1.5 years. He has
  as experience at a Linux Distributor using Python with yum,
  anaconda, and rpm-tools while building RPM packages. Now, he uses it
  to make useful tools for himself, and is interested in application
  frameworks such as Django, mercurial and wxPython. Tetsuya is a
  member of `Python Japan User's Group <http://www.python.jp/Zope/>`_
  and `Python Code Reading
  <http://groups.google.co.jp/group/python-code-reading>`_. The home
  page for his translation is http://ja.pymotw.com/.


Compendiums
-----------

Gerard Flanagan is working on a "Python compendium" called `The Hazel
Tree <http://www.thehazeltree.org/>`_.  He is converting a collection
of old and new of Python-related reference material into
reStructuredText and then building a single searchable repository from
the results.  I am very pleased to have PyMOTW included with works
from authors like Mark Pilgrim, Fredrik Lundh, Andrew Kuchling, and a
growing list of others.

Other Contributors
==================

Thank you to John Benediktsson for the original HTML-to-reST
conversion.

.. include:: copyright.rst
