===============================================
 platform -- Access system version information
===============================================

.. module:: platform
    :synopsis: Access system hardware, OS, and interpreter version information.

:Purpose: Probe the underlying platform's hardware, operating system, and interpreter version information.
:Available In: 2.3 and later

Although Python is often used as a cross-platform language, it is
occasionally necessary to know what sort of system a program is
running on. Build tools need that information, but an application
might also know that some of the libraries or external commands it
uses have different interfaces on different operating systems. For
example, a tool to manage the network configuration of an operating
system can define a portable representation of network interfaces,
aliases, IP addresses, etc. But once it actually needs to edit the
configuration files, it must know more about the host so it can use
the correct operating system configuration commands and files.  The
:mod:`platform` module includes the tools for learning about the
interpreter, operating system, and hardware platform where a program
is running.

.. note::

    The example output below was generated on a MacBook Pro3,1 running
    OS X 10.6.4, a VMware Fusion VM running CentOS 5.5, and a Dell PC
    running Microsoft Windows 2008.  Python was installed on the OS X
    and Windows systems using the pre-compiled installer from
    python.org.  The Linux system is running an interpreter built from
    source locally.

Interpreter
===========

There are four functions for getting information about the current
Python interpreter. :func:`python_version` and
:func:`python_version_tuple` return different forms of the interpreter
version with major, minor, and patchlevel components.
:func:`python_compiler` reports on the compiler used to build the
interpreter. And :func:`python_build` gives a version string for the
build of the interpreter.

.. include:: platform_python.py
    :literal:
    :start-after: #end_pymotw_header


OS X:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'platform_python.py'))
.. }}}

::

	$ python platform_python.py
	
	Version      : 2.7.2
	Version tuple: ('2', '7', '2')
	Compiler     : GCC 4.2.1 (Apple Inc. build 5666) (dot 3)
	Build        : ('v2.7.2:8527427914a2', 'Jun 11 2011 15:22:34')

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

:func:`platform` returns string containing a general purpose platform
identifier.  The function accepts two optional boolean arguments. If
*aliased* is True, the names in the return value are converted from a
formal name to their more common form. When *terse* is true, returns a
minimal value with some parts dropped.

.. include:: platform_platform.py
    :literal:
    :start-after: #end_pymotw_header

OS X:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'platform_platform.py'))
.. }}}

::

	$ python platform_platform.py
	
	Normal : Darwin-11.4.2-x86_64-i386-64bit
	Aliased: Darwin-11.4.2-x86_64-i386-64bit
	Terse  : Darwin-11.4.2

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
interpreter is running under can be retrieved as well. ``uname()``
returns a tuple containing the system, node, release, version,
machine, and processor values.  Individual values can be accessed
through functions of the same names:

:func:`system`
  returns the operating system name
:func:`node`
  returns the hostname of the server, not fully qualified
:func:`release`
  returns the operating system release number
:func:`version`
  returns the more detailed system version
:func:`machine`
  gives a hardware-type identifier such as ``'i386'``
:func:`processor`
  returns a real identifier for the processor, or the same value as
  machine() in many cases

.. include:: platform_os_info.py
    :literal:
    :start-after: #end_pymotw_header


OS X:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'platform_os_info.py'))
.. }}}

::

	$ python platform_os_info.py
	
	uname: ('Darwin', 'hubert.local', '11.4.2', 'Darwin Kernel Version 11.4.2: Thu Aug 23 16:25:48 PDT 2012; root:xnu-1699.32.7~1/RELEASE_X86_64', 'x86_64', 'i386')
	
	system   : Darwin
	node     : hubert.local
	release  : 11.4.2
	version  : Darwin Kernel Version 11.4.2: Thu Aug 23 16:25:48 PDT 2012; root:xnu-1699.32.7~1/RELEASE_X86_64
	machine  : x86_64
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
    uname: ('Windows', 'dhellmann', '2008ServerR2', '6.1.7600', 'AMD64', 
    'Intel64 Family 6 Model 15 Stepping 11, GenuineIntel')

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
executable program (defaulting to ``sys.executable``, the Python
interpreter). The return value is a tuple containing the bit
architecture and the linkage format used.

.. include:: platform_architecture.py
    :literal:
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

    `platform <https://docs.python.org/2/library/platform.html>`_
        Standard library documentation for this module.
