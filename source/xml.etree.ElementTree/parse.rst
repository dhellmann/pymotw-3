.. _xml.etree.ElementTree.parsing:

Parsing an XML Document
=======================

Parsed XML documents are represented in memory by :class:`ElementTree`
and :class:`Element` objects connected in a tree structure based on
the way the nodes in the XML document are nested.

Parsing an entire document with :func:`parse()` returns an
:class:`ElementTree` instance.  The tree knows about all of the data
in the input document, and the nodes of the tree can be searched or
manipulated in place.  While this flexibility can make working with
the parsed document more convenient, it typically takes more memory
than an event-based parsing approach since the entire document must be
loaded at one time.

The memory footprint of small, simple documents such as this list of
podcasts represented as an OPML outline is not significant:

.. literalinclude:: podcasts.opml
   :language: xml

To parse the file, pass an open file handle to :func:`parse()`.

.. include:: ElementTree_parse_opml.py
   :literal:
   :start-after: #end_pymotw_header

It will read the data, parse the XML, and return an
:class:`ElementTree` object.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ElementTree_parse_opml.py'))
.. }}}

::

    $ python ElementTree_parse_opml.py
    
    <xml.etree.ElementTree.ElementTree object at 0x100dca350>

.. {{{end}}}

Traversing the Parsed Tree
==========================

To visit all of the children in order, use :func:`iter` to create a
generator that iterates over the :class:`ElementTree` instance.

.. include:: ElementTree_dump_opml.py
   :literal:
   :start-after: #end_pymotw_header

This example prints the entire tree, one tag at a time.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ElementTree_dump_opml.py'))
.. }}}

::

    $ python ElementTree_dump_opml.py
    
    opml
    head
    title
    dateCreated
    dateModified
    body
    outline
    outline
    outline
    outline
    outline

.. {{{end}}}

To print only the groups of names and feed URLs for the podcasts,
leaving out of all of the data in the header section by iterating over
only the ``outline`` nodes and print the *text* and *xmlUrl*
attributes by looking up the values in the :attr:`attrib`
dictionary.

.. include:: ElementTree_show_feed_urls.py
   :literal:
   :start-after: #end_pymotw_header

The ``'outline'`` argument to :func:`iter` means processing is limited
to only nodes with the tag ``'outline'``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ElementTree_show_feed_urls.py'))
.. }}}

::

    $ python ElementTree_show_feed_urls.py
    
    Fiction
      tor.com / category / tordotstories
        http://www.tor.com/rss/category/TorDotStories
    Python
      PyCon Podcast
        http://advocacy.python.org/podcasts/pycon.rss
      A Little Bit of Python
        http://advocacy.python.org/podcasts/littlebit.rss

.. {{{end}}}

Finding Nodes in a Document
===========================

Walking the entire tree like this, searching for relevant nodes, can
be error prone.  The previous example had to look at each outline node
to determine if it was a group (nodes with only a :attr:`text`
attribute) or podcast (with both :attr:`text` and :attr:`xmlUrl`).  To
produce a simple list of the podcast feed URLs, without names or
groups, the logic could be simplified using :func:`findall()` to look
for nodes with more descriptive search characteristics.

As a first pass at converting the first version, an XPath argument
can be used to look for all outline nodes.

.. include:: ElementTree_find_feeds_by_tag.py
   :literal:
   :start-after: #end_pymotw_header

The logic in this version is not substantially different than the
version using :func:`getiterator()`.  It still has to check for the
presence of the URL, except that it does not print the group name when
the URL is not found.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ElementTree_find_feeds_by_tag.py'))
.. }}}

::

    $ python ElementTree_find_feeds_by_tag.py
    
    http://www.tor.com/rss/category/TorDotStories
    http://advocacy.python.org/podcasts/pycon.rss
    http://advocacy.python.org/podcasts/littlebit.rss

.. {{{end}}}

It is possible to take advantage of the fact that the outline nodes
are only nested two levels deep.  Changing the search path to
``.//outline/outline`` means the loop will process only the second
level of outline nodes.

.. include:: ElementTree_find_feeds_by_structure.py
   :literal:
   :start-after: #end_pymotw_header

All of the outline nodes nested two levels deep in the input are
expected to have the *xmlURL* attribute referring to the podcast feed,
so the loop can skip checking for the attribute before using it.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ElementTree_find_feeds_by_structure.py'))
.. }}}

::

    $ python ElementTree_find_feeds_by_structure.py
    
    http://www.tor.com/rss/category/TorDotStories
    http://advocacy.python.org/podcasts/pycon.rss
    http://advocacy.python.org/podcasts/littlebit.rss

.. {{{end}}}

This version is limited to the existing structure, though, so if the
outline nodes are ever rearranged into a deeper tree, it will stop
working.

Parsed Node Attributes
======================

The items returned by :func:`findall()` and :func:`iter()` are
:class:`Element` objects, each representing a node in the XML parse
tree.  Each :class:`Element` has attributes for accessing data pulled
out of the XML.  This can be illustrated with a somewhat more
contrived example input file, ``data.xml``.

.. literalinclude:: data.xml
   :language: xml
   :linenos:

The *attributes* of a node are available in the :attr:`attrib`
property, which acts like a dictionary.

.. include:: ElementTree_node_attributes.py
   :literal:
   :start-after: #end_pymotw_header

The node on line five of the input file has two attributes,
:attr:`name` and :attr:`foo`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ElementTree_node_attributes.py'))
.. }}}

::

    $ python ElementTree_node_attributes.py
    
    with_attributes
      foo  = "bar"
      name = "value"

.. {{{end}}}

The text content of the nodes is available, along with the *tail* text
that comes after the end of a close tag.

.. include:: ElementTree_node_text.py
   :literal:
   :start-after: #end_pymotw_header

The ``child`` node on line three contains embedded text, and the node
on line four has text with a tail (including whitespace).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ElementTree_node_text.py'))
.. }}}

::

    $ python ElementTree_node_text.py
    
    child
      child node text: Regular text.
      and tail text  : 
      
    child_with_tail
      child node text: Regular text.
      and tail text  : "Tail" text.
      

.. {{{end}}}

XML entity references embedded in the document are converted to the
appropriate characters before values are returned.

.. include:: ElementTree_entity_references.py
   :literal:
   :start-after: #end_pymotw_header

The automatic conversion means the implementation detail of
representing certain characters in an XML document can be ignored.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ElementTree_entity_references.py'))
.. }}}

::

    $ python ElementTree_entity_references.py
    
    entity_expansion
      in attribute: This & That
      in text     : That & This

.. {{{end}}}


Watching Events While Parsing
=============================

The other API for processing XML documents is event-based.  The
parser generates ``start`` events for opening tags and ``end`` events
for closing tags.  Data can be extracted from the document during the
parsing phase by iterating over the event stream, which is convenient
if it is not necessary to manipulate the entire document afterwards
and there is no need to hold the entire parsed document in memory.

Events can be one of:

``start``
  A new tag has been encountered.  The closing angle bracket of the
  tag was processed, but not the contents.
``end``
  The closing angle bracket of a closing tag has been processed.  All
  of the children were already processed.
``start-ns``
  Start a namespace declaration.
``end-ns``
  End a namespace declaration.

:func:`iterparse()` returns an iterable that produces tuples
containing the name of the event and the node triggering the event.

.. include:: ElementTree_show_all_events.py
   :literal:
   :start-after: #end_pymotw_header

By default, only ``end`` events are generated.  To see other events,
pass the list of desired event names to :func:`iterparse()`, as in
this example.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ElementTree_show_all_events.py'))
.. }}}

::

    $ python ElementTree_show_all_events.py
    
    start            opml         4309429072
    ..start          head         4309429136
    ....start        title        4309429200
    ....end          title        4309429200
    ....start        dateCreated  4309429392
    ....end          dateCreated  4309429392
    ....start        dateModified 4309429584
    ....end          dateModified 4309429584
    ..end            head         4309429136
    ..start          body         4309429968
    ....start        outline      4309430032
    ......start      outline      4309430096
    ......end        outline      4309430096
    ....end          outline      4309430032
    ....start        outline      4309430160
    ......start      outline      4309430224
    ......end        outline      4309430224
    ......start      outline      4309459024
    ......end        outline      4309459024
    ....end          outline      4309430160
    ..end            body         4309429968
    end              opml         4309429072

.. {{{end}}}

The event-style of processing is more natural for some operations,
such as converting XML input to some other format.  This technique can
be used to convert list of podcasts from the earlier examples from an
XML file to a CSV file, so they can be loaded into a spreadsheet or
database application.

.. include:: ElementTree_write_podcast_csv.py
   :literal:
   :start-after: #end_pymotw_header

This conversion program does not need to hold the entire parsed input
file in memory, and processing each node as it is encountered in the
input is more efficient.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ElementTree_write_podcast_csv.py', 
..         break_lines_at=68, line_break_mode='continue'))
.. }}}

::

    $ python ElementTree_write_podcast_csv.py
    
    "Fiction","tor.com / category / tordotstories","http://www.tor.com/r\
    ss/category/TorDotStories","http://www.tor.com/"
    "Python","PyCon Podcast","http://advocacy.python.org/podcasts/pycon.\
    rss","http://advocacy.python.org/podcasts/"
    "Python","A Little Bit of Python","http://advocacy.python.org/podcas\
    ts/littlebit.rss","http://advocacy.python.org/podcasts/"

.. {{{end}}}

.. note::

  The output from ``ElementTree_write_podcast_csv.py`` has been
  reformatted to fit on this page.  The output lines ending with
  ``\`` indicate an artificial line break.

Creating a Custom Tree Builder
==============================

A potentially more efficient means of handling parse events is to
replace the standard tree builder behavior with a custom version.  The
:class:`ElementTree` parser uses an :class:`XMLTreeBuilder` to process
the XML and call methods on a target class to save the results.  The
usual output is an :class:`ElementTree` instance created by the
default :class:`TreeBuilder` class.  Replacing :class:`TreeBuilder`
with another class allows it to receive the events before the
:class:`Element` nodes are instantiated, saving that portion of the
overhead.

The XML-to-CSV converter from the previous section can be
re-implemented as a tree builder.

.. include:: ElementTree_podcast_csv_treebuilder.py
   :literal:
   :start-after: #end_pymotw_header

:class:`PodcastListToCSV` implements the :class:`TreeBuilder`
protocol.  Each time a new XML tag is encountered, :func:`start()` is
called with the tag name and attributes.  When a closing tag is seen
:func:`end()` is called with the name.  In between, :func:`data()` is
called when a node has content (the tree builder is expected to keep
up with the "current" node).  When all of the input is processed,
:func:`close()` is called.  It can return a value, which will be
returned to the user of the :class:`XMLTreeBuilder`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ElementTree_podcast_csv_treebuilder.py', 
..                    break_lines_at=68, line_break_mode='continue'))
.. }}}

::

    $ python ElementTree_podcast_csv_treebuilder.py
    
    "Fiction","tor.com / category / tordotstories","http://www.tor.com/r\
    ss/category/TorDotStories","http://www.tor.com/"
    "Python","PyCon Podcast","http://advocacy.python.org/podcasts/pycon.\
    rss","http://advocacy.python.org/podcasts/"
    "Python","A Little Bit of Python","http://advocacy.python.org/podcas\
    ts/littlebit.rss","http://advocacy.python.org/podcasts/"

.. {{{end}}}


.. note::

  The output from ``ElementTree_podcast_csv_treebuidler.py`` has been
  reformatted to fit on this page.  The output lines ending with
  ``\`` indicate an artificial line break.


Parsing Strings
===============

To work with smaller bits of XML text, especially string literals that
might be embedded in the source of a program, use :func:`XML()` and
the string containing the XML to be parsed as the only argument.

.. include:: ElementTree_XML.py
   :literal:
   :start-after: #end_pymotw_header

Unlike with :func:`parse()`, the return value is an
:class:`Element` instance instead of an :class:`ElementTree`.  An
:class:`Element` supports the iterator protocol directly, so there is
no need to call :func:`getiterator`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ElementTree_XML.py'))
.. }}}

::

    $ python ElementTree_XML.py
    
    parsed = <Element 'root' at 0x100dcba50>
    group
    child
      text: "This is child "a"."
      id   = "a"
    child
      text: "This is child "b"."
      id   = "b"
    group
    child
      text: "This is child "c"."
      id   = "c"

.. {{{end}}}

For structured XML that uses the :attr:`id` attribute to identify
unique nodes of interest, :func:`XMLID()` is a convenient way to
access the parse results.

.. include:: ElementTree_XMLID.py
   :literal:
   :start-after: #end_pymotw_header

:func:`XMLID()` returns the parsed tree as an :class:`Element` object,
along with a dictionary mapping the :attr:`id` attribute strings to
the individual nodes in the tree.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'ElementTree_XMLID.py'))
.. }}}

::

    $ python ElementTree_XMLID.py
    
    a = <Element 'child' at 0x100dcab90>
    b = <Element 'child' at 0x100dcac50>
    c = <Element 'child' at 0x100dcae90>

.. {{{end}}}


.. seealso::

   Outline Processor Markup Language, OPML_
       Dave Winer's OPML specification and documentation.

   XML Path Language, XPath_
       A syntax for identifying parts of an XML document.

   `XPath Support in ElementTree <http://effbot.org/zone/element-xpath.htm>`_
       Part of Fredrick Lundh's original documentation for ElementTree.

   :mod:`csv`
       Read and write comma-separated-value files

.. _OPML: http://www.opml.org/

.. _XPath: http://www.w3.org/TR/xpath/
