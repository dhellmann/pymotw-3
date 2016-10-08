====================================
 urllib2 -- Network Resource Access
====================================

.. module:: urllib2
    :synopsis: Network Resource Access

:Purpose: A library for opening URLs that can be extended by defining custom protocol handlers.
:Python Version: 2.1 and later

The :mod:`urllib2` module provides an updated API for using Internet
resources identified by URLs.  It is designed to be extended by
individual applications to support new protocols or add variations to
existing protocols (such as handling HTTP basic authentication).

.. toctree::

   normal

.. only:: bonus

   .. toctree:: 

      bonus

.. seealso::

    `urllib2 <http://docs.python.org/library/urllib2.html>`_
        The standard library documentation for this module.

    :mod:`urllib`
        Original URL handling library.

    :mod:`urlparse`
        Work with the URL string itself.

    `urllib2 -- The Missing Manual <http://www.voidspace.org.uk/python/articles/urllib2.shtml>`_
        Michael Foord's write-up on using ``urllib2``.
    
    `Upload Scripts <http://www.voidspace.org.uk/python/cgi.shtml#upload>`_
        Example scripts from Michael Foord that illustrate how to upload a file
        using HTTP and then receive the data on the server.

    `HTTP client to POST using multipart/form-data <http://code.activestate.com/recipes/146306/>`_
        Python cookbook recipe showing how to encode and post data, including files,
        over HTTP.

    `Form content types <http://www.w3.org/TR/REC-html40/interact/forms.html#h-17.13.4>`_
        W3C specification for posting files or large amounts of data via HTTP forms.

    :mod:`mimetypes`
        Map filenames to mimetype.
    
    :mod:`mimetools`
        Tools for parsing MIME messages.
