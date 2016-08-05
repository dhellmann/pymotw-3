==============================================
 weakref -- Impermanent References to Objects
==============================================

.. module:: weakref
    :synopsis: Impermanent references to objects

:Purpose: Refer to an "expensive" object, but allow its memory to be reclaimed by the garbage collector if there are no other non-weak references.
:Python Version: 2.1 and later

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

.. include:: weakref_ref.py
    :literal:
    :start-after: #end_pymotw_header

In this case, since ``obj`` is deleted before the second call to the
reference, the :class:`ref` returns ``None``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'weakref_ref.py'))
.. }}}

::

	$ python weakref_ref.py
	
	obj: <__main__.ExpensiveObject object at 0x100da5750>
	ref: <weakref at 0x100d99b50; to 'ExpensiveObject' at 0x100da5750>
	r(): <__main__.ExpensiveObject object at 0x100da5750>
	deleting obj
	(Deleting <__main__.ExpensiveObject object at 0x100da5750>)
	r(): None

.. {{{end}}}

Reference Callbacks
===================

The :class:`ref` constructor accepts an optional callback function to
invoke when the referenced object is deleted.

.. include:: weakref_ref_callback.py
    :literal:
    :start-after: #end_pymotw_header

The callback receives the reference object as an argument after the
reference is "dead" and no longer refers to the original object. One
use for this feature is to remove the weak reference object from a
cache.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'weakref_ref_callback.py'))
.. }}}

::

	$ python weakref_ref_callback.py
	
	obj: <__main__.ExpensiveObject object at 0x100da1950>
	ref: <weakref at 0x100d99ba8; to 'ExpensiveObject' at 0x100da1950>
	r(): <__main__.ExpensiveObject object at 0x100da1950>
	deleting obj
	callback( <weakref at 0x100d99ba8; dead> )
	(Deleting <__main__.ExpensiveObject object at 0x100da1950>)
	r(): None

.. {{{end}}}

Proxies
=======

It is sometimes more convenient to use a proxy, rather than a weak
reference.  Proxies can be used as though they were the original
object, and do not need to be called before the object is accessible.
That means they can be passed to a library that does not know it is
receiving a reference instead of the real object.

.. include:: weakref_proxy.py
    :literal:
    :start-after: #end_pymotw_header

If the proxy is accessed after the referent object is removed, a
:class:`ReferenceError` exception is raised.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'weakref_proxy.py', ignore_error=True))
.. }}}

::

	$ python weakref_proxy.py
	
	via obj: My Object
	via ref: My Object
	via proxy: My Object
	(Deleting <__main__.ExpensiveObject object at 0x100da27d0>)
	via proxy:
	Traceback (most recent call last):
	  File "weakref_proxy.py", line 26, in <module>
	    print 'via proxy:', p.name
	ReferenceError: weakly-referenced object no longer exists

.. {{{end}}}

Cyclic References
=================

One use for weak references is to allow cyclic references without preventing
garbage collection. This example illustrates the difference between using
regular objects and proxies when a graph includes a cycle.

The :class:`Graph` class in ``weakref_graph.py`` accepts any object
given to it as the "next" node in the sequence. For the sake of
brevity, this implementation supports a single outgoing reference from
each node, which is of limited use generally, but makes it easy to
create cycles for these examples. The function :func:`demo` is a utility
function to exercise the graph class by creating a cycle and then
removing various references.

.. include:: weakref_graph.py
   :literal:
   :start-after: #end_pymotw_header

This example uses the :mod:`gc` module to help debug the leak. The
``DEBUG_LEAK`` flag causes :mod:`gc` to print information about
objects that cannot be seen other than through the reference the
garbage collector has to them.

.. include:: weakref_cycle.py
   :literal:
   :start-after: #end_pymotw_header

Even after deleting the local references to the :class:`Graph`
instances in :func:`demo()`, the graphs all show up in the garbage
list and cannot be collected.  Several dictionaries are also found in
the garbage list.  They are the :attr:`__dict__` values from the
:class:`Graph` instances, and contain the attributes for those
objects.  The graphs can be forcibly deleted, since the program knows
what they are.  Enabling unbuffered I/O by passing the ``-u`` option
to the interpreter ensures that the output from the :command:`print`
statements in this example program (written to standard output) and
the debug output from :mod:`gc` (written to standard error) are
interleaved correctly.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u weakref_cycle.py'))
.. }}}

::

	$ python -u weakref_cycle.py
	
	Setting up the cycle
	
	Set up graph:
	one.set_next(<Graph at 0x100db7590 name=two>)
	two.set_next(<Graph at 0x100db75d0 name=three>)
	three.set_next(<Graph at 0x100db7550 name=one>)
	
	Graph:
	one->two->three->one
	Collecting...
	Unreachable objects: 0
	Garbage:[]
	
	After 2 references removed:
	one->two->three->one
	Collecting...
	Unreachable objects: 0
	Garbage:[]
	
	Removing last reference:
	Collecting...
	gc: uncollectable <Graph 0x100db7550>
	gc: uncollectable <Graph 0x100db7590>
	gc: uncollectable <Graph 0x100db75d0>
	gc: uncollectable <dict 0x100c63c30>
	gc: uncollectable <dict 0x100c5e150>
	gc: uncollectable <dict 0x100c63810>
	Unreachable objects: 6
	Garbage:[<Graph at 0x100db7550 name=one>,
	 <Graph at 0x100db7590 name=two>,
	 <Graph at 0x100db75d0 name=three>,
	 {'name': 'one', 'other': <Graph at 0x100db7590 name=two>},
	 {'name': 'two', 'other': <Graph at 0x100db75d0 name=three>},
	 {'name': 'three', 'other': <Graph at 0x100db7550 name=one>}]
	
	Breaking the cycle and cleaning up garbage
	
	one.set_next(None)
	(Deleting two)
	two.set_next(None)
	(Deleting three)
	three.set_next(None)
	(Deleting one)
	one.set_next(None)
	
	Collecting...
	Unreachable objects: 0
	Garbage:[]

.. {{{end}}}


The next step is to create a more intelligent :class:`WeakGraph` class
that knows to avoid creating cycles with regular references by using
weak references when a cycle is detected.

.. include:: weakref_weakgraph.py
   :literal:
   :start-after: #end_pymotw_header

Since the :class:`WeakGraph` instances use proxies to refer to objects
that have already been seen, as :func:`demo()` removes all local
references to the objects, the cycle is broken and the garbage
collector can delete the objects.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'weakref_weakgraph.py', break_lines_at=69))
.. }}}

::

	$ python weakref_weakgraph.py
	
	Set up graph:
	one.set_next(<WeakGraph at 0x100db4790 name=two>)
	two.set_next(<WeakGraph at 0x100db47d0 name=three>)
	three.set_next(<weakproxy at 0x100dac6d8 to WeakGraph at 0x100db4750>
	)
	
	Graph:
	one->two->three
	Collecting...
	Unreachable objects: 0
	Garbage:[]
	
	After 2 references removed:
	one->two->three
	Collecting...
	Unreachable objects: 0
	Garbage:[]
	
	Removing last reference:
	(Deleting one)
	one.set_next(None)
	(Deleting two)
	two.set_next(None)
	(Deleting three)
	three.set_next(None)
	Collecting...
	Unreachable objects: 0
	Garbage:[]

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

.. include:: weakref_valuedict.py
    :literal:
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

::

	$ python weakref_valuedict.py
	
	CACHE TYPE: <type 'dict'>
	  all_refs ={'one': ExpensiveObject(one),
	 'three': ExpensiveObject(three),
	 'two': ExpensiveObject(two)}
	
	  Before, cache contains: ['three', 'two', 'one']
	    three = ExpensiveObject(three)
	    two = ExpensiveObject(two)
	    one = ExpensiveObject(one)
	
	  Cleanup:
	
	  After, cache contains: ['three', 'two', 'one']
	    three = ExpensiveObject(three)
	    two = ExpensiveObject(two)
	    one = ExpensiveObject(one)
	  demo returning
	    (Deleting ExpensiveObject(three))
	    (Deleting ExpensiveObject(two))
	    (Deleting ExpensiveObject(one))
	
	CACHE TYPE: weakref.WeakValueDictionary
	  all_refs ={'one': ExpensiveObject(one),
	 'three': ExpensiveObject(three),
	 'two': ExpensiveObject(two)}
	
	  Before, cache contains: ['three', 'two', 'one']
	    three = ExpensiveObject(three)
	    two = ExpensiveObject(two)
	    one = ExpensiveObject(one)
	
	  Cleanup:
	    (Deleting ExpensiveObject(three))
	    (Deleting ExpensiveObject(two))
	    (Deleting ExpensiveObject(one))
	
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

    `weakref <http://docs.python.org/lib/module-weakref.html>`_
        Standard library documentation for this module.

    :mod:`gc`
        The ``gc`` module is the interface to the interpreter's
        garbage collector.
