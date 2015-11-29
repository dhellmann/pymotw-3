=======================
 Processes and Threads
=======================

Python includes sophisticated tools for managing concurrent operations
using processes and threads.  Even many relatively simple programs can
be made to run faster by applying techniques for running parts of the
job concurrently using these modules.

:mod:`subprocess` provides an API for creating and communicating with
secondary processes.  It is especially good for running programs that
produce or consume text, since the API supports passing data back and
forth through the standard input and output channels of the new
process.

The :mod:`signal` module exposes the Unix signal mechanism for sending
events to other processes.  The signals are processed asynchronously,
usually by interrupting what the program is doing at the time the
signal arrives.  Signalling is useful as a coarse messaging system,
but other inter-process communication techniques are more reliable and
can deliver more complicated messages.

:mod:`threading` includes a high-level, object oriented, API for
working with concurrency from Python.  :class:`Thread` objects run
concurrently within the same process and share memory.  Using threads
is an easy way to scale for tasks that are more I/O bound than CPU
bound.

The :mod:`multiprocessing` module mirrors :mod:`threading`, except
that instead of a :class:`Thread` class it provides a
:class:`Process`.  Each :class:`Process` is a true system process
without shared memory, but :mod:`multiprocessing` provides features
for sharing data and passing messages between them so that in many
cases converting from threads to processes is as simple as changing a
few :command:`import` statements.

..
   .. toctree::
      :maxdepth: 1

      subprocess/index
      signal/index
      threading/index
      multiprocessing/index
   
