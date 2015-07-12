.. _sys-runtime:

===================
Runtime Environment
===================

:mod:`sys` provides low-level APIs for interacting with the system
outside of an application, by accepting command line arguments,
accessing user input, and passing messages and status values to the
user.

.. _sys-argv:

Command Line Arguments
======================

The arguments captured by the interpreter are processed there and not
passed to the program being run.  Any remaining options and arguments,
including the name of the script itself, are saved to
:const:`sys.argv` in case the program does need to use them.

.. include:: sys_argv.py
    :literal:
    :start-after: #end_pymotw_header

In the third example, the ``-u`` option is understood by the
interpreter, and is not passed to the program being run.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_argv.py'))
.. cog.out(run_script(cog.inFile, 'sys_argv.py -v foo blah', include_prefix=False))
.. cog.out(run_script(cog.inFile, '-u sys_argv.py', include_prefix=False))
.. }}}

::

	$ python3 sys_argv.py
	
	Arguments: ['sys_argv.py']

	$ python3 sys_argv.py -v foo blah
	
	Arguments: ['sys_argv.py', '-v', 'foo', 'blah']

	$ python3 -u sys_argv.py
	
	Arguments: ['sys_argv.py']

.. {{{end}}}

.. seealso::

    * :mod:`argparse` -- Module for parsing command line arguments.

.. _sys-input-output:

Input and Output Steams
=======================

Following the UNIX paradigm, Python programs can access three file
descriptors by default.

.. include:: sys_stdio.py
    :literal:
    :start-after: #end_pymotw_header

:const:`stdin` is the standard way to read input, usually from a
console but also from other programs via a pipeline.  :const:`stdout`
is the standard way to write output for a user (to the console) or to
be sent to the next program in a pipeline.  :const:`stderr` is
intended for use with warning or error messages.

.. {{{cog
.. cog.out(run_script(cog.inFile, interpreter='cat sys_stdio.py | python3 -u', script_name='sys_stdio.py'))
.. }}}

::

	$ cat sys_stdio.py | python3 -u sys_stdio.py
	
	STATUS: Reading from stdin
	STATUS: Writing data to stdout
	#!/usr/bin/env python
	#end_pymotw_header
	
	import sys
	
	print('STATUS: Reading from stdin', file=sys.stderr)
	
	data = sys.stdin.read()
	
	print('STATUS: Writing data to stdout', file=sys.stderr)
	
	sys.stdout.write(data)
	sys.stdout.flush()
	
	print('STATUS: Done', file=sys.stderr)
	STATUS: Done

.. {{{end}}}


.. seealso::

    * :mod:`subprocess` and :mod:`pipes` -- Both subprocess and pipes
      have features for pipelining programs together.

Returning Status
================

To return an exit code from a program, pass an integer value to
:func:`sys.exit`.

.. include:: sys_exit.py
    :literal:
    :start-after: #end_pymotw_header

A nonzero value means the program exited with an error.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sys_exit.py 0 ; echo "Exited $?"'))
.. cog.out(run_script(cog.inFile, 'sys_exit.py 1 ; echo "Exited $?"', include_prefix=False, ignore_error=True))
.. }}}

::

	$ python3 sys_exit.py 0 ; echo "Exited $?"
	
	Exited 0

	$ python3 sys_exit.py 1 ; echo "Exited $?"
	
	Exited 1

.. {{{end}}}
