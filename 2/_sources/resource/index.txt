======================================
resource -- System resource management
======================================

.. module:: resource
    :synopsis: System resource management

:Purpose: Manage the system resource limits for a Unix program.
:Available In: 1.5.2

The functions in :mod:`resource` probe the current system resources
consumed by a process, and place limits on them to control how much
load a program can impose on a system.

Current Usage
=============

Use :func:`getrusage()` to probe the resources used by the current
process and/or its children.  The return value is a data structure
containing several resource metrics based on the current state of the
system.

.. note::  

  Not all of the resource values gathered are displayed here.  Refer
  to the `stdlib docs
  <http://docs.python.org/2.7/library/resource.html#resource.getrusage>`_
  for a more complete list.

.. include:: resource_getrusage.py
    :literal:
    :start-after: #end_pymotw_header

Because the test program is extremely simple, it does not use very
many resources:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'resource_getrusage.py'))
.. }}}

::

	$ python resource_getrusage.py
	
	User time                 (ru_utime  ) = 0.010192
	System time               (ru_stime  ) = 0.005743
	Max. Resident Set Size    (ru_maxrss ) = 3891200
	Shared Memory Size        (ru_ixrss  ) = 0
	Unshared Memory Size      (ru_idrss  ) = 0
	Stack Size                (ru_isrss  ) = 0
	Block inputs              (ru_inblock) = 0
	Block outputs             (ru_oublock) = 0

.. {{{end}}}

Resource Limits
===============

Separate from the current actual usage, it is possible to check the
*limits* imposed on the application, and then change them.

.. include:: resource_getrlimit.py
    :literal:
    :start-after: #end_pymotw_header

The return value for each limit is a tuple containing the *soft* limit
imposed by the current configuration and the *hard* limit imposed by
the operating system.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'resource_getrlimit.py'))
.. }}}

::

	$ python resource_getrlimit.py
	
	Maximum core file size            (RLIMIT_CORE    ) :                    0  9223372036854775807
	Maximum CPU time                  (RLIMIT_CPU     ) :  9223372036854775807  9223372036854775807
	Maximum file size                 (RLIMIT_FSIZE   ) :  9223372036854775807  9223372036854775807
	Maximum heap size                 (RLIMIT_DATA    ) :  9223372036854775807  9223372036854775807
	Maximum stack size                (RLIMIT_STACK   ) :              8388608             67104768
	Maximum resident set size         (RLIMIT_RSS     ) :  9223372036854775807  9223372036854775807
	Maximum number of processes       (RLIMIT_NPROC   ) :                  709                 1064
	Maximum number of open files      (RLIMIT_NOFILE  ) :                 2560  9223372036854775807
	Maximum lockable memory address   (RLIMIT_MEMLOCK ) :  9223372036854775807  9223372036854775807

.. {{{end}}}

The limits can be changed with :func:`setrlimit()`.  For example, to
control the number of files a process can open the :const:`RLIMIT_NOFILE`
value can be set to use a smaller soft limit value.

.. include:: resource_setrlimit_nofile.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'resource_setrlimit_nofile.py'))
.. }}}

::

	$ python resource_setrlimit_nofile.py
	
	Soft limit starts as  : 2560
	Soft limit changed to : 4
	random has fd = 3
	[Errno 24] Too many open files: '/dev/null'

.. {{{end}}}

It can also be useful to limit the amount of CPU time a process should
consume, to avoid eating up too much time.  When the process runs past
the allotted amount of time, it it sent a :const:`SIGXCPU` signal.

.. include:: resource_setrlimit_cpu.py
    :literal:
    :start-after: #end_pymotw_header

Normally the signal handler should flush all open files and close
them, but in this case it just prints a message and exits.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'resource_setrlimit_cpu.py', ignore_error=True))
.. }}}

::

	$ python resource_setrlimit_cpu.py
	
	Soft limit starts as  : 9223372036854775807
	Soft limit changed to : 1
	
	Starting: Thu Feb 21 06:36:32 2013
	EXPIRED : Thu Feb 21 06:36:33 2013
	(time ran out)

.. {{{end}}}


.. seealso::

    `resource <http://docs.python.org/2.7/library/resource.html>`_
        The standard library documentation for this module.

    :mod:`signal`
        For details on registering signal handlers.
