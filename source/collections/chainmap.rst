===========================================
 ChainMap --- search multiple dictionaries
===========================================

The :class:`ChainMap` class manages a sequence of dictionaries,
searching them in order to find values associated with keys. A
:class:`ChainMap` makes a good "context" container, since it can be
treated as a stack with changes happening as the stack grows, then
being discarded again as the stack shrinks.

Accessing Values
================

The :class:`ChainMap` supports the same API as a regular dictionary
for accessing existing values.

.. include:: collections_chainmap_read.py
   :literal:
   :start-after: #end_pymotw_header

The child mappings are searched in the order they are passed to the
constructor, so the value reported for the key ``'c'`` comes from the
``a`` dictionary.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'collections_chainmap_read.py'))
.. }}}

::

	$ python3 collections_chainmap_read.py
	
	Individual Values
	a = A
	b = B
	c = C
	
	Keys = ['c', 'b', 'a']
	Values = ['C', 'B', 'A']
	
	Items:
	c = C
	b = B
	a = A
	
	"d" in m: False

.. {{{end}}}

Reordering
==========

The :class:`ChainMap` stores the list of mappings over which it
searches in a list in its :attr:`maps` attribute. The list is mutable,
so it is possible to add new mappings directly or to change the order
of the elements to control look-up and update behavior.

.. include:: collections_chainmap_reorder.py
   :literal:
   :start-after: #end_pymotw_header

When the list of mappings is reversed, the value associated with
``'c'`` changes.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'collections_chainmap_reorder.py'))
.. }}}

::

	$ python3 collections_chainmap_reorder.py
	
	[{'c': 'C', 'a': 'A'}, {'c': 'D', 'b': 'B'}]
	c = C
	
	[{'c': 'D', 'b': 'B'}, {'c': 'C', 'a': 'A'}]
	c = D

.. {{{end}}}

Updating Values
===============

A :class:`ChainMap` does not cache the values in the child mappings,
so if their contents are modified the results are reflected when the
:class:`ChainMap` is accessed.

.. include:: collections_chainmap_update_behind.py
   :literal:
   :start-after: #end_pymotw_header

Changing the values associated with existing keys and adding new
elements works the same way.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'collections_chainmap_update_behind.py'))
.. }}}

::

	$ python3 collections_chainmap_update_behind.py
	
	Before: C
	After : E

.. {{{end}}}

It is also possible to set values through the :class:`ChainMap`
directly, though only the first mapping in the chain is actually
modified.

.. include:: collections_chainmap_update_directly.py
   :literal:
   :start-after: #end_pymotw_header

When the new value is stored using ``m``, the ``a`` mapping is
updated.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'collections_chainmap_update_directly.py'))
.. }}}

::

	$ python3 collections_chainmap_update_directly.py
	
	Before: ChainMap({'c': 'C', 'a': 'A'}, {'c': 'D', 'b': 'B'})
	After : ChainMap({'c': 'E', 'a': 'A'}, {'c': 'D', 'b': 'B'})
	a: {'c': 'E', 'a': 'A'}

.. {{{end}}}

:class:`ChainMap` provides a convenience method for creating a new
instance with one extra mapping at the front of the :attr:`maps` list
to make it easy to avoid modifying the existing underlying data
structures.

.. include:: collections_chainmap_new_child.py
   :literal:
   :start-after: #end_pymotw_header

This stacking behavior is what makes it convenient to use
:class:`ChainMap` instances as template or application contexts, since
it is easy to add or update values in one iteration, then discard the
changes for the next iteration.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'collections_chainmap_new_child.py'))
.. }}}

::

	$ python3 collections_chainmap_new_child.py
	
	m1 before: ChainMap({'c': 'C', 'a': 'A'}, {'c': 'D', 'b': 'B'})
	m2 before: ChainMap({}, {'c': 'C', 'a': 'A'}, {'c': 'D', 'b': 'B
	'})
	m1 after: ChainMap({'c': 'C', 'a': 'A'}, {'c': 'D', 'b': 'B'})
	m2 after: ChainMap({'c': 'E'}, {'c': 'C', 'a': 'A'}, {'c': 'D', 
	'b': 'B'})

.. {{{end}}}
