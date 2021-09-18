=================================
tabnanny -- Indentation validator
=================================

.. module:: tabnanny
    :synopsis: Scan Python source code looking for suspicious indentation.

:Purpose: Scan Python source code looking for suspicious indentation.
:Available In: 2.1.3 and later

Consistent use of indentation is important in a langauge like Python,
where white-space is significant.  The :mod:`tabnanny` module provides
a scanner to report on "ambiguous" use of indentation.

Running from the Command Line
=============================

The simplest way to use :mod:`tabnanny` is to run it from the command
line, passing the names of files to check.  If you pass directory
names, the directories are scanned recursively to find `.py` files to
check.

When I ran tabnanny across the PyMOTW source code, I found one old
module with tabs instead of spaces::

    $ python -m tabnanny .
    ./PyMOTW/Queue/fetch_podcasts.py 78 "\t\tfor enclosure in entry.get('enclosures', []):\n"

Sure enough, line 78 of `fetch_podcasts.py` had two tabs instead of 8
spaces.  I didn't see this by looking at it in my editor because I
have my tabstops set to 4 spaces, so visually there was no difference.

::

        for enclosure in entry.get('enclosures', []):
            print 'Queuing:', enclosure['url']
            enclosure_queue.put(enclosure['url'])

Correcting line 78 and running tabnanny again showed another error on
line 79.  One last problem showed up on line 80.

If you want to scan files, but not see the details about the error,
you can use the `-q` option to suppress all information except the
filename.

::

    $ python -m tabnanny -q .
    ./PyMOTW/Queue/fetch_podcasts.py

To see more information about the files being scanned, use the `-v` option.

::

    $ python -m tabnanny -v ./PyMOTW/Queue
    './PyMOTW/Queue': listing directory
    './PyMOTW/Queue/__init__.py': Clean bill of health.
    './PyMOTW/Queue/feedparser.py': Clean bill of health.
    './PyMOTW/Queue/fetch_podcasts.py': *** Line 78: trouble in tab city! ***
    offending line: "\t\tfor enclosure in entry.get('enclosures', []):\n"
    indent not greater e.g. at tab sizes 1, 2


Using within Your Program
=========================

As soon as I discovered the mistake in my Queue example, I decided I
needed to add an automatic check to my PyMOTW build process.  I
created a ``tabcheck`` task in my ``pavement.py`` build script so I
could run `paver tabcheck` and scan the code I'm working on for
PyMOTW.  This is possible because tabnanny exposes its `check()`
function as a public API.

Here's an example of using tabnanny that doesn't require understanding
Paver's task definition decorators.

.. include:: tabnanny_check.py
   :literal:
   :start-after: #end_pymotw_header

And in action:

::

	$ python tabnanny_check.py ../Queue
	'../Queue': listing directory
	'../Queue/__init__.py': Clean bill of health.
	'../Queue/feedparser.py': Clean bill of health.
	'../Queue/fetch_podcasts.py': *** Line 78: trouble in tab city! ***
	offending line: "\t\tfor enclosure in entry.get('enclosures', []):\n"
	indent not greater e.g. at tab sizes 1, 2

.. note:: 

  If you run these examples against the PyMOTW code it won't report
  the same errors, since I have fixed my code in this release.

.. seealso::

    `tabnanny <http://docs.python.org/2.7/library/tabnanny.html>`_
        The standard library documentation for this module.

    :mod:`tokenize`
        Lexical scanner for Python source code.
