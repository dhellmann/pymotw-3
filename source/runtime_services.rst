==================
 Runtime Features
==================

This chapter covers the features of the Python standard library that
allow a program to interact with the interpreter or the environment in
which it runs.

During start-up, the interpreter loads the :mod:`site` module to
configure settings specific to the current installation.  The import
path is constructed from a combination of environment settings,
interpreter build parameters, and configuration files.

The :mod:`sys` module is one of the largest in the standard library.
It includes functions for accessing a broad range of interpreter and
system settings, including interpreter build settings and limits;
command line arguments and program exit codes; exception handling;
thread debugging and control; the import mechanism and imported
modules; runtime control flow tracing; and standard input and output
streams for the process.

While :mod:`sys` is focused on interpreter settings, :mod:`os`
provides access to operating system information.  It can be used for
portable interfaces to system calls that return details about the
running process such as its owner and environment variables.  It also
includes functions for working with the file system and process
management.

Python is often used as a cross-platform language for creating
portable programs.  Even in a program intended to run anywhere, it is
occasionally necessary to know the operating system or hardware
architecture of the current system.  The :mod:`platform` module
provides functions to retrieve runtime settings

The limits for system resources such as the maximum process stack size
or number of open files can be probed and changed through the
:mod:`resource` module.  It also reports the current consumption
rates, so a process can be monitored for resource leaks.

The :mod:`gc` module gives access to the internal state of Python's
garbage collection system.  It includes information useful for
detecting and breaking object cycles, turning the collector on and
off, and adjusting thresholds that automatically trigger collection
sweeps.

The :mod:`sysconfig` module holds the compile-time variables from the
build scripts, and can be used by build and packaging tools to
generate paths and other settings dynamically.

.. It includes modules that provide the ability to probe
.. and control the operating system or hardware platform, adjust the
.. garbage collection system, examine the interpreter installation, and
.. introspect objects and code.

.. toctree::
    :maxdepth: 1

    sys/index

..
    site/index
    os/index
    platform/index
    resource/index
    gc/index
    sysconfig/index
