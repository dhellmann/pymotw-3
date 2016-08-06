===============================================
 weakref --- Impermanent References to Objects
===============================================

.. module:: weakref
    :synopsis: Impermanent references to objects

:Purpose: Refer to an "expensive" object, but allow its memory to be
          reclaimed by the garbage collector if there are no other
          non-weak references.

The :mod:`weakref` module supports weak references to objects. A
normal reference increments the reference count on the object and
prevents it from being garbage collected. This is not always
desirable, either when a circular reference might be present or when
building a cache of objects that should be deleted when memory is
needed.  A weak reference is a handle to an object that does not keep
it from being cleaned up automatically.

References
==========

Weak references to objects are managed through the :class:`ref`
class. To retrieve the original object, call the reference object.

.. literalinclude:: weakref_ref.py
   :caption:
   :start-after: #end_pymotw_header

In this case, since ``obj`` is deleted before the second call to the
reference, the :class:`ref` returns ``None``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'weakref_ref.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 weakref_ref.py
	
	obj: <__main__.ExpensiveObject object at 0x1007b1a58>
	ref: <weakref at 0x1007a92c8; to 'ExpensiveObject' at
	0x1007b1a58>
	r(): <__main__.ExpensiveObject object at 0x1007b1a58>
	deleting obj
	(Deleting <__main__.ExpensiveObject object at 0x1007b1a58>)
	r(): None

.. {{{end}}}

Reference Callbacks
===================

The :class:`ref` constructor accepts an optional callback function to
invoke when the referenced object is deleted.

.. literalinclude:: weakref_ref_callback.py
   :caption:
   :start-after: #end_pymotw_header

The callback receives the reference object as an argument after the
reference is "dead" and no longer refers to the original object. One
use for this feature is to remove the weak reference object from a
cache.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'weakref_ref_callback.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 weakref_ref_callback.py
	
	obj: <__main__.ExpensiveObject object at 0x1018b1978>
	ref: <weakref at 0x1018a92c8; to 'ExpensiveObject' at
	0x1018b1978>
	r(): <__main__.ExpensiveObject object at 0x1018b1978>
	deleting obj
	(Deleting <__main__.ExpensiveObject object at 0x1018b1978>)
	callback(<weakref at 0x1018a92c8; dead>)
	r(): None

.. {{{end}}}

Proxies
=======

It is sometimes more convenient to use a proxy, rather than a weak
reference.  Proxies can be used as though they were the original
object, and do not need to be called before the object is accessible.
That means they can be passed to a library that does not know it is
receiving a reference instead of the real object.

.. literalinclude:: weakref_proxy.py
   :caption:
   :start-after: #end_pymotw_header

If the proxy is accessed after the referent object is removed, a
:class:`ReferenceError` exception is raised.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'weakref_proxy.py', ignore_error=True))
.. }}}

.. code-block:: none

	$ python3 weakref_proxy.py
	
	via obj: My Object
	via ref: My Object
	via proxy: My Object
	(Deleting <__main__.ExpensiveObject object at 0x1007aa7b8>)
	Traceback (most recent call last):
	  File "weakref_proxy.py", line 30, in <module>
	    print('via proxy:', p.name)
	ReferenceError: weakly-referenced object no longer exists

.. {{{end}}}

Caching Objects
===============

The :class:`ref` and :class:`proxy` classes are considered "low
level". While they are useful for maintaining weak references to
individual objects and allowing cycles to be garbage collected, the
:class:`WeakKeyDictionary` and :class:`WeakValueDictionary` provide a
more appropriate API for creating a cache of several objects.

The :class:`WeakValueDictionary` uses weak references to the values it
holds, allowing them to be garbage collected when other code is not
actually using them.  Using explicit calls to the garbage collector
illustrates the difference between memory handling with a regular
dictionary and :class:`WeakValueDictionary`:

.. literalinclude:: weakref_valuedict.py
   :caption:
   :start-after: #end_pymotw_header

Any loop variables that refer to the values being cached must be
cleared explicitly so the reference count of the object is
decremented. Otherwise, the garbage collector would not remove the
objects and they would remain in the cache. Similarly, the *all_refs*
variable is used to hold references to prevent them from being garbage
collected prematurely.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'weakref_valuedict.py'))
.. }}}

.. code-block:: none

	$ python3 weakref_valuedict.py
	
	CACHE TYPE: <class 'dict'>
	  all_refs = {'one': ExpensiveObject(one),
	 'three': ExpensiveObject(three),
	 'two': ExpensiveObject(two)}
	
	  Before, cache contains: ['one', 'three', 'two']
	    one = ExpensiveObject(one)
	    three = ExpensiveObject(three)
	    two = ExpensiveObject(two)
	
	  Cleanup:
	
	  After, cache contains: ['one', 'three', 'two']
	    one = ExpensiveObject(one)
	    three = ExpensiveObject(three)
	    two = ExpensiveObject(two)
	  demo returning
	    (Deleting ExpensiveObject(one))
	    (Deleting ExpensiveObject(three))
	    (Deleting ExpensiveObject(two))
	
	CACHE TYPE: <class 'weakref.WeakValueDictionary'>
	  all_refs = {'one': ExpensiveObject(one),
	 'three': ExpensiveObject(three),
	 'two': ExpensiveObject(two)}
	
	  Before, cache contains: ['one', 'three', 'two']
	    one = ExpensiveObject(one)
	    three = ExpensiveObject(three)
	    two = ExpensiveObject(two)
	
	  Cleanup:
	    (Deleting ExpensiveObject(one))
	    (Deleting ExpensiveObject(three))
	    (Deleting ExpensiveObject(two))
	
	  After, cache contains: []
	  demo returning

.. {{{end}}}

The :class:`WeakKeyDictionary` works similarly but uses weak
references for the keys instead of the values in the dictionary.

.. warning::

    The library documentation for :mod:`weakref` contains this
    warning:

    Caution: Because a :class:`WeakValueDictionary` is built on top of
    a Python dictionary, it must not change size when iterating over
    it. This can be difficult to ensure for a
    :class:`WeakValueDictionary` because actions performed by the
    program during iteration may cause items in the dictionary to
    vanish "by magic" (as a side effect of garbage collection).

.. seealso::

   * :pydoc:`weakref`

   * :mod:`gc` -- The ``gc`` module is the interface to the
     interpreter's garbage collector.
