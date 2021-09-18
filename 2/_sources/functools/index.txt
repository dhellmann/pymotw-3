===============================================
 functools -- Tools for Manipulating Functions
===============================================

.. module:: functools
    :synopsis: Tools for working with functions.

:Purpose: Functions that operate on other functions.
:Available In: 2.5 and later

The :mod:`functools` module provides tools for working with functions
and other callable objects, to adapt or extend them for new purposes
without completely rewriting them.

Decorators
==========

The primary tool supplied by the :mod:`functools` module is the class
:class:`partial`, which can be used to "wrap" a callable object with
default arguments. The resulting object is itself callable, and can be
treated as though it is the original function.  It takes all of the
same arguments as the original, and can be invoked with extra
positional or named arguments as well.

partial
-------

This example shows two simple :class:`partial` objects for the
function :func:`myfunc`.  Notice that :func:`show_details` prints the
:attr:`func`, :attr:`args`, and :attr:`keywords` attributes of the
partial object.

.. include:: functools_partial.py
    :literal:
    :start-after: #end_pymotw_header

At the end of the example, the first :class:`partial` created is
invoked without passing a value for *a*, causing an exception.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'functools_partial.py', ignore_error=True, break_lines_at=70))
.. }}}

::

	$ python functools_partial.py
	
	myfunc:
		object: <function myfunc at 0x100468c08>
		__name__: myfunc
		__doc__ 'Docstring for myfunc().'
		called myfunc with: ('a', 3)
	
	partial with named default:
		object: <functools.partial object at 0x10046b050>
		__doc__ 'partial(func, *args, **keywords) - new function with partial
	 application\n    of the given arguments and keywords.\n'
		func: <function myfunc at 0x100468c08>
		args: ()
		keywords: {'b': 4}
		called myfunc with: ('default a', 4)
		called myfunc with: ('override b', 5)
	
	partial with defaults:
		object: <functools.partial object at 0x10046b0a8>
		__doc__ 'partial(func, *args, **keywords) - new function with partial
	 application\n    of the given arguments and keywords.\n'
		func: <function myfunc at 0x100468c08>
		args: ('default a',)
		keywords: {'b': 99}
		called myfunc with: ('default a', 99)
		called myfunc with: ('default a', 'override b')
	
	Insufficient arguments:
	Traceback (most recent call last):
	  File "functools_partial.py", line 49, in <module>
	    p1()
	TypeError: myfunc() takes at least 1 argument (1 given)

.. {{{end}}}



update_wrapper
--------------

The partial object does not have :attr:`__name__` or :attr:`__doc__`
attributes by default, and without those attributes decorated
functions are more difficult to debug. Using :func:`update_wrapper`,
copies or adds attributes from the original function to the
:class:`partial` object.

.. include:: functools_update_wrapper.py
    :literal:
    :start-after: #end_pymotw_header

The attributes added to the wrapper are defined in
:const:`functools.WRAPPER_ASSIGNMENTS`, while
:const:`functools.WRAPPER_UPDATES` lists values to be modified.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'functools_update_wrapper.py', break_lines_at=70))
.. }}}

::

	$ python functools_update_wrapper.py
	
	myfunc:
		object: <function myfunc at 0x100468c80>
		__name__: myfunc
		__doc__ 'Docstring for myfunc().'
	
	raw wrapper:
		object: <functools.partial object at 0x10046c0a8>
		__name__: (no __name__)
		__doc__ 'partial(func, *args, **keywords) - new function with partial
	 application\n    of the given arguments and keywords.\n'
	
	Updating wrapper:
		assign: ('__module__', '__name__', '__doc__')
		update: ('__dict__',)
	
	updated wrapper:
		object: <functools.partial object at 0x10046c0a8>
		__name__: myfunc
		__doc__ 'Docstring for myfunc().'
	

.. {{{end}}}

Other Callables
---------------

Partials work with any callable object, not just standalone functions.

.. include:: functools_method.py
    :literal:
    :start-after: #end_pymotw_header

This example creates partials from an instance, and methods of an
instance.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'functools_method.py', break_lines_at=68))
.. }}}

::

	$ python functools_method.py
	
	meth1 straight:
		object: <bound method MyClass.meth1 of <__main__.MyClass object at 
	0x10046a3d0>>
		__name__: meth1
		__doc__ 'Docstring for meth1().'
		called meth1 with: (<__main__.MyClass object at 0x10046a3d0>, 'no d
	efault for a', 3)
	
	meth1 wrapper:
		object: <functools.partial object at 0x10046c158>
		__name__: meth1
		__doc__ 'Docstring for meth1().'
		called meth1 with: (<__main__.MyClass object at 0x10046a3d0>, 'a go
	es here', 4)
	
	meth2:
		object: <bound method MyClass.meth2 of <__main__.MyClass object at 
	0x10046a3d0>>
		__name__: meth2
		__doc__ 'Docstring for meth2'
		called meth2 with: (<__main__.MyClass object at 0x10046a3d0>, 'no d
	efault for c', 6)
	
	wrapped meth2:
		object: <functools.partial object at 0x10046c0a8>
		__name__: meth2
		__doc__ 'Docstring for meth2'
		called meth2 with: ('wrapped c', 'no default for c', 6)
	
	instance:
		object: <__main__.MyClass object at 0x10046a3d0>
		__name__: (no __name__)
		__doc__ 'Demonstration class for functools'
		called object with: (<__main__.MyClass object at 0x10046a3d0>, 'no 
	default for e', 6)
	
	instance wrapper:
		object: <functools.partial object at 0x10046c1b0>
		__name__: (no __name__)
		__doc__ 'partial(func, *args, **keywords) - new function with parti
	al application\n    of the given arguments and keywords.\n'
		called object with: (<__main__.MyClass object at 0x10046a3d0>, 'e g
	oes here', 7)

.. {{{end}}}


wraps
-----

Updating the properties of a wrapped callable is especially useful
when used in a decorator, since the transformed function ends up with
properties of the original, "bare", function.

.. include:: functools_wraps.py
    :literal:
    :start-after: #end_pymotw_header

:mod:`functools` provides a decorator, :func:`wraps`, which applies
:func:`update_wrapper` to the decorated function.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'functools_wraps.py'))
.. }}}

::

	$ python functools_wraps.py
	
	myfunc:
		object: <function myfunc at 0x10046c050>
		__name__: myfunc
		__doc__ None
	
		myfunc: ('unwrapped, default b', 2)
		myfunc: ('unwrapped, passing b', 3)
	
	wrapped_myfunc:
		object: <function myfunc at 0x10046c0c8>
		__name__: myfunc
		__doc__ None
	
		decorated: ('decorated defaults', 1)
			myfunc: ('decorated defaults', 1)
		decorated: ('args to decorated', 4)
			myfunc: ('args to decorated', 4)

.. {{{end}}}

Comparison
==========

Under Python 2, classes can define a :func:`__cmp__` method that
returns ``-1``, ``0``, or ``1`` based on whether the object is less
than, equal to, or greater than the item being compared.  Python 2.1
introduces the *rich comparison* methods API, :func:`__lt__`,
:func:`__le__`, :func:`__eq__`, :func:`__ne__`, :func:`__gt__`, and
:func:`__ge__`, which perform a single comparison operation and return
a boolean value.  Python 3 deprecated :func:`__cmp__` in favor of
these new methods, so :mod:`functools` provides tools to make it
easier to write Python 2 classes that comply with the new comparison
requirements in Python 3.

Rich Comparison
---------------

The rich comparison API is designed to allow classes with complex
comparisons to implement each test in the most efficient way possible.
However, for classes where comparison is relatively simple, there is
no point in manually creating each of the rich comparison methods.
The :func:`total_ordering` class decorator takes a class that provides
some of the methods, and adds the rest of them.

.. include:: functools_total_ordering.py
   :literal:
   :start-after: #end_pymotw_header

The class must provide an implmentation of :func:`__eq__` and any one
of the other rich comparison methods.  The decorator adds
implementations of the other methods that work by using the
comparisons provided.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'functools_total_ordering.py'))
.. }}}

::

	$ python functools_total_ordering.py
	
	Methods:
	
	[('__eq__', <unbound method MyObject.__eq__>),
	 ('__ge__', <unbound method MyObject.__ge__>),
	 ('__gt__', <unbound method MyObject.__gt__>),
	 ('__init__', <unbound method MyObject.__init__>),
	 ('__le__', <unbound method MyObject.__le__>),
	 ('__lt__', <unbound method MyObject.__lt__>)]
	
	Comparisons:
	
	a < b :
	  testing __gt__(1, 2)
	  testing __eq__(1, 2)
	  result of a < b: True
	
	a <= b:
	  testing __gt__(1, 2)
	  result of a <= b: True
	
	a == b:
	  testing __eq__(1, 2)
	  result of a == b: False
	
	a >= b:
	  testing __gt__(1, 2)
	  testing __eq__(1, 2)
	  result of a >= b: False
	
	a > b :
	  testing __gt__(1, 2)
	  result of a > b: False

.. {{{end}}}

Collation Order
---------------

Since old-style comparison functions are deprecated in Python 3, the
:data:`cmp` argument to functions like :func:`sort` are also no longer
supported.  Python 2 programs that use comparison functions can use
:func:`cmp_to_key` to convert them to a function that returns a
*collation key*, which is used to determine the position in the final
sequence.

.. include:: functools_cmp_to_key.py
   :literal:
   :start-after: #end_pymotw_header

.. note::

  Normally :func:`cmp_to_key` would be used directly, but in this
  example an extra wrapper function is introduced to print out more
  information as the key function is being called.

The output shows that :func:`sorted` starts by calling
:func:`get_key_wrapper` for each item in the sequence to produce a
key.  The keys returned by :func:`cmp_to_key` are instances of a class
defined in :mod:`functools` that implements the rich comparison API
based on the return value of the provided old-style comparison
function.  After all of the keys are created, the sequence is sorted
by comparing the keys.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'functools_cmp_to_key.py'))
.. }}}

::

	$ python functools_cmp_to_key.py
	
	key_wrapper(MyObject(5)) -> <functools.K object at 0x100466558>
	key_wrapper(MyObject(4)) -> <functools.K object at 0x100466590>
	key_wrapper(MyObject(3)) -> <functools.K object at 0x1004665c8>
	key_wrapper(MyObject(2)) -> <functools.K object at 0x100466600>
	key_wrapper(MyObject(1)) -> <functools.K object at 0x100466638>
	comparing MyObject(4) and MyObject(5)
	comparing MyObject(3) and MyObject(4)
	comparing MyObject(2) and MyObject(3)
	comparing MyObject(1) and MyObject(2)
	MyObject(1)
	MyObject(2)
	MyObject(3)
	MyObject(4)
	MyObject(5)

.. {{{end}}}



.. seealso::

    `functools <http://docs.python.org/2.7/library/functools.html>`_
        The standard library documentation for this module.
    
    `Rich comparison methods <http://docs.python.org/reference/datamodel.html#object.__lt__>`__
        Description of the rich comparison methods from the Python Reference Guide.
