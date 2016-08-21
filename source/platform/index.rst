========================================
 platform -- System Version Information
========================================

.. module:: platform
    :synopsis: System version information

:Purpose: Probe the underlying platform's hardware, operating system, and interpreter version information.

Although Python is often used as a cross-platform language, it is
occasionally necessary to know what sort of system a program is
running on. Build tools need that information, but an application
might also know that some of the libraries or external commands it
uses have different interfaces on different operating systems. For
example, a tool to manage the network configuration of an operating
system can define a portable representation of network interfaces,
aliases, IP addresses, etc. But when the time comes to edit the
configuration files, it must know more about the host so it can use
the correct operating system configuration commands and files.  The
:mod:`platform` module includes the tools for learning about the
interpreter, operating system, and hardware platform where a program
is running.

.. note::

    The example output in this section was generated on three systems:
    a MacBook Pro3,1 running OS X 10.6.5, a VMware Fusion VM running
    CentOS 5.5, and a Dell PC running Microsoft Windows 2008.  Python
    was installed on the OS X and Windows systems using the
    pre-compiled installer from python.org.  The Linux system is
    running an interpreter built from source locally.

Interpreter
===========

There are four functions for getting information about the current
Python interpreter. :func:`python_version` and
:func:`python_version_tuple` return different forms of the interpreter
version with major, minor, and patch level components.
:func:`python_compiler` reports on the compiler used to build the
interpreter. And :func:`python_build` gives a version string for the
build of the interpreter.

.. literalinclude:: platform_python.py
    :caption:
    :start-after: #end_pymotw_header


OS X:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'platform_python.py'))
.. }}}

::

	$ python platform_python.py
	
	Version      : 2.7.0
	Version tuple: ('2', '7', '0')
	Compiler     : GCC 4.0.1 (Apple Inc. build 5493)
	Build        : ('r27:82508', 'Jul  3 2010 21:12:11')

.. {{{end}}}

Linux::

    $ python platform_python.py 

    Version      : 2.7.0
    Version tuple: ('2', '7', '0')
    Compiler     : GCC 4.1.2 20080704 (Red Hat 4.1.2-46)
    Build        : ('r27', 'Aug 20 2010 11:37:51')

Windows::

    C:> python.exe platform_python.py

    Version      : 2.7.0
    Version tuple: ['2', '7', '0']
    Compiler     : MSC v.1500 64 bit (AMD64)
    Build        : ('r27:82525', 'Jul  4 2010 07:43:08')

Platform
========

The :func:`platform` function returns a string containing a general
purpose platform identifier.  The function accepts two optional
boolean arguments. If *aliased* is True, the names in the return value
are converted from a formal name to their more common form. When
*terse* is true, a minimal value with some parts dropped is returned
instead of the full string.

.. literalinclude:: platform_platform.py
    :caption:
    :start-after: #end_pymotw_header

OS X:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'platform_platform.py'))
.. }}}

::

	$ python platform_platform.py
	
	Normal : Darwin-10.5.0-i386-64bit
	Aliased: Darwin-10.5.0-i386-64bit
	Terse  : Darwin-10.5.0

.. {{{end}}}

Linux::

    $ python platform_platform.py 

    Normal : Linux-2.6.18-194.3.1.el5-i686-with-redhat-5.5-Final
    Aliased: Linux-2.6.18-194.3.1.el5-i686-with-redhat-5.5-Final
    Terse  : Linux-2.6.18-194.3.1.el5-i686-with-glibc2.3

Windows::

    C:> python.exe platform_platform.py

    Normal : Windows-2008ServerR2-6.1.7600
    Aliased: Windows-2008ServerR2-6.1.7600
    Terse  : Windows-2008ServerR2
    

Operating System and Hardware Info
==================================

More detailed information about the operating system and hardware the
interpreter is running under can be retrieved as well. :func:`uname`
returns a tuple containing the system, node, release, version,
machine, and processor values.  Individual values can be accessed
through functions of the same names, listed in :table:`Platform
Information Functions`.

.. table:: Platform Information Functions

  =================  ============
  Function           Return Value
  =================  ============
  :func:`system`     operating system name
  :func:`node`       host name of the server, not fully qualified
  :func:`release`    operating system release number
  :func:`version`    more detailed system version
  :func:`machine`    a hardware-type identifier, such as ``'i386'``
  :func:`processor`  a real identifier for the processor (the same value as :func:`machine` in many cases)
  =================  ============

.. literalinclude:: platform_os_info.py
    :caption:
    :start-after: #end_pymotw_header


OS X:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'platform_os_info.py', 
..                    break_lines_at=65, line_break_mode='wrap'))
.. }}}

::

	$ python platform_os_info.py
	
	uname: ('Darwin', 'farnsworth.local', '10.5.0', 'Darwin Kernel
	Version 10.5.0: Fri Nov  5 23:20:39 PDT 2010;
	root:xnu-1504.9.17~1/RELEASE_I386', 'i386', 'i386')
	
	system   : Darwin
	node     : farnsworth.local
	release  : 10.5.0
	version  : Darwin Kernel Version 10.5.0: Fri Nov  5 23:20:39 PDT
	2010; root:xnu-1504.9.17~1/RELEASE_I386
	machine  : i386
	processor: i386

.. {{{end}}}

Linux::

    $ python platform_os_info.py 

    uname: ('Linux', 'hermes.hellfly.net', '2.6.18-194.3.1.el5', 
    '#1 SMP Thu May 13 13:09:10 EDT 2010', 'i686', 'i686')
    
    system   : Linux
    node     : hermes.hellfly.net
    release  : 2.6.18-194.3.1.el5
    version  : #1 SMP Thu May 13 13:09:10 EDT 2010
    machine  : i686
    processor: i686

Windows::

    C:> python.exe platform_os_info.py

    uname: ('Windows', 'dhellmann', '2008ServerR2', '6.1.7600', 
    'AMD64', 'Intel64 Family 6 Model 15 Stepping 11, GenuineIntel')

    system   : Windows
    node     : dhellmann
    release  : 2008ServerR2
    version  : 6.1.7600
    machine  : AMD64
    processor: Intel64 Family 6 Model 15 Stepping 11, GenuineIntel
    

Executable Architecture
=======================

Individual program architecture information can be probed using the
:func:`architecture` function. The first argument is the path to an
executable program (defaulting to :data:`sys.executable`, the Python
interpreter). The return value is a tuple containing the bit
architecture and the linkage format used.

.. literalinclude:: platform_architecture.py
    :caption:
    :start-after: #end_pymotw_header


OS X:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'platform_architecture.py'))
.. }}}

::

	$ python platform_architecture.py
	
	interpreter: ('64bit', '')
	/bin/ls    : ('64bit', '')

.. {{{end}}}

Linux::

    $ python platform_architecture.py 

    interpreter: ('32bit', 'ELF')
    /bin/ls    : ('32bit', 'ELF')

Windows::

    C:> python.exe platform_architecture.py

    interpreter  : ('64bit', 'WindowsPE')
    iexplore.exe : ('64bit', '')

.. seealso::

    `platform <http://docs.python.org/lib/module-platform.html>`_
        Standard library documentation for this module.
