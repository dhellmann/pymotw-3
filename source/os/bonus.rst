File System Permissions
=======================

The function :func:`access()` can be used to test the access rights a
process has for a file.

.. include:: os_access.py
    :literal:
    :start-after: #end_pymotw_header

The results will vary depending on how the example code is installed,
but the output will be similar to this:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_access.py'))
.. }}}

::

	$ python os_access.py
	
	Testing: os_access.py
	Exists: True
	Readable: True
	Writable: True
	Executable: False

.. {{{end}}}


The library documentation for :func:`access()` includes two special
warnings. First, there is not much sense in calling :func:`access()`
to test whether a file can be opened before actually calling
:func:`open()` on it. There is a small, but real, window of time
between the two calls during which the permissions on the file could
change. The other warning applies mostly to networked file systems that
extend the POSIX permission semantics. Some file system types may
respond to the POSIX call that a process has permission to access a
file, then report a failure when the attempt is made using
:func:`open()` for some reason not tested via the POSIX call. All in
all, it is better to call :func:`open()` with the required mode and
catch the :class:`IOError` raised if there is a problem.
