==========================================================
xmlrpclib -- Client-side library for XML-RPC communication
==========================================================

.. module:: xmlrpclib
    :synopsis: Client-side library for XML-RPC communication.

:Purpose: Client-side library for XML-RPC communication.
:Available In: 2.2 and later

We have already looked at :mod:`SimpleXMLRPCServer`, the library for
creating an XML-RPC server. The :mod:`xmlrpclib` module lets you
communicate from Python with any XML-RPC server written in any
language.

.. note::

    All of the examples below use the server defined in
    ``xmlrpclib_server.py``, available in the source distribution and
    repeated here for reference:

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
and HTTPS are supported out of the box, as are basic
authentication. You would only need to provide a transport class if
your communication channel was not one of the supported types. It
would be an interesting exercise, for example, to implement XML-RPC
over SMTP. Not terribly useful, but interesting.

The verbose option gives you debugging information useful for working
out where communication errors might be happening.

.. include:: xmlrpclib_ServerProxy_verbose.py
    :literal:
    :start-after: #end_pymotw_header

::

    $ python xmlrpclib_ServerProxy_verbose.py
    Ping: connect: (localhost, 9000)
    connect fail: ('localhost', 9000)
    connect: (localhost, 9000)
    connect fail: ('localhost', 9000)
    connect: (localhost, 9000)
    send: 'POST /RPC2 HTTP/1.0\r\nHost: localhost:9000\r\nUser-Agent: xmlrpclib.py/1.0.1 (by www.pythonware.com)\r\nContent-Type: text/xml\r\nContent-Length: 98\r\n\r\n'
    send: "<?xml version='1.0'?>\n<methodCall>\n<methodName>ping</methodName>\n<params>\n</params>\n</methodCall>\n"
    reply: 'HTTP/1.0 200 OK\r\n'
    header: Server: BaseHTTP/0.3 Python/2.5.1
    header: Date: Sun, 06 Jul 2008 19:56:13 GMT
    header: Content-type: text/xml
    header: Content-length: 129
    body: "<?xml version='1.0'?>\n<methodResponse>\n<params>\n<param>\n<value><boolean>1</boolean></value>\n</param>\n</params>\n</methodResponse>\n"
    True

You can change the default encoding from UTF-8 if you need to use an
alternate system.

.. include:: xmlrpclib_ServerProxy_encoding.py
    :literal:
    :start-after: #end_pymotw_header

The server should automatically detect the correct encoding.

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
    Not allowed:
    Traceback (most recent call last):
      File "/Users/dhellmann/Documents/PyMOTW/in_progress/xmlrpclib/xmlrpclib_ServerProxy_allow_none.py", line 17, in <module>
        print 'Not allowed:', server.show_type(None)
      File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/xmlrpclib.py", line 1147, in __call__
        return self.__send(self.__name, args)
      File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/xmlrpclib.py", line 1431, in __request
        allow_none=self.__allow_none)
      File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/xmlrpclib.py", line 1080, in dumps
        data = m.dumps(params)
      File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/xmlrpclib.py", line 623, in dumps
        dump(v, write)
      File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/xmlrpclib.py", line 635, in __dump
        f(self, value, write)
      File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/xmlrpclib.py", line 639, in dump_nil
        raise TypeError, "cannot marshal None unless allow_none is enabled"
    TypeError: cannot marshal None unless allow_none is enabled


The *use_datetime* option lets you pass :mod:`datetime` and related
objects in to the proxy or receive them from the server. If
*use_datetime* is False, the internal :class:`DateTime` class is used
to represent dates instead.

Data Types
==========

The XML-RPC protocol recognizes a limited set of common data
types. The types can be passed as arguments or return values and
combined to create more complex data structures.

.. include:: xmlrpclib_types.py
    :literal:
    :start-after: #end_pymotw_header


The simple types::

    $ python xmlrpclib_types.py
    boolean               : ['True', "<type 'bool'>", True]
    integer               : ['1', "<type 'int'>", 1]
    floating-point number : ['2.5', "<type 'float'>", 2.5]
    string                : ['some text', "<type 'str'>", 'some text']
    datetime              : ['20080706T16:22:49', "<type 'instance'>", <DateTime '20080706T16:22:49' at a5d030>]
    array                 : ["['a', 'list']", "<type 'list'>", ['a', 'list']]
    array                 : ["['a', 'tuple']", "<type 'list'>", ['a', 'tuple']]
    structure             : ["{'a': 'dictionary'}", "<type 'dict'>", {'a': 'dictionary'}]


And they can be nested to create values of arbitrary complexity:

.. include:: xmlrpclib_types_nested.py
    :literal:
    :start-after: #end_pymotw_header

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


Passing Objects
===============

Instances of Python classes are treated as structures and passed as a
dictionary, with the attributes of the object as values in the
dictionary.

.. include:: xmlrpclib_types_object.py
    :literal:
    :start-after: #end_pymotw_header


Round-tripping the value gives a dictionary on the client, since there
is nothing encoded in the values to tell the server (or client) that
it should be instantiated as part of a class.

::

    $ python xmlrpclib_types_object.py
    o= MyObj(1, 'b goes here')
    ["{'a': 1, 'b': 'b goes here'}", "<type 'dict'>", {'a': 1, 'b': 'b goes here'}]
    o2= MyObj(2, MyObj(1, 'b goes here'))
    ["{'a': 2, 'b': {'a': 1, 'b': 'b goes here'}}", "<type 'dict'>", {'a': 2, 'b': {'a': 1, 'b': 'b goes here'}}]


Binary Data
===========

All values passed to the server are encoded and escaped
automatically. However, some data types may contain characters that
are not valid XML. For example, binary image data may include byte
values in the ASCII control range 0 to 31.  If you need to pass binary
data, it is best to use the :class:`Binary` class to encode it for
transport.

.. include:: xmlrpclib_Binary.py
    :literal:
    :start-after: #end_pymotw_header

If we pass the string containing a NULL byte to :func:`show_type()`,
an exception is raised in the XML parser:

::

    $ python xmlrpclib_Binary.py
    Local string: This is a string with control characters
    As binary: This is a string with control characters
    As string:
    Traceback (most recent call last):
      File "/Users/dhellmann/Documents/PyMOTW/in_progress/xmlrpclib/xmlrpclib_Binary.py", line 21, in <module>
        print 'As string:', server.show_type(s)
      File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/xmlrpclib.py", line 1147, in __call__
        return self.__send(self.__name, args)
      File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/xmlrpclib.py", line 1437, in __request
        verbose=self.__verbose
      File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/xmlrpclib.py", line 1201, in request
        return self._parse_response(h.getfile(), sock)
      File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/xmlrpclib.py", line 1340, in _parse_response
        return u.close()
      File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/xmlrpclib.py", line 787, in close
        raise Fault(**self._stack[0])
    xmlrpclib.Fault: <Fault 1: "<class 'xml.parsers.expat.ExpatError'>:not well-formed (invalid token): line 6, column 55">


:class:`Binary` objects can also be used to send objects using
:mod:`pickle`. The normal security issues related to sending what
amounts to executable code over the wire apply here (i.e., don't do
this unless you're sure your communication channel is secure).

.. include:: xmlrpclib_Binary_pickle.py
    :literal:
    :start-after: #end_pymotw_header


Remember, the data attribute of the :class:`Binary` instance contains
the pickled version of the object, so it has to be unpickled before it
can be used. That results in a different object (with a new id value).

::

    $ python xmlrpclib_Binary_pickle.py
    Local: MyObj(1, 'b goes here') 9620936
    As object: ["{'a': 1, 'b': 'b goes here'}", "<type 'dict'>", {'a': 1, 'b': 'b goes here'}]
    From pickle: MyObj(1, 'b goes here') 11049200


Exception Handling
==================

Since the XML-RPC server might be written in any language, exception
classes cannot be transmitted directly. Instead, exceptions raised in
the server are converted to :class:`Fault` objects and raised as
exceptions locally in the client.

.. include:: xmlrpclib_exception.py
    :literal:
    :start-after: #end_pymotw_header


::

    $ python xmlrpclib_exception.py
    Fault code: 1
    Message   : <type 'exceptions.RuntimeError'>:A message


MultiCall
=========

Multicall is an extension to the XML-RPC protocol to allow more than
one call to be sent at the same time, with the responses collected and
returned to the caller. The :class:`MultiCall` class was added to
:mod:`xmlrpclib` in Python 2.4. To use a :class:`MultiCall` instance,
invoke the methods on it as with a :class:`ServerProxy`, then call the
object with no arguments. The result is an iterator with the results.

.. include:: xmlrpclib_MultiCall.py
    :literal:
    :start-after: #end_pymotw_header

::

    $ python xmlrpclib_MultiCall.py
    0 True
    1 ['1', "<type 'int'>", 1]
    2 ['string', "<type 'str'>", 'string']


If one of the calls causes a :class:`Fault` or otherwise raises an
exception, the exception is raised when the result is produced from
the iterator and no more results are available.

.. include:: xmlrpclib_MultiCall_exception.py
    :literal:
    :start-after: #end_pymotw_header

::

    $ python xmlrpclib_MultiCall_exception.py
    0 True
    1 ['1', "<type 'int'>", 1]
    Traceback (most recent call last):
      File "/Users/dhellmann/Documents/PyMOTW/in_progress/xmlrpclib/xmlrpclib_MultiCall_exception.py", line 21, in <module>
        for i, r in enumerate(multicall()):
      File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/xmlrpclib.py", line 949, in __getitem__
        raise Fault(item['faultCode'], item['faultString'])
    xmlrpclib.Fault: <Fault 1: "<type 'exceptions.RuntimeError'>:Next to last call stops execution">

.. seealso::

    `xmlrpclib <https://docs.python.org/2/library/xmlrpclib.html>`_
        Standard library documentation for this module.

    :mod:`SimpleXMLRPCServer`
        An XML-RPC server implementation.
