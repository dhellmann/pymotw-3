=========================================
 SimpleXMLRPCServer -- An XML-RPC server
=========================================

.. module:: SimpleXMLRPCServer
    :synopsis: Implements an XML-RPC server.

:Purpose: Implements an XML-RPC server.
:Python Version: 2.2 and later

The :mod:`SimpleXMLRPCServer` module contains classes for creating
cross-platform, language-independent servers using the XML-RPC
protocol. Client libraries exist for many other languages besides
Python, making XML-RPC an easy choice for building RPC-style services.

.. note::

    All of the examples provided here include a client module as well
    to interact with the demonstration server. To run the examples,
    use two separate shell windows, one for the server and one for the
    client.

A Simple Server
===============

This simple server example exposes a single function that takes the
name of a directory and returns the contents. The first step is to
create the :class:`SimpleXMLRPCServer` instance and tell it where to
listen for incoming requests ('localhost' port 9000 in this
case). Then a function is defined to be part of the service, and
registered so the server knows how to call it. The final step is to
put the server into an infinite loop receiving and responding to
requests.

.. warning::

    This implementation has obvious security implications.  Do not run
    it on a server on the open Internet or in any environment where
    security might be an issue.

.. include:: SimpleXMLRPCServer_function.py
    :literal:
    :start-after: #end_pymotw_header

The server can be accessed at the URL ``http://localhost:9000`` using
:mod:`xmlrpclib`.  This client code illustrates how to call the
:func:`list_contents()` service from Python.

.. include:: SimpleXMLRPCServer_function_client.py
    :literal:
    :start-after: #end_pymotw_header

The :class:`ServerProxy` is connected to the server using its base
URL, and then methods are called directly on the proxy. Each method
invoked on the proxy is translated into a request to the server. The
arguments are formatted using XML, and then sent to the server in a
POST message. The server unpacks the XML and determines which function
to call based on the method name invoked from the client. The
arguments are passed to the function, and the return value is
translated back to XML to be returned to the client.

Starting the server gives::

    $ python SimpleXMLRPCServer_function.py 

    Use Control-C to exit

Running the client in a second window shows the contents of the
``/tmp`` directory.

::

    $ python SimpleXMLRPCServer_function_client.py 

    ['.s.PGSQL.5432', '.s.PGSQL.5432.lock', '.X0-lock', '.X11-unix', 
    'ccc_exclude.1mkahl', 'ccc_exclude.BKG3gb', 'ccc_exclude.M5jrgo', 
    'ccc_exclude.SPecwL', 'com.hp.launchport', 'emacs527',
    'hsperfdata_dhellmann', 'launch-8hGHUp', 'launch-RQnlcc', 
    'launch-trsdly', 'launchd-242.T5UzTy', 'var_backups']

After the request is finished, log output appears in the server
window.

::

    $ python SimpleXMLRPCServer_function.py 

    Use Control-C to exit
    DEBUG:root:list_contents(/tmp)
    localhost - - [29/Jun/2008 09:32:07] "POST /RPC2 HTTP/1.0" 200 -

The first line of output is from the :func:`logging.debug` call inside
:func:`list_contents()`. The second line is from the server logging
the request because *logRequests* is ``True``.

Alternate API Names
===================

Sometimes the function names used inside a module or library are not
the names that should be used in the external API.  Names may change
because a platform-specific implementation is loaded, the service API
is built dynamically based on a configuration file, or real functions
can be replaced with stubs for testing.  To register a function with
an alternate name, pass the name as the second argument to
:func:`register_function()`, like this:

.. include:: SimpleXMLRPCServer_alternate_name.py
    :literal:
    :start-after: #end_pymotw_header

The client should now use the name :func:`dir` instead of
:func:`list_contents`:

.. include:: SimpleXMLRPCServer_alternate_name_client.py
    :literal:
    :start-after: #end_pymotw_header

Calling :func:`list_contents` results in an error, since the server no
longer has a handler registered by that name.

::

    $ python SimpleXMLRPCServer_alternate_name_client.py
    
    dir(): ['ccc_exclude.GIqLcR', 'ccc_exclude.kzR42t', 
    'ccc_exclude.LV04nf', 'ccc_exclude.Vfzylm', 'emacs527', 
    'icssuis527', 'launch-9hTTwf', 'launch-kCXjtT', 
    'launch-Nwc3AB', 'launch-pwCgej', 'launch-Xrku4Q', 
    'launch-YtDZBJ', 'launchd-167.AfaNuZ', 'var_backups']
    
    list_contents(): 
    ERROR: <Fault 1: '<type \'exceptions.Exception\'>:method 
    "list_contents" is not supported'>


Dotted API Names
================

Individual functions can be registered with names that are not
normally legal for Python identifiers. For example, a period
(``.``) can be included in the names to separate the namespace in the service. The
next example extends the "directory" service to add "create" and
"remove" calls. All of the functions are registered using the prefix
"``dir.``" so that the same server can provide other services using a
different prefix. One other difference in this example is that some of
the functions return ``None``, so the server has to be told to
translate the ``None`` values to a nil value.

.. include:: SimpleXMLRPCServer_dotted_name.py
    :literal:
    :start-after: #end_pymotw_header


To call the service functions in the client, simply refer to them with the
dotted name.

.. include:: SimpleXMLRPCServer_dotted_name_client.py
    :literal:
    :start-after: #end_pymotw_header

Assuming there is no ``/tmp/EXAMPLE`` file on the current system,
the output for the sample client script is:

::

    $ python SimpleXMLRPCServer_dotted_name_client.py

    BEFORE       : False
    CREATE       : None
    SHOULD EXIST : True
    REMOVE       : None
    AFTER        : False


Arbitrary API Names
===================

Another interesting feature is the ability to register functions with
names that are otherwise invalid Python object attribute names. This
example service registers a function with the name "``multiply
args``".

.. include:: SimpleXMLRPCServer_arbitrary_name.py
    :literal:
    :start-after: #end_pymotw_header

Since the registered name contains a space, dot notation cannot be
used to access it directly from the proxy.  Using :func:`getattr` does
work, however.

.. include:: SimpleXMLRPCServer_arbitrary_name_client.py
    :literal:
    :start-after: #end_pymotw_header

Avoid creating services with names like this, though.  This example is
provided not necessarily because it is a good idea, but because
existing services with arbitrary names exist, and new programs may
need to be able to call them.

::

    $ python SimpleXMLRPCServer_arbitrary_name_client.py

    25


Exposing Methods of Objects
===========================

The earlier sections talked about techniques for establishing APIs
using good naming conventions and namespacing. Another way to
incorporate namespacing into an API is to use instances of classes and
expose their methods. The first example can be recreated using an
instance with a single method.

.. include:: SimpleXMLRPCServer_instance.py
    :literal:
    :start-after: #end_pymotw_header

A client can call the method directly:

.. include:: SimpleXMLRPCServer_instance_client.py
    :literal:
    :start-after: #end_pymotw_header

The output is::

    $ python SimpleXMLRPCServer_instance_client.py

    ['ccc_exclude.1mkahl', 'ccc_exclude.BKG3gb', 'ccc_exclude.M5jrgo', 
    'ccc_exclude.SPecwL', 'com.hp.launchport', 'emacs527', 
    'hsperfdata_dhellmann', 'launch-8hGHUp', 'launch-RQnlcc', 
    'launch-trsdly', 'launchd-242.T5UzTy', 'var_backups']

The "``dir.``" prefix for the service has been lost, though.  It can
be restored by defining a class to set up a service tree that can be
invoked from clients.

.. include:: SimpleXMLRPCServer_instance_dotted_names.py
    :literal:
    :start-after: #end_pymotw_header

By registering the instance of :class:`ServiceRoot` with
*allow_dotted_names* enabled, the server has permission to walk the
tree of objects when a request comes in to find the named method using
:func:`getattr`.

.. include:: SimpleXMLRPCServer_instance_dotted_names_client.py
    :literal:
    :start-after: #end_pymotw_header

The output of :func:`dir.list` is the same as with the previous
implementations.

::

    $ python SimpleXMLRPCServer_instance_dotted_names_client.py

    ['ccc_exclude.1mkahl', 'ccc_exclude.BKG3gb', 'ccc_exclude.M5jrgo', 
    'ccc_exclude.SPecwL', 'com.hp.launchport', 'emacs527', 
    'hsperfdata_dhellmann', 'launch-8hGHUp', 'launch-RQnlcc', 
    'launch-trsdly', 'launchd-242.T5UzTy', 'var_backups']


Dispatching Calls
=================

By default, :func:`register_instance()` finds all callable attributes
of the instance with names not starting with an underscore ("``_``") and registers
them with their name. To be more careful about the exposed methods,
custom dispatching logic can be used. For example:

.. include:: SimpleXMLRPCServer_instance_with_prefix.py
    :literal:
    :start-after: #end_pymotw_header

The :func:`public()` method of :class:`MyService` is marked as exposed
to the XML-RPC service while :func:`private()` is not. The
:func:`_dispatch()` method is invoked when the client tries to access
a function that is part of :class:`MyService`. It first enforces the
use of a prefix ("``prefix.``" in this case, but any string can be
used).  Then it requires the function to have an attribute called
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
    private(): 
    ERROR: <Fault 1: '<type \'exceptions.Exception\'>:method 
    "prefix.private" is not supported'>
    public() without prefix: 
    ERROR: <Fault 1: '<type \'exceptions.Exception\'>:method 
    "public" is not supported'>

There are several other ways to override the dispatching mechanism,
including subclassing directly from :class:`SimpleXMLRPCServer`. Refer
to the docstrings in the module for more details.


Introspection API
=================

As with many network services, it is possible to query an XML-RPC
server to ask it what methods it supports and learn how to use
them. :class:`SimpleXMLRPCServer` includes a set of public methods for
performing this introspection. By default they are turned off, but can
be enabled with :func:`register_introspection_functions()`.  Support
for :func:`system.listMethods()` and :func:`system.methodHelp()` can
be added to a service by defining :func:`_listMethods()` and
:func:`_methodHelp()` on the service class.

.. include:: SimpleXMLRPCServer_introspection.py
    :literal:
    :start-after: #end_pymotw_header

In this case, the convenience function :func:`list_public_methods()`
scans an instance to return the names of callable attributes that do
not start with underscore (``_``). Redefine :func:`_listMethods()` to
apply whatever rules are desired.  Similarly, for this basic example
:func:`_methodHelp()` returns the docstring of the function, but could
be written to build a help string from another source.

This client queries the server and reports on all of the publicly
callable methods.

.. include:: SimpleXMLRPCServer_introspection_client.py
    :literal:
    :start-after: #end_pymotw_header

The system methods are included in the results.

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

    `SimpleXMLRPCServer <http://docs.python.org/lib/module-SimpleXMLRPCServer.html>`_
        Standard library documentation for this module.

    `XML-RPC How To <http://www.tldp.org/HOWTO/XML-RPC-HOWTO/index.html>`_
        Describes how to use XML-RPC to implement clients and servers in 
        a variety of languages.

    `XML-RPC Extensions`_
        Specifies an extension to the XML-RPC protocol.

    :mod:`xmlrpclib`
        XML-RPC client library

.. _XML-RPC Extensions: http://ontosys.com/xml-rpc/extensions.php
