=======================================================
 urllib.robotparser --- Internet Spider Access Control
=======================================================

.. module:: urllib.robotparser
    :synopsis: Internet spider access control

:mod:`robotparser` implements a parser for the ``robots.txt`` file
format, including a function that checks if a given user agent
can access a resource.  It is intended for use in well-behaved spiders,
or other crawler applications that need to either be throttled or
otherwise restricted.

robots.txt
==========

The ``robots.txt`` file format is a simple text-based access control
system for computer programs that automatically access web resources
("spiders", "crawlers", etc.).  The file is made up of records that
specify the user agent identifier for the program followed by a list
of URLs (or URL prefixes) the agent may not access.

This is the ``robots.txt`` file for ``https://pymotw.com/``:

.. literalinclude:: robots.txt
    :caption:

It prevents access to some of the parts of the site that are expensive
to compute and would overload the server if a search engine tried to
index them.  For a more complete set of examples of ``robots.txt``,
refer to `The Web Robots Page`_.

Testing Access Permissions
==========================

Using the data presented earlier, a simple crawler can test whether it
is allowed to download a page using ``RobotFileParser.can_fetch()``.

.. literalinclude:: urllib_robotparser_simple.py
    :caption:
    :start-after: #end_pymotw_header

The URL argument to ``can_fetch()`` can be a path relative to the
root of the site, or full URL.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'urllib_robotparser_simple.py'))
.. }}}

.. code-block:: none

	$ python3 urllib_robotparser_simple.py
	
	  True : /
	  True : https://pymotw.com/
	
	  True : /PyMOTW/
	  True : https://pymotw.com/PyMOTW/
	
	 False : /admin/
	 False : https://pymotw.com/admin/
	
	 False : /downloads/PyMOTW-1.92.tar.gz
	 False : https://pymotw.com/downloads/PyMOTW-1.92.tar.gz
	

.. {{{end}}}

Long-lived Spiders
==================

An application that takes a long time to process the resources it
downloads or that is throttled to pause between downloads should
check for new ``robots.txt`` files periodically based on the age of
the content it has downloaded already.  The age is not managed
automatically, but there are convenience methods to make tracking it
easier.

.. literalinclude:: urllib_robotparser_longlived.py
    :caption:
    :start-after: #end_pymotw_header

This extreme example downloads a new ``robots.txt`` file if the one it
has is more than one second old.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'urllib_robotparser_longlived.py'))
.. }}}

.. code-block:: none

	$ python3 urllib_robotparser_longlived.py
	
	age: 0 
	  True : /
	
	age: 1 
	  True : /PyMOTW/
	
	age: 2 rereading robots.txt
	 False : /admin/
	
	age: 1 
	 False : /downloads/PyMOTW-1.92.tar.gz
	

.. {{{end}}}

A nicer version of the long-lived application might request the
modification time for the file before downloading the entire thing.
On the other hand, ``robots.txt`` files are usually fairly small, so
it is not that much more expensive to just retrieve the entire document
again.


.. seealso::

   * :pydoc:`urllib.robotparser`

   * `The Web Robots Page`_ -- Description of ``robots.txt`` format.

.. _The Web Robots Page: http://www.robotstxt.org/orig.html
