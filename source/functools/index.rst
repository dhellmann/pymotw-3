===============================================
 functools -- Tools for Manipulating Functions
===============================================

.. module:: functools
    :synopsis: Tools for working with functions.

:Purpose: Functions that operate on other functions.

The :mod:`functools` module provides tools for adapting or extending
functions and other callable objects, without completely rewriting
them.

Decorators
==========

The primary tool supplied by the :mod:`functools` module is the class
:class:`partial`, which can be used to "wrap" a callable object with
default arguments. The resulting object is itself callable, and can be
treated as though it is the original function.  It takes all of the
same arguments as the original, and can be invoked with extra
positional or named arguments as well.  A :class:`partial` can be used
instead of a :command:`lambda` to provide default arguments to a
function, while leaving some arguments unspecified.

Partial Objects
---------------

This example shows two simple :class:`partial` objects for the
function :func:`myfunc`.  The output of :func:`show_details` includes
the :attr:`func`, :attr:`args`, and :attr:`keywords` attributes of the
partial object.

.. literalinclude:: functools_partial.py
    :caption:
    :start-after: #end_pymotw_header

At the end of the example, the first :class:`partial` created is
invoked without passing a value for *a*, causing an exception.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'functools_partial.py', ignore_error=True))
.. }}}

::

	$ python3 functools_partial.py
	
	myfunc:
	  object: <function myfunc at 0x100757f28>
	  __name__: myfunc
	  called myfunc with: ('a', 3)
	
	partial with named default:
	  object: functools.partial(<function myfunc at 0x100757f28>, b=
	4)
	  func: <function myfunc at 0x100757f28>
	  args: ()
	  keywords: {'b': 4}
	  called myfunc with: ('passing a', 4)
	  called myfunc with: ('override b', 5)
	
	partial with defaults:
	  object: functools.partial(<function myfunc at 0x100757f28>, 'd
	efault a', b=99)
	  func: <function myfunc at 0x100757f28>
	  args: ('default a',)
	  keywords: {'b': 99}
	  called myfunc with: ('default a', 99)
	  called myfunc with: ('default a', 'override b')
	
	Insufficient arguments:
	Traceback (most recent call last):
	  File "functools_partial.py", line 51, in <module>
	    p1()
	TypeError: myfunc() missing 1 required positional argument: 'a'

.. {{{end}}}



Acquiring Function Properties
-----------------------------

The :class:`partial` object does not have :attr:`__name__` or :attr:`__doc__`
attributes by default, and without those attributes, decorated
functions are more difficult to debug. Using :func:`update_wrapper`,
copies or adds attributes from the original function to the
:class:`partial` object.

.. literalinclude:: functools_update_wrapper.py
    :caption:
    :start-after: #end_pymotw_header

The attributes added to the wrapper are defined in
:const:`WRAPPER_ASSIGNMENTS`, while :const:`WRAPPER_UPDATES` lists
values to be modified.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'functools_update_wrapper.py', line_break_mode='wrap'))
.. }}}

::

	$ python3 functools_update_wrapper.py
	
	myfunc:
	  object: <function myfunc at 0x100757f28>
	  __name__: myfunc
	  __doc__ 'Docstring for myfunc().'
	
	raw wrapper:
	  object: functools.partial(<function myfunc at 0x100757f28>,
	b=4)
	  __name__: (no __name__)
	  __doc__ 'partial(func, *args, **keywords) - new function with
	partial application\n    of the given arguments and keywords.\n'
	
	Updating wrapper:
	  assign: ('__module__', '__name__', '__qualname__', '__doc__',
	'__annotations__')
	  update: ('__dict__',)
	
	updated wrapper:
	  object: functools.partial(<function myfunc at 0x100757f28>,
	b=4)
	  __name__: myfunc
	  __doc__ 'Docstring for myfunc().'
	

.. {{{end}}}

Other Callables
---------------

Partials work with any callable object, not just standalone functions.

.. literalinclude:: functools_method.py
    :caption:
    :start-after: #end_pymotw_header

This example creates partials from an instance and methods of an
instance.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'functools_method.py'))
.. }}}

::

	$ python3 functools_method.py
	
	calling method1 directly:
	  object: <bound method MyClass.method1 of <__main__.MyClass obj
	ect at 0x1018b1c18>>
	  __name__: method1
	  __doc__ 'Docstring for method1().'
	  called method1 with: (<__main__.MyClass object at 0x1018b1c18>
	, 'no default for a', 3)
	
	calling method1 wrapped:
	  object: functools.partial(<bound method MyClass.method1 of <__
	main__.MyClass object at 0x1018b1c18>>, b=4)
	  __name__: method1
	  __doc__ 'Docstring for method1().'
	  called method1 with: (<__main__.MyClass object at 0x1018b1c18>
	, 'a goes here', 4)
	
	calling method2 directly:
	  object: <bound method MyClass.method2 of <__main__.MyClass obj
	ect at 0x1018b1c18>>
	  __name__: method2
	  __doc__ 'Docstring for method2'
	  called method2 with: (<__main__.MyClass object at 0x1018b1c18>
	, 'no default for c', 6)
	
	calling method2 wrapped:
	  object: functools.partial(<function MyClass.method2 at 0x101ae
	2048>, 'wrapped c')
	  __name__: method2
	  __doc__ 'Docstring for method2'
	  called method2 with: ('wrapped c', 'no default for c', 7)
	
	instance:
	  object: <__main__.MyClass object at 0x1018b1c18>
	  __name__: (no __name__)
	  __doc__ 'Demonstration class for functools'
	  called object with: (<__main__.MyClass object at 0x1018b1c18>,
	 'no default for e', 6)
	
	instance wrapper:
	  object: functools.partial(<__main__.MyClass object at 0x1018b1
	c18>, f=8)
	  __name__: (no __name__)
	  __doc__ 'Demonstration class for functools'
	  called object with: (<__main__.MyClass object at 0x1018b1c18>,
	 'e goes here', 8)

.. {{{end}}}

Methods and Functions
---------------------

While :func:`partial` returns a callable ready to be used directly,
:func:`partialmethod` returns a callable ready to be used as an
unbound method of an object. In the following example, the same
standalone function is added as an attribute of ``MyClass`` twice,
once using :func:`partialmethod` as ``method1()`` and again using
:func:`partial` as ``method2()``.

.. literalinclude:: functools_partialmethod.py
   :caption:
   :start-after: #end_pymotw_header

``method1()`` can be called from an instance of ``MyClass``, and the
instance is passed as the first argument just as with methods defined
normally. ``method2()`` is not set up as a bound method, and so the
``self`` argument must be passed explicitly, or the call will result
in a :class:`TypeError`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'functools_partialmethod.py', line_break_mode='wrap'))
.. }}}

::

	$ python3 functools_partialmethod.py
	
	standalone
	  called standalone with: (None, 1, 2)
	
	method1 as partialmethod
	  called standalone with: (<__main__.MyClass object at
	0x1007b1a20>, 1, 2)
	  self.attr = instance attribute
	
	method2 as partial
	ERROR: standalone() missing 1 required positional argument:
	'self'

.. {{{end}}}

Acquiring Function Properties for Decorators
--------------------------------------------

Updating the properties of a wrapped callable is especially useful
when used in a decorator, since the transformed function ends up with
properties of the original "bare" function.

.. literalinclude:: functools_wraps.py
    :caption:
    :start-after: #end_pymotw_header

:mod:`functools` provides a decorator, :func:`wraps`, that applies
:func:`update_wrapper` to the decorated function.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'functools_wraps.py'))
.. }}}

::

	$ python3 functools_wraps.py
	
	myfunc:
	  object: <function myfunc at 0x1014cdf28>
	  __name__: myfunc
	  __doc__ 'myfunc() is not complicated'
	
	  myfunc: ('unwrapped, default b', 2)
	  myfunc: ('unwrapped, passing b', 3)
	
	wrapped_myfunc:
	  object: <function myfunc at 0x1014e2048>
	  __name__: myfunc
	  __doc__ 'myfunc() is not complicated'
	
	  decorated: ('decorated defaults', 1)
	     myfunc: ('decorated defaults', 1)
	  decorated: ('args to wrapped', 4)
	     myfunc: ('args to wrapped', 4)
	
	decorated_myfunc:
	  object: <function decorated_myfunc at 0x1014e2158>
	  __name__: decorated_myfunc
	  __doc__ None
	
	  decorated: ('decorated defaults', 1)
	     myfunc: ('decorated defaults', 1)
	  decorated: ('args to decorated', 4)
	     myfunc: ('args to decorated', 4)

.. {{{end}}}

Comparison
==========

Under Python 2, classes could define a :func:`__cmp__` method that
returns ``-1``, ``0``, or ``1`` based on whether the object is less
than, equal to, or greater than the item being compared.  Python 2.1
introduced the *rich comparison* methods API (:func:`__lt__`,
:func:`__le__`, :func:`__eq__`, :func:`__ne__`, :func:`__gt__`, and
:func:`__ge__`), which perform a single comparison operation and return
a boolean value.  Python 3 deprecated :func:`__cmp__` in favor of
these new methods and :mod:`functools` provides tools to make it
easier to write classes that comply with the new comparison
requirements in Python 3.

Rich Comparison
---------------

The rich comparison API is designed to allow classes with complex
comparisons to implement each test in the most efficient way possible.
However, for classes where comparison is relatively simple, there is
no point in manually creating each of the rich comparison methods.
The :func:`total_ordering` class decorator takes a class that provides
some of the methods, and adds the rest of them.

.. literalinclude:: functools_total_ordering.py
   :caption:
   :start-after: #end_pymotw_header

The class must provide implementation of :func:`__eq__` and one other
rich comparison method.  The decorator adds implementations of the
rest of the methods that work by using the comparisons provided.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'functools_total_ordering.py'))
.. }}}

::

	$ python3 functools_total_ordering.py
	
	Methods:
	
	[('__eq__', <function MyObject.__eq__ at 0x101c98d90>),
	 ('__ge__', <function _ge_from_gt at 0x1019b9a60>),
	 ('__gt__', <function MyObject.__gt__ at 0x101c98e18>),
	 ('__init__', <function MyObject.__init__ at 0x101c98d08>),
	 ('__le__', <function _le_from_gt at 0x1019b9ae8>),
	 ('__lt__', <function _lt_from_gt at 0x1019b99d8>)]
	
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
supported.  Older programs that use comparison functions can use
:func:`cmp_to_key` to convert them to a function that returns a
*collation key*, which is used to determine the position in the final
sequence.

.. literalinclude:: functools_cmp_to_key.py
   :caption:
   :start-after: #end_pymotw_header

Normally :func:`cmp_to_key` would be used directly, but in this
example an extra wrapper function is introduced to print out more
information as the key function is being called.

The output shows that :func:`sorted` starts by calling
:func:`get_key_wrapper` for each item in the sequence to produce a
key.  The keys returned by :func:`cmp_to_key` are instances of a class
defined in :mod:`functools` that implements the rich comparison API
using the old-style comparison function passed in.  After all of the
keys are created, the sequence is sorted by comparing the keys.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'functools_cmp_to_key.py', line_break_mode='wrap'))
.. }}}

::

	$ python3 functools_cmp_to_key.py
	
	key_wrapper(MyObject(5)) -> <functools.KeyWrapper object at
	0x1011bf430>
	key_wrapper(MyObject(4)) -> <functools.KeyWrapper object at
	0x1011bf450>
	key_wrapper(MyObject(3)) -> <functools.KeyWrapper object at
	0x1011bf470>
	key_wrapper(MyObject(2)) -> <functools.KeyWrapper object at
	0x1011bf490>
	key_wrapper(MyObject(1)) -> <functools.KeyWrapper object at
	0x1011bf6b0>
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

Caching
=======

The :func:`lru_cache` decorator wraps a function in a
least-recently-used cache with a fixed size. Arguments to the function
are used to build a hash key, which is then mapped to the
result. Subsequent calls with the same arguments will fetch the value
from the cache instead of calling the function. The decorator also
adds methods to the function to examine the state of the cache
(:func:`cache_info`) and empty the cache (:func:`cache_clear`).

.. literalinclude:: functools_lru_cache.py
   :caption:
   :start-after: #end_pymotw_header

This example makes several calls to ``expensive()`` in a set of nested
loops. The second time those calls are made with the same values the
results appear in the cache. When the cache is cleared and the loops
are run again, the values must be recomputed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'functools_lru_cache.py'))
.. }}}

::

	$ python3 functools_lru_cache.py
	
	First set of calls:
	expensive(0, 0)
	expensive(0, 1)
	expensive(1, 0)
	expensive(1, 1)
	CacheInfo(hits=0, misses=4, maxsize=128, currsize=4)
	
	Second set of calls:
	expensive(0, 2)
	expensive(1, 2)
	expensive(2, 0)
	expensive(2, 1)
	expensive(2, 2)
	CacheInfo(hits=4, misses=9, maxsize=128, currsize=9)
	
	Clearing cache:
	CacheInfo(hits=0, misses=0, maxsize=128, currsize=0)
	
	Third set of calls:
	expensive(0, 0)
	expensive(0, 1)
	expensive(1, 0)
	expensive(1, 1)
	CacheInfo(hits=0, misses=4, maxsize=128, currsize=4)

.. {{{end}}}

To prevent the cache from growing without bounds in a long-running
process, it is given a maximum size. The default is 128 entries, but
that can be changed for each cache using the ``maxsize`` argument.

.. literalinclude:: functools_lru_cache_expire.py
   :caption:
   :start-after: #end_pymotw_header

In this example the cache size is set to 2 entries. When the third set
of unique arguments (``3, 4``) is used the oldest item in the cache is
dropped and replaced with the new result.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'functools_lru_cache_expire.py'))
.. }}}

::

	$ python3 functools_lru_cache_expire.py
	
	Establish the cache
	(1, 2) called expensive(1, 2)
	(2, 3) called expensive(2, 3)
	
	Use cached items
	(1, 2) cache hit
	(2, 3) cache hit
	
	Compute a new value, triggering cache expiration
	(3, 4) called expensive(3, 4)
	
	Cache still contains one old item
	(2, 3) cache hit
	
	Oldest item needs to be recomputed
	(1, 2) called expensive(1, 2)

.. {{{end}}}



.. expiring items from the cache
.. args that can't be hashed

.. seealso::

    * :pydoc:`functools`

    * `Rich comparison methods
      <http://docs.python.org/reference/datamodel.html#object.__lt__>`__
      -- Description of the rich comparison methods from the Python
      Reference Guide.

    * `Isolated @memoize
      <http://nedbatchelder.com/blog/201601/isolated_memoize.html>`__
      -- Article on creating memoizing decorators that work well with
      unit tests, by Ned Batchelder.

    * :mod:`inspect` -- Introspection API for live objects.
