===========================
 Working with Subprocesses
===========================

It is frequently necessary to work with other programs and
processes. As with network I/O, :mod:`asyncio` includes two
abstractions for starting another program and then interacting with
it.

Protocol Abstraction
====================

This example uses a coroutine to launch a process to run ``df`` to
find the free space on local disks. It uses :func:`subprocess_exec` to
to launch the process and tie it to a protocol class that knows how to
read the ``df`` command output and parse it. Because both the
``stdin`` and ``stderr`` arguments are set to ``None``, those
communication channels are not connected to the new process.

.. literalinclude:: asyncio_subprocess_protocol.py
   :lines: 58-77

The class :class:`DFProtocol` is derived from
:class:`SubprocessProtocol`, which defines the API for a class to
communicate with another process through pipes. The ``done`` argument
is expected to be a :class:`Future` that the caller will use to watch
for the process to finish.

.. literalinclude:: asyncio_subprocess_protocol.py
   :lines: 13-18

As with socket communication, :func:`connection_made` is invoked when
the input channels to the new process are set up. The ``transport``
argument is an instance of a subclass of
:class:`BaseSubprocessTransport`. It can read data output by the
process and write data to the process' input, if the process was
configured to receive input.

.. literalinclude:: asyncio_subprocess_protocol.py
   :lines: 20-22

When the process has generated output, :func:`pipe_data_received` is
invoked with the file descriptor where the data was emitted, and the
actual data read from the pipe. The protocol class saves the data in a
buffer for later processing.

.. literalinclude:: asyncio_subprocess_protocol.py
   :lines: 24-26

When the process terminates, :func:`process_exited` is called. The
exit code of the process is available from the transport object by
calling :func:`get_returncode`. In this case, if there is no error
reported the available output is decoded and parsed before being
returned through the :class:`Future` instance. If there is an error,
the results are assumed to be empty. Setting the result of the future
tells :func:`run_df` that the process has exited, so it cleans up and
then returns the results.

.. literalinclude:: asyncio_subprocess_protocol.py
   :lines: 29-38

The command output is parsed into a sequence of dictionaries mapping
the header names to their values for each line of output, and the
resulting list is returned.

.. literalinclude:: asyncio_subprocess_protocol.py
   :lines: 40-55

The :func:`run_df` coroutine is run using :func:`run_until_complete`,
then the results are examined and the free space on each device is
printed.

.. literalinclude:: asyncio_subprocess_protocol.py
   :lines: 80-

The output below shows the sequence of steps taken, and the free space
on three drives on the system where it was run.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_subprocess_protocol.py'))
.. }}}

::

	$ python3 asyncio_subprocess_protocol.py
	
	in run_df
	launching process
	transport <_UnixSubprocessTransport pid=78087 running stdout=<_U
	nixReadPipeTransport fd=7 polling>>
	process started 78087
	waiting for process to complete
	read 332 bytes
	process exited
	return code 0
	parsing results
	
	Free space:
	/                        : 233Gi
	/Volumes/hubertinternal  : 157Gi
	/Volumes/hubert-tm       : 2.3Ti

.. {{{end}}}

