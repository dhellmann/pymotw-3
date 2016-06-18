=========================================
 xmlrpclib -- Client Library for XML-RPC
=========================================

.. module:: xmlrpclib
    :synopsis: Client library for XML-RPC

:Purpose: Client-side library for XML-RPC communication.
:Python Version: 2.2 and later

XML-RPC is a lightweight remote procedure call protocol built on top
of HTTP and XML.  The :mod:`xmlrpclib` module lets a Python program
communicate with an XML-RPC server written in any language.

All of the examples in this section use the server defined in
``xmlrpclib_server.py``, available in the source distribution and
included here for reference:

.. include:: xmlrpclib_server.py
    :literal:
    :start-after: #end_pymotw_header


Connecting to a Server
======================

The simplest way to connect a client to a server is to instantiate a
:class:`ServerProxy` object, giving it the URI of the server. For
example, the demo server runs on port 9000 of localhost:

.. include:: xmlrpclib_ServerProxy.py
    :literal:
    :start-after: #end_pymotw_header

In this case, the :func:`ping()` method of the service takes no
arguments and returns a single boolean value.

::

    $ python xmlrpclib_ServerProxy.py

    Ping: True


Other options are available to support alternate transport. Both HTTP
and HTTPS are supported out of the box, both with basic
authentication. To implement a new communication channel, only a new
transport class is needed.  It could be an interesting exercise, for
example, to implement XML-RPC over SMTP.

.. include:: xmlrpclib_ServerProxy_verbose.py
    :literal:
    :start-after: #end_pymotw_header

The *verbose* option gives debugging information useful for resolving
communication errors.

::

    $ python xmlrpclib_ServerProxy_verbose.py

    Ping: connect: (localhost, 9000)
    connect fail: ('localhost', 9000)
    connect: (localhost, 9000)
    connect fail: ('localhost', 9000)
    connect: (localhost, 9000)
    send: 'POST /RPC2 HTTP/1.0\r\nHost: localhost:9000\r\nUser-Agent:
     xmlrpclib.py/1.0.1 (by www.pythonware.com)\r\nContent-Type: text
    /xml\r\nContent-Length: 98\r\n\r\n'
    send: "<?xml version='1.0'?>\n<methodCall>\n<methodName>ping</met
    hodName>\n<params>\n</params>\n</methodCall>\n"
    reply: 'HTTP/1.0 200 OK\r\n'
    header: Server: BaseHTTP/0.3 Python/2.5.1
    header: Date: Sun, 06 Jul 2008 19:56:13 GMT
    header: Content-type: text/xml
    header: Content-length: 129
    body: "<?xml version='1.0'?>\n<methodResponse>\n<params>\n<param
    >\n<value><boolean>1</boolean></value>\n</param>\n</params>\n</m
    ethodResponse>\n"
    True

The default encoding can be changed from UTF-8 if an alternate system
is needed.

.. include:: xmlrpclib_ServerProxy_encoding.py
    :literal:
    :start-after: #end_pymotw_header

The server automatically detects the correct encoding.

::

    $ python xmlrpclib_ServerProxy_encoding.py

    Ping: True


The *allow_none* option controls whether Python's ``None`` value is
automatically translated to a nil value or if it causes an error.

.. include:: xmlrpclib_ServerProxy_allow_none.py
    :literal:
    :start-after: #end_pymotw_header

The error is raised locally if the client does not allow ``None``, but
can also be raised from within the server if it is not configured to
allow ``None``.

::

    $ python xmlrpclib_ServerProxy_allow_none.py

    Allowed: ['None', "<type 'NoneType'>", None]
    ERROR: cannot marshal None unless allow_none is enabled


Data Types
==========

The XML-RPC protocol recognizes a limited set of common data
types. The types can be passed as arguments or return values and
combined to create more complex data structures.

.. include:: xmlrpclib_types.py
    :literal:
    :start-after: #end_pymotw_header


The simple types are

::

    $ python xmlrpclib_types.py
        
    boolean     : True
                  <type 'bool'>
                  True
    integer     : 1
                  <type 'int'>
                  1
    float       : 2.5
                  <type 'float'>
                  2.5
    string      : some text
                  <type 'str'>
                  some text
    datetime    : 20101128T20:15:21
                  <type 'instance'>
                  20101128T20:15:21
    array       : ['a', 'list']
                  <type 'list'>
                  ['a', 'list']
    array       : ['a', 'tuple']
                  <type 'list'>
                  ['a', 'tuple']
    structure   : {'a': 'dictionary'}
                  <type 'dict'>
                  {'a': 'dictionary'}


The supported types can be nested to create values of arbitrary
complexity.

.. include:: xmlrpclib_types_nested.py
    :literal:
    :start-after: #end_pymotw_header

This program passes a list of dictionaries containing all of the
supported types to the sample server, which returns the data.  Tuples
are converted to lists and :class:`datetime` instances are converted
to :class:`DateTime` objects, but otherwise the data is unchanged.

::

    $ python xmlrpclib_types_nested.py

    Before:
    [{'array': ('a', 'tuple'),
      'boolean': True,
      'datetime': datetime.datetime(2008, 7, 6, 16, 24, 52, 348849),
      'floating-point number': 2.5,
      'integer': 0,
      'string': 'some text',
      'structure': {'a': 'dictionary'}},
     {'array': ('a', 'tuple'),
      'boolean': True,
      'datetime': datetime.datetime(2008, 7, 6, 16, 24, 52, 348849),
      'floating-point number': 2.5,
      'integer': 1,
      'string': 'some text',
      'structure': {'a': 'dictionary'}},
     {'array': ('a', 'tuple'),
      'boolean': True,
      'datetime': datetime.datetime(2008, 7, 6, 16, 24, 52, 348849),
      'floating-point number': 2.5,
      'integer': 2,
      'string': 'some text',
      'structure': {'a': 'dictionary'}}]

    After:
    [{'array': ['a', 'tuple'],
      'boolean': True,
      'datetime': <DateTime '20080706T16:24:52' at a5be18>,
      'floating-point number': 2.5,
      'integer': 0,
      'string': 'some text',
      'structure': {'a': 'dictionary'}},
     {'array': ['a', 'tuple'],
      'boolean': True,
      'datetime': <DateTime '20080706T16:24:52' at a5bf30>,
      'floating-point number': 2.5,
      'integer': 1,
      'string': 'some text',
      'structure': {'a': 'dictionary'}},
     {'array': ['a', 'tuple'],
      'boolean': True,
      'datetime': <DateTime '20080706T16:24:52' at a5bf80>,
      'floating-point number': 2.5,
      'integer': 2,
      'string': 'some text',
      'structure': {'a': 'dictionary'}}]

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

.. include:: xmlrpclib_types_object.py
    :literal:
    :start-after: #end_pymotw_header


When the value is sent back to the client from the server the result
is a dictionary on the client, since there is nothing encoded in the
values to tell the server (or client) that it should be instantiated
as part of a class.

::

    $ python xmlrpclib_types_object.py

    o  : MyObj(1, 'b goes here')
	["{'a': 1, 'b': 'b goes here'}", "<type 'dict'>", 
     {'a': 1, 'b': 'b goes here'}]
    o2 : MyObj(2, MyObj(1, 'b goes here'))
    ["{'a': 2, 'b': {'a': 1, 'b': 'b goes here'}}",
     "<type 'dict'>",
     {'a': 2, 'b': {'a': 1, 'b': 'b goes here'}}]


Binary Data
===========

All values passed to the server are encoded and escaped
automatically. However, some data types may contain characters that
are not valid XML. For example, binary image data may include byte
values in the ASCII control range 0 to 31.  To pass binary data, it is
best to use the :class:`Binary` class to encode it for transport.

.. include:: xmlrpclib_Binary.py
    :literal:
    :start-after: #end_pymotw_header

If the string containing a NULL byte is passed to :func:`show_type()`,
an exception is raised in the XML parser.

::

    $ python xmlrpclib_Binary.py

    Local string: This is a string with control characters
    As binary: This is a string with control characters
    As string: 
    ERROR: <Fault 1: "<class 'xml.parsers.expat.ExpatError'>:not 
    well-formed (invalid token): line 6, column 55">


:class:`Binary` objects can also be used to send objects using
:mod:`pickle`. The normal security issues related to sending what
amounts to executable code over the wire apply here (i.e., do not do
this unless the communication channel is secure).

.. include:: xmlrpclib_Binary_pickle.py
    :literal:
    :start-after: #end_pymotw_header


The data attribute of the :class:`Binary` instance contains the
pickled version of the object, so it has to be unpickled before it can
be used. That results in a different object (with a new id value).

::

    $ python xmlrpclib_Binary_pickle.py
    
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

.. include:: xmlrpclib_exception.py
    :literal:
    :start-after: #end_pymotw_header

The original error message is saved in the :attr:`faultString`
attribute, and :attr:`faultCode` is set to an XML-RPC error number.

::

    $ python xmlrpclib_exception.py

    Fault code: 1
    Message   : <type 'exceptions.RuntimeError'>:A message


Combining Calls Into One Message
================================

Multicall is an extension to the XML-RPC protocol that allows more than
one call to be sent at the same time, with the responses collected and
returned to the caller. The :class:`MultiCall` class was added to
:mod:`xmlrpclib` in Python 2.4. 

.. include:: xmlrpclib_MultiCall.py
    :literal:
    :start-after: #end_pymotw_header

To use a :class:`MultiCall` instance, invoke the methods on it as with
a :class:`ServerProxy`, then call the object with no arguments to
actually run the remote functions. The return value is an iterator
that yields the results from all of the calls.

::

    $ python xmlrpclib_MultiCall.py

    0 True
    1 ['1', "<type 'int'>", 1]
    2 ['string', "<type 'str'>", 'string']


If one of the calls causes a :class:`Fault`, the exception is raised
when the result is produced from the iterator and no more results are
available.

.. include:: xmlrpclib_MultiCall_exception.py
    :literal:
    :start-after: #end_pymotw_header

Since the third response, from :func:`raises_exception`, generates an
exception, the response from :func:`show_type` is not accessible.

::

    $ python xmlrpclib_MultiCall_exception.py
    
    0 True
    1 ['1', "<type 'int'>", 1]
    ERROR: <Fault 1: "<type 'exceptions.RuntimeError'>:Next to last call 
    stops execution">

.. seealso::

    `xmlrpclib <http://docs.python.org/lib/module-xmlrpclib.html>`_
        Standard library documentation for this module.

    :mod:`SimpleXMLRPCServer`
        An XML-RPC server implementation.
