=============================================
robotparser -- Internet spider access control
=============================================

.. module:: robotparser
    :synopsis: Internet spider access control

:Purpose: Parse robots.txt file used to control Internet spiders
:Available In: 2.1.3 and later

:mod:`robotparser` implements a parser for the ``robots.txt`` file format, including a simple function for checking if a given user agent can access a resource.  It is intended for use in well-behaved spiders or other crawler applications that need to either be throttled or otherwise restricted.

.. note::

    The :mod:`robotparser` module has been renamed :mod:`urllib.robotparser` in Python 3.0.
    Existing code using :mod:`robotparser` can be updated using 2to3.

robots.txt
==========

The ``robots.txt`` file format is a simple text-based access control system for computer programs that automatically access web resources ("spiders", "crawlers", etc.).  The file is made up of records that specify the user agent identifier for the program followed by a list of URLs (or URL prefixes) the agent may not access.  

This is the ``robots.txt`` file for ``http://www.doughellmann.com/``:

.. include:: robots.txt
    :literal:

It prevents access to some of the expensive parts of my site that would overload the server if a search engine tried to index them.  For a more complete set of examples, refer to `The Web Robots Page`_.

Simple Example
==============

Using the data above, a simple crawler can test whether it is allowed to download a page using the ``RobotFileParser``'s ``can_fetch()`` method.

.. include:: robotparser_simple.py
    :literal:
    :start-after: #end_pymotw_header

The URL argument to ``can_fetch()`` can be a path relative to the root of the site, or full URL.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'robotparser_simple.py'))
.. }}}

::

	$ python robotparser_simple.py
	
	  True : /
	  True : http://www.doughellmann.com/
	
	  True : /PyMOTW/
	  True : http://www.doughellmann.com/PyMOTW/
	
	  True : /admin/
	  True : http://www.doughellmann.com/admin/
	
	 False : /downloads/PyMOTW-1.92.tar.gz
	 False : http://www.doughellmann.com/downloads/PyMOTW-1.92.tar.gz
	

.. {{{end}}}



Long-lived Spiders
==================

An application that takes a long time to process the resources it downloads or that is throttled to pause between downloads may want to check for new ``robots.txt`` files periodically based on the age of the content it has downloaded already.  The age is not managed automatically, but there are convenience methods to make tracking it easier.

.. include:: robotparser_longlived.py
    :literal:
    :start-after: #end_pymotw_header

This extreme example downloads a new ``robots.txt`` file if the one it has is more than 1 second old.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'robotparser_longlived.py'))
.. }}}

::

	$ python robotparser_longlived.py
	
	
	age: 0
	  True : /
	
	age: 1
	  True : /PyMOTW/
	
	age: 2 re-reading robots.txt
	 False : /admin/
	
	age: 1
	 False : /downloads/PyMOTW-1.92.tar.gz

.. {{{end}}}

A "nicer" version of the long-lived application might request the modification time for the file before downloading the entire thing.  On the other hand, ``robots.txt`` files are usually fairly small, so it isn't that much more expensive to just grab the entire document again.


.. seealso::

    `robotparser <http://docs.python.org/2.7/library/robotparser.html>`_
        The standard library documentation for this module.

    `The Web Robots Page`_
        Description of robots.txt format.

.. _The Web Robots Page: http://www.robotstxt.org/orig.html
