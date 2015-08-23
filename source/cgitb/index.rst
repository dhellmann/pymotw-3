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

Standard Traceback Dumps
========================

Python's default exception handling behavior is to print a traceback
to the standard error output stream with the call stack leading up to
the error position.  This basic output frequently contains enough
information to understand the cause of the exception and permit a fix.

.. include:: cgitb_basic_traceback.py
   :literal:
   :start-after: #end_pymotw_header

This sample program has a subtle error in :func:`func2()`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'cgitb_basic_traceback.py', ignore_error=True))
.. }}}

::

	$ python cgitb_basic_traceback.py
	
	Traceback (most recent call last):
	  File "cgitb_basic_traceback.py", line 17, in <module>
	    func1(1, 5)
	  File "cgitb_basic_traceback.py", line 15, in func1
	    return func2(a, c)
	  File "cgitb_basic_traceback.py", line 11, in func2
	    return a / divisor
	ZeroDivisionError: integer division or modulo by zero

.. {{{end}}}

Enabling Detailed Tracebacks
============================

While the basic traceback includes enough information to spot the
error, enabling :mod:`cgitb` gives more detail.  :mod:`cgitb`
replaces :data:`sys.excepthook` with a function that gives extended
tracebacks.

.. literalinclude:: cgitb_local_vars.py
   :lines: 10-11

The error report from this example is much more extensive than the
original.  Each frame of the stack is listed, along with:

* the full path to the source file, instead of just the base name
* the values of the arguments to each function in the stack
* a few lines of source context from around the line in the error path
* the values of variables in the expression causing the error

Having access to the variables involved in the error stack can help
find a logical error that occurs somewhere higher in the stack than
the line where the actual exception is generated.

.. NOT RUNNING
.. cog.out(run_script(cog.inFile, 'cgitb_local_vars.py', 
..                    ignore_error=True, break_lines_at=68, line_break_mode='fill'))

::

	$ python cgitb_local_vars.py
	
	<type 'exceptions.ZeroDivisionError'>
	Python 2.7: /Users/dhellmann/.virtualenvs/pymotw/bin/python
	Sat Dec  4 12:59:15 2010
	
	A problem occurred in a Python script.  Here is the sequence of
	function calls leading up to the error, in the order they occurred.
	
	 /Users/dhellmann/Documents/PyMOTW/book/PyMOTW/cgitb/cgitb_local_var
	 s.py in <module>()
	   16 def func1(a, b):
	   17     c = b - 5
	   18     return func2(a, c)
	   19 
	   20 func1(1, 5)
	func1 = <function func1>
	
	 /Users/dhellmann/Documents/PyMOTW/book/PyMOTW/cgitb/cgitb_local_var
	 s.py in func1(a=1, b=5)
	   16 def func1(a, b):
	   17     c = b - 5
	   18     return func2(a, c)
	   19 
	   20 func1(1, 5)
	global func2 = <function func2>
	a = 1
	c = 0
	
	 /Users/dhellmann/Documents/PyMOTW/book/PyMOTW/cgitb/cgitb_local_var
	 s.py in func2(a=1, divisor=0)
	   12 
	   13 def func2(a, divisor):
	   14     return a / divisor
	   15 
	   16 def func1(a, b):
	a = 1
	divisor = 0
	<type 'exceptions.ZeroDivisionError'>: integer division or modulo by
	zero
	    __class__ = <type 'exceptions.ZeroDivisionError'>
	    __dict__ = {}
	    __doc__ = 'Second argument to a division or modulo operation was
	    zero.'
        ...method references removed...
	    args = ('integer division or modulo by zero',)
	    message = 'integer division or modulo by zero'
	
	The above is a description of an error in a Python program.  Here is
	the original traceback:
	
	Traceback (most recent call last):
	  File "cgitb_local_vars.py", line 20, in <module>
	    func1(1, 5)
	  File "cgitb_local_vars.py", line 18, in func1
	    return func2(a, c)
	  File "cgitb_local_vars.py", line 14, in func2
	    return a / divisor
	ZeroDivisionError: integer division or modulo by zero
	

In the case of this code with a :class:`ZeroDivisionError`, it is
apparent that the problem is introduced in the computation of the
value of ``c`` in :func:`func1`, rather than where the value is used
in :func:`func2`.

The end of the output also includes the full details of the exception
object (in case it has attributes other than ``message`` that would be
useful for debugging) and the original form of a traceback dump.

Local Variables in Tracebacks
=============================

The code in :mod:`cgitb` that examines the variables used in the stack
frame leading to the error is smart enough to evaluate object
attributes to display them, too.

.. include:: cgitb_with_classes.py
   :literal:
   :start-after: #end_pymotw_header

If a function or method includes a lot of in-line comments,
whitespace, or other code that makes it very long, then having the
default of five lines of context may not provide enough direction.
When the body of the function is pushed out of the code window
displayed, there is not enough context to understand the location of
the error.  Using a larger context value with :mod:`cgitb` solves this
problem.  Passing an integer as the *context* argument to
:func:`enable()` controls the amount of code displayed for each line
of the traceback.

This output show that ``self.a`` and ``self.b`` are involved in the
error-prone code.

.. NOT RUNNING
.. cog.out(run_script(cog.inFile, 'cgitb_with_classes.py', 
..                    ignore_error=True, break_lines_at=68, line_break_mode='fill'))

::

	$ python cgitb_with_classes.py | grep -v method
	
	<type 'exceptions.ZeroDivisionError'>
	Python 2.7: /Users/dhellmann/.virtualenvs/pymotw/bin/python
	Sat Dec  4 12:59:16 2010
	
	A problem occurred in a Python script.  Here is the sequence of
	function calls leading up to the error, in the order they occurred.
	
	 /Users/dhellmann/Documents/PyMOTW/book/PyMOTW/cgitb/cgitb_with_clas
	 ses.py in <module>()
	   20         self.a = a
	   21         self.b = b
	   22         self.c = self.a * self.b
	   23         # Really
	   24         # long
	   25         # comment
	   26         # goes
	   27         # here.
	   28         self.d = self.a / self.b
	   29         return
	   30 
	   31 o = BrokenClass(1, 0)
	o undefined
	BrokenClass = <class '__main__.BrokenClass'>
	
	 /Users/dhellmann/Documents/PyMOTW/book/PyMOTW/cgitb/cgitb_with_clas
	 ses.py in __init__(self=<__main__.BrokenClass object>, a=1, b=0)
	   20         self.a = a
	   21         self.b = b
	   22         self.c = self.a * self.b
	   23         # Really
	   24         # long
	   25         # comment
	   26         # goes
	   27         # here.
	   28         self.d = self.a / self.b
	   29         return
	   30 
	   31 o = BrokenClass(1, 0)
	self = <__main__.BrokenClass object>
	self.d undefined
	self.a = 1
	self.b = 0
	<type 'exceptions.ZeroDivisionError'>: integer division or modulo by
	zero
	    __class__ = <type 'exceptions.ZeroDivisionError'>
	    __dict__ = {}
	    __doc__ = 'Second argument to a division or modulo operation was
	    zero.'
        ...method references removed...
	    args = ('integer division or modulo by zero',)
	    message = 'integer division or modulo by zero'
	
	The above is a description of an error in a Python program.  Here is
	the original traceback:
	
	Traceback (most recent call last):
	  File "cgitb_with_classes.py", line 31, in <module>
	    o = BrokenClass(1, 0)
	  File "cgitb_with_classes.py", line 28, in __init__
	    self.d = self.a / self.b
	ZeroDivisionError: integer division or modulo by zero


Exception Properties
====================

In addition to the local variables from each stack frame, :mod:`cgitb`
shows all properties of the exception object.  Extra properties on
custom exception types are printed as part of the error report.

.. include:: cgitb_exception_properties.py
   :literal:
   :start-after: #end_pymotw_header

In this example, the *bad_value* property is included along with the
standard *message* and *args* values.

.. NOT RUNNING
.. cog.out(run_script(cog.inFile, 'cgitb_exception_properties.py', 
..                    ignore_error=True, break_lines_at=68, line_break_mode='fill'))

::

	$ python cgitb_exception_properties.py
	
	<class '__main__.MyException'>
	Python 2.7: /Users/dhellmann/.virtualenvs/pymotw/bin/python
	Sat Dec  4 12:59:16 2010
	
	A problem occurred in a Python script.  Here is the sequence of
	function calls leading up to the error, in the order they occurred.
	
	 /Users/dhellmann/Documents/PyMOTW/book/PyMOTW/cgitb/cgitb_exception
	 _properties.py in <module>()
	   18         self.bad_value = bad_value
	   19         Exception.__init__(self, message)
	   20         return
	   21 
	   22 raise MyException('Normal message', bad_value=99)
	MyException = <class '__main__.MyException'>
	bad_value undefined
	<class '__main__.MyException'>: Normal message
	    __class__ = <class '__main__.MyException'>
	    __dict__ = {'bad_value': 99}
	    __doc__ = 'Add extra properties to a special exception\n    '
	    __module__ = '__main__'
        ...method references removed...
	    args = ('Normal message',)
	    bad_value = 99
	    message = 'Normal message'
	
	The above is a description of an error in a Python program.  Here is
	the original traceback:
	
	Traceback (most recent call last):
	  File "cgitb_exception_properties.py", line 22, in <module>
	    raise MyException('Normal message', bad_value=99)
	MyException: Normal message
	
	

.. {{{end}}}


HTML Output
===========

Because :mod:`cgitb` was originally developed for handling exceptions
in web applications, no discussion would be complete without
mentioning its original HTML output format.  The earlier examples all
shows plain text output.  To produce HTML instead, leave out the
*format* argument (or specify ``"html"``).  Most modern web
applications are constructed using a framework that includes an error
reporting facility, so the HTML form is largely obsolete.

Logging Tracebacks
==================

For many situations, printing the traceback details to standard error
is the best resolution.  In a production system, however, logging the
errors is even better.  The :func:`enable()` function includes an optional
argument, *logdir*, to enable error logging.  When a directory name is
provided, each exception is logged to its own file in the given
directory.

.. include:: cgitb_log_exception.py
   :literal:
   :start-after: #end_pymotw_header

Even though the error display is suppressed, a message is printed
describing where to go to find the error log.

.. {{{cog
.. path('PyMOTW/cgitb/LOGS').rmtree()
.. sh('mkdir -p PyMOTW/cgitb/LOGS')
.. cog.out(run_script(cog.inFile, 'cgitb_log_exception.py', 
..                    ignore_error=True, break_lines_at=68, line_break_mode='fill'))
.. cog.out(run_script(cog.inFile, 'ls LOGS', interpreter=None, include_prefix=False))
.. cog.out(run_script(cog.inFile, 'cat LOGS/*.txt', interpreter=None, include_prefix=False, 
..                    ignore_error=True, break_lines_at=68, line_break_mode='fill'))
.. }}}

::

	$ python cgitb_log_exception.py
	
	<p>A problem occurred in a Python script.
	<p> /Users/dhellmann/Documents/PyMOTW/book/PyMOTW/cgitb/LOGS/tmpy2v8
	NM.txt contains the description of this error.

	$ ls LOGS
	
	tmpy2v8NM.txt

	$ cat LOGS/*.txt
	
	<type 'exceptions.ZeroDivisionError'>
	Python 2.7: /Users/dhellmann/.virtualenvs/pymotw/bin/python
	Sat Dec  4 12:59:15 2010
	
	A problem occurred in a Python script.  Here is the sequence of
	function calls leading up to the error, in the order they occurred.
	
	 /Users/dhellmann/Documents/PyMOTW/book/PyMOTW/cgitb/cgitb_log_excep
	 tion.py in <module>()
	   17 
	   18 def func(a, divisor):
	   19     return a / divisor
	   20 
	   21 func(1, 0)
	func = <function func>
	
	 /Users/dhellmann/Documents/PyMOTW/book/PyMOTW/cgitb/cgitb_log_excep
	 tion.py in func(a=1, divisor=0)
	   17 
	   18 def func(a, divisor):
	   19     return a / divisor
	   20 
	   21 func(1, 0)
	a = 1
	divisor = 0
	<type 'exceptions.ZeroDivisionError'>: integer division or modulo by
	zero
	    __class__ = <type 'exceptions.ZeroDivisionError'>
	    __delattr__ = <method-wrapper '__delattr__' of
	    exceptions.ZeroDivisionError object>
	    __dict__ = {}
	    __doc__ = 'Second argument to a division or modulo operation was
	    zero.'
	    __format__ = <built-in method __format__ of
	    exceptions.ZeroDivisionError object>
	    __getattribute__ = <method-wrapper '__getattribute__' of
	    exceptions.ZeroDivisionError object>
	    __getitem__ = <method-wrapper '__getitem__' of
	    exceptions.ZeroDivisionError object>
	    __getslice__ = <method-wrapper '__getslice__' of
	    exceptions.ZeroDivisionError object>
	    __hash__ = <method-wrapper '__hash__' of
	    exceptions.ZeroDivisionError object>
	    __init__ = <method-wrapper '__init__' of
	    exceptions.ZeroDivisionError object>
	    __new__ = <built-in method __new__ of type object>
	    __reduce__ = <built-in method __reduce__ of
	    exceptions.ZeroDivisionError object>
	    __reduce_ex__ = <built-in method __reduce_ex__ of
	    exceptions.ZeroDivisionError object>
	    __repr__ = <method-wrapper '__repr__' of
	    exceptions.ZeroDivisionError object>
	    __setattr__ = <method-wrapper '__setattr__' of
	    exceptions.ZeroDivisionError object>
	    __setstate__ = <built-in method __setstate__ of
	    exceptions.ZeroDivisionError object>
	    __sizeof__ = <built-in method __sizeof__ of
	    exceptions.ZeroDivisionError object>
	    __str__ = <method-wrapper '__str__' of
	    exceptions.ZeroDivisionError object>
	    __subclasshook__ = <built-in method __subclasshook__ of type
	    object>
	    __unicode__ = <built-in method __unicode__ of
	    exceptions.ZeroDivisionError object>
	    args = ('integer division or modulo by zero',)
	    message = 'integer division or modulo by zero'
	
	The above is a description of an error in a Python program.  Here is
	the original traceback:
	
	Traceback (most recent call last):
	  File "cgitb_log_exception.py", line 21, in <module>
	    func(1, 0)
	  File "cgitb_log_exception.py", line 19, in func
	    return a / divisor
	ZeroDivisionError: integer division or modulo by zero
	

.. {{{end}}}


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
