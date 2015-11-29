============
 Networking
============

Network communication is used to retrieve data needed for an algorithm
running locally, share information for distributed processing, and to
manage cloud services.  Python's standard library comes complete with
modules for creating network services, as well as for accessing
existing services remotely.

The low-level :mod:`socket` library provides direct access to the
native C socket library, and can be used to communicate with any
network service.  :mod:`select` watches multiple sockets
simultaneously, and is useful for allowing network servers to
communicate with multiple clients simultaneously.

The frameworks in :mod:`SocketServer` abstract out a lot of the
repetitive work necessary to create a new network server.  The
classes can be combined to create servers that fork or use threads and
support TCP or UDP.  Only the actual message handling needs to be
provided by the application.

:mod:`asyncore` implements an asynchronous networking stack with a
callback-based API.  It encapsulates the polling loop and buffering,
and invokes appropriate handlers when data is received.  The framework
in :mod:`asynchat` simplifies the work needed to create bi-directional
message based protocols on top of :mod:`asyncore`.

..
   .. toctree::
       :maxdepth: 1

       socket/index
       select/index
       SocketServer/index
       asyncore/index
       asynchat/index


..    io/index
..    ssl/index
