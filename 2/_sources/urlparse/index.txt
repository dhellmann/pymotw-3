============================================
urlparse -- Split URL into component pieces.
============================================

.. module:: urlparse
    :synopsis: Split URL into component pieces.

:Purpose: Split URL into component pieces.
:Available In: since 1.4

The :mod:`urlparse` module provides functions for breaking URLs down
into their component parts, as defined by the relevant RFCs.

Parsing
=======

The return value from the :func:`urlparse()` function is an object
which acts like a tuple with 6 elements.

.. include:: urlparse_urlparse.py
    :literal:
    :start-after: #end_pymotw_header

The parts of the URL available through the tuple interface are the scheme,
network location, path, parameters, query, and fragment.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'urlparse_urlparse.py'))
.. }}}

::

	$ python urlparse_urlparse.py
	
	ParseResult(scheme='http', netloc='netloc', path='/path', params='parameters', query='query=argument', fragment='fragment')

.. {{{end}}}


Although the return value acts like a tuple, it is really based on a
:ref:`namedtuple <collections-namedtuple>`, a subclass of tuple that
supports accessing the parts of the URL via named attributes instead
of indexes. That's especially useful if, like me, you can't remember
the index order. In addition to being easier to use for the
programmer, the attribute API also offers access to several values not
available in the tuple API.

.. include:: urlparse_urlparseattrs.py
    :literal:
    :start-after: #end_pymotw_header

The *username* and *password* are available when present in the input
URL and ``None`` when not. The *hostname* is the same value as
*netloc*, in all lower case.  And the *port* is converted to an
integer when present and ``None`` when not.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'urlparse_urlparseattrs.py'))
.. }}}

::

	$ python urlparse_urlparseattrs.py
	
	scheme  : http
	netloc  : user:pass@NetLoc:80
	path    : /path
	params  : parameters
	query   : query=argument
	fragment: fragment
	username: user
	password: pass
	hostname: netloc (netloc in lower case)
	port    : 80

.. {{{end}}}

The :func:`urlsplit()` function is an alternative to
:func:`urlparse()`. It behaves a little different, because it does not
split the parameters from the URL. This is useful for URLs following
:rfc:`2396`, which supports parameters for each segment of the path.

.. include:: urlparse_urlsplit.py
    :literal:
    :start-after: #end_pymotw_header

Since the parameters are not split out, the tuple API will show 5
elements instead of 6, and there is no *params* attribute.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'urlparse_urlsplit.py'))
.. }}}

::

	$ python urlparse_urlsplit.py
	
	SplitResult(scheme='http', netloc='user:pass@NetLoc:80', path='/path;parameters/path2;parameters2', query='query=argument', fragment='fragment')
	scheme  : http
	netloc  : user:pass@NetLoc:80
	path    : /path;parameters/path2;parameters2
	query   : query=argument
	fragment: fragment
	username: user
	password: pass
	hostname: netloc (netloc in lower case)
	port    : 80

.. {{{end}}}

To simply strip the fragment identifier from a URL, as you might need
to do to find a base page name from a URL, use :func:`urldefrag()`.

.. include:: urlparse_urldefrag.py
    :literal:
    :start-after: #end_pymotw_header

The return value is a tuple containing the base URL and the fragment.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'urlparse_urldefrag.py'))
.. }}}

::

	$ python urlparse_urldefrag.py
	
	http://netloc/path;parameters?query=argument#fragment
	http://netloc/path;parameters?query=argument
	fragment

.. {{{end}}}

Unparsing
=========

There are several ways to assemble a split URL back together into a
single string. The parsed URL object has a :func:`geturl()` method.

.. include:: urlparse_geturl.py
    :literal:
    :start-after: #end_pymotw_header

:func:`geturl()` only works on the object returned by
:func:`urlparse()` or :func:`urlsplit()`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'urlparse_geturl.py'))
.. }}}

::

	$ python urlparse_geturl.py
	
	ORIG  : http://netloc/path;parameters?query=argument#fragment
	PARSED: http://netloc/path;parameters?query=argument#fragment

.. {{{end}}}

If you have a regular tuple of values, you can use
:func:`urlunparse()` to combine them into a URL.

.. include:: urlparse_urlunparse.py
    :literal:
    :start-after: #end_pymotw_header

While the :class:`ParseResult` returned by :func:`urlparse()` can be
used as a tuple, in this example I explicitly create a new tuple to
show that :func:`urlunparse()` works with normal tuples, too.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'urlparse_urlunparse.py'))
.. }}}

::

	$ python urlparse_urlunparse.py
	
	ORIG  : http://netloc/path;parameters?query=argument#fragment
	PARSED: <class 'urlparse.ParseResult'> ParseResult(scheme='http', netloc='netloc', path='/path', params='parameters', query='query=argument', fragment='fragment')
	TUPLE : <type 'tuple'> ('http', 'netloc', '/path', 'parameters', 'query=argument', 'fragment')
	NEW   : http://netloc/path;parameters?query=argument#fragment

.. {{{end}}}

If the input URL included superfluous parts, those may be dropped from the
unparsed version of the URL.

.. include:: urlparse_urlunparseextra.py
    :literal:
    :start-after: #end_pymotw_header

In this case, the *parameters*, *query*, and *fragment* are all
missing in the original URL. The new URL does not look the same as the
original, but is equivalent according to the standard.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'urlparse_urlunparseextra.py'))
.. }}}

::

	$ python urlparse_urlunparseextra.py
	
	ORIG  : http://netloc/path;?#
	PARSED: <class 'urlparse.ParseResult'> ParseResult(scheme='http', netloc='netloc', path='/path', params='', query='', fragment='')
	TUPLE : <type 'tuple'> ('http', 'netloc', '/path', '', '', '')
	NEW   : http://netloc/path

.. {{{end}}}

Joining
=======

In addition to parsing URLs, :mod:`urlparse` includes
:func:`urljoin()` for constructing absolute URLs from relative
fragments.

.. include:: urlparse_urljoin.py
    :literal:
    :start-after: #end_pymotw_header

In the example, the relative portion of the path (``"../"``) is taken
into account when the second URL is computed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'urlparse_urljoin.py'))
.. }}}

::

	$ python urlparse_urljoin.py
	
	http://www.example.com/path/anotherfile.html
	http://www.example.com/anotherfile.html

.. {{{end}}}

.. seealso::

    `urlparse <https://docs.python.org/2/library/urlparse.html>`_
        Standard library documentation for this module.

    :mod:`urllib`
        Retrieve the contents of a resource identified by a URL.

    :mod:`urllib2`
        Alternative API for accessing remote URLs.
