==========
 Concepts
==========

Event Loop
==========

The framework provided by :mod:`asyncio` is centered on the *event
loop*, a first class object responsible for efficiently handling I/O
events, system events, and application context changes. Several loop
implementations are provided, to take advantage of operating system
capabilities efficiently. While a reasonable default is usually
selected automatically, it is also possible to pick a particular event
loop implementation from within the application.

An application interacts with the event loop explicitly to register
code to be run, and lets the event loop make the necessary calls into
application code at the right time. For example, network server open
sockets and then register to be told when input events occur on
them. Application code is expected to yield control again after a
short period of time when no more work can be done in the current
context. For example, if there is no more data to read from a socket
the server should yield control back to the event loop.

Coroutines
==========

The mechanism for yielding control back to the event loop depends on
the abstraction layer being used, but underlying everything is the
concept of Python's *coroutines*, special functions that give up
control to the caller without losing their state. Coroutines are
similar to generators, and in fact generators can be used to implement
coroutines in versions of Python without native support for coroutine
objects.

Protocols and Transports
========================

A class-based abstraction layer for *protocols* and *transports* is
also provided for writing code using callbacks instead of writing
coroutines directly. In both models, explicitly changing context by
re-entering the event loop takes the place of implicit context changes
in Python's threading implementation.

Futures
=======

A *future* is a data structure representing the result of work that
has not been completed yet. The event loop can watch for a
:class:`Future` object to be set to done, allowing one part of an
application to wait for another part to finish some work.

Tasks
=====

A :class:`Task` is a subclass of :class:`Future` that knows how to
wrap and manage the execution for a coroutine. Tasks can be scheduled
with the event loop to run when the resources they need are available,
and to produce a result that can be consumed by other coroutines.

..
  The fundamental API for the event loop to interact
  with application code is through a :class:`Future`, an object that
  represents a result that has not yet been computed. 

   *coroutines*, 




..
  In the case of an :mod:`asyncio` coroutine, control is yielded
  when the application needs to wait for something to happen, such as
  I/O buffers to be ready for reading or writing.




  Most programs manage their own control flow, relying on the
  underlying threading or process management of the language runtime or
  operating system to change context as needed.  An application based on
  :mod:`asyncio` lets the event loop decide what code to run at any given time, and 


   sets up its code so that the event loop will run it,
   and then turns control over to the loop.

