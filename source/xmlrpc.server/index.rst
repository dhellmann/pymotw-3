==========================================
 SimpleXMLRPCServer --- An XML-RPC server
==========================================

.. module:: xmlrpc.server
    :synopsis: Implements an XML-RPC server.

:Purpose: Implements an XML-RPC server.

The :mod:`xmlrpc.server` module contains classes for creating
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

.. literalinclude:: xmlrpc_function.py
   :caption:
   :start-after: #end_pymotw_header

The server can be accessed at the URL ``http://localhost:9000`` using
:mod:`xmlrpc.client`.  This client code illustrates how to call the
:func:`list_contents` service from Python.

.. literalinclude:: xmlrpc_function_client.py
   :caption:
   :start-after: #end_pymotw_header

The :class:`ServerProxy` is connected to the server using its base
URL, and then methods are called directly on the proxy. Each method
invoked on the proxy is translated into a request to the server. The
arguments are formatted using XML, and then sent to the server in a
POST message. The server unpacks the XML and determines which function
to call based on the method name invoked from the client. The
arguments are passed to the function, and the return value is
translated back to XML to be returned to the client.

Starting the server gives the following output.

::

    $ python3 xmlrpc_function.py 

    Use Control-C to exit

Running the client in a second window shows the contents of the
``/tmp`` directory.

::

    $ python3 xmlrpc_function_client.py 

    ['com.apple.launchd.aoGXonn8nV', 'com.apple.launchd.ilryIaQugf',
    'example.db.db',
    'KSOutOfProcessFetcher.501.ppfIhqX0vjaTSb8AJYobDV7Cu68=',
    'pymotw_import_example.shelve.db']

After the request is finished, log output appears in the server
window.

::

    $ python3 xmlrpc_function.py 

    Use Control-C to exit
    INFO:root:list_contents(/tmp)
    127.0.0.1 - - [18/Jun/2016 19:54:54] "POST /RPC2 HTTP/1.1" 200 -

The first line of output is from the :func:`logging.info` call inside
:func:`list_contents`. The second line is from the server logging the
request because *logRequests* is ``True``.

Alternate API Names
===================

Sometimes the function names used inside a module or library are not
the names that should be used in the external API.  Names may change
because a platform-specific implementation is loaded, the service API
is built dynamically based on a configuration file, or real functions
can be replaced with stubs for testing.  To register a function with
an alternate name, pass the name as the second argument to
:func:`register_function()`, like this:

.. literalinclude:: xmlrpc_alternate_name.py
   :caption:
   :start-after: #end_pymotw_header

The client should now use the name :func:`dir` instead of
:func:`list_contents`:

.. literalinclude:: xmlrpc_alternate_name_client.py
   :caption:
   :start-after: #end_pymotw_header

Calling :func:`list_contents` results in an error, since the server no
longer has a handler registered by that name.

::

    $ python3 xmlrpc_alternate_name_client.py

    dir(): ['com.apple.launchd.aoGXonn8nV',
    'com.apple.launchd.ilryIaQugf', 'example.db.db',
    'KSOutOfProcessFetcher.501.ppfIhqX0vjaTSb8AJYobDV7Cu68=',
    'pymotw_import_example.shelve.db']

    ERROR: <Fault 1: '<class \'Exception\'>:method "list_contents"
    is not supported'>


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

.. literalinclude:: xmlrpc_dotted_name.py
   :caption:
   :start-after: #end_pymotw_header

To call the service functions in the client, simply refer to them with the
dotted name.

.. literalinclude:: xmlrpc_dotted_name_client.py
   :caption:
   :start-after: #end_pymotw_header

Assuming there is no ``/tmp/EXAMPLE`` file on the current system,
the output for the sample client script is:

::

    $ python3 xmlrpc_dotted_name_client.py

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

.. literalinclude:: xmlrpc_arbitrary_name.py
   :caption:
   :start-after: #end_pymotw_header

Since the registered name contains a space, dot notation cannot be
used to access it directly from the proxy.  Using :func:`getattr` does
work, however.

.. literalinclude:: xmlrpc_arbitrary_name_client.py
   :caption:
   :start-after: #end_pymotw_header

Avoid creating services with names like this, though.  This example is
provided not necessarily because it is a good idea, but because
existing services with arbitrary names exist, and new programs may
need to be able to call them.

::

    $ python3 xmlrpc_arbitrary_name_client.py

    25

Exposing Methods of Objects
===========================

The earlier sections talked about techniques for establishing APIs
using good naming conventions and namespacing. Another way to
incorporate namespacing into an API is to use instances of classes and
expose their methods. The first example can be recreated using an
instance with a single method.

.. literalinclude:: xmlrpc_instance.py
   :caption:
   :start-after: #end_pymotw_header

A client can call the method directly:

.. literalinclude:: xmlrpc_instance_client.py
   :caption:
   :start-after: #end_pymotw_header

The output is::

    $ python3 xmlrpc_instance_client.py

    ['com.apple.launchd.aoGXonn8nV', 'com.apple.launchd.ilryIaQugf',
    'example.db.db',
    'KSOutOfProcessFetcher.501.ppfIhqX0vjaTSb8AJYobDV7Cu68=',
    'pymotw_import_example.shelve.db']

The "``dir.``" prefix for the service has been lost, though.  It can
be restored by defining a class to set up a service tree that can be
invoked from clients.

.. literalinclude:: xmlrpc_instance_dotted_names.py
   :caption:
   :start-after: #end_pymotw_header

By registering the instance of :class:`ServiceRoot` with
*allow_dotted_names* enabled, the server has permission to walk the
tree of objects when a request comes in to find the named method using
:func:`getattr`.

.. literalinclude:: xmlrpc_instance_dotted_names_client.py
   :caption:
   :start-after: #end_pymotw_header

The output of :func:`dir.list` is the same as with the previous
implementations.

::

    $ python3 xmlrpc_instance_dotted_names_client.py

    ['com.apple.launchd.aoGXonn8nV', 'com.apple.launchd.ilryIaQugf',
    'example.db.db',
    'KSOutOfProcessFetcher.501.ppfIhqX0vjaTSb8AJYobDV7Cu68=',
    'pymotw_import_example.shelve.db']


Dispatching Calls
=================

By default, :func:`register_instance()` finds all callable attributes
of the instance with names not starting with an underscore ("``_``") and registers
them with their name. To be more careful about the exposed methods,
custom dispatching logic can be used. For example:

.. literalinclude:: xmlrpc_instance_with_prefix.py
   :caption:
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

.. literalinclude:: xmlrpc_instance_with_prefix_client.py
   :caption:
   :start-after: #end_pymotw_header

and the resulting output, with the expected error messages trapped and
reported::

    $ python3 xmlrpc_instance_with_prefix_client.py

    public(): This is public

    ERROR: <Fault 1: '<class \'Exception\'>:method "prefix.private" is
    not supported'>

    ERROR: <Fault 1: '<class \'Exception\'>:method "public" is not
    supported'>

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

.. literalinclude:: xmlrpc_introspection.py
   :caption:
   :start-after: #end_pymotw_header

In this case, the convenience function :func:`list_public_methods()`
scans an instance to return the names of callable attributes that do
not start with underscore (``_``). Redefine :func:`_listMethods()` to
apply whatever rules are desired.  Similarly, for this basic example
:func:`_methodHelp()` returns the docstring of the function, but could
be written to build a help string from another source.

This client queries the server and reports on all of the publicly
callable methods.

.. literalinclude:: xmlrpc_introspection_client.py
   :caption:
   :start-after: #end_pymotw_header

The system methods are included in the results.

::

    $ python3 xmlrpc_introspection_client.py
    
    ============================================================
    list
    ------------------------------------------------------------
    list(dir_name) => [<filenames>]
    
    Returns a list containing the contents of
    the named directory.
    
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

   * :pydoc:`xmlrpc.server`

   * :mod:`xmlrpc.client` -- XML-RPC client.

   * `XML-RPC How To
     <http://www.tldp.org/HOWTO/XML-RPC-HOWTO/index.html>`_ --
     Describes how to use XML-RPC to implement clients and servers in
     a variety of languages.

   * `XML-RPC Extensions`_ -- Specifies an extension to the XML-RPC
     protocol.

.. _XML-RPC Extensions: http://ontosys.com/xml-rpc/extensions.php
