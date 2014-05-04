  ..
     Snippets
     --------
     pyissue - builds reference to a python bug
     porting - starts new section
     mod - builds reference to a module


===========================================
 Changes in Modules Between Python 2 and 3
===========================================

.. _porting-atexit:

atexit
======

When :mod:`atexit` was updated to include a C implementation
(:pyissue:`1680961`), a regression was introduced in the error
handling logic that caused only the summary of the exception to be
shown, without the traceback. This regression was fixed in Python 3.3
(:pyissue:`18776`).


