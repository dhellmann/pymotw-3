==============================================
 subprocess -- Work with additional processes
==============================================

.. module:: subprocess
    :synopsis: Work with additional processes

:Purpose: Spawn and communicate with additional processes.
:Available In: 2.4 and later

The :mod:`subprocess` module provides a consistent interface to
creating and working with additional processes. It offers a
higher-level interface than some of the other available modules, and
is intended to replace functions such as :func:`os.system`,
:func:`os.spawn*`, :func:`os.popen*`, :func:`popen2.*` and
:func:`commands.*`. To make it easier to compare :mod:`subprocess`
with those other modules, many of the examples here re-create the ones
used for :mod:`os` and :mod:`popen`.

The :mod:`subprocess` module defines one class, :class:`Popen` and a
few wrapper functions that use that class. The constructor for
:class:`Popen` takes arguments to set up the new process so the parent
can communicate with it via pipes.  It provides all of the
functionality of the other modules and functions it replaces, and
more. The API is consistent for all uses, and many of the extra steps
of overhead needed (such as closing extra file descriptors and
ensuring the pipes are closed) are "built in" instead of being handled
by the application code separately.

.. note::

    The API is roughly the same, but the underlying implementation is
    slightly different between Unix and Windows. All of the examples
    shown here were tested on Mac OS X. Behavior on a non-Unix OS will
    vary.

Running External Command
========================

To run an external command without interacting with it, such as one
would do with :ref:`os.system() <os-system>`, Use the :func:`call()`
function.

.. include:: subprocess_os_system.py
    :literal:
    :start-after: #end_pymotw_header

The command line arguments are passed as a list of strings, which
avoids the need for escaping quotes or other special characters that
might be interpreted by the shell.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'subprocess_os_system.py'))
.. }}}

::

	$ python subprocess_os_system.py
	
	__init__.py
	index.rst
	interaction.py
	repeater.py
	signal_child.py
	signal_parent.py
	subprocess_check_call.py
	subprocess_check_output.py
	subprocess_check_output_error.py
	subprocess_check_output_error_trap_output.py
	subprocess_os_system.py
	subprocess_pipes.py
	subprocess_popen2.py
	subprocess_popen3.py
	subprocess_popen4.py
	subprocess_popen_read.py
	subprocess_popen_write.py
	subprocess_shell_variables.py
	subprocess_signal_parent_shell.py
	subprocess_signal_setsid.py

.. {{{end}}}

Setting the *shell* argument to a true value causes :mod:`subprocess`
to spawn an intermediate shell process, and tell it to run the
command.  The default is to run the command directly.

.. include:: subprocess_shell_variables.py
    :literal:
    :start-after: #end_pymotw_header

Using an intermediate shell means that variables, glob patterns, and
other special shell features in the command string are processed
before the command is run.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'subprocess_shell_variables.py'))
.. }}}

::

	$ python subprocess_shell_variables.py
	
	/Users/dhellmann

.. {{{end}}}

Error Handling
--------------

The return value from :func:`call` is the exit code of the program.
The caller is responsible for interpreting it to detect errors.  The
:func:`check_call` function works like :func:`call` except that the
exit code is checked, and if it indicates an error happened then a
:class:`CalledProcessError` exception is raised.

.. include:: subprocess_check_call.py
   :literal:
   :start-after: #end_pymotw_header

The :command:`false` command always exits with a non-zero status code,
which :func:`check_call` interprets as an error.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'subprocess_check_call.py', ignore_error=True, break_lines_at=70))
.. }}}

::

	$ python subprocess_check_call.py
	
	Traceback (most recent call last):
	  File "subprocess_check_call.py", line 11, in <module>
	    subprocess.check_call(['false'])
	  File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.
	7/subprocess.py", line 511, in check_call
	    raise CalledProcessError(retcode, cmd)
	subprocess.CalledProcessError: Command '['false']' returned non-zero e
	xit status 1

.. {{{end}}}

Capturing Output
----------------

The standard input and output channels for the process started by
:func:`call` are bound to the parent's input and output.  That means
the calling programm cannot capture the output of the command.  Use
:func:`check_output` to capture the output for later processing.

.. include:: subprocess_check_output.py
   :literal:
   :start-after: #end_pymotw_header

The ``ls -1`` command runs successfully, so the text it prints to
standard output is captured and returned.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'subprocess_check_output.py'))
.. }}}

::

	$ python subprocess_check_output.py
	
	Have 462 bytes in output
	__init__.py
	index.rst
	interaction.py
	repeater.py
	signal_child.py
	signal_parent.py
	subprocess_check_call.py
	subprocess_check_output.py
	subprocess_check_output_error.py
	subprocess_check_output_error_trap_output.py
	subprocess_os_system.py
	subprocess_pipes.py
	subprocess_popen2.py
	subprocess_popen3.py
	subprocess_popen4.py
	subprocess_popen_read.py
	subprocess_popen_write.py
	subprocess_shell_variables.py
	subprocess_signal_parent_shell.py
	subprocess_signal_setsid.py
	

.. {{{end}}}

This script runs a series of commands in a subshell.  Messages are
sent to standard output and standard error before the commands exit
with an error code.

.. include:: subprocess_check_output_error.py
   :literal:
   :start-after: #end_pymotw_header

The message to standard error is printed to the console, but the
message to standard output is hidden.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'subprocess_check_output_error.py', ignore_error=True, break_lines_at=70))
.. }}}

::

	$ python subprocess_check_output_error.py
	
	to stderr
	Traceback (most recent call last):
	  File "subprocess_check_output_error.py", line 14, in <module>
	    shell=True,
	  File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.
	7/subprocess.py", line 544, in check_output
	    raise CalledProcessError(retcode, cmd, output=output)
	subprocess.CalledProcessError: Command 'echo to stdout; echo to stderr
	 1>&2; exit 1' returned non-zero exit status 1

.. {{{end}}}

To prevent error messages from commands run through
:func:`check_output` from being written to the console, set the
*stderr* parameter to the constant :const:`STDOUT`.

.. include:: subprocess_check_output_error_trap_output.py
   :literal:
   :start-after: #end_pymotw_header

Now the error and standard output channels are merged together so if
the command prints error messages, they are captured and not sent to
the console.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'subprocess_check_output_error_trap_output.py', ignore_error=True, break_lines_at=70))
.. }}}

::

	$ python subprocess_check_output_error_trap_output.py
	
	Traceback (most recent call last):
	  File "subprocess_check_output_error_trap_output.py", line 15, in <mo
	dule>
	    stderr=subprocess.STDOUT,
	  File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.
	7/subprocess.py", line 544, in check_output
	    raise CalledProcessError(retcode, cmd, output=output)
	subprocess.CalledProcessError: Command 'echo to stdout; echo to stderr
	 1>&2; exit 1' returned non-zero exit status 1

.. {{{end}}}




Working with Pipes Directly
===========================

By passing different arguments for *stdin*, *stdout*, and *stderr* it
is possible to mimic the variations of :func:`os.popen()`.

popen
-----

To run a process and read all of its output, set the *stdout* value to
:const:`PIPE` and call :func:`communicate`.

.. include:: subprocess_popen_read.py
    :literal:
    :start-after: #end_pymotw_header

This is similar to the way :func:`popen` works, except that the
reading is managed internally by the :class:`Popen` instance.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'subprocess_popen_read.py'))
.. }}}

::

	$ python subprocess_popen_read.py
	
	
	read:
		stdout: '"to stdout"\n'

.. {{{end}}}

To set up a pipe to allow the calling program to write data to it, set
*stdin* to :const:`PIPE`.

.. include:: subprocess_popen_write.py
    :literal:
    :start-after: #end_pymotw_header

To send data to the standard input channel of the process one time,
pass the data to :func:`communicate`.  This is similar to using
:func:`popen` with mode ``'w'``.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u subprocess_popen_write.py'))
.. }}}

::

	$ python -u subprocess_popen_write.py
	
	
	write:
		stdin: to stdin

.. {{{end}}}

popen2
------

To set up the :class:`Popen` instance for reading and writing, use a
combination of the previous techniques.

.. include:: subprocess_popen2.py
    :literal:
    :start-after: #end_pymotw_header

This sets up the pipe to mimic :func:`popen2`.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u subprocess_popen2.py'))
.. }}}

::

	$ python -u subprocess_popen2.py
	
	
	popen2:
		pass through: 'through stdin to stdout'

.. {{{end}}}

popen3
------

It is also possible watch both of the streams for stdout and stderr,
as with :func:`popen3`.

.. include:: subprocess_popen3.py
    :literal:
    :start-after: #end_pymotw_header

Reading from stderr works the same as with stdout.  Passing
:const:`PIPE` tells :class:`Popen` to attach to the channel, and
:func:`communicate` reads all of the data from it before returning.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u subprocess_popen3.py'))
.. }}}

::

	$ python -u subprocess_popen3.py
	
	
	popen3:
		pass through: 'through stdin to stdout'
		stderr      : 'to stderr\n'

.. {{{end}}}

popen4
------

To direct the error output from the process to its standard output
channel, use :const:`STDOUT` for *stderr* instead of :const:`PIPE`.

.. include:: subprocess_popen4.py
    :literal:
    :start-after: #end_pymotw_header

Combining the output in this way is similar to how :func:`popen4`
works.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u subprocess_popen4.py'))
.. }}}

::

	$ python -u subprocess_popen4.py
	
	
	popen4:
		combined output: 'through stdin to stdout\nto stderr\n'
		stderr value   : None

.. {{{end}}}

Connecting Segments of a Pipe
=============================

Multiple commands can be connected into a *pipeline*, similar to the
way the Unix shell works, by creating separate :class:`Popen`
instances and chaining their inputs and outputs together.  The
:attr:`stdout` attribute of one :class:`Popen` instance is used as the
*stdin* argument for the next in the pipeline, instead of the constant
:const:`PIPE`.  The output is read from the :attr:`stdout` handle for
the final command in the pipeline.

.. include:: subprocess_pipes.py
    :literal:
    :start-after: #end_pymotw_header

This example reproduces the command line ``cat index.rst | grep
".. include" | cut -f 3 -d:``, which reads the reStructuredText source
file for this section and finds all of the lines that include other
files, then prints only the filenames.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u subprocess_pipes.py'))
.. }}}

::

	$ python -u subprocess_pipes.py
	
	Included files:
		subprocess_os_system.py
		subprocess_shell_variables.py
		subprocess_check_call.py
		subprocess_check_output.py
		subprocess_check_output_error.py
		subprocess_check_output_error_trap_output.py
		subprocess_popen_read.py
		subprocess_popen_write.py
		subprocess_popen2.py
		subprocess_popen3.py
		subprocess_popen4.py
		subprocess_pipes.py
		repeater.py
		interaction.py
		signal_child.py
		signal_parent.py
		subprocess_signal_parent_shell.py
		subprocess_signal_setsid.py

.. {{{end}}}


Interacting with Another Command
================================

All of the above examples assume a limited amount of interaction. The
:func:`communicate()` method reads all of the output and waits for
child process to exit before returning. It is also possible to write
to and read from the individual pipe handles used by the
:class:`Popen` instance. A simple echo program that reads from
standard input and writes to standard output illustrates this:

.. include:: repeater.py
    :literal:
    :start-after: #end_pymotw_header

The script, ``repeater.py``, writes to stderr when it starts and
stops. That information can be used to show the lifetime of the child
process.

The next interaction example uses the stdin and stdout file handles
owned by the :class:`Popen` instance in different ways. In the first
example, a sequence of 10 numbers are written to stdin of the process,
and after each write the next line of output is read back. In the
second example, the same 10 numbers are written but the output is read
all at once using :func:`communicate()`.

.. include:: interaction.py
    :literal:
    :start-after: #end_pymotw_header

The ``"repeater.py: exiting"`` lines come at different points in the
output for each loop style.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u interaction.py'))
.. }}}

::

	$ python -u interaction.py
	
	One line at a time:
	repeater.py: starting
	0
	1
	2
	3
	4
	5
	6
	7
	8
	9
	repeater.py: exiting
	
	
	All output at once:
	repeater.py: starting
	repeater.py: exiting
	0
	1
	2
	3
	4
	5
	6
	7
	8
	9
	

.. {{{end}}}


Signaling Between Processes
===========================

The :mod:`os` examples include a demonstration of :ref:`signaling
between processes using os.fork() and os.kill()
<creating-processes-with-os-fork>`. Since each :class:`Popen` instance
provides a *pid* attribute with the process id of the child process,
it is possible to do something similar with :mod:`subprocess`. For
example, using this script for the child process to be executed by the
parent process

.. include:: signal_child.py
    :literal:
    :start-after: #end_pymotw_header

combined with this parent process

.. include:: signal_parent.py
    :literal:
    :start-after: #end_pymotw_header

the output is:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'signal_parent.py'))
.. }}}

::

	$ python signal_parent.py
	
	PARENT      : Pausing before sending signal...
	CHILD  14756: Setting up signal handler
	CHILD  14756: Pausing to wait for signal
	PARENT      : Signaling child
	CHILD  14756: Received USR1

.. {{{end}}}

.. _subprocess-process-groups:

Process Groups / Sessions
-------------------------

Because of the way the process tree works under Unix, if the process
created by :mod:`Popen` spawns sub-processes, those children will not
receive any signals sent to the parent.  That means, for example, it
will be difficult to cause them to terminate by sending
:const:`SIGINT` or :const:`SIGTERM`.

.. include:: subprocess_signal_parent_shell.py
    :literal:
    :start-after: #end_pymotw_header

The pid used to send the signal does not match the pid of the child of
the shell script waiting for the signal because in this example, there
are three separate processes interacting:

1. ``subprocess_signal_parent_shell.py``
2. The Unix shell process running the script created by the main python
   program.
3. ``signal_child.py``

.. {{{cog
.. cog.out(run_script(cog.inFile, 'subprocess_signal_parent_shell.py'))
.. }}}

::

	$ python subprocess_signal_parent_shell.py
	
	PARENT      : Pausing before sending signal to child 14759...
	Shell script in process 14759
	+ python signal_child.py
	CHILD  14760: Setting up signal handler
	CHILD  14760: Pausing to wait for signal
	PARENT      : Signaling child 14759
	CHILD  14760: Never received signal

.. {{{end}}}

The solution to this problem is to use a *process group* to associate
the children so they can be signaled together.  The process group is
created with :func:`os.setsid`, setting the "session id" to the
process id of the current process.  All child processes inherit the
session id, and since it should only be set set in the shell created
by :class:`Popen` and its descendants, :func:`os.setsid` should not be
called in the parent process.  Instead, the function is passed to
:class:`Popen` as the *preexec_fn* argument so it is run after the
:func:`fork` inside the new process, before it uses :func:`exec` to
run the shell.

.. include:: subprocess_signal_setsid.py
    :literal:
    :start-after: #end_pymotw_header

The sequence of events is:

1. The parent program instantiates :class:`Popen`.
2. The :class:`Popen` instance forks a new process.
3. The new process runs :func:`os.setsid`.
4. The new process runs :func:`exec` to start the shell.
5. The shell runs the shell script.
6. The shell script forks again and that process execs Python.
7. Python runs ``signal_child.py``.
8. The parent program signals the process group using the pid of the shell.
9. The shell and Python processes receive the signal.  The shell
   ignores it.  Python invokes the signal handler.

To signal the entire process group, use :func:`os.killpg` with the pid
value from the :class:`Popen` instance.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'subprocess_signal_setsid.py'))
.. }}}

::

	$ python subprocess_signal_setsid.py
	
	PARENT      : Pausing before sending signal to child 14763...
	Shell script in process 14763
	+ python signal_child.py
	CHILD  14764: Setting up signal handler
	CHILD  14764: Pausing to wait for signal
	PARENT      : Signaling process group 14763
	CHILD  14764: Received USR1

.. {{{end}}}


.. seealso::

    `subprocess <https://docs.python.org/2/library/subprocess.html>`_
        Standard library documentation for this module.

    :mod:`os`
        Although many are deprecated, the functions for working with processes
        found in the os module are still widely used in existing code.

    `UNIX SIgnals and Process Groups <http://www.frostbytes.com/~jimf/papers/signals/signals.html>`_
        A good description of UNIX signaling and how process groups work.


    `Advanced Programming in the UNIX(R) Environment <http://www.amazon.com/Programming-Environment-Addison-Wesley-Professional-Computing/dp/0201433079/ref=pd_bbs_3/002-2842372-4768037?ie=UTF8&s=books&amp;qid=1182098757&sr=8-3>`_
        Covers working with multiple processes, such as handling signals, closing duplicated
        file descriptors, etc.

    :mod:`pipes`
        Unix shell command pipeline templates in the standard library.
