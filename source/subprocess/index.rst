==============================================
 subprocess --- Spawning Additional Processes
==============================================

.. module:: subprocess
    :synopsis: Spawning additional processes

:Purpose: Start and communicate with additional processes.

The ``subprocess`` module supports three APIs for working with
processes. The :func:`run` function, added in Python 3.5, is a
high-level API for running a process and optionally collecting its
output. The functions :func:`call`, :func:`check_call`, and
:func:`check_output` are the former high-level API, carried over from
Python 2. They are still supported and widely used in existing
programs. The class :class:`Popen` is a low-level API used to build
the other APIs and useful for more complex process interactions. The
constructor for :class:`Popen` takes arguments to set up the new
process so the parent can communicate with it via pipes.  It provides
all of the functionality of the other modules and functions it
replaces, and more. The API is consistent for all uses, and many of
the extra steps of overhead needed (such as closing extra file
descriptors and ensuring the pipes are closed) are "built in" instead
of being handled by the application code separately.

The ``subprocess`` module is intended to replace functions such as
:func:`os.system`, :func:`os.spawnv`, the variations of :func:`popen`
in the :mod:`os` and :mod:`popen2` modules, as well as the
:func:`commands` module. To make it easier to compare
``subprocess`` with those other modules, many of the examples in
this section re-create the ones used for :mod:`os` and :mod:`popen2`.

.. note::

    The API for working on UNIX and Windows is roughly the same, but
    the underlying implementation is slightly different.  All of the
    examples shown here were tested on Mac OS X. Behavior on a
    non-UNIX OS may vary.

Running External Command
========================

To run an external command without interacting with it in the same way
as :func:`os.system`, use the :func:`run` function.

.. literalinclude:: subprocess_os_system.py
    :caption:
    :start-after: #end_pymotw_header

The command line arguments are passed as a list of strings, which
avoids the need for escaping quotes or other special characters that
might be interpreted by the shell. :func:`run` returns a
:class:`CompletedProcess` instance, with information about the process
like the exit code and output.

.. {{{cog
.. run_script(cog.inFile, 'rm -f *~ *.pyc', interpreter='')
.. cog.out(run_script(cog.inFile, 'subprocess_os_system.py'))
.. }}}

.. code-block:: none

	$ python3 subprocess_os_system.py
	
	index.rst
	interaction.py
	repeater.py
	signal_child.py
	signal_parent.py
	subprocess_check_output_error_trap_output.py
	subprocess_os_system.py
	subprocess_pipes.py
	subprocess_popen2.py
	subprocess_popen3.py
	subprocess_popen4.py
	subprocess_popen_read.py
	subprocess_popen_write.py
	subprocess_run_check.py
	subprocess_run_output.py
	subprocess_run_output_error.py
	subprocess_run_output_error_suppress.py
	subprocess_run_output_error_trap.py
	subprocess_shell_variables.py
	subprocess_signal_parent_shell.py
	subprocess_signal_setpgrp.py
	returncode: 0

.. {{{end}}}

Setting the ``shell`` argument to a true value causes ``subprocess``
to spawn an intermediate shell process which then runs the
command.  The default is to run the command directly.

.. literalinclude:: subprocess_shell_variables.py
    :caption:
    :start-after: #end_pymotw_header

Using an intermediate shell means that variables, glob patterns, and
other special shell features in the command string are processed
before the command is run.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'subprocess_shell_variables.py'))
.. }}}

.. code-block:: none

	$ python3 subprocess_shell_variables.py
	
	/Users/dhellmann
	returncode: 0

.. {{{end}}}

.. note::

  Using :func:`run` without passing ``check=True`` is equivalent to
  using :func:`call`, which only returned the exit code from the
  process.

Error Handling
--------------

The ``returncode`` attribute of the :class:`CompletedProcess` is the
exit code of the program.  The caller is responsible for interpreting
it to detect errors.  If the ``check`` argument to :func:`run` is
``True``, the exit code is checked and if it indicates an error
happened then a :class:`CalledProcessError` exception is raised.

.. literalinclude:: subprocess_run_check.py
   :caption:
   :start-after: #end_pymotw_header

The ``false`` command always exits with a non-zero status code,
which :func:`run` interprets as an error.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'subprocess_run_check.py', ignore_error=True))
.. }}}

.. code-block:: none

	$ python3 subprocess_run_check.py
	
	ERROR: Command '['false']' returned non-zero exit status 1

.. {{{end}}}

.. note::

   Passing ``check=True`` to :func:`run` makes it equivalent to using
   :func:`check_call`.

Capturing Output
----------------

The standard input and output channels for the process started by
:func:`run` are bound to the parent's input and output.  That means
the calling program cannot capture the output of the command.  Pass
:const:`PIPE` for the ``stdout`` and ``stderr`` arguments to capture
the output for later processing.

.. literalinclude:: subprocess_run_output.py
   :caption:
   :start-after: #end_pymotw_header

The ``ls -1`` command runs successfully, so the text it prints to
standard output is captured and returned.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'subprocess_run_output.py'))
.. }}}

.. code-block:: none

	$ python3 subprocess_run_output.py
	
	returncode: 0
	Have 522 bytes in stdout:
	index.rst
	interaction.py
	repeater.py
	signal_child.py
	signal_parent.py
	subprocess_check_output_error_trap_output.py
	subprocess_os_system.py
	subprocess_pipes.py
	subprocess_popen2.py
	subprocess_popen3.py
	subprocess_popen4.py
	subprocess_popen_read.py
	subprocess_popen_write.py
	subprocess_run_check.py
	subprocess_run_output.py
	subprocess_run_output_error.py
	subprocess_run_output_error_suppress.py
	subprocess_run_output_error_trap.py
	subprocess_shell_variables.py
	subprocess_signal_parent_shell.py
	subprocess_signal_setpgrp.py
	

.. {{{end}}}

.. note::

   Passing ``check=True`` and setting ``stdout`` to :const:`PIPE` is
   equivalent to using :func:`check_output`.

The next example runs a series of commands in a sub-shell.  Messages are
sent to standard output and standard error before the commands exit
with an error code.

.. literalinclude:: subprocess_run_output_error.py
   :caption:
   :start-after: #end_pymotw_header

The message to standard error is printed to the console, but the
message to standard output is hidden.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'subprocess_run_output_error.py',
..                    ignore_error=True, line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 subprocess_run_output_error.py
	
	to stderr
	ERROR: Command 'echo to stdout; echo to stderr 1>&2; exit 1'
	returned non-zero exit status 1

.. {{{end}}}

To prevent error messages from commands run through
:func:`run` from being written to the console, set the
``stderr`` parameter to the constant :const:`PIPE`.

.. literalinclude:: subprocess_run_output_error_trap.py
   :caption:
   :start-after: #end_pymotw_header

This example does not set ``check=True`` so the output of the command
is captured and printed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'subprocess_run_output_error_trap.py',
..                    ignore_error=True, line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 subprocess_run_output_error_trap.py
	
	returncode: 1
	Have 10 bytes in stdout: 'to stdout\n'
	Have 10 bytes in stderr: 'to stderr\n'

.. {{{end}}}

To capture error messages when using :func:`check_output`, set
``stderr`` to :const:`STDOUT`, and the messages will be merged with
the rest of the output from the command.

.. literalinclude:: subprocess_check_output_error_trap_output.py
   :caption:
   :start-after: #end_pymotw_header

The order of output may vary, depending on how buffering is applied to
the standard output stream and how much data is being printed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'subprocess_check_output_error_trap_output.py'))
.. }}}

.. code-block:: none

	$ python3 subprocess_check_output_error_trap_output.py
	
	Have 20 bytes in output: 'to stdout\nto stderr\n'

.. {{{end}}}

Suppressing Output
------------------

For cases where the output should not be shown or captured, use
:const:`DEVNULL` to suppress an output stream. This example suppresses
both the standard output and error streams.

.. literalinclude:: subprocess_run_output_error_suppress.py
   :caption:
   :start-after: #end_pymotw_header

The name :const:`DEVNULL` comes from the UNIX special device file,
``/dev/null``, which responds with end-of-file when opened for reading
and receives but ignores any amount of input when writing.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'subprocess_run_output_error_suppress.py'))
.. }}}

.. code-block:: none

	$ python3 subprocess_run_output_error_suppress.py
	
	returncode: 1
	stdout is None
	stderr is None

.. {{{end}}}

Working with Pipes Directly
===========================

The functions :func:`run`, :func:`call`, :func:`check_call`, and
:func:`check_output` are wrappers around the :class:`Popen` class.
Using :class:`Popen` directly gives more control over how the command
is run, and how its input and output streams are processed.  For
example, by passing different arguments for ``stdin``, ``stdout``, and
``stderr`` it is possible to mimic the variations of :func:`os.popen`.

One-way Communication With a Process
------------------------------------

To run a process and read all of its output, set the ``stdout`` value to
:const:`PIPE` and call :func:`communicate`.

.. literalinclude:: subprocess_popen_read.py
    :caption:
    :start-after: #end_pymotw_header

This is similar to the way :func:`popen` works, except that the
reading is managed internally by the :class:`Popen` instance.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'subprocess_popen_read.py'))
.. }}}

.. code-block:: none

	$ python3 subprocess_popen_read.py
	
	read:
	stdout: '"to stdout"\n'

.. {{{end}}}

To set up a pipe to allow the calling program to write data to it, set
``stdin`` to :const:`PIPE`.

.. literalinclude:: subprocess_popen_write.py
    :caption:
    :start-after: #end_pymotw_header

To send data to the standard input channel of the process one time,
pass the data to :func:`communicate`.  This is similar to using
:func:`popen` with mode ``'w'``.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u subprocess_popen_write.py'))
.. }}}

.. code-block:: none

	$ python3 -u subprocess_popen_write.py
	
	write:
	stdin: to stdin

.. {{{end}}}

Bi-directional Communication With a Process
-------------------------------------------

To set up the :class:`Popen` instance for reading and writing at the
same time, use a combination of the previous techniques.

.. literalinclude:: subprocess_popen2.py
    :caption:
    :start-after: #end_pymotw_header

This sets up the pipe to mimic :func:`popen2`.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u subprocess_popen2.py'))
.. }}}

.. code-block:: none

	$ python3 -u subprocess_popen2.py
	
	popen2:
	pass through: 'through stdin to stdout'

.. {{{end}}}

Capturing Error Output
----------------------

It is also possible watch both of the streams for ``stdout`` and ``stderr``,
as with :func:`popen3`.

.. literalinclude:: subprocess_popen3.py
    :caption:
    :start-after: #end_pymotw_header

Reading from ``stderr`` works the same as with ``stdout``.  Passing
:const:`PIPE` tells :class:`Popen` to attach to the channel, and
:func:`communicate` reads all of the data from it before returning.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u subprocess_popen3.py'))
.. }}}

.. code-block:: none

	$ python3 -u subprocess_popen3.py
	
	popen3:
	pass through: 'through stdin to stdout'
	stderr      : 'to stderr\n'

.. {{{end}}}

Combining Regular and Error Output
----------------------------------

To direct the error output from the process to its standard output
channel, use :const:`STDOUT` for ``stderr`` instead of :const:`PIPE`.

.. literalinclude:: subprocess_popen4.py
    :caption:
    :start-after: #end_pymotw_header

Combining the output in this way is similar to how :func:`popen4`
works.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u subprocess_popen4.py'))
.. }}}

.. code-block:: none

	$ python3 -u subprocess_popen4.py
	
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
``stdin`` argument for the next in the pipeline, instead of the constant
:const:`PIPE`.  The output is read from the :attr:`stdout` handle for
the final command in the pipeline.

.. literalinclude:: subprocess_pipes.py
    :caption:
    :start-after: #end_pymotw_header

The example reproduces the command line:

.. code-block:: none

   $ cat index.rst | grep ".. literalinclude" | cut -f 3 -d:

The pipeline reads the reStructuredText source file for this section
and finds all of the lines that include other files, then prints the
names of the files being included.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u subprocess_pipes.py'))
.. }}}

.. code-block:: none

	$ python3 -u subprocess_pipes.py
	
	Included files:
	subprocess_os_system.py
	subprocess_shell_variables.py
	subprocess_run_check.py
	subprocess_run_output.py
	subprocess_run_output_error.py
	subprocess_run_output_error_trap.py
	subprocess_check_output_error_trap_output.py
	subprocess_run_output_error_suppress.py
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
	subprocess_signal_setpgrp.py

.. {{{end}}}


Interacting with Another Command
================================

All of the previous examples assume a limited amount of
interaction. The :func:`communicate` method reads all of the output
and waits for child process to exit before returning. It is also
possible to write to and read from the individual pipe handles used by
the :class:`Popen` instance incrementally, as the program runs. A
simple echo program that reads from standard input and writes to
standard output illustrates this technique.

The script ``repeater.py`` is used as the child process in the next
example.  It reads from ``stdin`` and writes the values to ``stdout``, one
line at a time until there is no more input.  It also writes a message
to ``stderr`` when it starts and stops, showing the lifetime of
the child process.

.. literalinclude:: repeater.py
    :caption:
    :start-after: #end_pymotw_header

The next interaction example uses the :attr:`stdin` and :attr:`stdout`
file handles owned by the :class:`Popen` instance in different
ways. In the first example, a sequence of five numbers are written to
:attr:`stdin` of the process, and after each write the next line of
output is read back. In the second example, the same five numbers are
written but the output is read all at once using
:func:`communicate`.

.. literalinclude:: interaction.py
    :caption:
    :start-after: #end_pymotw_header

The ``"repeater.py: exiting"`` lines come at different points in the
output for each loop style.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u interaction.py'))
.. }}}

.. code-block:: none

	$ python3 -u interaction.py
	
	One line at a time:
	repeater.py: starting
	0
	1
	2
	3
	4
	repeater.py: exiting
	
	
	All output at once:
	repeater.py: starting
	repeater.py: exiting
	0
	1
	2
	3
	4
	

.. {{{end}}}


Signaling Between Processes
===========================

The process management examples for the :mod:`os` module include a
demonstration of signaling between processes using :func:`os.fork` and
:func:`os.kill`. Since each :class:`Popen` instance provides a *pid*
attribute with the process id of the child process, it is possible to
do something similar with ``subprocess``. The next example combines
two scripts.  This child process sets up a signal handler for the
:const:`USR` signal.

.. literalinclude:: signal_child.py
    :caption:
    :start-after: #end_pymotw_header

This script runs as the parent process.  It starts
``signal_child.py``, then sends the :const:`USR1` signal.

.. literalinclude:: signal_parent.py
    :caption:
    :start-after: #end_pymotw_header

The output is:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'signal_parent.py'))
.. }}}

.. code-block:: none

	$ python3 signal_parent.py
	
	PARENT      : Pausing before sending signal...
	CHILD  26976: Setting up signal handler
	CHILD  26976: Pausing to wait for signal
	PARENT      : Signaling child
	CHILD  26976: Received USR1

.. {{{end}}}

.. _subprocess-process-groups:

Process Groups / Sessions
-------------------------

If the process created by :class:`Popen` spawns sub-processes, those
children will not receive any signals sent to the parent.  That means
when using the ``shell`` argument to :class:`Popen` it will be difficult
to cause the command started in the shell to terminate by sending
:const:`SIGINT` or :const:`SIGTERM`.

.. literalinclude:: subprocess_signal_parent_shell.py
    :caption:
    :start-after: #end_pymotw_header

The pid used to send the signal does not match the pid of the child of
the shell script waiting for the signal, because in this example there
are three separate processes interacting:

1. The program ``subprocess_signal_parent_shell.py``
2. The shell process running the script created by the main python
   program
3. The program ``signal_child.py``

.. {{{cog
.. cog.out(run_script(cog.inFile, 'subprocess_signal_parent_shell.py'))
.. }}}

.. code-block:: none

	$ python3 subprocess_signal_parent_shell.py
	
	PARENT      : Pausing before signaling 26984...
	Shell script in process 26984
	+ python3 signal_child.py
	CHILD  26985: Setting up signal handler
	CHILD  26985: Pausing to wait for signal
	PARENT      : Signaling child 26984
	CHILD  26985: Never received signal

.. {{{end}}}

To send signals to descendants without knowing their process id, use a
*process group* to associate the children so they can be signaled
together.  The process group is created with :func:`os.setpgrp`,
which sets process group id to the process id of the current process.
All child processes inherit their process group from their parent, and
since it should only be set in the shell created by :class:`Popen`
and its descendants, :func:`os.setpgrp` should not be called in the
same process where the :class:`Popen` is created.  Instead, the
function is passed to :class:`Popen` as the ``preexec_fn`` argument so
it is run after the :func:`fork` inside the new process, before it
uses :func:`exec` to run the shell.  To signal the entire process
group, use :func:`os.killpg` with the :attr:`pid` value from the
:class:`Popen` instance.

.. literalinclude:: subprocess_signal_setpgrp.py
    :caption:
    :start-after: #end_pymotw_header

The sequence of events is

1. The parent program instantiates :class:`Popen`.
2. The :class:`Popen` instance forks a new process.
3. The new process runs :func:`os.setpgrp`.
4. The new process runs :func:`exec` to start the shell.
5. The shell runs the shell script.
6. The shell script forks again and that process execs Python.
7. Python runs ``signal_child.py``.
8. The parent program signals the process group using the pid of the shell.
9. The shell and Python processes receive the signal.  
10. The shell ignores the signal. 
11. The Python process running ``signal_child.py`` invokes the signal handler.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'subprocess_signal_setpgrp.py'))
.. }}}

.. code-block:: none

	$ python3 subprocess_signal_setpgrp.py
	
	Calling os.setpgrp() from 26992
	Process group is now 26992
	PARENT      : Pausing before signaling 26992...
	Shell script in process 26992
	+ python3 signal_child.py
	CHILD  26993: Setting up signal handler
	CHILD  26993: Pausing to wait for signal
	PARENT      : Signaling process group 26992
	CHILD  26993: Received USR1

.. {{{end}}}


.. seealso::

   * :pydoc:`subprocess`

   * :mod:`os` -- Although ``subprocess`` replaces many of them, the
     functions for working with processes found in the :mod:`os`
     module are still widely used in existing code.

   * `UNIX Signals and Process Groups
     <http://www.cs.ucsb.edu/~almeroth/classes/W99.276/assignment1/signals.html>`__
     -- A good description of UNIX signaling and how process groups
     work.

   * :mod:`signal` -- More details about using the ``signal`` module.

   * `Advanced Programming in the UNIX(R) Environment
     <http://www.amazon.com/Programming-Environment-Addison-Wesley-Professional-Computing/dp/0201433079/ref=pd_bbs_3/002-2842372-4768037?ie=UTF8&s=books&amp;qid=1182098757&sr=8-3>`__
     -- Covers working with multiple processes, such as handling
     signals, closing duplicated file descriptors, etc.

   * :mod:`pipes` -- Unix shell command pipeline templates in the
     standard library.
