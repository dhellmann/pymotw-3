============================================================
os -- Portable access to operating system specific features.
============================================================

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

.. toctree::

   normal

.. only:: bonus

   .. toctree::

      bonus

.. seealso::

    `os <http://docs.python.org/lib/module-os.html>`_
        Standard library documentation for this module.

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
