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

