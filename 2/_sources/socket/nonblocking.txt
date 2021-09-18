=========================================
 Non-blocking Communication and Timeouts
=========================================

By default a :class:`socket` is configured so that sending or
receiving data *blocks*, stopping program execution until the socket
is ready.  Calls to :func:`send` wait for buffer space to be available
for the outgoing data, and calls to :func:`recv` wait for the other
program to send data that can be read.  This form of I/O operation is
easy to understand, but can lead to inefficient operation and even
deadlocks, if both programs end up waiting for the other to send or
receive data.

There are a few ways to work around this situation.  One is to use a
separate thread for communicating with each socket.  This can
introduce other complexities, though, with communication between the
threads.  

Another option is to change the socket to not block at all, and return
immediately if it is not ready to handle the operation.  Use the
:func:`setblocking` method to change the blocking flag for a socket.
The default value is ``1``, which means to block.  Passing a value of
``0`` turns off blocking.  If the socket is has blocking turned off
and it is not ready for the operation, then :class:`socket.error` is
raised.

A compromise solution is to set a timeout value for socket operations.
Use :func:`settimeout` to change the timeout of a :class:`socket` to a
floating point value representing the number of seconds to block
before deciding the socket is not ready for the operation.  When the
timeout expires, a :class:`timeout` exception is raised.

.. seealso::

    Non-blocking I/O is covered in more detail in the examples for
    :mod:`select`.
