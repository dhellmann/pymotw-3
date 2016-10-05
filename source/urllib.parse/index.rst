=============================================
 urllib.parse --- Split URLs into Components
=============================================

.. module:: urllib.parse
    :synopsis: Split URL into components

:Purpose: Split URL into components

The :mod:`urllib.parse` module provides functions for breaking URLs
down into their component parts, as defined by the relevant RFCs.

Parsing
=======

The return value from the :func:`urlparse` function is an object
that acts like a :class:`tuple` with six elements.

.. literalinclude:: urllib_parse_urlparse.py
    :caption:
    :start-after: #end_pymotw_header

The parts of the URL available through the tuple interface are the
scheme, network location, path, path segment parameters (separated
from the path by a semicolon), query, and fragment.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'urllib_parse_urlparse.py', 
..                    break_lines_at=68, line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python urllib_parse_urlparse.py
	
	ParseResult(scheme='http', netloc='netloc', path='/path',
	params='param', query='query=arg', fragment='frag')

.. {{{end}}}

Although the return value acts like a tuple, it is really based on a
:class:`namedtuple`, a subclass of :class:`tuple` that supports
accessing the parts of the URL via named attributes as well as
indexes.  In addition to being easier to use for the programmer, the
attribute API also offers access to several values not available in
the :class:`tuple` API.

.. literalinclude:: urllib_parse_urlparseattrs.py
    :caption:
    :start-after: #end_pymotw_header

The *username* and *password* are available when present in the input
URL, and set to ``None`` when not. The *hostname* is the same value as
*netloc*, in all lower case.  And the *port* is converted to an
integer when present and ``None`` when not.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'urllib_parse_urlparseattrs.py'))
.. }}}

.. code-block:: none

	$ python urllib_parse_urlparseattrs.py
	
	scheme  : http
	netloc  : user:pwd@NetLoc:80
	path    : /path
	params  : param
	query   : query=arg
	fragment: frag
	username: user
	password: pwd
	hostname: netloc (netloc in lowercase)
	port    : 80

.. {{{end}}}

The :func:`urlsplit` function is an alternative to
:func:`urlparse`. It behaves a little differently, because it does not
split the parameters from the URL. This is useful for URLs following
RFC 2396, which supports parameters for each segment of the path.

.. literalinclude:: urllib_parse_urlsplit.py
    :caption:
    :start-after: #end_pymotw_header

Since the parameters are not split out, the tuple API will show five
elements instead of six, and there is no *params* attribute.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'urllib_parse_urlsplit.py', 
..                    break_lines_at=68, line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python urllib_parse_urlsplit.py
	
	SplitResult(scheme='http', netloc='user:pwd@NetLoc:80',
	path='/p1;param/p2;param', query='query=arg', fragment='frag')
	scheme  : http
	netloc  : user:pwd@NetLoc:80
	path    : /p1;param/p2;param
	query   : query=arg
	fragment: frag
	username: user
	password: pwd
	hostname: netloc (netloc in lowercase)
	port    : 80

.. {{{end}}}

To simply strip the fragment identifier from a URL, such as when
finding a base page name from a URL, use :func:`urldefrag`.

.. literalinclude:: urllib_parse_urldefrag.py
    :caption:
    :start-after: #end_pymotw_header

The return value is a tuple containing the base URL and the fragment.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'urllib_parse_urldefrag.py'))
.. }}}

.. code-block:: none

	$ python urllib_parse_urldefrag.py
	
	original: http://netloc/path;param?query=arg#frag
	url     : http://netloc/path;param?query=arg
	fragment: frag

.. {{{end}}}

Unparsing
=========

There are several ways to assemble the parts of a split URL back
together into a single string. The parsed URL object has a
:func:`geturl` method.

.. literalinclude:: urllib_parse_geturl.py
    :caption:
    :start-after: #end_pymotw_header

:func:`geturl` only works on the object returned by
:func:`urlparse` or :func:`urlsplit`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'urllib_parse_geturl.py'))
.. }}}

.. code-block:: none

	$ python urllib_parse_geturl.py
	
	ORIG  : http://netloc/path;param?query=arg#frag
	PARSED: http://netloc/path;param?query=arg#frag

.. {{{end}}}

A regular tuple containing strings can be combined into a URL with
:func:`urlunparse`.

.. literalinclude:: urllib_parse_urlunparse.py
    :caption:
    :start-after: #end_pymotw_header

While the :class:`ParseResult` returned by :func:`urlparse` can be
used as a tuple, this example explicitly creates a new tuple to show
that :func:`urlunparse` works with normal tuples, too.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'urllib_parse_urlunparse.py', 
..                    break_lines_at=68, line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python urllib_parse_urlunparse.py
	
	ORIG  : http://netloc/path;param?query=arg#frag
	PARSED: <class 'urlparse.ParseResult'> ParseResult(scheme='http',
	netloc='netloc', path='/path', params='param', query='query=arg',
	fragment='frag')
	TUPLE : <type 'tuple'> ('http', 'netloc', '/path', 'param',
	'query=arg', 'frag')
	NEW   : http://netloc/path;param?query=arg#frag

.. {{{end}}}

If the input URL included superfluous parts, those may be dropped from the
reconstructed URL.

.. literalinclude:: urllib_parse_urlunparseextra.py
    :caption:
    :start-after: #end_pymotw_header

In this case, *parameters*, *query*, and *fragment* are all
missing in the original URL. The new URL does not look the same as the
original, but is equivalent according to the standard.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'urllib_parse_urlunparseextra.py', 
..                    break_lines_at=68, line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python urllib_parse_urlunparseextra.py
	
	ORIG  : http://netloc/path;?#
	PARSED: <class 'urlparse.ParseResult'> ParseResult(scheme='http',
	netloc='netloc', path='/path', params='', query='', fragment='')
	TUPLE : <type 'tuple'> ('http', 'netloc', '/path', '', '', '')
	NEW   : http://netloc/path

.. {{{end}}}

Joining
=======

In addition to parsing URLs, :mod:`urlparse` includes
:func:`urljoin` for constructing absolute URLs from relative
fragments.

.. literalinclude:: urllib_parse_urljoin.py
    :caption:
    :start-after: #end_pymotw_header

In the example, the relative portion of the path (``"../"``) is taken
into account when the second URL is computed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'urllib_parse_urljoin.py'))
.. }}}

.. code-block:: none

	$ python urllib_parse_urljoin.py
	
	http://www.example.com/path/anotherfile.html
	http://www.example.com/anotherfile.html

.. {{{end}}}

Non-relative paths are handled in the same way as by
:func:`os.path.join`.

.. literalinclude:: urllib_parse_urljoin_with_path.py
   :caption:
   :start-after: #end_pymotw_header

If the path being joined to the URL starts with a slash (``/``), it
resets the URL's path to the top level.  If it does not start with a
slash, it is appended to the end of the path for the URL.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'urllib_parse_urljoin_with_path.py'))
.. }}}

.. code-block:: none

	$ python urllib_parse_urljoin_with_path.py
	
	http://www.example.com/subpath/file.html
	http://www.example.com/path/subpath/file.html

.. {{{end}}}



.. seealso::

   * :pydoc:`urllib.parse`

   * :mod:`urllib.request` -- Retrieve the contents of a resource
     identified by a URL.

   * :rfc:`1738` -- Uniform Resource Locator (URL) syntax

   * :rfc:`1808` -- Relative URLs

   * :rfc:`2396` -- Uniform Resource Identifier (URI) generic syntax

   * :rfc:`3986` -- Uniform Resource Identifier (URI) syntax

