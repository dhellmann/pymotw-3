============================================
 urllib.request --- Network Resource Access
============================================

.. module:: urllib.request
    :synopsis: Network Resource Access

:Purpose: A library for opening URLs that can be extended by defining
          custom protocol handlers.

The :mod:`urllib.request` module provides an API for using Internet
resources identified by URLs.  It is designed to be extended by
individual applications to support new protocols or add variations to
existing protocols (such as handling HTTP basic authentication).

HTTP GET
========

.. note::

    The test server for these examples is in ``http_server_GET.py``,
    from the examples for the :mod:`http.server` module. Start the
    server in one terminal window, then run these examples in another.

An HTTP GET operation is the simplest use of
:mod:`urllib.request`. Pass the URL to :func:`urlopen` to get a
"file-like" handle to the remote data.

.. literalinclude:: urllib2_urlopen.py
    :caption:
    :start-after: #end_pymotw_header

The example server accepts the incoming values and formats a plain
text response to send back. The return value from :func:`urlopen`
gives access to the headers from the HTTP server through the
:func:`info` method, and the data for the remote resource via
methods like :func:`read` and :func:`readlines`.

::

    $ python urllib2_urlopen.py

    RESPONSE: <addinfourl at 11940488 whose fp = <socket._fileobject 
    object at 0xb573f0>>
    URL     : http://localhost:8080/
    DATE    : Sun, 19 Jul 2009 14:01:31 GMT
    HEADERS :
    ---------
    Server: BaseHTTP/0.3 Python/2.6.2
    Date: Sun, 19 Jul 2009 14:01:31 GMT
    
    LENGTH  : 349
    DATA    :
    ---------
    CLIENT VALUES:
    client_address=('127.0.0.1', 55836) (localhost)
    command=GET
    path=/
    real path=/
    query=
    request_version=HTTP/1.1
    
    SERVER VALUES:
    server_version=BaseHTTP/0.3
    sys_version=Python/2.6.2
    protocol_version=HTTP/1.0
    
    HEADERS RECEIVED:
    accept-encoding=identity
    connection=close
    host=localhost:8080
    user-agent=Python-urllib/2.6
    

The file-like object returned by :func:`urlopen` is iterable:

.. literalinclude:: urllib2_urlopen_iterator.py
    :caption:
    :start-after: #end_pymotw_header

This example strips the trailing newlines and carriage returns before
printing the output.

::

    $ python urllib2_urlopen_iterator.py

    CLIENT VALUES:
    client_address=('127.0.0.1', 55840) (localhost)
    command=GET
    path=/
    real path=/
    query=
    request_version=HTTP/1.1
    
    SERVER VALUES:
    server_version=BaseHTTP/0.3
    sys_version=Python/2.6.2
    protocol_version=HTTP/1.0
    
    HEADERS RECEIVED:
    accept-encoding=identity
    connection=close
    host=localhost:8080
    user-agent=Python-urllib/2.6

Encoding Arguments
==================

Arguments can be passed to the server by encoding them with
:func:`urllib.parse.urlencode` and appending them to the URL.

.. literalinclude:: urllib2_http_get_args.py
    :caption:
    :start-after: #end_pymotw_header

The list of client values returned in the example output contains the
encoded query arguments.

::

    $ python urllib2_http_get_args.py

    Encoded: q=query+string&foo=bar
    CLIENT VALUES:
    client_address=('127.0.0.1', 55849) (localhost)
    command=GET
    path=/?q=query+string&foo=bar
    real path=/
    query=q=query+string&foo=bar
    request_version=HTTP/1.1
    
    SERVER VALUES:
    server_version=BaseHTTP/0.3
    sys_version=Python/2.6.2
    protocol_version=HTTP/1.0
    
    HEADERS RECEIVED:
    accept-encoding=identity
    connection=close
    host=localhost:8080
    user-agent=Python-urllib/2.6


HTTP POST
=========

.. note::

    The test server for these examples is in ``http_server_POST.py``,
    from the examples for the :mod:`http.server` module. Start the
    server in one terminal window, then run these examples in another.

To send form-encoded data to the remote server using POST instead GET,
pass the encoded query arguments as data to :func:`urlopen`.

.. literalinclude:: urllib2_urlopen_post.py
    :caption:
    :start-after: #end_pymotw_header

The server can decode the form data and access the individual values
by name.

::

    $ python urllib2_urlopen_post.py

    Client: ('127.0.0.1', 55943)
    User-agent: Python-urllib/2.6
    Path: /
    Form data:
    	q=query string
    	foo=bar


Adding Outgoing Headers
=======================

:func:`urlopen` is a convenience function that hides some of the
details of how the request is made and handled. More precise control
is possible by using a :class:`Request` instance directly.  For
example, custom headers can be added to the outgoing request to
control the format of data returned, specify the version of a document
cached locally, and tell the remote server the name of the software
client communicating with it.

.. warning:: needs attention

As the output from the earlier examples shows, the default
*User-agent* header value is made up of the constant
``Python-urllib``, followed by the Python interpreter version. When
creating an application that will access web resources owned by
someone else, it is courteous to include real user agent information
in the requests, so they can identify the source of the hits more
easily. Using a custom agent also allows them to control crawlers
using a ``robots.txt`` file (see the :mod:`robotparser` module).

.. literalinclude:: urllib2_request_header.py
    :caption:
    :start-after: #end_pymotw_header

After creating a :class:`Request` object, use :func:`add_header` to
set the user agent value before opening the request.  The last line of
the output shows the custom value.

::

    $ python urllib2_request_header.py

    CLIENT VALUES:
    client_address=('127.0.0.1', 55876) (localhost)
    command=GET
    path=/
    real path=/
    query=
    request_version=HTTP/1.1
    
    SERVER VALUES:
    server_version=BaseHTTP/0.3
    sys_version=Python/2.6.2
    protocol_version=HTTP/1.0
    
    HEADERS RECEIVED:
    accept-encoding=identity
    connection=close
    host=localhost:8080
    user-agent=PyMOTW (http://www.doughellmann.com/PyMOTW/)


Posting Form Data from a Request
================================

The outgoing data can be added to the :class:`Request` to have it
posted to the server.

.. literalinclude:: urllib2_request_post.py
    :caption:
    :start-after: #end_pymotw_header

The HTTP method used by the :class:`Request` changes from GET to POST
automatically after the data is added.

::

    $ python urllib2_request_post.py

    Request method before data: GET
    Request method after data : POST
    
    OUTGOING DATA:
    q=query+string&foo=bar
    
    SERVER RESPONSE:
    Client: ('127.0.0.1', 56044)
    User-agent: PyMOTW (http://www.doughellmann.com/PyMOTW/)
    Path: /
    Form data:
    	q=query string
    	foo=bar
    
.. note::

    Although the method is :func:`add_data`, its effect is *not*
    cumulative.  Each call replaces the previous data.


Uploading Files
===============

Encoding files for upload requires a little more work than simple
forms.  A complete MIME message needs to be constructed in the body of
the request, so that the server can distinguish incoming form fields
from uploaded files.

.. literalinclude:: urllib2_upload_files.py
    :caption:
    :start-after: #end_pymotw_header

The :class:`MultiPartForm` class can represent an arbitrary form as a
multi-part MIME message with attached files.

::

    $ python urllib2_upload_files.py
    
    OUTGOING DATA:
    --192.168.1.17.527.30074.1248020372.206.1
    Content-Disposition: form-data; name="firstname"
    
    Doug
    --192.168.1.17.527.30074.1248020372.206.1
    Content-Disposition: form-data; name="lastname"
    
    Hellmann
    --192.168.1.17.527.30074.1248020372.206.1
    Content-Disposition: file; name="biography"; filename="bio.txt"
    Content-Type: text/plain
    
    Python developer and blogger.
    --192.168.1.17.527.30074.1248020372.206.1--
    
    
    SERVER RESPONSE:
    Client: ('127.0.0.1', 57126)
    User-agent: PyMOTW (http://www.doughellmann.com/PyMOTW/)
    Path: /
    Form data:
    	lastname=Hellmann
    	Uploaded biography as "bio.txt" (29 bytes)
    	firstname=Doug
    

Creating Custom Protocol Handlers
=================================

:mod:`urllib.request` has built-in support for HTTP(S), FTP, and local
file access. To add support for other URL types, register another
protocol handler. For example, to support URLs pointing to arbitrary
files on remote NFS servers, without requiring users to mount the path
before accessing the file, create a class derived from
:class:`BaseHandler` and with a method :func:`nfs_open`.

The protocol-specific :func:`open` method is given a single argument, the
:class:`Request` instance, and it should return an object with a
:func:`read` method that can be used to read the data, an
:func:`info` method to return the response headers, and
:func:`geturl` to return the actual URL of the file being read. A
simple way to achieve that is to create an instance of
:class:`urllib.addurlinfo`, passing the headers, URL, and open file
handle in to the constructor.

.. literalinclude:: urllib2_nfs_handler.py
    :caption:
    :start-after: #end_pymotw_header

The :class:`FauxNFSHandler` and :class:`NFSFile` classes print
messages to illustrate where a real implementation would add mount and
unmount calls. Since this is just a simulation,
:class:`FauxNFSHandler` is primed with the name of a temporary
directory where it should look for all of its files.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'urllib2_nfs_handler.py'))
.. }}}

::

	$ python urllib2_nfs_handler.py

	FauxNFSHandler simulating mount:
	  Remote path: /path/to/the
	  Server     : remote_server
	  Local path : tmpoqqoAV
	  Filename   : file.txt
	
	READ CONTENTS: Contents of file.txt
	URL          : nfs://remote_server/path/to/the/file.txt
	HEADERS:
	  Content-length  = 20
	  Content-type    = text/plain
	NFSFile:
	  unmounting tmpoqqoAV
	  when file.txt is closed

.. {{{end}}}


.. seealso::

   * :pydoc:`urllib.request`

   * :mod:`urllib.parse` -- Work with the URL string itself.

   * `Form content types
     <http://www.w3.org/TR/REC-html40/interact/forms.html#h-17.13.4>`_
     -- W3C specification for posting files or large amounts of data
     via HTTP forms.

   * :mod:`mimetypes` -- Map filenames to mimetype.

   * :mod:`mimetools` -- Tools for parsing MIME messages.
