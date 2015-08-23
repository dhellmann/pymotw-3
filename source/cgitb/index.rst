=====================================
 cgitb -- Detailed Traceback Reports
=====================================

.. module:: cgitb
    :synopsis: Mis-named module that provides extended traceback information.

:Purpose: cgitb provides more detailed traceback information than :mod:`traceback`.
:Python Version: 2.2 and later

:mod:`cgitb` is a valuable debugging tool in the standard library.  It
was originally designed for showing errors and debugging information
in web applications and was later updated to include plain-text output
as well, but unfortunately was never renamed.  This has led to
obscurity and the module is not used as often as it could be.

.. toctree::

   normal

.. only:: bonus

   .. toctree:: 

      bonus

.. seealso::

    `cgitb <http://docs.python.org/library/cgitb.html>`_
        The standard library documentation for this module.

    :mod:`traceback`
        Standard library module for working with tracebacks.

    :mod:`inspect`
        The ``inspect`` module includes more functions for examining the
        stack.

    :mod:`sys`
        The ``sys`` module provides access to the current exception value
        and the ``excepthook`` handler invoked when an exception
        occurs.

    `Improved traceback module <http://thread.gmane.org/gmane.comp.python.devel/110326>`_
        Discussion on the Python development mailing list about
        improvements to the traceback module and related enhancements
        other developers use locally.
