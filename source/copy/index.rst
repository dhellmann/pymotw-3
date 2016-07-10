============================
 copy --- Duplicate Objects
============================

.. module:: copy
    :synopsis: Duplicating objects.

:Purpose: Provides functions for duplicating objects using shallow or deep copy semantics.

The :mod:`copy` module includes two functions, :func:`copy` and
:func:`deepcopy`, for duplicating existing objects.

Shallow Copies
==============

The *shallow copy* created by :func:`copy` is a new container
populated with references to the contents of the original object. When
making a shallow copy of a :class:`list` object, a new :class:`list`
is constructed and the elements of the original object are appended to
it.

.. literalinclude:: copy_shallow.py
   :caption:
   :start-after: #end_pymotw_header

For a shallow copy, the :class:`MyClass` instance is not duplicated, so
the reference in the :data:`dup` list is to the same object that is in 
:data:`my_list`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'copy_shallow.py'))
.. }}}

.. code-block:: none

	$ python3 copy_shallow.py
	
	             my_list: [<__main__.MyClass object at 0x1007a87b8>]
	                 dup: [<__main__.MyClass object at 0x1007a87b8>]
	      dup is my_list: False
	      dup == my_list: True
	dup[0] is my_list[0]: True
	dup[0] == my_list[0]: True

.. {{{end}}}


Deep Copies
===========

The *deep copy* created by :func:`deepcopy` is a new container
populated with copies of the contents of the original object. To make
a deep copy of a :class:`list`, a new :class:`list` is constructed,
the elements of the original list are copied, then those copies are
appended to the new list.

Replacing the call to :func:`copy` with :func:`deepcopy` makes the
difference in the output apparent.

.. literalinclude:: copy_deep.py
   :caption:
   :start-after: #end_pymotw_header
   :emphasize-lines: 20

The first element of the list is no longer the same object reference,
but when the two objects are compared they still evaluate as being
equal.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'copy_deep.py'))
.. }}}

.. code-block:: none

	$ python3 copy_deep.py
	
	             my_list: [<__main__.MyClass object at 0x1018a87b8>]
	                 dup: [<__main__.MyClass object at 0x1018b1b70>]
	      dup is my_list: False
	      dup == my_list: True
	dup[0] is my_list[0]: False
	dup[0] == my_list[0]: True

.. {{{end}}}


Customizing Copy Behavior
=========================

It is possible to control how copies are made using the
:func:`__copy__` and :func:`__deepcopy__` special methods.

* :func:`__copy__` is called without any arguments and should return a
  shallow copy of the object.

* :func:`__deepcopy__` is called with a memo dictionary, and should
  return a deep copy of the object. Any member attributes that need to
  be deep-copied should be passed to :func:`copy.deepcopy`, along with
  the memo dictionary, to control for recursion (The memo dictionary
  is explained in more detail later.).

This example illustrates how the methods are called:

.. literalinclude:: copy_hooks.py
   :caption:
   :start-after: #end_pymotw_header

The memo dictionary is used to keep track of the values that have been
copied already, to avoid infinite recursion.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'copy_hooks.py'))
.. }}}

.. code-block:: none

	$ python3 copy_hooks.py
	
	__copy__()
	__deepcopy__({})

.. {{{end}}}


Recursion in Deep Copy
======================

To avoid problems with duplicating recursive data structures,
:func:`deepcopy` uses a dictionary to track objects that have already
been copied. This dictionary is passed to the :func:`__deepcopy__`
method so it can be examined there as well.

The next example shows how an interconnected data structure such as a
directed graph can assist with protecting against recursion by
implementing a :func:`__deepcopy__` method.

.. literalinclude:: copy_recursion.py
   :caption:
   :start-after: #end_pymotw_header

The :class:`Graph` class includes a few basic directed graph
methods. An instance can be initialized with a name and a list of
existing nodes to which it is connected. The :func:`add_connection`
method is used to set up bi-directional connections. It is also used
by the deepcopy operator.

The :func:`__deepcopy__` method prints messages to show how it is
called, and manages the memo dictionary contents as needed. Instead of
copying the connection list wholesale, it creates a new list and
appends copies of the individual connections to it. That ensures that
the memo dictionary is updated as each new node is duplicated, and
avoids recursion issues or extra copies of nodes. As before, it
returns the copied object when it is done.

.. digraph:: copy_example
   :caption: Deep copy for an Object Graph With Cycles

   "root";
   "a" -> "root";
   "b" -> "root";
   "b" -> "a";
   "root" -> "a";
   "root" -> "b";

There are several cycles in the graph shown in :figure:`copy_example`,
but handling the recursion with the memo dictionary prevents the
traversal from causing a stack overflow error.  When the *root* node
is copied, the output is:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'copy_recursion.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 copy_recursion.py
	
	
	Calling __deepcopy__ for Graph(name=root, id=4314569528)
	  Memo dictionary:
	    (empty)
	  Copying to new object Graph(name=root, id=4315093592)
	
	Calling __deepcopy__ for Graph(name=a, id=4314569584)
	  Memo dictionary:
	    Graph(name=root, id=4314569528): Graph(name=root,
	id=4315093592)
	  Copying to new object Graph(name=a, id=4315094208)
	
	Calling __deepcopy__ for Graph(name=root, id=4314569528)
	  Already copied to Graph(name=root, id=4315093592)
	
	Calling __deepcopy__ for Graph(name=b, id=4315092248)
	  Memo dictionary:
	    4314569528: Graph(name=root, id=4315093592)
	    4315692808: [Graph(name=root, id=4314569528), Graph(name=a,
	id=4314569584)]
	    Graph(name=root, id=4314569528): Graph(name=root,
	id=4315093592)
	    4314569584: Graph(name=a, id=4315094208)
	    Graph(name=a, id=4314569584): Graph(name=a, id=4315094208)
	  Copying to new object Graph(name=b, id=4315177536)

.. {{{end}}}

The second time the *root* node is encountered, while the *a* node is
being copied, :func:`__deepcopy__` detects the recursion and re-uses
the existing value from the memo dictionary instead of creating a new
object.

.. seealso::

   * :pydoc:`copy`
