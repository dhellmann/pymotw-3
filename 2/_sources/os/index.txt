============================================================
os -- Portable access to operating system specific features.
============================================================

.. module:: os
    :synopsis: Portable access to operating system specific features.

:Purpose: Portable access to operating system specific features.
:Available In: 1.4 (or earlier)

The :mod:`os` module provides a wrapper for platform specific modules
such as :mod:`posix`, :mod:`nt`, and :mod:`mac`. The API for functions
available on all platform should be the same, so using the :mod:`os`
module offers some measure of portability. Not all functions are
available on all platforms, however. Many of the process management
functions described in this summary are not available for Windows.

The Python documentation for the :mod:`os` module is subtitled
"Miscellaneous operating system interfaces". The module consists
mostly of functions for creating and managing running processes or
filesystem content (files and directories), with a few other bits of
functionality thrown in besides.

.. note::

    Some of the example code below will only work on Unix-like
    operating systems.

Process Owner
=============

The first set of functions to cover are used for determining and
changing the process owner ids. These are mostly useful to authors of
daemons or special system programs which need to change permission
level rather than running as ``root``. This section does not try to
explain all of the intricate details of Unix security, process owners,
etc. See the References list below for more details.

This first script shows the real and effective user and group
information for a process, and then changes the effective values. This
is similar to what a daemon would need to do when it starts as root
during a system boot, to lower the privilege level and run as a
different user. 

.. note::

  Before running the example, change the :data:`TEST_GID` and
  :data:`TEST_UID` values to match a real user.

.. include:: os_process_user_example.py
    :literal:
    :start-after: #end_pymotw_header

When run as user with id of 527 and group 501 on OS X, this output is
produced:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_process_user_example.py'))
.. }}}

::

	$ python os_process_user_example.py
	
	BEFORE CHANGE:
	Effective User  : 527
	Effective Group : 501
	Actual User     : 527 dhellmann
	Actual Group    : 501
	Actual Groups   : [501, 401, 101, 500, 12, 33, 61, 80, 98, 100, 204, 102]
	
	CHANGED GROUP:
	Effective User  : 527
	Effective Group : 501
	Actual User     : 527 dhellmann
	Actual Group    : 501
	Actual Groups   : [501, 401, 101, 500, 12, 33, 61, 80, 98, 100, 204, 102]
	
	CHANGE USER:
	Effective User  : 527
	Effective Group : 501
	Actual User     : 527 dhellmann
	Actual Group    : 501
	Actual Groups   : [501, 401, 101, 500, 12, 33, 61, 80, 98, 100, 204, 102]
	

.. {{{end}}}

Notice that the values do not change. When not running as root,
processes cannot change their effective owner values. Any attempt to
set the effective user id or group id to anything other than that of
the current user causes an :ref:`OSError <exceptions-OSError>`.

Running the same script using :command:`sudo` so that it starts out
with root privileges is a different story.

.. Don't use cog here because sudo sometimes asks for a password.

::

	$ sudo python os_process_user_example.py
	BEFORE CHANGE:
	Effective User  : 0
	Effective Group : 0
	Actual User	 : 0 dhellmann
	Actual Group	: 0
	Actual Groups   : [0, 1, 2, 8, 29, 3, 9, 4, 5, 80, 20]
	
	CHANGED GROUP:
	Effective User  : 0
	Effective Group : 501
	Actual User	 : 0 dhellmann
	Actual Group	: 0
	Actual Groups   : [501, 1, 2, 8, 29, 3, 9, 4, 5, 80, 20]
	
	CHANGE USER:
	Effective User  : 527
	Effective Group : 501
	Actual User	 : 0 dhellmann
	Actual Group	: 0
	Actual Groups   : [501, 1, 2, 8, 29, 3, 9, 4, 5, 80, 20]
	

In this case, since it starts as root, it can change the effective
user and group for the process. Once the effective UID is changed, the
process is limited to the permissions of that user. Since non-root
users cannot change their effective group, the program needs to change
the group before changing the user.

Besides finding and changing the process owner, there are functions for
determining the current and parent process id, finding and changing the
process group and session ids, as well as finding the controlling terminal id.
These can be useful for sending signals between processes or for complex
applications such as writing a command line shell.

Process Environment
===================

Another feature of the operating system exposed to a program though
the :mod:`os` module is the environment. Variables set in the
environment are visible as strings that can be read through
:data:`os.environ` or :func:`getenv()`. Environment variables are
commonly used for configuration values such as search paths, file
locations, and debug flags. This example shows how to retrieve an
environment variable, and pass a value through to a child process.

.. include:: os_environ_example.py
    :literal:
    :start-after: #end_pymotw_header


The :data:`os.environ` object follows the standard Python mapping API
for retrieving and setting values. Changes to :data:`os.environ` are
exported for child processes.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u os_environ_example.py'))
.. }}}

::

	$ python -u os_environ_example.py
	
	Initial value: None
	Child process:
	
	
	Changed value: THIS VALUE WAS CHANGED
	Child process:
	THIS VALUE WAS CHANGED
	
	Removed value: None
	Child process:
	

.. {{{end}}}


Process Working Directory
=========================

Operating systems with hierarchical filesystems have a concept of the
*current working directory* -- the directory on the filesystem the
process uses as the starting location when files are accessed with
relative paths.  The current working directory can be retrieved with
:func:`getcwd` and changed with :func:`chdir`.

.. include:: os_cwd_example.py
    :literal:
    :start-after: #end_pymotw_header

:const:`os.curdir` and :const:`os.pardir` are used to refer to the
current and parent directories in a portable manner. The output should
not be surprising:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_cwd_example.py'))
.. }}}

::

	$ python os_cwd_example.py
	
	Starting: /Users/dhellmann/Documents/PyMOTW/src/PyMOTW/os
	Moving up one: ..
	After move: /Users/dhellmann/Documents/PyMOTW/src/PyMOTW

.. {{{end}}}


Pipes
=====

The :mod:`os` module provides several functions for managing the I/O
of child processes using *pipes*. The functions all work essentially
the same way, but return different file handles depending on the type
of input or output desired. For the most part, these functions are
made obsolete by the :mod:`subprocess` module (added in Python 2.4),
but there is a good chance legacy code uses them.

The most commonly used pipe function is :func:`popen()`. It creates a
new process running the command given and attaches a single stream to
the input or output of that process, depending on the *mode*
argument. While :func:`popen` functions work on Windows, some of these
examples assume a Unix-like shell. 

.. include:: os_popen.py
    :literal:
    :start-after: #end_pymotw_header

The descriptions of the streams also assume Unix-like terminology:

* stdin - The "standard input" stream for a process (file descriptor 0) is
  readable by the process. This is usually where terminal input goes.

* stdout - The "standard output" stream for a process (file descriptor
  1) is writable by the process, and is used for displaying regular
  output to the user.

* stderr - The "standard error" stream for a process (file descriptor 2) is
  writable by the process, and is used for conveying error messages.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u os_popen.py'))
.. }}}

::

	$ python -u os_popen.py
	
	popen, read:
		stdout: 'to stdout\n'
	
	popen, write:
		stdin: to stdin

.. {{{end}}}

The caller can only read from or write to the streams associated with
the child process, which limits the usefulness. The other
:func:`popen` variants provide additional streams so it is possible to
work with stdin, stdout, and stderr as needed.

For example, :func:`popen2()` returns a write-only stream attached to
stdin of the child process, and a read-only stream attached to its
stdout.

.. include:: os_popen2.py
    :literal:
    :start-after: #end_pymotw_header


This simplistic example illustrates bi-directional communication. The
value written to stdin is read by ``cat`` (because of the ``'-'``
argument), then written back to stdout. A more complicated process
could pass other types of messages back and forth through the pipe;
even serialized objects.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u os_popen2.py'))
.. }}}

::

	$ python -u os_popen2.py
	
	popen2:
		pass through: 'through stdin to stdout'

.. {{{end}}}

In most cases, it is desirable to have access to both stdout and
stderr. The stdout stream is used for message passing and the stderr
stream is used for errors, so reading from it separately reduces the
complexity for parsing any error messages. The :func:`popen3()`
function returns three open streams tied to stdin, stdout, and stderr
of the new process.

.. include:: os_popen3.py
    :literal:
    :start-after: #end_pymotw_header

Notice that the program has to read from and close both stdout and
stderr *separately*. There are some related to flow control and
sequencing when dealing with I/O for multiple processes. The I/O is
buffered, and if the caller expects to be able to read all of the data
from a stream then the child process must close that stream to
indicate the end-of-file. For more information on these issues, refer
to the `Flow Control Issues
<http://docs.python.org/2.7/library/popen2.html#popen2-flow-control>`__
section of the Python library documentation.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u os_popen3.py'))
.. }}}

::

	$ python -u os_popen3.py
	
	popen3:
		pass through: 'through stdin to stdout'
		stderr: ';to stderr\n'

.. {{{end}}}

And finally, :func:`popen4()` returns 2 streams, stdin and a merged
stdout/stderr.  This is useful when the results of the command need to
be logged, but not parsed directly.

.. include:: os_popen4.py
    :literal:
    :start-after: #end_pymotw_header

All of the messages written to both stdout and stderr are read
together.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u os_popen4.py'))
.. }}}

::

	$ python -u os_popen4.py
	
	popen4:
		combined output: 'through stdin to stdout;to stderr\n'

.. {{{end}}}

Besides accepting a single string command to be given to the shell for
parsing, :func:`popen2()`, :func:`popen3()`, and :func:`popen4()` also
accept a sequence of strings (command, followed by arguments). 

.. include:: os_popen2_seq.py
    :literal:
    :start-after: #end_pymotw_header

In this case, the arguments are not processed by the shell.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u os_popen2_seq.py'))
.. }}}

::

	$ python -u os_popen2_seq.py
	
	popen2, cmd as sequence:
		pass through: 'through stdin to stdout'

.. {{{end}}}


File Descriptors
================

:mod:`os` includes the standard set of functions for working with
low-level *file descriptors* (integers representing open files owned
by the current process). This is a lower-level API than is provided by
:class:`file` objects. They are not covered here because it is
generally easier to work directly with :class:`file` objects. Refer to
the library documentation for details.

Filesystem Permissions
======================

The function :func:`access()` can be used to test the access rights a
process has for a file.

.. include:: os_access.py
    :literal:
    :start-after: #end_pymotw_header

The results will vary depending on how the example code is installed,
but it will look something like this:

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
warnings. First, there isn't much sense in calling :func:`access()`
to test whether a file can be opened before actually calling
:func:`open()` on it. There is a small, but real, window of time
between the two calls during which the permissions on the file could
change. The other warning applies mostly to networked filesystems that
extend the POSIX permission semantics. Some filesystem types may
respond to the POSIX call that a process has permission to access a
file, then report a failure when the attempt is made using
:func:`open()` for some reason not tested via the POSIX call. All in
all, it is better to call :func:`open()` with the required mode and
catch the :ref:`IOError <exceptions-IOError>` raised if there is a
problem.

More detailed information about the file can be accessed using
:func:`stat()` or :func:`lstat()` (for checking the status of
something that might be a symbolic link).

.. include:: os_stat.py
    :literal:
    :start-after: #end_pymotw_header

Once again, the output will vary depending on how the example code was
installed. Try passing different filenames on the command line to
``os_stat.py``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_stat.py'))
.. }}}

::

	$ python os_stat.py
	
	os.stat(os_stat.py):
		Size: 1516
		Permissions: 0100644
		Owner: 527
		Device: 234881026
		Last modified: Sat Feb 19 19:18:23 2011

.. {{{end}}}


On Unix-like systems, file permissions can be changed using
:func:`chmod()`, passing the mode as an integer. Mode values can be
constructed using constants defined in the :mod:`stat` module.  This
example toggles the user's execute permission bit:

.. include:: os_stat_chmod.py
    :literal:
    :start-after: #end_pymotw_header


The script assumes it has the permissions necessary to modify the mode
of the file when run.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_stat_chmod.py'))
.. }}}

::

	$ python os_stat_chmod.py
	
	Adding execute permission

.. {{{end}}}

.. _os-directories:

Directories
===========

There are several functions for working with directories on the filesystem,
including creating, listing contents, and removing them.

.. include:: os_directories.py
    :literal:
    :start-after: #end_pymotw_header

There are two sets of functions for creating and deleting
directories. When creating a new directory with :func:`mkdir()`,
all of the parent directories must already exist. When removing a
directory with :func:`rmdir()`, only the leaf directory (the last
part of the path) is actually removed. In contrast,
:func:`makedirs()` and :func:`removedirs()` operate on all of
the nodes in the path.  :func:`makedirs()` will create any parts of
the path which do not exist, and :func:`removedirs()` will remove
all of the parent directories (assuming it can).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_directories.py'))
.. }}}

::

	$ python os_directories.py
	
	Creating os_directories_example
	Creating os_directories_example/example.txt
	Listing os_directories_example
	['example.txt']
	Cleaning up

.. {{{end}}}


Symbolic Links
==============

For platforms and filesystems that support them, there are functions
for working with symlinks.

.. include:: os_symlinks.py
    :literal:
    :start-after: #end_pymotw_header


Although :mod:`os` includes :func:`tempnam()` for creating
temporary filenames, it is not as secure as the :mod:`tempfile` module
and produces a :ref:`RuntimeWarning <exceptions-RuntimeWarning>`
message when it is used. In general it is better to use
:mod:`tempfile`, as in this example.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_symlinks.py'))
.. }}}

::

	$ python os_symlinks.py
	
	Creating link /var/folders/5q/8gk0wq888xlggz008k8dr7180000hg/T/tmpt1_Bsr -> os_symlinks.py
	Permissions: 0120755
	Points to: os_symlinks.py

.. {{{end}}}


Walking a Directory Tree
========================

The function :func:`walk()` traverses a directory recursively and
for each directory generates a tuple containing the directory path,
any immediate sub-directories of that path, and the names of any files
in that directory.  

.. include:: os_walk.py
    :literal:
    :start-after: #end_pymotw_header

This example shows a recursive directory listing.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_walk.py ../zipimport'))
.. }}}

::

	$ python os_walk.py ../zipimport
	
	
	../zipimport
		__init__.py
		__init__.pyc
		example_package/
		index.rst
		zipimport_example.zip
		zipimport_find_module.py
		zipimport_find_module.pyc
		zipimport_get_code.py
		zipimport_get_code.pyc
		zipimport_get_data.py
		zipimport_get_data.pyc
		zipimport_get_data_nozip.py
		zipimport_get_data_nozip.pyc
		zipimport_get_data_zip.py
		zipimport_get_data_zip.pyc
		zipimport_get_source.py
		zipimport_get_source.pyc
		zipimport_is_package.py
		zipimport_is_package.pyc
		zipimport_load_module.py
		zipimport_load_module.pyc
		zipimport_make_example.py
		zipimport_make_example.pyc
	
	../zipimport/example_package
		README.txt
		__init__.py
		__init__.pyc

.. {{{end}}}

.. _os-system:

Running External Commands
=========================

.. warning::

    Many of these functions for working with processes have limited
    portability. For a more consistent way to work with processes in a
    platform independent manner, see the :mod:`subprocess` module
    instead.

The simplest way to run a separate command, without interacting with
it at all, is :func:`system()`. It takes a single string which is
the command line to be executed by a sub-process running a shell.

.. include:: os_system_example.py
    :literal:
    :start-after: #end_pymotw_header

The return value of :func:`system` is the exit value of the shell
running the program packed into a 16 bit number, with the high byte
the exit status and the low byte the signal number that caused the
process to die, or zero.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u os_system_example.py'))
.. }}}

::

	$ python -u os_system_example.py
	
	total 248
	-rw-r--r--  1 dhellmann  dhellmann      0 Feb 19  2011 __init__.py
	-rw-r--r--  1 dhellmann  dhellmann  22700 Jul  8  2011 index.rst
	-rw-r--r--  1 dhellmann  dhellmann   1360 Feb 19  2011 os_access.py
	-rw-r--r--  1 dhellmann  dhellmann   1292 Feb 19  2011 os_cwd_example.py
	-rw-r--r--  1 dhellmann  dhellmann   1499 Feb 19  2011 os_directories.py
	-rw-r--r--  1 dhellmann  dhellmann   1573 Feb 19  2011 os_environ_example.py
	-rw-r--r--  1 dhellmann  dhellmann   1241 Feb 19  2011 os_exec_example.py
	-rw-r--r--  1 dhellmann  dhellmann   1267 Feb 19  2011 os_fork_example.py
	-rw-r--r--  1 dhellmann  dhellmann   1703 Feb 19  2011 os_kill_example.py
	-rw-r--r--  1 dhellmann  dhellmann   1476 Feb 19  2011 os_popen.py
	-rw-r--r--  1 dhellmann  dhellmann   1506 Feb 19  2011 os_popen2.py
	-rw-r--r--  1 dhellmann  dhellmann   1528 Feb 19  2011 os_popen2_seq.py
	-rw-r--r--  1 dhellmann  dhellmann   1658 Feb 19  2011 os_popen3.py
	-rw-r--r--  1 dhellmann  dhellmann   1567 Feb 19  2011 os_popen4.py
	-rw-r--r--  1 dhellmann  dhellmann   1395 Feb 19  2011 os_process_id_example.py
	-rw-r--r--  1 dhellmann  dhellmann   1896 Feb 19  2011 os_process_user_example.py
	-rw-r--r--  1 dhellmann  dhellmann   1206 Feb 19  2011 os_spawn_example.py
	-rw-r--r--  1 dhellmann  dhellmann   1516 Feb 19  2011 os_stat.py
	-rw-r--r--  1 dhellmann  dhellmann   1751 Feb 19  2011 os_stat_chmod.py
	-rwxr--r--  1 dhellmann  dhellmann      8 Feb 21 06:36 os_stat_chmod_example.txt
	-rw-r--r--  1 dhellmann  dhellmann   1421 Feb 19  2011 os_symlinks.py
	-rw-r--r--  1 dhellmann  dhellmann   1250 Feb 19  2011 os_system_background.py
	-rw-r--r--  1 dhellmann  dhellmann   1191 Feb 19  2011 os_system_example.py
	-rw-r--r--  1 dhellmann  dhellmann   1214 Feb 19  2011 os_system_shell.py
	-rw-r--r--  1 dhellmann  dhellmann   1499 Feb 19  2011 os_wait_example.py
	-rw-r--r--  1 dhellmann  dhellmann   1555 Feb 19  2011 os_waitpid_example.py
	-rw-r--r--  1 dhellmann  dhellmann   1643 Feb 19  2011 os_walk.py

.. {{{end}}}


Since the command is passed directly to the shell for processing, it can even
include shell syntax such as globbing or environment variables:

.. include:: os_system_shell.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u os_system_shell.py'))
.. }}}

::

	$ python -u os_system_shell.py
	
	drwx------  10 dhellmann  dhellmann  340 Feb 21 06:36 /var/folders/5q/8gk0wq888xlggz008k8dr7180000hg/T/

.. {{{end}}}


Unless the command is explicitly run in the background, the call to
:func:`system()` blocks until it is complete. Standard input,
output, and error from the child process are tied to the appropriate
streams owned by the caller by default, but can be redirected using
shell syntax.

.. include:: os_system_background.py
    :literal:
    :start-after: #end_pymotw_header


This is getting into shell trickery, though, and there are better ways to
accomplish the same thing.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u os_system_background.py'))
.. }}}

::

	$ python -u os_system_background.py
	
	Calling...
	Thu Feb 21 06:36:14 EST 2013
	Sleeping...
	Thu Feb 21 06:36:18 EST 2013

.. {{{end}}}

.. _creating-processes-with-os-fork:

Creating Processes with os.fork()
=================================

The POSIX functions :func:`fork()` and :func:`exec*()` (available
under Mac OS X, Linux, and other UNIX variants) are exposed via the
:mod:`os` module. Entire books have been written about reliably using
these functions, so check the library or bookstore for more details
than are presented here.

To create a new process as a clone of the current process, use
:func:`fork()`:

.. include:: os_fork_example.py
    :literal:
    :start-after: #end_pymotw_header

The output will vary based on the state of the system each time the
example is run, but it will look something like:

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u os_fork_example.py'))
.. }}}

::

	$ python -u os_fork_example.py
	
	Child process id: 14167
	I am the child

.. {{{end}}}

After the fork, there are two processes running the same code. For a
program to tell which one it is in, it needs to check the return value
of :func:`fork()`. If the value is ``0``, the current process is the
child.  If it is not ``0``, the program is running in the parent
process and the return value is the process id of the child process.

From the parent process, it is possible to send the child
signals. This is a bit more complicated to set up, and uses the
:mod:`signal` module. First, define a signal handler to be invoked
when the signal is received.

.. literalinclude:: os_kill_example.py
   :lines: 33-40

Then :func:`fork`, and in the parent pause a short amount of time
before sending a :const:`USR1` signal using :func:`kill()`. The
short pause gives the child process time to set up the signal handler.

.. literalinclude:: os_kill_example.py
   :lines: 42-48

In the child, set up the signal handler and go to sleep for a while to
give the parent time to send the signal:

.. literalinclude:: os_kill_example.py
   :language: python
   :lines: 49-53

A real application, wouldn't need (or want) to call :func:`sleep()`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_kill_example.py'))
.. }}}

::

	$ python os_kill_example.py
	
	Forking...
	PARENT: Pausing before sending signal...
	PARENT: Signaling 14170
	Forking...
	CHILD: Setting up signal handler
	CHILD: Pausing to wait for signal
	Received USR1 in process 14170

.. {{{end}}}


A simple way to handle separate behavior in the child process is to
check the return value of :func:`fork()` and branch. More complex
behavior may call for more code separation than a simple branch. In
other cases, there may be an existing program that needs to be
wrapped. For both of these situations, the :func:`exec*()` series
of functions can be used to run another program. 

.. include:: os_exec_example.py
    :literal:
    :start-after: #end_pymotw_header

When a program is "execed", the code from that program replaces the
code from the existing process.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_exec_example.py'))
.. }}}

::

	$ python os_exec_example.py
	
	total 320
	-rw-r-----  1 root        _lp         1193 Feb 21 06:26 025c6512ef714
	-rw-r--r--  1 root        wheel      70150 Feb 19 09:01 Carbon Copy Cloner-96-8F64ABE0-B932-4033-B71B-8815A11C13F1.growlRegDict
	-rw-r--r--  1 root        wheel      70150 Feb 19 09:01 Carbon Copy Cloner-96-F29FA27F-20E9-45F4-8FEB-B5BE8104239A.growlRegDict
	-rw-r--r--  1 dhellmann   wheel          0 Feb 19 09:03 CrashReportCopyLock-Doug Hellmann’s iPhone
	-rw-r--r--  1 dhellmann   wheel          0 Feb 19 23:52 CrashReportCopyLock-Fry
	-rw-r--r--  1 dhellmann   wheel          0 Feb 19 10:02 CrashReportCopyLock-Nibbler
	-rw-r--r--  1 dhellmann   wheel      12288 Feb 21 06:35 example.db
	drwx------  3 dhellmann   wheel        102 Feb 19 09:00 launch-CRQRox
	drwx------  3 dhellmann   wheel        102 Feb 19 15:39 launch-EId8eS
	drwx------  3 dhellmann   wheel        102 Feb 19 09:00 launch-XiBNeS
	drwx------  3 dhellmann   wheel        102 Feb 19 09:00 launch-m0jqKW
	drwx------  3 dhellmann   wheel        102 Feb 19 09:00 launch-n4P253
	drwx------  3 dhellmann   wheel        102 Feb 19 09:00 launchd-328.RnuGVc
	drwx------  3 _spotlight  wheel        102 Feb 19 09:06 launchd-587.onAzLG
	drwx------  2 dhellmann   wheel         68 Feb 19 15:46 ssh-DUxXnX9KUd
	drwxr-xr-x  2 dhellmann   dhellmann     68 Feb 20 03:15 var_backups

.. {{{end}}}


There are many variations of :func:`exec*()`, depending on the form in
which the arguments are available, whether the path and environment of
the parent process should be be copied to the child, etc. Refer to the
library documentation for complete details.

For all variations, the first argument is a path or filename and the
remaining arguments control how that program runs. They are either
passed as command line arguments or override the process "environment"
(see :data:`os.environ` and :data:`os.getenv`).

Waiting for a Child
===================

Many computationally intensive programs use multiple processes to work
around the threading limitations of Python and the Global Interpreter
Lock. When starting several processes to run separate tasks, the
master will need to wait for one or more of them to finish before
starting new ones, to avoid overloading the server. There are a few
different ways to do that using :func:`wait()` and related functions.

When it does not matter which child process might exit first, use
:func:`wait()`.  It returns as soon as any child process exits.

.. include:: os_wait_example.py
    :literal:
    :start-after: #end_pymotw_header


The return value from :func:`wait()` is a tuple containing the
process id and exit status ("a 16-bit number, whose low byte is the
signal number that killed the process, and whose high byte is the exit
status").

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_wait_example.py'))
.. }}}

::

	$ python os_wait_example.py
	
	PARENT: Forking 0
	WORKER 0: Starting
	WORKER 0: Finishing
	PARENT: Forking 0
	PARENT: Forking 1
	WORKER 1: Starting
	WORKER 1: Finishing
	PARENT: Forking 0
	PARENT: Forking 1
	PARENT: Forking 2
	WORKER 2: Starting
	WORKER 2: Finishing
	PARENT: Forking 0
	PARENT: Forking 1
	PARENT: Forking 2
	PARENT: Waiting for 0
	PARENT: (14176, 0)
	PARENT: Waiting for 1
	PARENT: (14177, 256)
	PARENT: Waiting for 2
	PARENT: (14178, 512)

.. {{{end}}}

To wait for a specific process, use :func:`waitpid()`.

.. include:: os_waitpid_example.py
    :literal:
    :start-after: #end_pymotw_header

Pass the process id of the target process, and :func:`waitpid` blocks
until that process exits.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_waitpid_example.py'))
.. }}}

::

	$ python os_waitpid_example.py
	
	PARENT: Forking 0
	WORKER 0: Starting
	WORKER 0: Finishing
	PARENT: Forking 0
	PARENT: Forking 1
	WORKER 1: Starting
	WORKER 1: Finishing
	PARENT: Forking 0
	PARENT: Forking 1
	PARENT: Forking 2
	WORKER 2: Starting
	WORKER 2: Finishing
	PARENT: Forking 0
	PARENT: Forking 1
	PARENT: Forking 2
	PARENT: Waiting for 14181
	PARENT: (14181, 0)
	PARENT: Waiting for 14182
	PARENT: (14182, 256)
	PARENT: Waiting for 14183
	PARENT: (14183, 512)

.. {{{end}}}

:func:`wait3()` and :func:`wait4()` work in a similar manner, but
return more detailed information about the child process with the pid,
exit status, and resource usage.

Spawn
=====

As a convenience, the :func:`spawn*()` family of functions handles the
:func:`fork()` and :func:`exec*()` in one statement:

.. include:: os_spawn_example.py
    :literal:
    :start-after: #end_pymotw_header

The first argument is a mode indicating whether or not to wait for the
process to finish before returning.  This example waits.  Use
:const:`P_NOWAIT` to let the other process start, but then resume in
the current process.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_spawn_example.py'))
.. }}}

::

	$ python os_spawn_example.py
	
	total 320
	-rw-r-----  1 root        _lp         1193 Feb 21 06:26 025c6512ef714
	-rw-r--r--  1 root        wheel      70150 Feb 19 09:01 Carbon Copy Cloner-96-8F64ABE0-B932-4033-B71B-8815A11C13F1.growlRegDict
	-rw-r--r--  1 root        wheel      70150 Feb 19 09:01 Carbon Copy Cloner-96-F29FA27F-20E9-45F4-8FEB-B5BE8104239A.growlRegDict
	-rw-r--r--  1 dhellmann   wheel          0 Feb 19 09:03 CrashReportCopyLock-Doug Hellmann’s iPhone
	-rw-r--r--  1 dhellmann   wheel          0 Feb 19 23:52 CrashReportCopyLock-Fry
	-rw-r--r--  1 dhellmann   wheel          0 Feb 19 10:02 CrashReportCopyLock-Nibbler
	-rw-r--r--  1 dhellmann   wheel      12288 Feb 21 06:35 example.db
	drwx------  3 dhellmann   wheel        102 Feb 19 09:00 launch-CRQRox
	drwx------  3 dhellmann   wheel        102 Feb 19 15:39 launch-EId8eS
	drwx------  3 dhellmann   wheel        102 Feb 19 09:00 launch-XiBNeS
	drwx------  3 dhellmann   wheel        102 Feb 19 09:00 launch-m0jqKW
	drwx------  3 dhellmann   wheel        102 Feb 19 09:00 launch-n4P253
	drwx------  3 dhellmann   wheel        102 Feb 19 09:00 launchd-328.RnuGVc
	drwx------  3 _spotlight  wheel        102 Feb 19 09:06 launchd-587.onAzLG
	drwx------  2 dhellmann   wheel         68 Feb 19 15:46 ssh-DUxXnX9KUd
	drwxr-xr-x  2 dhellmann   dhellmann     68 Feb 20 03:15 var_backups

.. {{{end}}}


.. seealso::

    `os <https://docs.python.org/2/library/os.html>`_
        Standard library documentation for this module.

    :mod:`subprocess`
        The subprocess module supersedes os.popen().

    :mod:`multiprocessing` 
        The multiprocessing module makes working with extra processes
        easier than doing all of the work yourself.

    :mod:`tempfile`
        The tempfile module for working with temporary files.

    *Unix Manual Page Introduction*
        Includes definitions of real and effective ids, etc.
        
        http://www.scit.wlv.ac.uk/cgi-bin/mansec?2+intro

    *Speaking UNIX, Part 8.*
        Learn how UNIX multitasks.
        
        http://www.ibm.com/developerworks/aix/library/au-speakingunix8/index.html

    *Unix Concepts*
        For more discussion of stdin, stdout, and stderr.
        
        http://www.linuxhq.com/guides/LUG/node67.html

    *Delve into Unix Process Creation*
        Explains the life cycle of a UNIX process.
        
        http://www.ibm.com/developerworks/aix/library/au-unixprocess.html

    `Advanced Programming in the UNIX(R) Environment <http://www.amazon.com/Programming-Environment-Addison-Wesley-Professional-Computing/dp/0201433079/ref=pd_bbs_3/002-2842372-4768037?ie=UTF8&s=books&amp;qid=1182098757&sr=8-3>`_
        Covers working with multiple processes, such as handling signals, closing duplicated
        file descriptors, etc.

    :ref:`article-file-access`
