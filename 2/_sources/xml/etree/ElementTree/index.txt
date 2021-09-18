=============================================
xml.etree.ElementTree -- XML Manipulation API
=============================================

.. module:: xml.etree.ElementTree
    :synopsis: XML Manipulation API

:Purpose: Generate and parse XML documents
:Python Version: 2.5 and later

The ElementTree library was contributed to the standard library by
Fredrick Lundh.  It includes tools for parsing XML using event-based
and document-based APIs, searching parsed documents with XPath
expressions, and creating new or modifying existing documents.

.. note::

  All of the examples in this section use the Python implementation of
  ElementTree for simplicity, but there is also a C implementation in
  :mod:`xml.etree.cElementTree`.

.. toctree::

   parse
   create


.. seealso::

    `xml.etree.ElementTree <http://docs.python.org/library/xml.etree.elementtree.html>`_
        The standard library documentation for this module.

    `ElementTree Overview <http://effbot.org/zone/element-index.htm>`_
        Fredrick Lundh's original documentation and links to the
        development versions of the ElementTree library.

    `Process XML in Python with ElementTree <http://www.ibm.com/developerworks/library/x-matters28/>`_
        IBM DeveloperWorks article by David Mertz.

    `lxml.etree <http://codespeak.net/lxml/>`_
        A separate implementation of the ElementTree API based on libxml2 with more complete XPath support.
