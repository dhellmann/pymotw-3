===============================================================
 os --- Portable access to operating system specific features
===============================================================

.. module:: os
    :synopsis: Portable access to operating system specific features.

:Purpose: Portable access to operating system specific features.
:Python Version: 1.4 and later

The :mod:`os` module provides a wrapper for platform specific modules
such as :mod:`posix`, :mod:`nt`, and :mod:`mac`. The API for functions
available on all platforms should be the same, so using the :mod:`os`
module offers some measure of portability. Not all functions are
available on every platform, however. Many of the process management
functions described in this summary are not available for Windows.

The Python documentation for the :mod:`os` module is subtitled
"Miscellaneous operating system interfaces". The module consists
mostly of functions for creating and managing running processes or
file system content (files and directories), with a few other bits of
functionality thrown in besides.

Process Owner
=============

The first set of functions provided by :mod:`os` are used for determining and
changing the process owner ids. These are most frequently used by authors of
daemons or special system programs that need to change permission
level rather than running as ``root``. This section does not try to
explain all of the intricate details of Unix security, process owners,
etc. See the references list at the end of this section for more
details.

The following example shows the real and effective user and group
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
    User (actual/effective)  : 527 / 527
    Group (actual/effective) : 501 / 501
    Actual Groups   : [501, 102, 204, 100, 98, 80, 61, 12, 500, 101]
    
    CHANGED GROUP:
    User (actual/effective)  : 527 / 527
    Group (actual/effective) : 501 / 501
    Actual Groups   : [501, 102, 204, 100, 98, 80, 61, 12, 500, 101]
    
    CHANGE USER:
    User (actual/effective)  : 527 / 527
    Group (actual/effective) : 501 / 501
    Actual Groups   : [501, 102, 204, 100, 98, 80, 61, 12, 500, 101]
    

.. {{{end}}}

The values do not change because when it is not running as root, a
process cannot change its effective owner value. Any attempt to set
the effective user id or group id to anything other than that of the
current user causes an :class:`OSError`.  Running the same script
using :command:`sudo` so that it starts out with root privileges is a
different story.

.. Don't use cog here because sudo sometimes asks for a password.

::

    $ sudo python os_process_user_example.py

    BEFORE CHANGE:
    User (actual/effective)  : 0 / 0
    Group (actual/effective) : 0 / 0
    Actual Groups   : [0, 204, 100, 98, 80, 61, 29, 20, 12, 9, 8,
    5, 4, 3, 2, 1]
    
    CHANGED GROUP:
    User (actual/effective)  : 0 / 0
    Group (actual/effective) : 0 / 501
    Actual Groups   : [501, 204, 100, 98, 80, 61, 29, 20, 12, 9, 
    8, 5, 4, 3, 2, 1]

    CHANGE USER:
    User (actual/effective)  : 0 / 527
    Group (actual/effective) : 0 / 501
    Actual Groups   : [501, 204, 100, 98, 80, 61, 29, 20, 12, 9, 
    8, 5, 4, 3, 2, 1]
    

In this case, since it starts as root, the script can change the
effective user and group for the process. Once the effective UID is
changed, the process is limited to the permissions of that user.
Because non-root users cannot change their effective group, the
program needs to change the group before changing the user.

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

Operating systems with hierarchical file systems have a concept of the
*current working directory* -- the directory on the file system the
process uses as the starting location when files are accessed with
relative paths.  The current working directory can be retrieved with
:func:`getcwd` and changed with :func:`chdir`.

.. include:: os_cwd_example.py
    :literal:
    :start-after: #end_pymotw_header

:const:`os.curdir` and :const:`os.pardir` are used to refer to the
current and parent directories in a portable manner.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_cwd_example.py'))
.. }}}

::

    $ python os_cwd_example.py
    
    Starting: /Users/dhellmann/Documents/PyMOTW/book/PyMOTW/os
    Moving up one: ..
    After move: /Users/dhellmann/Documents/PyMOTW/book/PyMOTW

.. {{{end}}}

File Descriptors
================

:mod:`os` includes the standard set of functions for working with
low-level *file descriptors* (integers representing open files owned
by the current process). This is a lower-level API than is provided by
:class:`file` objects. They are not covered here because it is
generally easier to work directly with :class:`file` objects. Refer to
the library documentation for details.

File System Permissions
=======================

Detailed information about a file can be accessed using
:func:`stat()` or :func:`lstat()` (for checking the status of
something that might be a symbolic link).

.. include:: os_stat.py
    :literal:
    :start-after: #end_pymotw_header

The output will vary depending on how the example code was
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
        Last modified: Sun Nov 14 09:40:36 2010

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

There are several functions for working with directories on the file system,
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
the path that do not exist, and :func:`removedirs()` will remove
all of the parent directories, as long as they are empty.

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

For platforms and file systems that support them, there are functions
for working with symlinks.

.. include:: os_symlinks.py
    :literal:
    :start-after: #end_pymotw_header

Use :func:`symlink` to create a symbolic link and :func:`readlink` for
reading it to determine the original file pointed to by the link.  The
:func:`lstat` function is like :func:`stat`, but operates on symbolic
links.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_symlinks.py'))
.. }}}

::

    $ python os_symlinks.py
    
    Creating link /tmp/os_symlinks.py -> os_symlinks.py
    Permissions: 0120755
    Points to: os_symlinks.py

.. {{{end}}}


Walking a Directory Tree
========================

The function :func:`walk()` traverses a directory recursively and for
each directory generates a :class:`tuple` containing the directory
path, any immediate sub-directories of that path, and a list of the
names of any files in that directory.

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

The most basic way to run a separate command, without interacting with
it at all, is :func:`system()`. It takes a single string argument, which is
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
    
    /Users/dhellmann/Documents/PyMOTW/book/PyMOTW/os

.. {{{end}}}


Since the command is passed directly to the shell for processing, it can
include shell syntax such as globbing or environment variables.

.. include:: os_system_shell.py
    :literal:
    :start-after: #end_pymotw_header

The environment variable ``$TMPDIR`` in this string is expanded when
the shell runs the command line.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u os_system_shell.py'))
.. }}}

::

    $ python -u os_system_shell.py
    
    /var/folders/9R/9R1t+tR02Raxzk+F71Q50U+++Uw/-Tmp-/

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
    Sat Dec  4 14:47:07 EST 2010
    Sleeping...
    Sat Dec  4 14:47:10 EST 2010

.. {{{end}}}

.. _creating-processes-with-os-fork:

Creating Processes with os.fork()
=================================

The POSIX functions :func:`fork()` and :func:`exec()` (available
under Mac OS X, Linux, and other UNIX variants) are exposed via the
:mod:`os` module. Entire books have been written about reliably using
these functions, so check the library or bookstore for more details
than are presented here in this introduction.

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
    
    I am the child
    Child process id: 14133

.. {{{end}}}

After the fork, there are two processes running the same code. For a
program to tell which one it is in, it needs to check the return value
of :func:`fork()`. If the value is ``0``, the current process is the
child.  If it is not ``0``, the program is running in the parent
process and the return value is the process id of the child process.

The parent can send signals to the child process using :func:`kill`
and the :mod:`signal` module. First, define a signal handler to be
invoked when the signal is received.

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

A real application, would not need (or want) to call :func:`sleep()`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_kill_example.py'))
.. }}}

::

    $ python os_kill_example.py
    
    Forking...
    PARENT: Pausing before sending signal...
    PARENT: Signaling 14136
    Forking...
    CHILD: Setting up signal handler
    CHILD: Pausing to wait for signal
    Received USR1 in process 14136

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

When a program is run by :func:`exec`, the code from that program replaces the
code from the existing process.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'os_exec_example.py'))
.. }}}

::

    $ python os_exec_example.py
    
    /Users/dhellmann/Documents/PyMOTW/book/PyMOTW/os

.. {{{end}}}


There are many variations of :func:`exec()`, depending on the form in
which the arguments are available, whether the path and environment of
the parent process should be copied to the child, etc.  For all
variations, the first argument is a path or filename and the remaining
arguments control how that program runs. They are either passed as
command line arguments or override the process "environment" (see
:data:`os.environ` and :data:`os.getenv`).  Refer to the library
documentation for complete details.

Waiting for a Child
===================

Many computationally intensive programs use multiple processes to work
around the threading limitations of Python and the global interpreter
lock. When starting several processes to run separate tasks, the
master will need to wait for one or more of them to finish before
starting new ones, to avoid overloading the server. There are a few
different ways to do that using :func:`wait()` and related functions.

When it does not matter which child process might exit first, use
:func:`wait()`.  It returns as soon as any child process exits.

.. include:: os_wait_example.py
    :literal:
    :start-after: #end_pymotw_header


The return value from :func:`wait()` is a tuple containing the process
id and exit status combined into a 16-bit value.  The low byte is the
number of the signal that killed the process, and the high byte is the
status code returned by the process when it exited.

.. NOT RUNNING because produces duplicate output that way
.. cog.out(run_script(cog.inFile, 'os_wait_example.py'))

::

    $ python os_wait_example.py

    PARENT 14154: Forking 0
    PARENT 14154: Forking 1
    WORKER 0: Starting
    PARENT: Waiting for 0
    WORKER 1: Starting
    WORKER 0: Finishing
    PARENT: Child done: (14155, 0)
    PARENT: Waiting for 1
    WORKER 1: Finishing
    PARENT: Child done: (14156, 256)

To wait for a specific process, use :func:`waitpid()`.

.. include:: os_waitpid_example.py
    :literal:
    :start-after: #end_pymotw_header

Pass the process id of the target process, and :func:`waitpid` blocks
until that process exits.

.. NOT RUNNING because produces duplicate output that way
.. cog.out(run_script(cog.inFile, 'os_waitpid_example.py'))

::

    $ python os_waitpid_example.py
    
    PARENT 14162: Forking 0
    PARENT 14162: Forking 1
    PARENT: Waiting for 14163
    WORKER 0: Starting
    WORKER 1: Starting
    WORKER 0: Finishing
    PARENT: Child done: (14163, 0)
    PARENT: Waiting for 14164
    WORKER 1: Finishing
    PARENT: Child done: (14164, 256)

:func:`wait3()` and :func:`wait4()` work in a similar manner, but
return more detailed information about the child process with the pid,
exit status, and resource usage.

Spawn
=====

As a convenience, the :func:`spawn()` family of functions handles the
:func:`fork()` and :func:`exec()` in one statement:

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
    
    /Users/dhellmann/Documents/PyMOTW/book/PyMOTW/os

.. {{{end}}}

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

.. seealso::

    `os <http://docs.python.org/lib/module-os.html>`_
        Standard library documentation for this module.

    :ref:`Porting notes for os <porting-os>`

    `Flow Control Issues <http://docs.python.org/library/popen2.html#popen2-flow-control>`__
        Standard library documentation of :func:`popen2` and how to
        prevent deadlocks.

    :mod:`signal`
        The section on the ``signal`` module goes over signal handling
        techniques in more detail.

    :mod:`subprocess`
        The ``subprocess`` module supersedes :func:`os.popen`.

    :mod:`multiprocessing` 
        The ``multiprocessing`` module makes working with extra processes
        easier.

    :ref:`shutil-directory-functions`
        The :mod:`shutil` module also includes functions for working
        with directory trees.

    :mod:`tempfile`
        The ``tempfile`` module for working with temporary files.

    `Unix Manual Page Introduction <http://www.scit.wlv.ac.uk/cgi-bin/mansec?2+intro>`__
        Includes definitions of real and effective ids, etc.

    `Speaking UNIX, Part 8. <http://www.ibm.com/developerworks/aix/library/au-speakingunix8/index.html>`__
        Learn how UNIX multitasks.

    `Unix Concepts <http://www.linuxhq.com/guides/LUG/node67.html>`__
        For more discussion of stdin, stdout, and stderr.

    `Delve into Unix Process Creation <http://www.ibm.com/developerworks/aix/library/au-unixprocess.html>`__
        Explains the life cycle of a UNIX process.

    *Advanced Programming in the UNIX(R) Environment*
        By W. Richard Stevens and Stephen A. Rago.  Published by
        Addison-Wesley Professional, 2005.  ISBN-10: 0201433079

        Covers working with multiple processes, such as handling signals, closing duplicated
        file descriptors, etc.
