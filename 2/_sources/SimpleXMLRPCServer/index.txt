===================================================
SimpleXMLRPCServer -- Implements an XML-RPC server.
===================================================

.. module:: SimpleXMLRPCServer
    :synopsis: Implements an XML-RPC server.

:Purpose: Implements an XML-RPC server.
:Available In: 2.2 and later

The :mod:`SimpleXMLRPCServer` module contains classes for creating
your own cross-platform, language-independent server using the XML-RPC
protocol. Client libraries exist for many other languages, making
XML-RPC an easy choice for building RPC-style services.

.. note::

    All of the examples provided here include a client module as well to
    interact with the demonstration server. If you want to download the code and
    run the examples, you will want to use 2 separate shell windows, one for the
    server and one for the client.

A Simple Server
===============

This simple server example exposes a single function that takes the
name of a directory and returns the contents. The first step is to
create the :class:`SimpleXMLRPCServer` instance and tell it where to
listen for incoming requests ('localhost' port 9000 in this
case). Then we define a function to be part of the service, and
register the function so the server knows how to call it. The final
step is to put the server into an infinite loop receiving and
responding to requests.

.. include:: SimpleXMLRPCServer_function.py
    :literal:
    :start-after: #end_pymotw_header

The server can be accessed at the URL http://localhost:9000 using
:mod:`xmlrpclib`.  This client code illustrates how to call the
:func:`list_contents()` service from Python.

.. include:: SimpleXMLRPCServer_function_client.py
    :literal:
    :start-after: #end_pymotw_header

Notice that we simply connect the :class:`ServerProxy` to the server
using its base URL, and then call methods directly on the proxy. Each
method invoked on the proxy is translated into a request to the
server. The arguments are formatted using XML, and then POSTed to the
server. The server unpacks the XML and figures out what function to
call based on the method name invoked from the client. The arguments
are passed to the function, and the return value is translated back to
XML to be returned to the client.

Starting the server gives::

    $ python SimpleXMLRPCServer_function.py 
    Use Control-C to exit

Running the client in a second window shows the contents of my
``/tmp`` directory::

    $ python SimpleXMLRPCServer_function_client.py 
    ['.s.PGSQL.5432', '.s.PGSQL.5432.lock', '.X0-lock', '.X11-unix', 'ccc_exclude.1mkahl', 
    'ccc_exclude.BKG3gb', 'ccc_exclude.M5jrgo', 'ccc_exclude.SPecwL', 'com.hp.launchport', 'emacs527',
    'hsperfdata_dhellmann', 'launch-8hGHUp', 'launch-RQnlcc', 'launch-trsdly', 'launchd-242.T5UzTy', 
    'var_backups']

and after the request is finished, log output appears in the server
window::

    $ python SimpleXMLRPCServer_function.py 
    Use Control-C to exit
    DEBUG:root:list_contents(/tmp)
    localhost - - [29/Jun/2008 09:32:07] "POST /RPC2 HTTP/1.0" 200 -

The first line of output is from the ``logging.debug()`` call inside
:func:`list_contents()`. The second line is from the server logging
the request because *logRequests* is ``True``.

Alternate Names
===============

Sometimes the function names you use inside your modules or libraries
are not the names you want to use in your external API. You might need
to load a platform-specific implementation, build the service API
dynamically based on a configuration file, or replace real functions
with stubs for testing. If you want to register a function with an
alternate name, pass the name as the second argument to
:func:`register_function()`, like this:

.. include:: SimpleXMLRPCServer_alternate_name.py
    :literal:
    :start-after: #end_pymotw_header

The client should now use the name ``dir()`` instead of
``list_contents()``:

.. include:: SimpleXMLRPCServer_alternate_name_client.py
    :literal:
    :start-after: #end_pymotw_header

Calling ``list_contents()`` results in an error, since the server no
longer has a handler registered by that name.

::

    $ python SimpleXMLRPCServer_alternate_name_client.py
    dir(): ['.s.PGSQL.5432', '.s.PGSQL.5432.lock', '.X0-lock', '.X11-unix', 'ccc_exclude.1mkahl', 'ccc_exclude.BKG3gb', 'ccc_exclude.M5jrgo', 'ccc_exclude.SPecwL', 'com.hp.launchport', 'emacs527', 'hsperfdata_dhellmann', 'launch-8hGHUp', 'launch-RQnlcc', 'launch-trsdly', 'launchd-242.T5UzTy', 'temp_textmate.V6YKzm', 'var_backups']
    list_contents():
    Traceback (most recent call last):
      File "/Users/dhellmann/Documents/PyMOTW/in_progress/SimpleXMLRPCServer/SimpleXMLRPCServer_alternate_name_client.py", line 15, in <module>
        print 'list_contents():', proxy.list_contents('/tmp')
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
    xmlrpclib.Fault: <Fault 1: '<type \'exceptions.Exception\'>:method "list_contents" is not supported'>


Dotted Names
============

Individual functions can be registered with names that are not
normally legal for Python identifiers. For example, you can include
'.' in your names to separate the namespace in the service. This
example extends our "directory" service to add "create" and "remove"
calls. All of the functions are registered using the prefix "``dir.``"
so that the same server can provide other services using a different
prefix. One other difference in this example is that some of the
functions return ``None``, so we have to tell the server to translate
the ``None`` values to a nil value (see `XML-RPC Extensions`_).

.. include:: SimpleXMLRPCServer_dotted_name.py
    :literal:
    :start-after: #end_pymotw_header


To call the service functions in the client, simply refer to them with the
dotted name, like so:

.. include:: SimpleXMLRPCServer_dotted_name_client.py
    :literal:
    :start-after: #end_pymotw_header

and (assuming you don't have a ``/tmp/EXAMPLE`` file on your system)
the output for the sample client script looks like::

    $ python SimpleXMLRPCServer_dotted_name_client.py
    BEFORE       : False
    CREATE       : None
    SHOULD EXIST : True
    REMOVE       : None
    AFTER        : False


Arbitrary Names
===============

A less useful, but potentially interesting feature is the ability to register
functions with names that are otherwise invalid attribute names. This example
service registers a function with the name "``multiply args``".

.. include:: SimpleXMLRPCServer_arbitrary_name.py
    :literal:
    :start-after: #end_pymotw_header

Since the registered name contains a space, we can't use dot notation
to access it directly from the proxy. We can, however, use
``getattr()``.

.. include:: SimpleXMLRPCServer_arbitrary_name_client.py
    :literal:
    :start-after: #end_pymotw_header

You should avoid creating services with names like this, though.  This
example is provided not necessarily because it is a good idea, but
because you may encounter existing services with arbitrary names and
need to be able to call them.

::

    $ python SimpleXMLRPCServer_arbitrary_name_client.py
    25


Exposing Methods of Objects
===========================

The earlier sections talked about techniques for establishing APIs
using good naming conventions and namespacing. Another way to
incorporate namespacing into your API is to use instances of classes
and expose their methods. We can recreate the first example using an
instance with a single method.

.. include:: SimpleXMLRPCServer_instance.py
    :literal:
    :start-after: #end_pymotw_header

A client can call the method directly:

.. include:: SimpleXMLRPCServer_instance_client.py
    :literal:
    :start-after: #end_pymotw_header

and receive output like::

    $ python SimpleXMLRPCServer_instance_client.py
    ['.s.PGSQL.5432', '.s.PGSQL.5432.lock', '.X0-lock', '.X11-unix', 'ccc_exclude.1mkahl', 
    'ccc_exclude.BKG3gb', 'ccc_exclude.M5jrgo', 'ccc_exclude.SPecwL', 'com.hp.launchport', 
    'emacs527', 'hsperfdata_dhellmann', 'launch-8hGHUp', 'launch-RQnlcc', 'launch-trsdly', 
    'launchd-242.T5UzTy', 'temp_textmate.XNiIdy', 'var_backups']

We've lost the "``dir.``" prefix for the service, though, so let's
define a class to let us set up a service tree that can be invoked
from clients.

.. include:: SimpleXMLRPCServer_instance_dotted_names.py
    :literal:
    :start-after: #end_pymotw_header

By registering the instance of :class:`ServiceRoot` with
*allow_dotted_names* enabled, we give the server permission to walk
the tree of objects when a request comes in to find the named method
using ``getattr()``.

.. include:: SimpleXMLRPCServer_instance_dotted_names_client.py
    :literal:
    :start-after: #end_pymotw_header

::

    $ python SimpleXMLRPCServer_instance_dotted_names_client.py
    ['.s.PGSQL.5432', '.s.PGSQL.5432.lock', '.X0-lock', '.X11-unix', 'ccc_exclude.1mkahl', 'ccc_exclude.BKG3gb', 'ccc_exclude.M5jrgo', 'ccc_exclude.SPecwL', 'com.hp.launchport', 'emacs527', 'hsperfdata_dhellmann', 'launch-8hGHUp', 'launch-RQnlcc', 'launch-trsdly', 'launchd-242.T5UzTy', 'temp_textmate.adghkQ', 'var_backups']


Dispatching Calls Yourself
==========================

By default, :func:`register_instance()` finds all callable attributes
of the instance with names not starting with '``_``' and registers
them with their name. If you want to be more careful about the exposed
methods, you could provide your own dispatching logic. For example:

.. include:: SimpleXMLRPCServer_instance_with_prefix.py
    :literal:
    :start-after: #end_pymotw_header

The :func:`public()` method of :class:`MyService` is marked as exposed
to the XML-RPC service while :func:`private()` is not. The
:func:`_dispatch()` method is invoked when the client tries to access
a function that is part of :class:`MyService`. It first enforces the
use of a prefix ("``prefix.``" in this case, but you can use any
string).  Then it requires the function to have an attribute called
*exposed* with a true value. The exposed flag is set on a function
using a decorator for convenience.

Here are a few sample client calls:

.. include:: SimpleXMLRPCServer_instance_with_prefix_client.py
    :literal:
    :start-after: #end_pymotw_header

and the resulting output, with the expected error messages trapped and
reported::

    $ python SimpleXMLRPCServer_instance_with_prefix_client.py
    public(): This is public
    private(): ERROR: <Fault 1: '<type \'exceptions.Exception\'>:method "prefix.private" is not supported'>
    public() without prefix: ERROR: <Fault 1: '<type \'exceptions.Exception\'>:method "public" is not supported'>

There are several other ways to override the dispatching mechanism, including
subclassing directly from SimpleXMLRPCServer. Check out the docstrings in the
module for more details.


Introspection API
=================

As with many network services, it is possible to query an XML-RPC
server to ask it what methods it supports and learn how to use
them. :class:`SimpleXMLRPCServer` includes a set of public methods for
performing this introspection. By default they are turned off, but can
be enabled with :func:`register_introspection_functions()`. You can
add explicit support for :func:`system.listMethods()` and
:func:`system.methodHelp()` by defining :func:`_listMethods()` and
:func:`_methodHelp()` on your service class. For example,

.. include:: SimpleXMLRPCServer_introspection.py
    :literal:
    :start-after: #end_pymotw_header

In this case, the convenience function :func:`list_public_methods()`
scans an instance to return the names of callable attributes that do
not start with '``_``'. You can redefine :func:`_listMethods()` to
apply whatever rules you like.  Similarly, for this basic example
:func:`_methodHelp()` returns the docstring of the function, but could
be written to build a help string from another source.

This client queries the server and reports on all of the publicly
callable methods.

.. include:: SimpleXMLRPCServer_introspection_client.py
    :literal:
    :start-after: #end_pymotw_header

Notice that the system methods are included in the results.

::

    $ python SimpleXMLRPCServer_introspection_client.py
    ============================================================
    list
    ------------------------------------------------------------
    list(dir_name) => [<filenames>]

    Returns a list containing the contents of the named directory.

    ============================================================
    system.listMethods
    ------------------------------------------------------------
    system.listMethods() => ['add', 'subtract', 'multiple']

    Returns a list of the methods supported by the server.

    ============================================================
    system.methodHelp
    ------------------------------------------------------------
    system.methodHelp('add') => "Adds two integers together"

    Returns a string containing documentation for the specified method.

    ============================================================
    system.methodSignature
    ------------------------------------------------------------
    system.methodSignature('add') => [double, int, int]

    Returns a list describing the signature of the method. In the
    above example, the add method takes two integers as arguments
    and returns a double result.

    This server does NOT support system.methodSignature.


.. seealso::

    `SimpleXMLRPCServer <https://docs.python.org/2/library/simplexmlrpcserver.html>`_
        Standard library documentation for this module.

    `XML-RPC How To <http://www.tldp.org/HOWTO/XML-RPC-HOWTO/index.html>`_
        Describes how to use XML-RPC to implement clients and servers in 
        a variety of languages.

    `XML-RPC Extensions`_
        Specifies an extension to the XML-RPC protocol.

    :mod:`xmlrpclib`
        XML-RPC client library

.. _XML-RPC Extensions: http://ontosys.com/xml-rpc/extensions.php
