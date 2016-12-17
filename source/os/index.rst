===============================================================
 os --- Portable access to operating system specific features
===============================================================

.. module:: os
    :synopsis: Portable access to operating system specific features.

:Purpose: Portable access to operating system specific features.

The ``os`` module provides a wrapper for platform specific modules
such as :mod:`posix`, :mod:`nt`, and :mod:`mac`. The API for functions
available on all platforms should be the same, so using the ``os``
module offers some measure of portability. Not all functions are
available on every platform, however. Many of the process management
functions described in this summary are not available for Windows.

The Python documentation for the ``os`` module is subtitled
"Miscellaneous operating system interfaces". The module consists
mostly of functions for creating and managing running processes or
file system content (files and directories), with a few other bits of
functionality thrown in besides.

Examining the File System Contents
==================================

To prepare a list of the contents of a directory on the file system,
use :func:`listdir`.

.. literalinclude:: os_listdir.py
   :caption:
   :start-after: #end_pymotw_header

The return value is a list of all of the named members of the
directory given. No distinction is made between files, subdirectories,
or symlinks.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_listdir.py .', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 os_listdir.py .
	
	['index.rst', 'os_access.py', 'os_cwd_example.py',
	'os_directories.py', 'os_environ_example.py',
	'os_exec_example.py', 'os_fork_example.py',
	'os_kill_example.py', 'os_listdir.py', 'os_listdir.py~',
	'os_process_id_example.py', 'os_process_user_example.py',
	'os_rename_replace.py', 'os_rename_replace.py~',
	'os_scandir.py', 'os_scandir.py~', 'os_spawn_example.py',
	'os_stat.py', 'os_stat_chmod.py', 'os_stat_chmod_example.txt',
	'os_strerror.py', 'os_strerror.py~', 'os_symlinks.py',
	'os_system_background.py', 'os_system_example.py',
	'os_system_shell.py', 'os_wait_example.py',
	'os_waitpid_example.py', 'os_walk.py']

.. {{{end}}}

The function :func:`walk` traverses a directory recursively and for
each subdirectory generates a :class:`tuple` containing the directory
path, any immediate sub-directories of that path, and a list of the
names of any files in that directory.

.. literalinclude:: os_walk.py
   :caption:
   :start-after: #end_pymotw_header

This example shows a recursive directory listing.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_walk.py ../zipimport'))
.. }}}

.. code-block:: none

	$ python3 os_walk.py ../zipimport
	
	../zipimport
	  __init__.py
	  __pycache__/
	  example_package/
	  index.rst
	  zipimport_example.zip
	  zipimport_find_module.py
	  zipimport_get_code.py
	  zipimport_get_data.py
	  zipimport_get_data_nozip.py
	  zipimport_get_data_zip.py
	  zipimport_get_source.py
	  zipimport_is_package.py
	  zipimport_load_module.py
	  zipimport_make_example.py
	
	../zipimport/__pycache__
	  __init__.cpython-35.pyc
	  zipimport_find_module.cpython-35.pyc
	  zipimport_get_code.cpython-35.pyc
	  zipimport_get_data.cpython-35.pyc
	  zipimport_get_data_nozip.cpython-35.pyc
	  zipimport_get_data_zip.cpython-35.pyc
	  zipimport_get_source.cpython-35.pyc
	  zipimport_is_package.cpython-35.pyc
	  zipimport_load_module.cpython-35.pyc
	  zipimport_make_example.cpython-35.pyc
	
	../zipimport/example_package
	  README.txt
	  __init__.py
	  __pycache__/
	
	../zipimport/example_package/__pycache__
	  __init__.cpython-35.pyc
	

.. {{{end}}}

If more information is needed than the names of the files, it is
likely to be more efficient to use :func:`scandir` than
:func:`listdir` because more information is collected in one system
call when the directory is scanned.

.. literalinclude:: os_scandir.py
   :caption:
   :start-after: #end_pymotw_header

:func:`scandir` returns a sequence of :class:`DirEntry` instances for
the items in the directory. The object has several attributes and
methods for accessing metadata about the file.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_scandir.py .'))
.. }}}

.. code-block:: none

	$ python3 os_scandir.py .
	
	index.rst file
	os_access.py file
	os_cwd_example.py file
	os_directories.py file
	os_environ_example.py file
	os_exec_example.py file
	os_fork_example.py file
	os_kill_example.py file
	os_listdir.py file
	os_listdir.py~ file
	os_process_id_example.py file
	os_process_user_example.py file
	os_rename_replace.py file
	os_rename_replace.py~ file
	os_scandir.py file
	os_scandir.py~ file
	os_spawn_example.py file
	os_stat.py file
	os_stat_chmod.py file
	os_stat_chmod_example.txt file
	os_strerror.py file
	os_strerror.py~ file
	os_symlinks.py file
	os_system_background.py file
	os_system_example.py file
	os_system_shell.py file
	os_wait_example.py file
	os_waitpid_example.py file
	os_walk.py file

.. {{{end}}}



Managing File System Permissions
================================

Detailed information about a file can be accessed using :func:`stat`
or :func:`lstat` (for checking the status of something that might be a
symbolic link).

.. literalinclude:: os_stat.py
   :caption:
   :start-after: #end_pymotw_header

The output will vary depending on how the example code was
installed. Try passing different filenames on the command line to
``os_stat.py``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_stat.py'))
.. cog.out(run_script(cog.inFile, 'os_stat.py index.rst', include_prefix=False))
.. }}}

.. code-block:: none

	$ python3 os_stat.py
	
	os.stat(os_stat.py):
	  Size: 593
	  Permissions: 0o100644
	  Owner: 527
	  Device: 16777218
	  Created      : Sat Dec 17 12:03:26 2016
	  Last modified: Sat Dec 17 12:03:26 2016
	  Last accessed: Sat Dec 17 12:03:32 2016

	$ python3 os_stat.py index.rst
	
	os.stat(index.rst):
	  Size: 26932
	  Permissions: 0o100644
	  Owner: 527
	  Device: 16777218
	  Created      : Sat Dec 17 12:03:21 2016
	  Last modified: Sat Dec 17 12:03:21 2016
	  Last accessed: Sat Dec 17 12:03:31 2016

.. {{{end}}}


On Unix-like systems, file permissions can be changed using
:func:`chmod`, passing the mode as an integer. Mode values can be
constructed using constants defined in the :mod:`stat` module.  This
example toggles the user's execute permission bit:

.. literalinclude:: os_stat_chmod.py
   :caption:
   :start-after: #end_pymotw_header

The script assumes it has the permissions necessary to modify the mode
of the file when run.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_stat_chmod.py'))
.. }}}

.. code-block:: none

	$ python3 os_stat_chmod.py
	
	Adding execute permission

.. {{{end}}}

The function :func:`access` can be used to test the access rights a
process has for a file.

.. literalinclude:: os_access.py
   :caption:
   :start-after: #end_pymotw_header

The results will vary depending on how the example code is installed,
but the output will be similar to this:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_access.py'))
.. }}}

.. code-block:: none

	$ python3 os_access.py
	
	Testing: os_access.py
	Exists: True
	Readable: True
	Writable: True
	Executable: False

.. {{{end}}}

The library documentation for :func:`access` includes two special
warnings. First, there is not much sense in calling :func:`access` to
test whether a file can be opened before actually calling :func:`open`
on it. There is a small, but real, window of time between the two
calls during which the permissions on the file could change. The other
warning applies mostly to networked file systems that extend the POSIX
permission semantics. Some file system types may respond to the POSIX
call that a process has permission to access a file, then report a
failure when the attempt is made using :func:`open` for some reason
not tested via the POSIX call. All in all, it is better to call
:func:`open` with the required mode and catch the :class:`IOError`
raised if there is a problem.

.. _os-directories:

Creating and Deleting Directories
=================================

There are several functions for working with directories on the file
system, including creating, listing contents, and removing them.

.. literalinclude:: os_directories.py
   :caption:
   :start-after: #end_pymotw_header

There are two sets of functions for creating and deleting
directories. When creating a new directory with :func:`mkdir`, all of
the parent directories must already exist. When removing a directory
with :func:`rmdir`, only the leaf directory (the last part of the
path) is actually removed. In contrast, :func:`makedirs` and
:func:`removedirs` operate on all of the nodes in the path.
:func:`makedirs` will create any parts of the path that do not exist,
and :func:`removedirs` will remove all of the parent directories, as
long as they are empty.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_directories.py'))
.. }}}

.. code-block:: none

	$ python3 os_directories.py
	
	Creating os_directories_example
	Creating os_directories_example/example.txt
	Cleaning up

.. {{{end}}}

Working with Symbolic Links
===========================

For platforms and file systems that support them, there are functions
for working with symlinks.

.. literalinclude:: os_symlinks.py
   :caption:
   :start-after: #end_pymotw_header

Use :func:`symlink` to create a symbolic link and :func:`readlink` for
reading it to determine the original file pointed to by the link.  The
:func:`lstat` function is like :func:`stat`, but operates on symbolic
links.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_symlinks.py'))
.. }}}

.. code-block:: none

	$ python3 os_symlinks.py
	
	Creating link /tmp/os_symlinks.py -> os_symlinks.py
	Permissions: 0o120755
	Points to: os_symlinks.py

.. {{{end}}}

Safely Replacing an Existing File
=================================

Replacing or renaming an existing file is not idempotent and may
expose applications to race conditions. The :func:`rename` and
:func:`replace` functions implement safe algorithms for these actions,
using atomic operations on POSIX-compliant systems when possible.

.. literalinclude:: os_rename_replace.py
   :caption:
   :start-after: #end_pymotw_header

The :func:`rename` and :func:`replace` functions work across
filesystems, most of the time. Renaming a file may fail if it is being
moved to a new fileystem or if the destination already exists.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_rename_replace.py'))
.. }}}

.. code-block:: none

	$ python3 os_rename_replace.py
	
	Starting: ['rename_start.txt']
	After rename: ['rename_finish.txt']
	Contents: 'starting as rename_start.txt'
	After replace: 'ending with contents of rename_new_contents.txt'

.. {{{end}}}



Detecting and Changing the Process Owner
========================================

The first set of functions provided by ``os`` are used for
determining and changing the process owner ids. These are most
frequently used by authors of daemons or special system programs that
need to change permission level rather than running as ``root``. This
section does not try to explain all of the intricate details of Unix
security, process owners, etc. See the references list at the end of
this section for more details.

The following example shows the real and effective user and group
information for a process, and then changes the effective values. This
is similar to what a daemon would need to do when it starts as root
during a system boot, to lower the privilege level and run as a
different user.

.. note::

  Before running the example, change the :data:`TEST_GID` and
  :data:`TEST_UID` values to match a real user defined on the system.

.. literalinclude:: os_process_user_example.py
   :caption:
   :start-after: #end_pymotw_header

When run as user with id of 502 and group 502 on OS X, this output is
produced:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_process_user_example.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 os_process_user_example.py
	
	BEFORE CHANGE:
	User (actual/effective)  : 527 / 527
	Group (actual/effective) : 501 / 501
	Actual Groups   : [501, 701, 402, 702, 500, 12, 61, 80, 98, 398,
	399, 33, 100, 204, 395]
	
	ERROR: Could not change effective group. Rerun as root.
	ERROR: Could not change effective user. Rerun as root.

.. {{{end}}}

The values do not change because when it is not running as root, a
process cannot change its effective owner value. Any attempt to set
the effective user id or group id to anything other than that of the
current user causes an :class:`OSError`.  Running the same script
using ``sudo`` so that it starts out with root privileges is a
different story.

.. Don't use cog here because sudo sometimes asks for a password.

.. code-block:: none

    $ sudo python3 os_process_user_example.py

    BEFORE CHANGE:

    User (actual/effective)  : 0 / 0
    Group (actual/effective) : 0 / 0
    Actual Groups : [0, 1, 2, 3, 4, 5, 8, 9, 12, 20, 29, 61, 80,
    702, 33, 98, 100, 204, 395, 398, 399, 701]

    CHANGE GROUP:
    User (actual/effective)  : 0 / 0
    Group (actual/effective) : 0 / 502
    Actual Groups   : [0, 1, 2, 3, 4, 5, 8, 9, 12, 20, 29, 61, 80,
    702, 33, 98, 100, 204, 395, 398, 399, 701]

    CHANGE USER:
    User (actual/effective)  : 0 / 502
    Group (actual/effective) : 0 / 502
    Actual Groups   : [0, 1, 2, 3, 4, 5, 8, 9, 12, 20, 29, 61, 80,
    702, 33, 98, 100, 204, 395, 398, 399, 701]

In this case, since it starts as root, the script can change the
effective user and group for the process. Once the effective UID is
changed, the process is limited to the permissions of that user.
Because non-root users cannot change their effective group, the
program needs to change the group before changing the user.

Managing the Process Environment
================================

Another feature of the operating system exposed to a program though
the ``os`` module is the environment. Variables set in the
environment are visible as strings that can be read through
:data:`os.environ` or :func:`getenv`. Environment variables are
commonly used for configuration values such as search paths, file
locations, and debug flags. This example shows how to retrieve an
environment variable, and pass a value through to a child process.

.. literalinclude:: os_environ_example.py
   :caption:
   :start-after: #end_pymotw_header

The :data:`os.environ` object follows the standard Python mapping API
for retrieving and setting values. Changes to :data:`os.environ` are
exported for child processes.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u os_environ_example.py'))
.. }}}

.. code-block:: none

	$ python3 -u os_environ_example.py
	
	Initial value: None
	Child process:
	
	
	Changed value: THIS VALUE WAS CHANGED
	Child process:
	THIS VALUE WAS CHANGED
	
	Removed value: None
	Child process:
	

.. {{{end}}}

Managing the Process Working Directory
======================================

Operating systems with hierarchical file systems have a concept of the
*current working directory* -- the directory on the file system the
process uses as the starting location when files are accessed with
relative paths.  The current working directory can be retrieved with
:func:`getcwd` and changed with :func:`chdir`.

.. literalinclude:: os_cwd_example.py
   :caption:
   :start-after: #end_pymotw_header

:const:`os.curdir` and :const:`os.pardir` are used to refer to the
current and parent directories in a portable manner.

.. Only elide part of the prefix for the path so it is possible to see
   the relative change in the output.

.. {{{cog
.. def _elide_cwd(infile, line):
..     import os.path
..     basedir = os.path.abspath(path(infile).dirname() / '..' / '..' / '..')
..     line = line.replace(basedir, '...')
..     return line
.. cog.out(run_script(cog.inFile, 'os_cwd_example.py', line_cleanups=[_elide_cwd]))
.. }}}

.. code-block:: none

	$ python3 os_cwd_example.py
	
	Starting: .../pymotw-3/source/os
	Moving up one: ..
	After move: .../pymotw-3/source

.. {{{end}}}

.. _os-system:

Running External Commands
=========================

.. warning::

    Many of these functions for working with processes have limited
    portability. For a more consistent way to work with processes in a
    platform independent manner, see the :mod:`subprocess` module
    instead.

The most basic way to run a separate command, without interacting with
it at all, is :func:`system`. It takes a single string argument, which is
the command line to be executed by a sub-process running a shell.

.. literalinclude:: os_system_example.py
   :caption:
   :start-after: #end_pymotw_header

The return value of :func:`system` is the exit value of the shell
running the program packed into a 16 bit number, with the high byte
the exit status and the low byte the signal number that caused the
process to die, or zero.

.. {{{cog
.. def _elide_docs(infile, line):
..     import os.path
..     basedir = os.path.abspath(path(infile).dirname() / '..' / '..' / '..').replace('Dropbox', 'Documents')
..     line = line.replace(basedir, '...')
..     return line
.. cog.out(run_script(cog.inFile, '-u os_system_example.py', line_cleanups=[_elide_docs]))
.. }}}

.. code-block:: none

	$ python3 -u os_system_example.py
	
	.../pymotw-3/source/os

.. {{{end}}}


Since the command is passed directly to the shell for processing, it can
include shell syntax such as globbing or environment variables.

.. literalinclude:: os_system_shell.py
   :caption:
   :start-after: #end_pymotw_header

The environment variable ``$TMPDIR`` in this string is expanded when
the shell runs the command line.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u os_system_shell.py'))
.. }}}

.. code-block:: none

	$ python3 -u os_system_shell.py
	
	/var/folders/5q/8gk0wq888xlggz008k8dr7180000hg/T/

.. {{{end}}}


Unless the command is explicitly run in the background, the call to
:func:`system` blocks until it is complete. Standard input,
output, and error from the child process are tied to the appropriate
streams owned by the caller by default, but can be redirected using
shell syntax.

.. literalinclude:: os_system_background.py
   :caption:
   :start-after: #end_pymotw_header

This is getting into shell trickery, though, and there are better ways to
accomplish the same thing.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u os_system_background.py'))
.. }}}

.. code-block:: none

	$ python3 -u os_system_background.py
	
	Calling...
	Sat Dec 17 12:03:32 EST 2016
	Sleeping...
	Sat Dec 17 12:03:35 EST 2016

.. {{{end}}}

.. _creating-processes-with-os-fork:

Creating Processes with os.fork()
=================================

The POSIX functions :func:`fork` and :func:`exec` (available under Mac
OS X, Linux, and other Unix variants) are exposed via the ``os``
module. Entire books have been written about reliably using these
functions, so check the library or bookstore for more details than are
presented here in this introduction.

To create a new process as a clone of the current process, use
:func:`fork`:

.. literalinclude:: os_fork_example.py
   :caption:
   :start-after: #end_pymotw_header

The output will vary based on the state of the system each time the
example is run, but it will look something like:

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u os_fork_example.py'))
.. }}}

.. code-block:: none

	$ python3 -u os_fork_example.py
	
	Child process id: 23559
	I am the child

.. {{{end}}}

After the fork, there are two processes running the same code. For a
program to tell which one it is in, it needs to check the return value
of :func:`fork`. If the value is ``0``, the current process is the
child.  If it is not ``0``, the program is running in the parent
process and the return value is the process id of the child process.

.. literalinclude:: os_kill_example.py
   :caption:
   :start-after: #end_pymotw_header

The parent can send signals to the child process using :func:`kill`
and the :mod:`signal` module. First, define a signal handler to be
invoked when the signal is received.  Then :func:`fork`, and in the
parent pause a short amount of time before sending a :const:`USR1`
signal using :func:`kill`. This example uses a short pause to give
the child process time to set up the signal handler. A real
application, would not need (or want) to call :func:`sleep`.  In the
child, set up the signal handler and go to sleep for a while to give
the parent time to send the signal.


.. {{{cog
.. cog.out(run_script(cog.inFile, '-u os_kill_example.py'))
.. }}}

.. code-block:: none

	$ python3 -u os_kill_example.py
	
	Forking...
	PARENT: Pausing before sending signal...
	CHILD: Setting up signal handler
	CHILD: Pausing to wait for signal
	PARENT: Signaling 23562
	Received USR1 in process 23562

.. {{{end}}}

A simple way to handle separate behavior in the child process is to
check the return value of :func:`fork` and branch. More complex
behavior may call for more code separation than a simple branch. In
other cases, there may be an existing program that needs to be
wrapped. For both of these situations, the :func:`exec*` series
of functions can be used to run another program. 

.. literalinclude:: os_exec_example.py
   :caption:
   :start-after: #end_pymotw_header

When a program is run by :func:`exec`, the code from that program replaces the
code from the existing process.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_exec_example.py', line_cleanups=[_elide_cwd]))
.. }}}

.. code-block:: none

	$ python3 os_exec_example.py
	
	.../pymotw-3/source/os

.. {{{end}}}

There are many variations of :func:`exec`, depending on the form in
which the arguments are available, whether the path and environment of
the parent process should be copied to the child, etc.  For all
variations, the first argument is a path or filename and the remaining
arguments control how that program runs. They are either passed as
command line arguments or override the process "environment" (see
:data:`os.environ` and :data:`os.getenv`).  Refer to the library
documentation for complete details.

Waiting for Child Processes
===========================

Many computationally intensive programs use multiple processes to work
around the threading limitations of Python and the global interpreter
lock. When starting several processes to run separate tasks, the
master will need to wait for one or more of them to finish before
starting new ones, to avoid overloading the server. There are a few
different ways to do that using :func:`wait` and related functions.

When it does not matter which child process might exit first, use
:func:`wait`.  It returns as soon as any child process exits.

.. literalinclude:: os_wait_example.py
   :caption:
   :start-after: #end_pymotw_header

The return value from :func:`wait` is a tuple containing the process
id and exit status combined into a 16-bit value.  The low byte is the
number of the signal that killed the process, and the high byte is the
status code returned by the process when it exited.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u os_wait_example.py'))
.. }}}

.. code-block:: none

	$ python3 -u os_wait_example.py
	
	PARENT 23613: Forking 0
	PARENT 23613: Forking 1
	PARENT: Waiting for 0
	WORKER 0: Starting
	WORKER 1: Starting
	WORKER 0: Finishing
	PARENT: Child done: (23619, 0)
	PARENT: Waiting for 1
	WORKER 1: Finishing
	PARENT: Child done: (23620, 256)

.. {{{end}}}

To wait for a specific process, use :func:`waitpid`.

.. literalinclude:: os_waitpid_example.py
   :caption:
   :start-after: #end_pymotw_header

Pass the process id of the target process, and :func:`waitpid` blocks
until that process exits.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u os_waitpid_example.py'))
.. }}}

.. code-block:: none

	$ python3 -u os_waitpid_example.py
	
	PARENT 23701: Forking 0
	PARENT 23701: Forking 1
	PARENT: Waiting for 23702
	WORKER 0: Starting
	WORKER 1: Starting
	WORKER 0: Finishing
	PARENT: Child done: (23702, 0)
	PARENT: Waiting for 23703
	WORKER 1: Finishing
	PARENT: Child done: (23703, 256)

.. {{{end}}}

:func:`wait3` and :func:`wait4` work in a similar manner, but return
more detailed information about the child process with the pid, exit
status, and resource usage.

Spawning New Processes
======================

As a convenience, the :func:`spawn` family of functions handles the
:func:`fork` and :func:`exec` in one statement:

.. literalinclude:: os_spawn_example.py
   :caption:
   :start-after: #end_pymotw_header

The first argument is a mode indicating whether or not to wait for the
process to finish before returning.  This example waits.  Use
:const:`P_NOWAIT` to let the other process start, but then resume in
the current process.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_spawn_example.py', line_cleanups=[_elide_cwd]))
.. }}}

.. code-block:: none

	$ python3 os_spawn_example.py
	
	.../pymotw-3/source/os

.. {{{end}}}

Operating System Error Codes
============================

Error codes defined by the operating system and managed in the
:mod:`errno` module can be translated to message strings using
:func:`strerror`.

.. literalinclude:: os_strerror.py
   :caption:
   :start-after: #end_pymotw_header

This example shows the messages associated with some error codes that
come up frequently.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_strerror.py'))
.. }}}

.. code-block:: none

	$ python3 os_strerror.py
	
	[ 2] ENOENT: No such file or directory
	[ 4] EINTR : Interrupted system call
	[16] EBUSY : Resource busy

.. {{{end}}}

.. seealso::

   * :pydoc:`os`

   * :ref:`Porting notes for os <porting-os>`

   * :mod:`signal` -- The section on the ``signal`` module goes over
     signal handling techniques in more detail.

   * :mod:`subprocess` -- The ``subprocess`` module supersedes
     :func:`os.popen`.

   * :mod:`multiprocessing` -- The ``multiprocessing`` module makes
     working with extra processes easier.

   * :mod:`tempfile` -- The ``tempfile`` module for working with
     temporary files.

   * :ref:`shutil-directory-functions` -- The :mod:`shutil` module
     also includes functions for working with directory trees.

   * `Speaking UNIX,
     Part 8. <http://www.ibm.com/developerworks/aix/library/au-speakingunix8/index.html>`__
     -- Learn how UNIX multitasks.

   * `Standard streams <https://en.wikipedia.org/wiki/Standard_streams>`__
     -- For more discussion of stdin, stdout, and stderr.

   * `Delve into Unix Process Creation
     <http://www.ibm.com/developerworks/aix/library/au-unixprocess.html>`__
     -- Explains the life cycle of a Unix process.

   * *Advanced Programming in the UNIX(R) Environment* By W. Richard
     Stevens and Stephen A. Rago.  Published by Addison-Wesley
     Professional, 2005.  ISBN-10: 0201433079 -- This book covers
     working with multiple processes, such as handling signals,
     closing duplicated file descriptors, etc.
