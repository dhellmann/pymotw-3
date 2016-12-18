===================================================================
 OrderedDict --- remember the order keys are added to a dictionary
===================================================================

An ``OrderedDict`` is a dictionary subclass that remembers the
order in which its contents are added.

.. literalinclude:: collections_ordereddict_iter.py
   :caption:
   :start-after: #end_pymotw_header

A regular ``dict`` does not track the insertion order, and
iterating over it produces the values in order based on how the keys
are stored in the hash table, which is in turn influenced by a random
value to reduce collisions.  In an ``OrderedDict``, by contrast,
the order the items are inserted is remembered and used when creating
an iterator.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'collections_ordereddict_iter.py'))
.. }}}

.. code-block:: none

	$ python3 collections_ordereddict_iter.py
	
	Regular dictionary:
	c C
	b B
	a A
	
	OrderedDict:
	a A
	b B
	c C

.. {{{end}}}

Equality
========

A regular ``dict`` looks at its contents when testing for
equality.  An ``OrderedDict`` also considers the order the items
were added.

.. literalinclude:: collections_ordereddict_equality.py
   :caption:
   :start-after: #end_pymotw_header

In this case, since the two ordered dictionaries are created from
values in a different order, they are considered to be different.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'collections_ordereddict_equality.py'))
.. }}}

.. code-block:: none

	$ python3 collections_ordereddict_equality.py
	
	dict       :
	True
	OrderedDict:
	False

.. {{{end}}}

Re-ordering
===========

It is possible to change the order of the keys in an
``OrderedDict`` by moving them either to the beginning or the end
of the sequence using ``move_to_end()``.

.. literalinclude:: collections_ordereddict_move_to_end.py
   :caption:
   :start-after: #end_pymotw_header

The ``last`` argument tells ``move_to_end()`` whether to move the
item to be the last item in the key sequence (when ``True``), or the
first (when ``False``).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'collections_ordereddict_move_to_end.py'))
.. }}}

.. code-block:: none

	$ python3 collections_ordereddict_move_to_end.py
	
	Before:
	a A
	b B
	c C
	
	move_to_end():
	a A
	c C
	b B
	
	move_to_end(last=False):
	b B
	a A
	c C

.. {{{end}}}



.. seealso::

   * `PYTHONHASHSEED
     <https://docs.python.org/3.5/using/cmdline.html#envvar-PYTHONHASHSEED>`__
     -- Environment variable to control the random seed value added to
     the hash algorithm for key locations in the dictionary.
