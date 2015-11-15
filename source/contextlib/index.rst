==========================================
 contextlib --- Context Manager Utilities
==========================================

.. module:: contextlib
    :synopsis: Utilities for creating and working with context managers.

:Purpose: Utilities for creating and working with context managers.

The :mod:`contextlib` module contains utilities for working with
context managers and the :command:`with` statement.

Context Manager API
===================

A *context manager* is responsible for a resource within a code block,
possibly creating it when the block is entered and then cleaning it up
after the block is exited.  For example, files support the context
manager API to make it easy to ensure they are closed after all
reading or writing is done.

.. include:: contextlib_file.py
   :literal:
   :start-after: #end_pymotw_header

A context manager is enabled by the :command:`with` statement, and the
API involves two methods.  The :func:`__enter__` method is run when
execution flow enters the code block inside the :command:`with`.  It
returns an object to be used within the context.  When execution flow
leaves the :command:`with` block, the :func:`__exit__` method of the
context manager is called to clean up any resources being used.

.. include:: contextlib_api.py
   :literal:
   :start-after: #end_pymotw_header

Combining a context manager and the :command:`with` statement is a
more compact way of writing a :command:`try:finally` block, since the
context manager's :func:`__exit__` method is always called, even if an
exception is raised.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_api.py'))
.. }}}

::

	$ python3 contextlib_api.py
	
	__init__()
	__enter__()
	Doing work in the context
	__exit__()

.. {{{end}}}

The :func:`__enter__` method can return any object to be associated
with a name specified in the :command:`as` clause of the
:command:`with` statement.  In this example, the :class:`Context`
returns an object that uses the open context.

.. include:: contextlib_api_other_object.py
   :literal:
   :start-after: #end_pymotw_header

The value associated with the variable :data:`c` is the object
returned by :func:`__enter__`, which is not necessarily the
:class:`Context` instance created in the :command:`with` statement.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_api_other_object.py'))
.. }}}

::

	$ python3 contextlib_api_other_object.py
	
	Context.__init__()
	Context.__enter__()
	WithinContext.__init__(<__main__.Context object at 0x1021a97b8>)
	WithinContext.do_something()
	Context.__exit__()
	WithinContext.__del__

.. {{{end}}}

The :func:`__exit__` method receives arguments containing details of
any exception raised in the :command:`with` block.  

.. include:: contextlib_api_error.py
   :literal:
   :start-after: #end_pymotw_header

If the context manager can handle the exception, :func:`__exit__`
should return a true value to indicate that the exception does not
need to be propagated.  Returning false causes the exception to be
re-raised after :func:`__exit__` returns.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_api_error.py', ignore_error=True))
.. }}}

::

	$ python3 contextlib_api_error.py
	
	__init__(True)
	__enter__()
	__exit__()
	  exc_type = <class 'RuntimeError'>
	  exc_val  = error message handled
	  exc_tb   = <traceback object at 0x1012e0dc8>
	
	__init__(False)
	__enter__()
	__exit__()
	  exc_type = <class 'RuntimeError'>
	  exc_val  = error message propagated
	  exc_tb   = <traceback object at 0x1012e0dc8>
	Traceback (most recent call last):
	  File "contextlib_api_error.py", line 34, in <module>
	    raise RuntimeError('error message propagated')
	RuntimeError: error message propagated

.. {{{end}}}

Context Managers as Function Decorators
=======================================

The class :class:`ContextDecorator` adds support to regular context
manager classes to let them be used as function decorators as well as
context managers.

.. include:: contextlib_decorator.py
   :literal:
   :start-after: #end_pymotw_header

One difference with using the context manager as a decorator is that
the value returned by :func:`__enter__` is not available inside the
function being decorated, unlike when using :command:`with` and
:command:`as`. Arguments passed to the decorated function are
available in the usual way.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_decorator.py'))
.. }}}

::

	$ python3 contextlib_decorator.py
	
	__init__(as decorator)
	
	__init__(as context manager)
	__enter__(as context manager)
	Doing work in the context
	__exit__(as context manager)
	
	__enter__(as decorator)
	Doing work in the wrapped function
	__exit__(as decorator)

.. {{{end}}}



From Generator to Context Manager
=================================

Creating context managers the traditional way, by writing a class with
:func:`__enter__()` and :func:`__exit__()` methods, is not
difficult. But sometimes writing everything out fully is extra
overhead for a trivial bit of context. In those sorts of situations,
use the :func:`contextmanager()` decorator to convert a generator
function into a context manager.

.. include:: contextlib_contextmanager.py
    :literal:
    :start-after: #end_pymotw_header

The generator should initialize the context, yield exactly one time,
then clean up the context. The value yielded, if any, is bound to the
variable in the :command:`as` clause of the :command:`with`
statement. Exceptions from within the :command:`with` block are
re-raised inside the generator, so they can be handled there.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_contextmanager.py',
..                    ignore_error=True))
.. }}}

::

	$ python3 contextlib_contextmanager.py
	
	Normal:
	  entering
	  inside with statement: {}
	  exiting
	
	Handled error:
	  entering
	  ERROR: showing example of handling an error
	  exiting
	
	Unhandled error:
	  entering
	  exiting
	Traceback (most recent call last):
	  File "contextlib_contextmanager.py", line 32, in <module>
	    raise ValueError('this exception is not handled')
	ValueError: this exception is not handled

.. {{{end}}}

The context manager returned by :func:`contextmanager` is derived from
:class:`ContextDecorator`, so it also works as a function decorator.

.. include:: contextlib_contextmanager_decorator.py
   :literal:
   :start-after: #end_pymotw_header

As in the :class:`ContextDecorator` example above, when the context
manager is used as a decorator the value yielded by the generator is
not available inside the function being decorated. Arguments passed to
the decorated function are still available, as demonstrated by
:func:`throw_error` in this example.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_contextmanager_decorator.py', 
..                    ignore_error=True))
.. }}}

::

	$ python3 contextlib_contextmanager_decorator.py
	
	Normal:
	  entering
	  inside with statement
	  exiting
	
	Handled error:
	  entering
	  ERROR: showing example of handling an error
	  exiting
	
	Unhandled error:
	  entering
	  exiting
	Traceback (most recent call last):
	  File "contextlib_contextmanager_decorator.py", line 43, in <mo
	dule>
	    throw_error(ValueError('this exception is not handled'))
	  File "/Library/Frameworks/Python.framework/Versions/3.5/lib/py
	thon3.5/contextlib.py", line 30, in inner
	    return func(*args, **kwds)
	  File "contextlib_contextmanager_decorator.py", line 33, in thr
	ow_error
	    raise err
	ValueError: this exception is not handled

.. {{{end}}}

Closing Open Handles
====================

The :class:`file` class supports the context manager API directly, but
some other objects that represent open handles do not. The example
given in the standard library documentation for :mod:`contextlib` is
the object returned from :func:`urllib.urlopen`.  There are other
legacy classes that use a :func:`close` method but do not support the
context manager API. To ensure that a handle is closed, use
:func:`closing()` to create a context manager for it.

.. include:: contextlib_closing.py
    :literal:
    :start-after: #end_pymotw_header

The handle is closed whether there is an error in the :command:`with`
block or not.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_closing.py'))
.. }}}

::

	$ python3 contextlib_closing.py
	
	Normal Example:
	  __init__()
	  inside with statement: open
	  close()
	  outside with statement: closed
	
	Error handling example:
	  __init__()
	  raising from inside with statement
	  close()
	  Had an error: error message

.. {{{end}}}

Ignoring Exceptions
===================

It is frequently useful to ignore exceptions raised by libraries,
because the error indicates that the desired state has already been
achieved, or it can otherwise be ignored. The most common way to
ignore exceptions is with a ``try:except`` statement with only a
``pass`` statement in the ``except`` block.

.. include:: contextlib_ignore_error.py
   :literal:
   :start-after: #end_pymotw_header

In this case, the operation fails and the error is ignored.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_ignore_error.py'))
.. }}}

::

	$ python3 contextlib_ignore_error.py
	
	trying non-idempotent operation
	done

.. {{{end}}}

The ``try:except`` form can be replaced with
:func:`contextlib.suppress` to more explicitly suppress a class of
exceptions happening anywhere in the ``with`` block.

.. include:: contextlib_suppress.py
   :literal:
   :start-after: #end_pymotw_header

In this updated version, the exception is discarded entirely.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_suppress.py'))
.. }}}

::

	$ python3 contextlib_suppress.py
	
	trying non-idempotent operation
	done

.. {{{end}}}

Redirecting Output Streams
==========================

Poorly designed library code may write directly to ``sys.stdout`` or
``sys.stderr``, without providing arguments to configure different
output destinations. The :func:`redirect_stdout` and
:func:`redirect_stderr` context managers can be used to capture output
from functions like this, for which the source cannot be changed to
accept a new output argument.

.. include:: contextlib_redirect.py
   :literal:
   :start-after: #end_pymotw_header

In this example, ``misbehaving_function()`` writes to both ``stdout``
and ``stderr``, but the two context managers send that output to the
same :class:`io.StringIO` instance where it is saved to be used later.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_redirect.py'))
.. }}}

::

	$ python3 contextlib_redirect.py
	
	(stdout) A: 5
	(stderr) A: 5
	

.. {{{end}}}

.. note::

   Both :func:`redirect_stdout` and :func:`redirect_stderr` modify
   global state by replacing objects in the :mod:`sys` module, and
   should be used with care. The functions are not thread-safe, and
   may interfere with other operations that expect the standard output
   streams to be attached to terminal devices.


.. seealso::

   * :pydoc:`contextlib`

   * :pep:`343` -- The :command:`with` statement.

   * `Context Manager Types
     <http://docs.python.org/library/stdtypes.html#typecontextmanager>`__
     -- Description of the context manager API from the standard
     library documentation.

   * `With Statement Context Managers
     <http://docs.python.org/reference/datamodel.html#context-managers>`__
     -- Description of the context manager API from the Python
     Reference Guide.
