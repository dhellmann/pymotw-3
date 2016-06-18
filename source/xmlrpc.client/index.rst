==============================================
 xmlrpc.client --- Client Library for XML-RPC
==============================================

.. module:: xmlrpc.client
    :synopsis: Client library for XML-RPC

:Purpose: Client-side library for XML-RPC communication.

XML-RPC is a lightweight remote procedure call protocol built on top
of HTTP and XML.  The :mod:`xmlrpclib` module lets a Python program
communicate with an XML-RPC server written in any language.

All of the examples in this section use the server defined in
``xmlrpc_server.py``, available in the source distribution and
included here for reference:

.. literalinclude:: xmlrpc_server.py
   :caption:
   :start-after: #end_pymotw_header

Connecting to a Server
======================

The simplest way to connect a client to a server is to instantiate a
:class:`ServerProxy` object, giving it the URI of the server. For
example, the demo server runs on port 9000 of localhost:

.. literalinclude:: xmlrpc_ServerProxy.py
   :caption:
   :start-after: #end_pymotw_header

In this case, the :func:`ping()` method of the service takes no
arguments and returns a single boolean value.

::

    $ python3 xmlrpc_ServerProxy.py

    Ping: True

Other options are available to support alternate transport. Both HTTP
and HTTPS are supported out of the box, both with basic
authentication. To implement a new communication channel, only a new
transport class is needed.  It could be an interesting exercise, for
example, to implement XML-RPC over SMTP.

.. literalinclude:: xmlrpc_ServerProxy_verbose.py
   :caption:
   :start-after: #end_pymotw_header

The *verbose* option gives debugging information useful for resolving
communication errors.

::

    $ python3 xmlrpc_ServerProxy_verbose.py

    send: b'POST /RPC2 HTTP/1.1\r\nHost: localhost:9000\r\n
    Accept-Encoding: gzip\r\nContent-Type: text/xml\r\n
    User-Agent: Python-xmlrpc/3.5\r\nContent-Length: 98\r\n\r\n'
    send: b"<?xml version='1.0'?>\n<methodCall>\n<methodName>
    ping</methodName>\n<params>\n</params>\n</methodCall>\n"
    reply: 'HTTP/1.0 200 OK\r\n'
    header: Server header: Date header: Content-type header:
    Content-length body: b"<?xml version='1.0'?>\n<methodResponse>\n
    <params>\n<param>\n<value><boolean>1</boolean></value>\n</param>
    \n</params>\n</methodResponse>\n"
    Ping: True

The default encoding can be changed from UTF-8 if an alternate system
is needed.

.. literalinclude:: xmlrpc_ServerProxy_encoding.py
   :caption:
   :start-after: #end_pymotw_header

The server automatically detects the correct encoding.

::

    $ python3 xmlrpc_ServerProxy_encoding.py

    Ping: True


The *allow_none* option controls whether Python's ``None`` value is
automatically translated to a nil value or if it causes an error.

.. literalinclude:: xmlrpc_ServerProxy_allow_none.py
   :caption:
   :start-after: #end_pymotw_header

The error is raised locally if the client does not allow ``None``, but
can also be raised from within the server if it is not configured to
allow ``None``.

::

    $ python3 xmlrpc_ServerProxy_allow_none.py

    Allowed: ['None', "<type 'NoneType'>", None]
    ERROR: cannot marshal None unless allow_none is enabled


Data Types
==========

The XML-RPC protocol recognizes a limited set of common data
types. The types can be passed as arguments or return values and
combined to create more complex data structures.

.. literalinclude:: xmlrpc_types.py
   :caption:
   :start-after: #end_pymotw_header


The simple types are

.. {{{cog
.. cog.out(run_script(cog.inFile, 'xmlrpc_types.py'))
.. }}}

::

	$ python3 xmlrpc_types.py
	
	boolean     : True
	              <class 'bool'>
	              True
	integer     : 1
	              <class 'int'>
	              1
	float       : 2.5
	              <class 'float'>
	              2.5
	string      : some text
	              <class 'str'>
	              some text
	datetime    : 20160618T17:16:23
	              <class 'xmlrpc.client.DateTime'>
	              20160618T17:16:23
	array       : ['a', 'list']
	              <class 'list'>
	              ['a', 'list']
	array       : ['a', 'tuple']
	              <class 'list'>
	              ['a', 'tuple']
	structure   : {'a': 'dictionary'}
	              <class 'dict'>
	              {'a': 'dictionary'}

.. {{{end}}}

The supported types can be nested to create values of arbitrary
complexity.

.. literalinclude:: xmlrpc_types_nested.py
   :caption:
   :start-after: #end_pymotw_header

This program passes a list of dictionaries containing all of the
supported types to the sample server, which returns the data.  Tuples
are converted to lists and :class:`datetime` instances are converted
to :class:`DateTime` objects, but otherwise the data is unchanged.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'xmlrpc_types_nested.py'))
.. }}}

::

	$ python3 xmlrpc_types_nested.py
	
	Before:
	[{'array': ('a', 'tuple'),
	  'boolean': True,
	  'datetime': datetime.datetime(2016, 6, 18, 17, 16, 23, 652391)
	,
	  'floating-point number': 2.5,
	  'integer': 0,
	  'string': 'some text',
	  'structure': {'a': 'dictionary'}},
	 {'array': ('a', 'tuple'),
	  'boolean': True,
	  'datetime': datetime.datetime(2016, 6, 18, 17, 16, 23, 652391)
	,
	  'floating-point number': 2.5,
	  'integer': 1,
	  'string': 'some text',
	  'structure': {'a': 'dictionary'}},
	 {'array': ('a', 'tuple'),
	  'boolean': True,
	  'datetime': datetime.datetime(2016, 6, 18, 17, 16, 23, 652391)
	,
	  'floating-point number': 2.5,
	  'integer': 2,
	  'string': 'some text',
	  'structure': {'a': 'dictionary'}}]
	
	After:
	[{'array': ['a', 'tuple'],
	  'boolean': True,
	  'datetime': <DateTime '20160618T17:16:23' at 0x1016ccb00>,
	  'floating-point number': 2.5,
	  'integer': 0,
	  'string': 'some text',
	  'structure': {'a': 'dictionary'}},
	 {'array': ['a', 'tuple'],
	  'boolean': True,
	  'datetime': <DateTime '20160618T17:16:23' at 0x1016cccc0>,
	  'floating-point number': 2.5,
	  'integer': 1,
	  'string': 'some text',
	  'structure': {'a': 'dictionary'}},
	 {'array': ['a', 'tuple'],
	  'boolean': True,
	  'datetime': <DateTime '20160618T17:16:23' at 0x1016cce10>,
	  'floating-point number': 2.5,
	  'integer': 2,
	  'string': 'some text',
	  'structure': {'a': 'dictionary'}}]

.. {{{end}}}

XML-RPC supports dates as a native type, and :mod:`xmlrpclib` can use
one of two classes to represent the date values in the outgoing proxy
or when they are received from the server.  By default an internal
version of :class:`DateTime` is used, but the *use_datetime* option
turns on support for using the classes in the :mod:`datetime` module.

Passing Objects
===============

Instances of Python classes are treated as structures and passed as a
dictionary, with the attributes of the object as values in the
dictionary.

.. literalinclude:: xmlrpc_types_object.py
   :caption:
   :start-after: #end_pymotw_header

When the value is sent back to the client from the server the result
is a dictionary on the client, since there is nothing encoded in the
values to tell the server (or client) that it should be instantiated
as part of a class.

::

    $ python3 xmlrpc_types_object.py

    o  : MyObj(1, 'b goes here')
    ["{'b': 'b goes here', 'a': 1}", "<class 'dict'>",
    {'a': 1, 'b': 'b goes here'}]
    o2 : MyObj(2, MyObj(1, 'b goes here'))
    ["{'b': {'b': 'b goes here', 'a': 1}, 'a': 2}",
     "<class 'dict'>",
     {'a': 2, 'b': {'a': 1, 'b': 'b goes here'}}]


Binary Data
===========

All values passed to the server are encoded and escaped
automatically. However, some data types may contain characters that
are not valid XML. For example, binary image data may include byte
values in the ASCII control range 0 to 31.  To pass binary data, it is
best to use the :class:`Binary` class to encode it for transport.

.. literalinclude:: xmlrpc_Binary.py
   :caption:
   :start-after: #end_pymotw_header

If the string containing a NULL byte is passed to :func:`show_type()`,
an exception is raised in the XML parser as it processes the response.

::

    $ python3 xmlrpc_Binary.py

    Local string: This is a string with control characters
    As binary: This is a string with control characters
    As string: 
    ERROR: <Fault 1: "<class 'xml.parsers.expat.ExpatError'>:not 
    well-formed (invalid token): line 6, column 55">


:class:`Binary` objects can also be used to send objects using
:mod:`pickle`. The normal security issues related to sending what
amounts to executable code over the wire apply here (i.e., do not do
this unless the communication channel is secure).

.. include:: xmlrpc_Binary_pickle.py
    :literal:
    :start-after: #end_pymotw_header


The data attribute of the :class:`Binary` instance contains the
pickled version of the object, so it has to be unpickled before it can
be used. That results in a different object (with a new id value).

::

    $ python3 xmlrpc_Binary_pickle.py
    
    Local: 4321077872
    MyObj(1, 'b goes here')
    
    As object:
    ["{'a': 1, 'b': 'b goes here'}", "<type 'dict'>", 
     {'a': 1, 'b': 'b goes here'}]
    
    From pickle: 4321252344
    MyObj(1, 'b goes here')

Exception Handling
==================

Since the XML-RPC server might be written in any language, exception
classes cannot be transmitted directly. Instead, exceptions raised in
the server are converted to :class:`Fault` objects and raised as
exceptions locally in the client.

.. literalinclude:: xmlrpc_exception.py
   :caption:
   :start-after: #end_pymotw_header

The original error message is saved in the :attr:`faultString`
attribute, and :attr:`faultCode` is set to an XML-RPC error number.

::

    $ python3 xmlrpc_exception.py

    Fault code: 1
    Message   : <type 'exceptions.RuntimeError'>:A message


Combining Calls Into One Message
================================

Multicall is an extension to the XML-RPC protocol that allows more than
one call to be sent at the same time, with the responses collected and
returned to the caller. The :class:`MultiCall` class was added to
:mod:`xmlrpclib` in Python 2.4. 

.. literalinclude:: xmlrpc_MultiCall.py
   :caption:
   :start-after: #end_pymotw_header

To use a :class:`MultiCall` instance, invoke the methods on it as with
a :class:`ServerProxy`, then call the object with no arguments to
actually run the remote functions. The return value is an iterator
that yields the results from all of the calls.

::

    $ python3 xmlrpc_MultiCall.py

    0 True
    1 ['1', "<type 'int'>", 1]
    2 ['string', "<type 'str'>", 'string']


If one of the calls causes a :class:`Fault`, the exception is raised
when the result is produced from the iterator and no more results are
available.

.. literalinclude:: xmlrpc_MultiCall_exception.py
   :caption:
   :start-after: #end_pymotw_header

Since the third response, from :func:`raises_exception`, generates an
exception, the response from :func:`show_type` is not accessible.

::

    $ python3 xmlrpc_MultiCall_exception.py
    
    0 True
    1 ['1', "<type 'int'>", 1]
    ERROR: <Fault 1: "<type 'exceptions.RuntimeError'>:Next to last call 
    stops execution">

.. seealso::

    `xmlrpclib <http://docs.python.org/lib/module-xmlrpclib.html>`_
        Standard library documentation for this module.

    :mod:`SimpleXMLRPCServer`
        An XML-RPC server implementation.
