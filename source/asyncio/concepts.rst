==========
 Concepts
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

The mechanism for yielding depends on the abstraction layer being
used, but underlying everything is the concept of Python's
*coroutines*, functions that give up control to the caller without
losing their state. Python 3.5 introduced new language features to
define such co-routines natively using ``async def`` and ``await``,
but earlier versions of Python 3 can use generator functions wrapped
with the ``@asyncio.coroutine`` decorator and ``yield from`` to
achieve the same effect.  A class-based abstraction layer for
*protocols* and *transports* is also provided for writing code using
callbacks instead of writing coroutines directly. In both models,
explicitly changing context by re-entering the event loop takes the
place of implicit context changes in Python's threading
implementation.



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

