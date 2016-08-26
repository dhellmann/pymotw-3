==========================================
 linecache -- Read Text Files Efficiently
==========================================

.. module:: linecache
    :synopsis: Read text files efficiently

:Purpose: Retrieve lines of text from files or imported Python modules, holding a cache of the results to make reading many lines from the same file more efficient.

The :mod:`linecache` module is used within other parts of the Python
standard library when dealing with Python source files. The
implementation of the cache holds the contents of files, parsed into
separate lines, in memory. The API returns the requested line(s) by
indexing into a :class:`list`, and saves time over repeatedly reading the file
and parsing lines to find the one desired. This is especially useful
when looking for multiple lines from the same file, such as when
producing a traceback for an error report.

.. toctree::

   normal

.. only:: bonus

   .. toctree::

      bonus
    
.. seealso::

    `linecache <http://docs.python.org/library/linecache.html>`_
        The standard library documentation for this module.

    http://www.ipsum.com/
        Lorem Ipsum generator.
