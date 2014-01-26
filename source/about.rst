.. spelling::

   blog

===============================
About Python Module of the Week
===============================

PyMOTW-3 is a series of articles written by `Doug Hellmann
<http://doughellmann.com/>`_.  to demonstrate how to use the modules of
the Python_ 3 standard library. It is based on the original PyMOTW_
series, which covered Python 2.7.

.. _Python: http://www.python.org/
.. _PyMOTW: http://pymotw.com/2/

See the project home page at http://pymotw.com/3/ for
updates and the latest release.

..  Source code is available from http://bitbucket.org/dhellmann/pymotw-3/.

Complete documentation for the standard library can be found on the
Python web site at http://docs.python.org/library/.

Tools
=====

The source text for PyMOTW is reStructuredText_ and the HTML output is
created using Sphinx_.

.. _reStructuredText: http://docutils.sourceforge.net/

.. _Sphinx: http://sphinx.pocoo.org/

The output from all the example programs has been generated with
CPython (see below for version) and inserted into the text using cog_.

.. _cog: http://nedbatchelder.com/code/cog/

.. {{{cog
.. cog.out(run_script(cog.inFile, '-V'))
.. }}}

::

	$ python3 -V
	
	Python 3.3.2

.. {{{end}}}

.. warning::

  Some of the features described here may not be available in earlier
  versions of the standard library. When in doubt, refer to the
  documentation for the version of Python you are using.


Subscribe
=========

As new articles are written, they are posted to my blog
(http://doughellmann.com/).  Updates are available by RSS from
http://feeds.doughellmann.com/PyMOTW and `email
<http://feedburner.google.com/fb/a/mailverify?uri=PyMOTW&amp;loc=en_US>`_.
