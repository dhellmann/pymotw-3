==========================
 gc --- Garbage Collector
==========================

.. module:: gc
    :synopsis: Garbage Collector

:Purpose: Manages memory used by Python objects

``gc`` exposes the underlying memory management mechanism of
Python, the automatic garbage collector.  The module includes
functions for controlling how the collector operates and to examine
the objects known to the system, either pending collection or stuck in
reference cycles and unable to be freed.

Tracing References
==================

With ``gc`` the incoming and outgoing references between objects
can be used to find cycles in complex data structures.  If a data
structure is known to have a cycle, custom code can be used to examine
its properties.  If the cycle is in unknown code, the
``get_referents()`` and ``get_referrers()`` functions can be
used to build generic debugging tools.

For example, ``get_referents()`` shows the objects *referred to*
by the input arguments.

.. literalinclude:: gc_get_referents.py
   :caption:
   :start-after: #end_pymotw_header

In this case, the ``Graph`` instance ``three`` holds references
to its instance dictionary (in the ``__dict__`` attribute) and its
class.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gc_get_referents.py'))
.. }}}

.. code-block:: none

	$ python3 gc_get_referents.py
	
	Linking nodes Graph(one).next = Graph(two)
	Linking nodes Graph(two).next = Graph(three)
	Linking nodes Graph(three).next = Graph(one)
	
	three refers to:
	{'name': 'three', 'next': Graph(one)}
	<class '__main__.Graph'>

.. {{{end}}}

The next example uses a :mod:`Queue` to perform a breadth-first
traversal of all of the object references looking for cycles.  The
items inserted into the queue are tuples containing the reference
chain so far and the next object to examine.  It starts with
``three``, and looks at everything it refers to.  Skipping classes
avoids looking at methods, modules, etc.

.. literalinclude:: gc_get_referents_cycles.py
   :caption:
   :start-after: #end_pymotw_header

The cycle in the nodes is easily found by watching for objects that
have already been processed.  To avoid holding references to those
objects, their ``id()`` values are cached in a set.  The
dictionary objects found in the cycle are the ``__dict__`` values for
the ``Graph`` instances, and hold their instance attributes.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gc_get_referents_cycles.py'))
.. }}}

.. code-block:: none

	$ python3 gc_get_referents_cycles.py
	
	Linking nodes Graph(one).next = Graph(two)
	Linking nodes Graph(two).next = Graph(three)
	Linking nodes Graph(three).next = Graph(one)
	
	Examining: Graph(three)
	Examining: {'next': Graph(one), 'name': 'three'}
	Examining: Graph(one)
	Examining: {'next': Graph(two), 'name': 'one'}
	Examining: Graph(two)
	Examining: {'next': Graph(three), 'name': 'two'}
	
	Found a cycle to Graph(three):
	  0:  Graph(three)
	  1:  {'name': 'three', 'next': Graph(one)}
	  2:  Graph(one)
	  3:  {'name': 'one', 'next': Graph(two)}
	  4:  Graph(two)
	  5:  {'name': 'two', 'next': Graph(three)}

.. {{{end}}}

Forcing Garbage Collection
==========================

Although the garbage collector runs automatically as the interpreter
executes a program, it can be triggered to run at a specific time when
there are a lot of objects to free or there is not much work happening
and the collector will not hurt application performance.  Trigger
collection using ``collect()``.

.. literalinclude:: gc_collect.py
   :caption:
   :start-after: #end_pymotw_header

In this example, the cycle is cleared as soon as collection runs the
first time, since nothing refers to the ``Graph`` nodes except
themselves.  ``collect()`` returns the number of "unreachable"
objects it found.  In this case, the value is ``6`` because there are
three objects with their instance attribute dictionaries.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gc_collect.py'))
.. }}}

.. code-block:: none

	$ python3 gc_collect.py
	
	Linking nodes Graph(one).next = Graph(two)
	Linking nodes Graph(two).next = Graph(three)
	Linking nodes Graph(three).next = Graph(one)
	
	Collecting 0 ...
	Unreachable objects: 6
	Remaining Garbage: []
	
	Collecting 1 ...
	Unreachable objects: 0
	Remaining Garbage: []

.. {{{end}}}

Finding References to Objects that Cannot be Collected
======================================================

Looking for the object holding a reference to something in the garbage
list is a little trickier than seeing what an object references.
Because the code asking about the reference needs to hold a reference
itself, some of the referrers need to be ignored.  This example
creates a graph cycle, then works through the ``Graph`` instances
and removes the reference in the "parent" node.

.. literalinclude:: gc_get_referrers.py
   :caption:
   :start-after: #end_pymotw_header

This sort of logic is overkill if the cycles are understood, but for
an unexplained cycle in data using ``get_referrers()`` can expose
the unexpected relationship.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gc_get_referrers.py'))
.. }}}

.. code-block:: none

	$ python3 gc_get_referrers.py
	
	Linking nodes Graph(one).next = Graph(two)
	Linking nodes Graph(two).next = Graph(three)
	Linking nodes Graph(three).next = Graph(one)
	
	Collecting...
	Graph(one).__del__()
	Graph(two).__del__()
	Graph(three).__del__()
	Unreachable objects: 6
	Remaining Garbage: []
	
	Clearing referrers:
	
	Clearing gc.garbage:
	
	Collecting...
	Unreachable objects: 0
	Remaining Garbage: []

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
be examined with ``get_threshold()``.

.. literalinclude:: gc_get_threshold.py
   :caption:
   :start-after: #end_pymotw_header

The return value is a tuple with the threshold for each generation.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gc_get_threshold.py'))
.. }}}

.. code-block:: none

	$ python3 gc_get_threshold.py
	
	(700, 10, 10)

.. {{{end}}}

The thresholds can be changed with ``set_threshold()``.  This
example program uses a command line argument to set the threshold for
generation ``0`` then allocates a series of objects.

.. literalinclude:: gc_threshold.py
   :caption:
   :start-after: #end_pymotw_header

Different threshold values introduce the garbage collection sweeps at
different times, shown here because debugging is enabled.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u gc_threshold.py 5'))
.. }}}

.. code-block:: none

	$ python3 -u gc_threshold.py 5
	
	gc: collecting generation 1...
	gc: objects in each generation: 240 1439 4709
	gc: done, 0.0013s elapsed
	Thresholds: (5, 1, 1)
	Clear the collector by forcing a run
	gc: collecting generation 2...
	gc: objects in each generation: 1 0 6282
	gc: done, 0.0025s elapsed
	
	gc: collecting generation 0...
	gc: objects in each generation: 5 0 6275
	gc: done, 0.0000s elapsed
	Creating objects
	gc: collecting generation 0...
	gc: objects in each generation: 8 0 6275
	gc: done, 0.0000s elapsed
	Created 0
	Created 1
	Created 2
	gc: collecting generation 1...
	gc: objects in each generation: 9 2 6275
	gc: done, 0.0000s elapsed
	Created 3
	Created 4
	Created 5
	gc: collecting generation 0...
	gc: objects in each generation: 9 0 6280
	gc: done, 0.0000s elapsed
	Created 6
	Created 7
	Created 8
	gc: collecting generation 0...
	gc: objects in each generation: 9 3 6280
	gc: done, 0.0000s elapsed
	Created 9
	Exiting

.. {{{end}}}

A smaller threshold causes the sweeps to run more frequently.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u gc_threshold.py 2'))
.. }}}

.. code-block:: none

	$ python3 -u gc_threshold.py 2
	
	gc: collecting generation 1...
	gc: objects in each generation: 240 1439 4709
	gc: done, 0.0003s elapsed
	Thresholds: (2, 1, 1)
	Clear the collector by forcing a run
	gc: collecting generation 2...
	gc: objects in each generation: 1 0 6282
	gc: done, 0.0010s elapsed
	gc: collecting generation 0...
	gc: objects in each generation: 3 0 6275
	gc: done, 0.0000s elapsed
	
	Creating objects
	gc: collecting generation 0...
	gc: objects in each generation: 6 0 6275
	gc: done, 0.0000s elapsed
	gc: collecting generation 1...
	gc: objects in each generation: 3 4 6275
	gc: done, 0.0000s elapsed
	Created 0
	Created 1
	gc: collecting generation 0...
	gc: objects in each generation: 4 0 6277
	gc: done, 0.0000s elapsed
	Created 2
	gc: collecting generation 0...
	gc: objects in each generation: 8 1 6277
	gc: done, 0.0000s elapsed
	Created 3
	Created 4
	gc: collecting generation 1...
	gc: objects in each generation: 4 3 6277
	gc: done, 0.0000s elapsed
	Created 5
	gc: collecting generation 0...
	gc: objects in each generation: 8 0 6281
	gc: done, 0.0000s elapsed
	Created 6
	Created 7
	gc: collecting generation 0...
	gc: objects in each generation: 4 2 6281
	gc: done, 0.0000s elapsed
	Created 8
	gc: collecting generation 1...
	gc: objects in each generation: 8 3 6281
	gc: done, 0.0000s elapsed
	Created 9
	Exiting

.. {{{end}}}

Debugging
=========

Debugging memory leaks can be challenging.  ``gc`` includes several
options to expose the inner workings to make the job easier.  The
options are bit-flags meant to be combined and passed to
``set_debug()`` to configure the garbage collector while the program
is running.  Debugging information is printed to ``sys.stderr``.

The ``DEBUG_STATS`` flag turns on statistics reporting, causing
the garbage collector to report when it is running, the number of
objects tracked for each generation, and the amount of time it took to
perform the sweep.

.. literalinclude:: gc_debug_stats.py
   :caption:
   :start-after: #end_pymotw_header

This example output shows two separate runs of the collector because
it runs once when it is invoked explicitly, and a second time when the
interpreter exits.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gc_debug_stats.py'))
.. }}}

.. code-block:: none

	$ python3 gc_debug_stats.py
	
	gc: collecting generation 2...
	gc: objects in each generation: 123 1063 4711
	gc: done, 0.0008s elapsed
	Exiting
	gc: collecting generation 2...
	gc: objects in each generation: 1 0 5880
	gc: done, 0.0007s elapsed
	gc: collecting generation 2...
	gc: objects in each generation: 99 0 5688
	gc: done, 2114 unreachable, 0 uncollectable, 0.0011s elapsed
	gc: collecting generation 2...
	gc: objects in each generation: 0 0 3118
	gc: done, 292 unreachable, 0 uncollectable, 0.0003s elapsed

.. {{{end}}}

Enabling ``DEBUG_COLLECTABLE`` and ``DEBUG_UNCOLLECTABLE``
causes the collector to report on whether each object it examines can
or cannot be collected.

.. literalinclude:: gc_debug_collectable_objects.py
   :caption:
   :start-after: #end_pymotw_header

The two classes ``Graph`` and ``CleanupGraph`` are
constructed so it is possible to create structures that can be
collected automatically and structures where cycles need to be
explicitly broken by the user.

The output shows that the ``Graph`` instances :obj:`one` and
:obj:`two` create a cycle, but can still be collected because they do
not have a finalizer and their only incoming references are from other
objects that can be collected.  Although ``CleanupGraph`` has a
finalizer, :obj:`three` is reclaimed as soon as its reference count
goes to zero. In contrast, :obj:`four` and :obj:`five` create a cycle
and cannot be freed.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u gc_debug_collectable_objects.py'))
.. }}}

.. code-block:: none

	$ python3 -u gc_debug_collectable_objects.py
	
	Creating Graph 0x101be71d0 (one)
	Creating Graph 0x101be7240 (two)
	Linking nodes Graph(one).next = Graph(two)
	Linking nodes Graph(two).next = Graph(one)
	Creating CleanupGraph 0x101be7320 (three)
	Creating CleanupGraph 0x101be7358 (four)
	Creating CleanupGraph 0x101be7390 (five)
	Linking nodes CleanupGraph(four).next = CleanupGraph(five)
	Linking nodes CleanupGraph(five).next = CleanupGraph(four)
	CleanupGraph(three).__del__()
	
	Collecting
	gc: collectable <Graph 0x101be71d0>
	gc: collectable <Graph 0x101be7240>
	gc: collectable <dict 0x101894108>
	gc: collectable <dict 0x101894148>
	gc: collectable <CleanupGraph 0x101be7358>
	gc: collectable <CleanupGraph 0x101be7390>
	gc: collectable <dict 0x101bee548>
	gc: collectable <dict 0x101bee488>
	CleanupGraph(four).__del__()
	CleanupGraph(five).__del__()
	Done

.. {{{end}}}

If seeing the objects that cannot be collected is not enough
information to understand where data is being retained, enable
``DEBUG_SAVEALL`` to cause ``gc`` to preserve all objects it
finds without any references in the :obj:`garbage` list.

.. literalinclude:: gc_debug_saveall.py
   :caption:
   :start-after: #end_pymotw_header

This allows the objects to be examined after garbage collection, which
is helpful if, for example, the constructor cannot be changed to print
the object id when each object is created.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u gc_debug_saveall.py'))
.. }}}

.. code-block:: none

	$ python3 -u gc_debug_saveall.py
	
	CleanupGraph(three).__del__()
	Collecting
	gc: collectable <Graph 0x101be7240>
	gc: collectable <Graph 0x101be72e8>
	gc: collectable <dict 0x101994108>
	gc: collectable <dict 0x101994148>
	gc: collectable <CleanupGraph 0x101be73c8>
	gc: collectable <CleanupGraph 0x101be7400>
	gc: collectable <dict 0x101bee548>
	gc: collectable <dict 0x101bee488>
	CleanupGraph(four).__del__()
	CleanupGraph(five).__del__()
	Done
	Retained: Graph(one) 0x101be7240
	Retained: Graph(two) 0x101be72e8
	Retained: CleanupGraph(four) 0x101be73c8
	Retained: CleanupGraph(five) 0x101be7400

.. {{{end}}}

For simplicity, ``DEBUG_LEAK`` is defined as a combination of all
of the other options.

.. literalinclude:: gc_debug_leak.py
   :caption:
   :start-after: #end_pymotw_header

Keep in mind that because ``DEBUG_SAVEALL`` is enabled by
``DEBUG_LEAK``, even the unreferenced objects that would normally
have been collected and deleted are retained.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u gc_debug_leak.py'))
.. }}}

.. code-block:: none

	$ python3 -u gc_debug_leak.py
	
	CleanupGraph(three).__del__()
	Collecting
	gc: collectable <Graph 0x1013e7240>
	gc: collectable <Graph 0x1013e72e8>
	gc: collectable <dict 0x101194108>
	gc: collectable <dict 0x101194148>
	gc: collectable <CleanupGraph 0x1013e73c8>
	gc: collectable <CleanupGraph 0x1013e7400>
	gc: collectable <dict 0x1013ee548>
	gc: collectable <dict 0x1013ee488>
	CleanupGraph(four).__del__()
	CleanupGraph(five).__del__()
	Done
	Retained: Graph(one) 0x1013e7240
	Retained: Graph(two) 0x1013e72e8
	Retained: CleanupGraph(four) 0x1013e73c8
	Retained: CleanupGraph(five) 0x1013e7400

.. {{{end}}}


.. seealso::

   * :pydoc:`gc`

   * :ref:`Porting notes for gc <porting-gc>`

   * :mod:`weakref` -- The ``weakref`` module provides a way to create
     references to objects without increasing their reference count,
     so they can still be garbage collected.

   * `Supporting Cyclic Garbage Collection
     <https://docs.python.org/3/c-api/gcsupport.html>`__ -- Background
     material from Python's C API documentation.

   * `How does Python manage memory?
     <http://effbot.org/pyfaq/how-does-python-manage-memory.htm>`__ --
     An article on Python memory management by Fredrik Lundh.
