=======================
gc -- Garbage Collector
=======================

.. module:: gc
    :synopsis: Garbage Collector

:Purpose: Manages memory used by Python objects
:Available In: 2.1+

:mod:`gc` exposes the underlying memory management mechanism of
Python, the automatic garbage collector.  The module includes
functions for controlling how the collector operates and to examine
the objects known to the system, either pending collection or stuck in
reference cycles and unable to be freed.

Tracing References
==================

With :mod:`gc` you can use the incoming and outgoing references
between objects to find cycles in complex data structures.  If you
know the data structure with the cycle, you can construct custom code
to examine its properties.  If not, you can the
:func:`get_referents()` and :func:`get_referrers()` functions to build
generic debugging tools.

For example, :func:`get_referents()` shows the objects *referred to*
by the input arguments.

.. include:: gc_get_referents.py
   :literal:
   :start-after: #end_pymotw_header

In this case, the :class:`Graph` instance ``three`` holds references
to its instance dictionary (in the ``__dict__`` attribute) and its
class.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gc_get_referents.py'))
.. }}}

::

	$ python gc_get_referents.py
	
	Linking nodes Graph(one).next = Graph(two)
	Linking nodes Graph(two).next = Graph(three)
	Linking nodes Graph(three).next = Graph(one)
	
	three refers to:
	{'name': 'three', 'next': Graph(one)}
	<class '__main__.Graph'>

.. {{{end}}}

This example uses a :mod:`Queue` to perform a breadth-first traversal
of all of the object references looking for cycles.  The items
inserted into the queue are tuples containing the reference chain so
far and the next object to examine.  It starts with ``three``, and
look at everything it refers to.  Skipping classes lets us avoid
looking at methods, modules, etc.

.. include:: gc_get_referents_cycles.py
   :literal:
   :start-after: #end_pymotw_header

The cycle in the nodes is easily found by watching for objects that
have already been processed.  To avoid holding references to those
objects, their :func:`id()` values are cached in a set.  The
dictionary objects found in the cycle are the ``__dict__`` values for
the :class:`Graph` instances, and hold their instance attributes.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gc_get_referents_cycles.py'))
.. }}}

::

	$ python gc_get_referents_cycles.py
	
	Linking nodes Graph(one).next = Graph(two)
	Linking nodes Graph(two).next = Graph(three)
	Linking nodes Graph(three).next = Graph(one)
	
	Examining: Graph(three)
	Examining: {'name': 'three', 'next': Graph(one)}
	Examining: Graph(one)
	Examining: {'name': 'one', 'next': Graph(two)}
	Examining: Graph(two)
	Examining: {'name': 'two', 'next': Graph(three)}
	
	Found a cycle to Graph(three):
	  0: Graph(three)
	  1: {'name': 'three', 'next': Graph(one)}
	  2: Graph(one)
	  3: {'name': 'one', 'next': Graph(two)}
	  4: Graph(two)
	  5: {'name': 'two', 'next': Graph(three)}

.. {{{end}}}


Forcing Garbage Collection
==========================

Although the garbage collector runs automatically as the interpreter
executes your program, you may want to trigger collection to run at a
specific time when you know there are a lot of objects to free or
there is not much work happening in your application.  Trigger
collection using :func:`collect()`.

.. include:: gc_collect.py
   :literal:
   :start-after: #end_pymotw_header

In this example, the cycle is cleared as soon as collection runs the
first time, since nothing refers to the :class:`Graph` nodes except
themselves.  :func:`collect()` returns the number of "unreachable"
objects it found.  In this case, the value is ``6`` because there are
3 objects with their instance attribute dictionaries.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gc_collect.py'))
.. }}}

::

	$ python gc_collect.py
	
	Linking nodes Graph(one).next = Graph(two)
	Linking nodes Graph(two).next = Graph(three)
	Linking nodes Graph(three).next = Graph(one)
	
	Collecting 0 ...
	Unreachable objects: 6
	Remaining Garbage:[]
	
	Collecting 1 ...
	Unreachable objects: 0
	Remaining Garbage:[]
	

.. {{{end}}}

If :class:`Graph` has a :func:`__del__()` method, however, the garbage
collector cannot break the cycle.  

.. include:: gc_collect_with_del.py
   :literal:
   :start-after: #end_pymotw_header

Because more than one object in the cycle has a finalizer method, the
order in which the objects need to be finalized and then garbage
collected cannot be determined, so the garbage collector plays it safe
and keeps the objects.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gc_collect_with_del.py'))
.. }}}

::

	$ python gc_collect_with_del.py
	
	Graph(one).next = Graph(two)
	Graph(two).next = Graph(three)
	Graph(three).next = Graph(one)
	Collecting...
	Unreachable objects: 6
	Remaining Garbage:[Graph(one), Graph(two), Graph(three)]

.. {{{end}}}

When the cycle is broken, the :class:`Graph` instances can be
collected.

.. include:: gc_collect_break_cycle.py
   :literal:
   :start-after: #end_pymotw_header

Because ``gc.garbage`` holds a reference to the objects from the
previous garbage collection run, it needs to be cleared out after the
cycle is broken to reduce the reference counts so they can be
finalized and freed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gc_collect_break_cycle.py'))
.. }}}

::

	$ python gc_collect_break_cycle.py
	
	Linking nodes Graph(one).next = Graph(two)
	Linking nodes Graph(two).next = Graph(three)
	Linking nodes Graph(three).next = Graph(one)
	
	Collecting...
	Unreachable objects: 6
	Remaining Garbage:[Graph(one), Graph(two), Graph(three)]
	
	Breaking the cycle
	Linking nodes Graph(one).next = None
	Removing references in gc.garbage
	Graph(two).__del__()
	Graph(three).__del__()
	Graph(one).__del__()
	
	Collecting...
	Unreachable objects: 0
	Remaining Garbage:[]

.. {{{end}}}


Finding References to Objects that Can't be Collected
=====================================================

Looking for the object holding a reference to something in the garbage
is a little trickier than seeing what an object references.  Because
the code asking about the reference needs to hold a reference itself,
some of the referrers need to be ignored.  This example creates a
graph cycle, then works through the :class:`Graph` instances in the
garbage and removes the reference in the "parent" node.

.. include:: gc_get_referrers.py
   :literal:
   :start-after: #end_pymotw_header

This sort of logic is overkill if you understand why the cycles are
being created in the first place, but if you have an unexplained cycle
in your data using :func:`get_referrers()` can expose the unexpected
relationship.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gc_get_referrers.py'))
.. }}}

::

	$ python gc_get_referrers.py
	
	Linking nodes Graph(one).next = Graph(two)
	Linking nodes Graph(two).next = Graph(three)
	Linking nodes Graph(three).next = Graph(one)
	
	Collecting...
	Unreachable objects: 6
	Remaining Garbage:[Graph(one), Graph(two), Graph(three)]
	
	Clearing referrers:
	Looking for references to Graph(one)
	Looking for references to {'name': 'three', 'next': Graph(one)}
	Linking nodes Graph(three).next = None
	Looking for references to Graph(two)
	Looking for references to {'name': 'one', 'next': Graph(two)}
	Linking nodes Graph(one).next = None
	Looking for references to Graph(three)
	Looking for references to {'name': 'two', 'next': Graph(three)}
	Linking nodes Graph(two).next = None
	
	Clearing gc.garbage:
	Graph(three).__del__()
	Graph(two).__del__()
	Graph(one).__del__()
	
	Collecting...
	Unreachable objects: 0
	Remaining Garbage:[]

.. {{{end}}}


Collection Thresholds and Generations
=====================================

The garbage collector maintains three lists of objects it sees as it
runs, one for each "generation" tracked by the collector.  As objects
are examined in each generation, they are either collected or they age
into subsequent generations until they finally reach the stage where
they are kept permanently.

The collector routines can be tuned to occur at different frequencies
based on the difference between the number of object allocations and
deallocations between runs.  When the number of allocations minus the
number of deallocations is greater than the threshold for the
generation, the garbage collector is run.  The current thresholds can
be examined with :func:`get_threshold()`.

.. include:: gc_get_threshold.py
   :literal:
   :start-after: #end_pymotw_header

The return value is a tuple with the threshold for each generation.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gc_get_threshold.py'))
.. }}}

::

	$ python gc_get_threshold.py
	
	(700, 10, 10)

.. {{{end}}}

The thresholds can be changed with :func:`set_threshold()`.  This
example program reads the threshold for generation ``0`` from the
command line, adjusts the :mod:`gc` settings, then allocates a series
of objects.

.. include:: gc_threshold.py
   :literal:
   :start-after: #end_pymotw_header

Different threshold values introduce the garbage collection sweeps at
different times, shown here because debugging is enabled.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u gc_threshold.py 5'))
.. }}}

::

	$ python -u gc_threshold.py 5
	
	Thresholds: (5, 1, 1)
	Clear the collector by forcing a run
	gc: collecting generation 2...
	gc: objects in each generation: 144 3163 0
	gc: done, 0.0004s elapsed.
	
	Creating objects
	gc: collecting generation 0...
	gc: objects in each generation: 7 0 3234
	gc: done, 0.0000s elapsed.
	Created 0
	Created 1
	Created 2
	Created 3
	Created 4
	gc: collecting generation 0...
	gc: objects in each generation: 6 4 3234
	gc: done, 0.0000s elapsed.
	Created 5
	Created 6
	Created 7
	Created 8
	Created 9
	gc: collecting generation 2...
	gc: objects in each generation: 5 6 3232
	gc: done, 0.0004s elapsed.

.. {{{end}}}

A smaller threshold causes the sweeps to run more frequently.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u gc_threshold.py 2'))
.. }}}

::

	$ python -u gc_threshold.py 2
	
	Thresholds: (2, 1, 1)
	Clear the collector by forcing a run
	gc: collecting generation 2...
	gc: objects in each generation: 144 3163 0
	gc: done, 0.0004s elapsed.
	
	Creating objects
	gc: collecting generation 0...
	gc: objects in each generation: 3 0 3234
	gc: done, 0.0000s elapsed.
	gc: collecting generation 0...
	gc: objects in each generation: 4 3 3234
	gc: done, 0.0000s elapsed.
	Created 0
	Created 1
	gc: collecting generation 1...
	gc: objects in each generation: 3 4 3234
	gc: done, 0.0000s elapsed.
	Created 2
	Created 3
	Created 4
	gc: collecting generation 0...
	gc: objects in each generation: 5 0 3239
	gc: done, 0.0000s elapsed.
	Created 5
	Created 6
	Created 7
	gc: collecting generation 0...
	gc: objects in each generation: 5 3 3239
	gc: done, 0.0000s elapsed.
	Created 8
	Created 9
	gc: collecting generation 2...
	gc: objects in each generation: 2 6 3235
	gc: done, 0.0004s elapsed.

.. {{{end}}}



Debugging
=========

Debugging memory leaks can be challenging.  :mod:`gc` includes several
options to expose the inner workings to make the job easier.  The
options are bit-flags meant to be combined and passed to
:func:`set_debug()` to configure the garbage collector while your
program is running.  Debugging information is printed to :ref:`stderr
<sys-input-output>`.

The :const:`DEBUG_STATS` flag turns on statistics reporting, causing
the garbage collector to report when it is running, the number of
objects tracked for each generation, and the amount of time it took to
perform the sweep.

.. include:: gc_debug_stats.py
   :literal:
   :start-after: #end_pymotw_header

This example output shows two separate runs of the collector because
it runs once when it is invoked explicitly, and a second time when the
interpreter exits.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gc_debug_stats.py'))
.. }}}

::

	$ python gc_debug_stats.py
	
	gc: collecting generation 2...
	gc: objects in each generation: 667 2808 0
	gc: done, 0.0011s elapsed.
	gc: collecting generation 2...
	gc: objects in each generation: 0 0 3164
	gc: done, 0.0009s elapsed.

.. {{{end}}}

Enabling :const:`DEBUG_COLLECTABLE` and :const:`DEBUG_UNCOLLECTABLE`
causes the collector to report on whether each object it examines can
or cannot be collected.  You need to combine these flags need with
:const:`DEBUG_OBJECTS` so :mod:`gc` will print information about
the objects being held.

.. include:: gc_debug_collectable_objects.py
   :literal:
   :start-after: #end_pymotw_header

The two classes :class:`Graph` and :class:`CleanupGraph` are
constructed so it is possible to create structures that are
automatically collectable and structures where cycles need to be
explicitly broken by the user.

The output shows that the :class:`Graph` instances :obj:`one` and
:obj:`two` create a cycle, but are still collectable because they do
not have a finalizer and their only incoming references are from other
objects that can be collected.  Although :class:`CleanupGraph` has a
finalizer, :obj:`three` is reclaimed as soon as its reference count
goes to zero. In contrast, :obj:`four` and :obj:`five` create a cycle
and cannot be freed.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u gc_debug_collectable_objects.py'))
.. }}}

::

	$ python -u gc_debug_collectable_objects.py
	
	Creating Graph 0x10045f750 (one)
	Creating Graph 0x10045f790 (two)
	Linking nodes Graph(one).next = Graph(two)
	Linking nodes Graph(two).next = Graph(one)
	Creating CleanupGraph 0x10045f7d0 (three)
	Creating CleanupGraph 0x10045f810 (four)
	Creating CleanupGraph 0x10045f850 (five)
	Linking nodes CleanupGraph(four).next = CleanupGraph(five)
	Linking nodes CleanupGraph(five).next = CleanupGraph(four)
	CleanupGraph(three).__del__()
	
	Collecting
	gc: collectable <Graph 0x10045f750>
	gc: collectable <Graph 0x10045f790>
	gc: collectable <dict 0x100360a30>
	gc: collectable <dict 0x100361cc0>
	gc: uncollectable <CleanupGraph 0x10045f810>
	gc: uncollectable <CleanupGraph 0x10045f850>
	gc: uncollectable <dict 0x100361de0>
	gc: uncollectable <dict 0x100362140>
	Done

.. {{{end}}}

The flag :const:`DEBUG_INSTANCES` works much the same way for
instances of old-style classes (not derived from :class:`object`.

.. include:: gc_debug_collectable_instances.py
   :literal:
   :start-after: #end_pymotw_header

In this case, however, the :class:`dict` objects holding the instance
attributes are not included in the output.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u gc_debug_collectable_instances.py'))
.. }}}

::

	$ python -u gc_debug_collectable_instances.py
	
	Creating Graph 0x1004687a0 (one)
	Creating Graph 0x1004687e8 (two)
	Linking nodes Graph(one).next = Graph(two)
	Linking nodes Graph(two).next = Graph(one)
	Creating CleanupGraph 0x100468878 (three)
	Creating CleanupGraph 0x1004688c0 (four)
	Creating CleanupGraph 0x100468908 (five)
	Linking nodes CleanupGraph(four).next = CleanupGraph(five)
	Linking nodes CleanupGraph(five).next = CleanupGraph(four)
	CleanupGraph(three).__del__()
	
	Collecting
	gc: collectable <Graph instance at 0x1004687a0>
	gc: collectable <Graph instance at 0x1004687e8>
	gc: uncollectable <CleanupGraph instance at 0x1004688c0>
	gc: uncollectable <CleanupGraph instance at 0x100468908>
	Done

.. {{{end}}}

If seeing the uncollectable objects is not enough information to
understand where data is being retained, you can enable
:const:`DEBUG_SAVEALL` to cause :mod:`gc` to preserve all objects it
finds without any references in the :obj:`garbage` list, so you can
examine them.  This is helpful if, for example, you don't have access
to the constructor to print the object id when each object is created.

.. include:: gc_debug_saveall.py
   :literal:
   :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u gc_debug_saveall.py'))
.. }}}

::

	$ python -u gc_debug_saveall.py
	
	CleanupGraph(three).__del__()
	Collecting
	gc: collectable <Graph 0x10045f790>
	gc: collectable <Graph 0x10045f7d0>
	gc: collectable <dict 0x100361890>
	gc: collectable <dict 0x100361cb0>
	gc: uncollectable <CleanupGraph 0x10045f850>
	gc: uncollectable <CleanupGraph 0x10045f890>
	gc: uncollectable <dict 0x100361dd0>
	gc: uncollectable <dict 0x100362130>
	Done
	Retained: Graph(one) 0x10045f790
	Retained: Graph(two) 0x10045f7d0
	Retained: CleanupGraph(four) 0x10045f850
	Retained: CleanupGraph(five) 0x10045f890

.. {{{end}}}

For simplicity, :const:`DEBUG_LEAK` is defined as a combination of all
of the other options.

.. include:: gc_debug_leak.py
   :literal:
   :start-after: #end_pymotw_header

Keep in mind that because :const:`DEBUG_SAVEALL` is enabled by
:const:`DEBUG_LEAK`, even the unreferenced objects that would normally
have been collected and deleted are retained.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u gc_debug_leak.py'))
.. }}}

::

	$ python -u gc_debug_leak.py
	
	CleanupGraph(three).__del__()
	Collecting
	gc: collectable <Graph 0x10045f790>
	gc: collectable <Graph 0x10045f7d0>
	gc: collectable <dict 0x100360a20>
	gc: collectable <dict 0x100361c20>
	gc: uncollectable <CleanupGraph 0x10045f850>
	gc: uncollectable <CleanupGraph 0x10045f890>
	gc: uncollectable <dict 0x100361d40>
	gc: uncollectable <dict 0x1003620a0>
	Done
	Retained: Graph(one) 0x10045f790
	Retained: Graph(two) 0x10045f7d0
	Retained: CleanupGraph(four) 0x10045f850
	Retained: CleanupGraph(five) 0x10045f890

.. {{{end}}}


.. seealso::

    `gc <http://docs.python.org/2.7/library/gc.html>`_
        The standard library documentation for this module.

    :mod:`weakref`
        The :mod:`weakref` module gives you references to objects
        without increasing their reference count, so they can still be
        garbage collected.

    `Supporting Cyclic Garbage Collection <http://docs.python.org/c-api/gcsupport.html>`__
        Background material from Python's C API documentation.

    `How does Python manage memory? <http://effbot.org/pyfaq/how-does-python-manage-memory.htm>`__
        An article on Python memory management by Fredrik Lundh.
