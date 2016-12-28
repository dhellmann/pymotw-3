==========================================
 contextlib --- Context Manager Utilities
==========================================

.. module:: contextlib
    :synopsis: Utilities for creating and working with context managers.

The ``contextlib`` module contains utilities for working with
context managers and the ``with`` statement.

Context Manager API
===================

A *context manager* is responsible for a resource within a code block,
possibly creating it when the block is entered and then cleaning it up
after the block is exited.  For example, files support the context
manager API to make it easy to ensure they are closed after all
reading or writing is done.

.. literalinclude:: contextlib_file.py
   :caption:
   :start-after: #end_pymotw_header

A context manager is enabled by the ``with`` statement, and the
API involves two methods.  The ``__enter__()`` method is run when
execution flow enters the code block inside the ``with``.  It
returns an object to be used within the context.  When execution flow
leaves the ``with`` block, the ``__exit__()`` method of the
context manager is called to clean up any resources being used.

.. literalinclude:: contextlib_api.py
   :caption:
   :start-after: #end_pymotw_header

Combining a context manager and the ``with`` statement is a
more compact way of writing a ``try:finally`` block, since the
context manager's ``__exit__()`` method is always called, even if an
exception is raised.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_api.py'))
.. }}}

.. code-block:: none

	$ python3 contextlib_api.py
	
	__init__()
	__enter__()
	Doing work in the context
	__exit__()

.. {{{end}}}

The ``__enter__()`` method can return any object to be associated
with a name specified in the ``as`` clause of the
``with`` statement.  In this example, the ``Context``
returns an object that uses the open context.

.. literalinclude:: contextlib_api_other_object.py
   :caption:
   :start-after: #end_pymotw_header

The value associated with the variable ``c`` is the object
returned by ``__enter__()``, which is not necessarily the
``Context`` instance created in the ``with`` statement.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_api_other_object.py'))
.. }}}

.. code-block:: none

	$ python3 contextlib_api_other_object.py
	
	Context.__init__()
	Context.__enter__()
	WithinContext.__init__(<__main__.Context object at 0x1007b1c50>)
	WithinContext.do_something()
	Context.__exit__()
	WithinContext.__del__

.. {{{end}}}

The ``__exit__()`` method receives arguments containing details of
any exception raised in the ``with`` block.  

.. literalinclude:: contextlib_api_error.py
   :caption:
   :start-after: #end_pymotw_header

If the context manager can handle the exception, ``__exit__()``
should return a true value to indicate that the exception does not
need to be propagated.  Returning false causes the exception to be
re-raised after ``__exit__()`` returns.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_api_error.py', ignore_error=True))
.. }}}

.. code-block:: none

	$ python3 contextlib_api_error.py
	
	__init__(True)
	__enter__()
	__exit__()
	  exc_type = <class 'RuntimeError'>
	  exc_val  = error message handled
	  exc_tb   = <traceback object at 0x10115cc88>
	
	__init__(False)
	__enter__()
	__exit__()
	  exc_type = <class 'RuntimeError'>
	  exc_val  = error message propagated
	  exc_tb   = <traceback object at 0x10115cc88>
	Traceback (most recent call last):
	  File "contextlib_api_error.py", line 33, in <module>
	    raise RuntimeError('error message propagated')
	RuntimeError: error message propagated

.. {{{end}}}

Context Managers as Function Decorators
=======================================

The class ``ContextDecorator`` adds support to regular context
manager classes to let them be used as function decorators as well as
context managers.

.. literalinclude:: contextlib_decorator.py
   :caption:
   :start-after: #end_pymotw_header

One difference with using the context manager as a decorator is that
the value returned by ``__enter__()`` is not available inside the
function being decorated, unlike when using ``with`` and
``as``. Arguments passed to the decorated function are
available in the usual way.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_decorator.py'))
.. }}}

.. code-block:: none

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
``__enter__()`` and ``__exit__()`` methods, is not
difficult. But sometimes writing everything out fully is extra
overhead for a trivial bit of context. In those sorts of situations,
use the ``contextmanager()`` decorator to convert a generator
function into a context manager.

.. literalinclude:: contextlib_contextmanager.py
    :caption:
    :start-after: #end_pymotw_header

The generator should initialize the context, yield exactly one time,
then clean up the context. The value yielded, if any, is bound to the
variable in the ``as`` clause of the ``with``
statement. Exceptions from within the ``with`` block are
re-raised inside the generator, so they can be handled there.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_contextmanager.py',
..                    ignore_error=True))
.. }}}

.. code-block:: none

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

The context manager returned by ``contextmanager()`` is derived from
``ContextDecorator``, so it also works as a function decorator.

.. literalinclude:: contextlib_contextmanager_decorator.py
   :caption:
   :start-after: #end_pymotw_header

As in the ``ContextDecorator`` example above, when the context
manager is used as a decorator the value yielded by the generator is
not available inside the function being decorated. Arguments passed to
the decorated function are still available, as demonstrated by
``throw_error()`` in this example.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_contextmanager_decorator.py', 
..                    ignore_error=True, line_break_mode='wrap'))
.. }}}

.. code-block:: none

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
	  File "contextlib_contextmanager_decorator.py", line 43, in
	<module>
	    throw_error(ValueError('this exception is not handled'))
	  File ".../lib/python3.5/contextlib.py", line 30, in inner
	    return func(*args, **kwds)
	  File "contextlib_contextmanager_decorator.py", line 33, in
	throw_error
	    raise err
	ValueError: this exception is not handled

.. {{{end}}}

Closing Open Handles
====================

The ``file`` class supports the context manager API directly, but
some other objects that represent open handles do not. The example
given in the standard library documentation for ``contextlib`` is
the object returned from ``urllib.urlopen()``.  There are other
legacy classes that use a ``close()`` method but do not support the
context manager API. To ensure that a handle is closed, use
``closing()`` to create a context manager for it.

.. literalinclude:: contextlib_closing.py
    :caption:
    :start-after: #end_pymotw_header

The handle is closed whether there is an error in the ``with``
block or not.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_closing.py'))
.. }}}

.. code-block:: none

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

.. literalinclude:: contextlib_ignore_error.py
   :caption:
   :start-after: #end_pymotw_header

In this case, the operation fails and the error is ignored.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_ignore_error.py'))
.. }}}

.. code-block:: none

	$ python3 contextlib_ignore_error.py
	
	trying non-idempotent operation
	done

.. {{{end}}}

The ``try:except`` form can be replaced with
``contextlib.suppress()`` to more explicitly suppress a class of
exceptions happening anywhere in the ``with`` block.

.. literalinclude:: contextlib_suppress.py
   :caption:
   :start-after: #end_pymotw_header

In this updated version, the exception is discarded entirely.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_suppress.py'))
.. }}}

.. code-block:: none

	$ python3 contextlib_suppress.py
	
	trying non-idempotent operation
	done

.. {{{end}}}

Redirecting Output Streams
==========================

Poorly designed library code may write directly to ``sys.stdout`` or
``sys.stderr``, without providing arguments to configure different
output destinations. The ``redirect_stdout()`` and
``redirect_stderr()`` context managers can be used to capture output
from functions like this, for which the source cannot be changed to
accept a new output argument.

.. literalinclude:: contextlib_redirect.py
   :caption:
   :start-after: #end_pymotw_header

In this example, ``misbehaving_function()`` writes to both ``stdout``
and ``stderr``, but the two context managers send that output to the
same ``io.StringIO`` instance where it is saved to be used later.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_redirect.py'))
.. }}}

.. code-block:: none

	$ python3 contextlib_redirect.py
	
	(stdout) A: 5
	(stderr) A: 5
	

.. {{{end}}}

.. note::

   Both ``redirect_stdout()`` and ``redirect_stderr()`` modify
   global state by replacing objects in the :mod:`sys` module, and
   should be used with care. The functions are not thread-safe, and
   may interfere with other operations that expect the standard output
   streams to be attached to terminal devices.

Dynamic Context Manager Stacks
==============================

Most context managers operate on one object at a time, such as a
single file or database handle. In these cases, the object is known in
advance and the code using the context manager can be built around
that one object. In other cases, a program may need to create an
unknown number of objects in a context, while wanting all of them to
be cleaned up when control flow exits the context. ``ExitStack``
was created to handle these more dynamic cases.

An ``ExitStack`` instance maintains a stack data structure of
cleanup callbacks. The callbacks are populated explicitly within the
context, and any registered callbacks are called in the reverse order
when control flow exits the context. The result is like having multple
nested ``with`` statements, except they are established
dynamically.

Stacking Context Managers
-------------------------

There are several ways to populate the ``ExitStack``.  This
example uses ``enter_context()`` to add a new context manager to the
stack.

.. literalinclude:: contextlib_exitstack_enter_context.py
   :caption:
   :start-after: #end_pymotw_header

``enter_context()`` first calls ``__enter__()`` on the context
manager, and then registers its ``__exit__()`` method as a callback
to be invoked as the stack is undone.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_exitstack_enter_context.py',
..                    ignore_error=True))
.. }}}

.. code-block:: none

	$ python3 contextlib_exitstack_enter_context.py
	
	0 entering
	1 entering
	inside context
	1 exiting
	0 exiting

.. {{{end}}}

The context managers given to ``ExitStack`` are treated as though
they are in a series of nested ``with`` statements. Errors that
happen anywhere within the context propagate through the normal error
handling of the context managers. These context manager classes
illustrate the way errors propagate.

.. literalinclude:: contextlib_context_managers.py
   :caption:
   :start-after: #end_pymotw_header

The examples using these classes are based around
``variable_stack()``, which uses the context managers passed to
construct an ``ExitStack``, building up the overall context one
by one. The examples below pass different context managers to explore
the error handling behavior. First, the normal case of no exceptions.

.. literalinclude:: contextlib_exitstack_enter_context_errors.py
   :lines: 20-24

Then, an example of handling exceptions within the context managers at
the end of the stack, in which all of the open contexts are closed as
the stack is unwound.

.. literalinclude:: contextlib_exitstack_enter_context_errors.py
   :lines: 26-31

Next, an example of handling exceptions within the context managers in
the middle of the stack, in which the error does not occur until some
contexts are already closed, so those contexts do not see the error.

.. literalinclude:: contextlib_exitstack_enter_context_errors.py
   :lines: 33-39

Finally, an example of the exception remaining unhandled and
propagating up to the calling code.

.. literalinclude:: contextlib_exitstack_enter_context_errors.py
   :lines: 41-

If any context manager in the stack receives an exception and returns
a ``True`` value, it prevents that exception from propagating up to
any other context managers.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_exitstack_enter_context_errors.py'))
.. }}}

.. code-block:: none

	$ python3 contextlib_exitstack_enter_context_errors.py
	
	No errors:
	  HandleError(1): entering
	  PassError(2): entering
	  PassError(2): exiting
	  HandleError(1): exiting False
	  outside of stack, any errors were handled
	
	Error at the end of the context stack:
	  HandleError(1): entering
	  HandleError(2): entering
	  ErrorOnExit(3): entering
	  ErrorOnExit(3): throwing error
	  HandleError(2): handling exception RuntimeError('from 3',)
	  HandleError(2): exiting True
	  HandleError(1): exiting False
	  outside of stack, any errors were handled
	
	Error in the middle of the context stack:
	  HandleError(1): entering
	  PassError(2): entering
	  ErrorOnExit(3): entering
	  HandleError(4): entering
	  HandleError(4): exiting False
	  ErrorOnExit(3): throwing error
	  PassError(2): passing exception RuntimeError('from 3',)
	  PassError(2): exiting
	  HandleError(1): handling exception RuntimeError('from 3',)
	  HandleError(1): exiting True
	  outside of stack, any errors were handled
	
	Error ignored:
	  PassError(1): entering
	  ErrorOnExit(2): entering
	  ErrorOnExit(2): throwing error
	  PassError(1): passing exception RuntimeError('from 2',)
	  PassError(1): exiting
	error handled outside of context

.. {{{end}}}

Arbitrary Context Callbacks
---------------------------

``ExitStack`` also supports arbitrary callbacks for closing a
context, making it easy to clean up resources that are not controlled
via a context manager.

.. literalinclude:: contextlib_exitstack_callbacks.py
   :caption:
   :start-after: #end_pymotw_header

Just as with the ``__exit__()`` methods of full context managers,
the callbacks are invoked in the reverse order that they are
registered.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_exitstack_callbacks.py'))
.. }}}

.. code-block:: none

	$ python3 contextlib_exitstack_callbacks.py
	
	closing callback((), {'arg3': 'val3'})
	closing callback(('arg1', 'arg2'), {})

.. {{{end}}}

The callbacks are invoked regardless of whether an error occurred, and
they are not given any information about whether an error
occurred. Their return value is ignored.

.. literalinclude:: contextlib_exitstack_callbacks_error.py
   :caption:
   :start-after: #end_pymotw_header

Because they do not have access to the error, callbacks are unable to
suppress exceptions from propagating through the rest of the stack of
context managers.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_exitstack_callbacks_error.py'))
.. }}}

.. code-block:: none

	$ python3 contextlib_exitstack_callbacks_error.py
	
	closing callback((), {'arg3': 'val3'})
	closing callback(('arg1', 'arg2'), {})
	ERROR: thrown error

.. {{{end}}}

Callbacks make a convenient way to clearly define cleanup logic
without the overhead of creating a new context manager class. To
improve code readability, that logic can be encapsulated in an inline
function, and ``callback()`` can be used as a decorator.

.. literalinclude:: contextlib_exitstack_callbacks_decorator.py
   :caption:
   :start-after: #end_pymotw_header

There is no way to specify the arguments for functions registered
using the decorator form of ``callback()``. However, if the cleanup
callback is defined inline, scope rules give it access to variables
defined in the calling code.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_exitstack_callbacks_decorator.py'))
.. }}}

.. code-block:: none

	$ python3 contextlib_exitstack_callbacks_decorator.py
	
	within the context
	inline_cleanup()
	local_resource = 'resource created in context'

.. {{{end}}}

Partial Stacks
--------------

Sometimes when building complex contexts it is useful to be able to
abort an operation if the context cannot be completely constructed,
but to delay the cleanup of all resources until a later time if they
can all be set up properly. For example, if an operation needs several
long-lived network connections, it may be best to not start the
operation if one connection fails. However, if all of the connections
can be opened they need to stay open longer than the duration of a
single context manager. The ``pop_all()`` method of
``ExitStack`` can be used in this scenario.

``pop_all()`` clears all of the context managers and callbacks from
the stack on which it is called, and returns a new stack pre-populated
with those same context managers and callbacks. The ``close()``
method of the new stack can be invoked later, after the original stack
is gone, to clean up the resources.

.. literalinclude:: contextlib_exitstack_pop_all.py
   :caption:
   :start-after: #end_pymotw_header

This example uses the same context manager classes defined earlier,
with the difference that ``ErrorOnEnter`` produces an error on
``__enter__()`` instead of ``__exit__()``. Inside
``variable_stack()``, if all of the contexts are entered without
error then the ``close()`` method of a new ``ExitStack`` is
returned. If a handled error occurs, ``variable_stack()`` returns
``None`` to indicate that the cleanup work is already done. And if an
unhandled error occurs, the partial stack is cleaned up and the error
is propagated.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'contextlib_exitstack_pop_all.py'))
.. }}}

.. code-block:: none

	$ python3 contextlib_exitstack_pop_all.py
	
	No errors:
	  HandleError(1): entering
	  HandleError(2): entering
	  HandleError(2): exiting False
	  HandleError(1): exiting False
	
	Handled error building context manager stack:
	  HandleError(1): entering
	  ErrorOnEnter(2): throwing error on enter
	  HandleError(1): handling exception RuntimeError('from 2',)
	  HandleError(1): exiting True
	no cleaner returned
	
	Unhandled error building context manager stack:
	  PassError(1): entering
	  ErrorOnEnter(2): throwing error on enter
	  PassError(1): passing exception RuntimeError('from 2',)
	  PassError(1): exiting
	caught error from 2

.. {{{end}}}



.. seealso::

   * :pydoc:`contextlib`

   * :pep:`343` -- The ``with`` statement.

   * `Context Manager Types
     <https://docs.python.org/library/stdtypes.html#typecontextmanager>`__
     -- Description of the context manager API from the standard
     library documentation.

   * `With Statement Context Managers
     <https://docs.python.org/reference/datamodel.html#context-managers>`__
     -- Description of the context manager API from the Python
     Reference Guide.

   * `Resource management in Python 3.3, or contextlib.ExitStack FTW!
     <http://www.wefearchange.org/2013/05/resource-management-in-python-33-or.html>`__
     -- Description of using ``ExitStack`` to deploy safe code
     from Barry Warsaw.
