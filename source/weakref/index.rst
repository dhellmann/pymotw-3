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
	
	obj: <__main__.ExpensiveObject object at 0x1018b1a58>
	ref: <weakref at 0x1018a92c8; to 'ExpensiveObject' at
	0x1018b1a58>
	r(): <__main__.ExpensiveObject object at 0x1018b1a58>
	deleting obj
	(Deleting <__main__.ExpensiveObject object at 0x1018b1a58>)
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
	
	obj: <__main__.ExpensiveObject object at 0x1007b1978>
	ref: <weakref at 0x1007a92c8; to 'ExpensiveObject' at
	0x1007b1978>
	r(): <__main__.ExpensiveObject object at 0x1007b1978>
	deleting obj
	(Deleting <__main__.ExpensiveObject object at 0x1007b1978>)
	callback(<weakref at 0x1007a92c8; dead>)
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

Cyclic References
=================

One use for weak references is to allow cyclic references without
preventing garbage collection. This example illustrates the difference
between using regular objects and proxies when a graph includes a
cycle.

The :class:`Graph` class in ``weakref_graph.py`` accepts any object
given to it as the "next" node in the sequence. For the sake of
brevity, this implementation supports a single outgoing reference from
each node, which is of limited use generally, but makes it easy to
create cycles for these examples. The function :func:`demo` is a
utility function to exercise the graph class by creating a cycle and
then removing various references.

.. literalinclude:: weakref_graph.py
   :caption:
   :start-after: #end_pymotw_header

This example uses the :mod:`gc` module to help debug the leak. The
``DEBUG_LEAK`` flag is a combination of several other debugging
flags. ``DEBUG_UNCOLLECTABLE`` causes :mod:`gc` to print information
about objects that cannot be seen other than through the reference the
garbage collector has to them. Using ``DEBUG_COLLECTABLE`` causes
:mod:`gc` to report on the objects it is deleting when it detects an
object that is safe to collect.

The :func:`get_objects` function returns a list of all of the objects
being tracked by the garbage collector, and can be used to find
objects that have references outside of the current scope. In
``collect_and_show_garbage()``, the loop looks for :class:`Graph`
instances known to the garbage collector and then shows the objects
they refer to, including their attribute dictionary and their class.

.. literalinclude:: weakref_cycle.py
   :caption:
   :start-after: #end_pymotw_header

After deleting the local references to the :class:`Graph` instances in
:func:`demo()`, the graphs are all deleted automatically. Enabling
unbuffered I/O by passing the ``-u`` option to the interpreter ensures
that the output from the :command:`print` statements in this example
program (written to standard output) and the debug output from
:mod:`gc` (written to standard error) are interleaved correctly.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u weakref_cycle.py'))
.. }}}

.. code-block:: none

	$ python3 -u weakref_cycle.py
	
	Setting up the cycle
	
	Set up graph:
	  one.set_next(<Graph at 0x1013d5358 name=two>)
	  two.set_next(<Graph at 0x1014019b0 name=three>)
	  three.set_next(<Graph at 0x1012b1978 name=one>)
	
	Graph:
	  one->two->three->one
	Collecting...
	Unreachable objects: 0
	Tracked Graph objects:
	  <Graph at 0x1012b1978 name=one>
	    -> {'other': <Graph at 0x1013d5358 name=two>, 'name': 'one'}
	    -> <class 'weakref_graph.Graph'>
	  <Graph at 0x1013d5358 name=two>
	    -> {'other': <Graph at 0x1014019b0 name=three>, 'name': 'two
	'}
	    -> <class 'weakref_graph.Graph'>
	  <Graph at 0x1014019b0 name=three>
	    -> {'other': <Graph at 0x1012b1978 name=one>, 'name': 'three
	'}
	    -> <class 'weakref_graph.Graph'>
	
	After 2 references removed:
	  one->two->three->one
	Collecting...
	Unreachable objects: 0
	Tracked Graph objects:
	  <Graph at 0x1012b1978 name=one>
	    -> {'other': <Graph at 0x1013d5358 name=two>, 'name': 'one'}
	    -> <class 'weakref_graph.Graph'>
	  <Graph at 0x1013d5358 name=two>
	    -> {'other': <Graph at 0x1014019b0 name=three>, 'name': 'two
	'}
	    -> <class 'weakref_graph.Graph'>
	  <Graph at 0x1014019b0 name=three>
	    -> {'other': <Graph at 0x1012b1978 name=one>, 'name': 'three
	'}
	    -> <class 'weakref_graph.Graph'>
	
	Removing last reference:
	Collecting...
	gc: collectable <Graph 0x1012b1978>
	gc: collectable <dict 0x1012940c8>
	gc: collectable <Graph 0x1013d5358>
	gc: collectable <dict 0x101294108>
	gc: collectable <Graph 0x1014019b0>
	gc: collectable <dict 0x1013e7c48>
	(Deleting one)
	  one.set_next(None)
	(Deleting two)
	  two.set_next(None)
	(Deleting three)
	  three.set_next(None)
	Unreachable objects: 6
	Tracked Graph objects:
	
	Collecting...
	Unreachable objects: 2
	Tracked Graph objects:

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

.. code-block:: none

	$ python3 weakref_weakgraph.py
	
	Set up graph:
	  one.set_next(<WeakGraph at 0x101beb710 name=two>)
	  two.set_next(<WeakGraph at 0x101beb748 name=three>)
	  three.set_next(<weakproxy at 0x101bdee08 to WeakGraph at 0x101bd540
	0>)
	
	Graph:
	  one->two->three
	Collecting...
	Unreachable objects: 0
	Tracked Graph objects:
	  <WeakGraph at 0x101bd5400 name=one>
	    -> {'other': <WeakGraph at 0x101beb710 name=two>, 'name': 'one'}
	    -> <class '__main__.WeakGraph'>
	  <WeakGraph at 0x101beb710 name=two>
	    -> {'other': <WeakGraph at 0x101beb748 name=three>, 'name': 'two'
	}
	    -> <class '__main__.WeakGraph'>
	  <WeakGraph at 0x101beb748 name=three>
	    -> {'other': <weakproxy at 0x101bdee08 to WeakGraph at 0x101bd540
	0>, 'name': 'three'}
	    -> <class '__main__.WeakGraph'>
	  <weakproxy at 0x101bdee08 to WeakGraph at 0x101bd5400>
	
	After 2 references removed:
	  one->two->three
	Collecting...
	Unreachable objects: 0
	Tracked Graph objects:
	  <WeakGraph at 0x101bd5400 name=one>
	    -> {'other': <WeakGraph at 0x101beb710 name=two>, 'name': 'one'}
	    -> <class '__main__.WeakGraph'>
	  <WeakGraph at 0x101beb710 name=two>
	    -> {'other': <WeakGraph at 0x101beb748 name=three>, 'name': 'two'
	}
	    -> <class '__main__.WeakGraph'>
	  <WeakGraph at 0x101beb748 name=three>
	    -> {'other': <weakproxy at 0x101bdee08 to WeakGraph at 0x101bd540
	0>, 'name': 'three'}
	    -> <class '__main__.WeakGraph'>
	  <weakproxy at 0x101bdee08 to WeakGraph at 0x101bd5400>
	
	Removing last reference:
	(Deleting one)
	  one.set_next(None)
	(Deleting two)
	  two.set_next(None)
	(Deleting three)
	  three.set_next(None)
	Collecting...
	Unreachable objects: 0
	Tracked Graph objects:

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

.. code-block:: none

	$ python3 weakref_valuedict.py
	
	CACHE TYPE: <class 'dict'>
	  all_refs = {'one': ExpensiveObject(one),
	 'three': ExpensiveObject(three),
	 'two': ExpensiveObject(two)}
	
	  Before, cache contains: dict_keys(['one', 'three', 'two'])
	    one = ExpensiveObject(one)
	    three = ExpensiveObject(three)
	    two = ExpensiveObject(two)
	
	  Cleanup:
	
	  After, cache contains: dict_keys(['one', 'three', 'two'])
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
	
	  Before, cache contains: <generator object WeakValueDictionary.
	keys at 0x101bcf8e0>
	    one = ExpensiveObject(one)
	    three = ExpensiveObject(three)
	    two = ExpensiveObject(two)
	
	  Cleanup:
	    (Deleting ExpensiveObject(one))
	    (Deleting ExpensiveObject(three))
	    (Deleting ExpensiveObject(two))
	
	  After, cache contains: <generator object WeakValueDictionary.k
	eys at 0x1018068e0>
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
