==========================
 enum -- Enumeration Type
==========================

.. module:: enum
   :synopsis: Defines enumeration type

The :mod:`enum` module defines an enumeration type with iteration and
comparison capabilities. It can be used to create well-defined symbols
for values, instead of using literal integer or strings.

Creating Enumerations
=====================

A new enumeration is defined using the ``class`` syntax by subclassing
:class:`Enum` and adding class attributes describing the values.

.. literalinclude:: enum_create.py
   :caption:
   :start-after: #end_pymotw_header

The members of the :class:`Enum` are converted to instances as the
class is parsed. Each instance has a ``name`` property corresponding
to the member name and a ``value`` property corresponding to the value
assigned to the name in the class definition.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'enum_create.py'))
.. }}}

::

	$ python3 enum_create.py
	
	
	Member name: wont_fix
	Member value: 4

.. {{{end}}}

Iteration
=========

Iterating over the enum *class* produces the individual members of the
enumeration.

.. literalinclude:: enum_iterate.py
   :caption:
   :start-after: #end_pymotw_header

The members are produced in the order they are declared in the class
definition. The names and values are not used to sort them in any way.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'enum_iterate.py'))
.. }}}

::

	$ python3 enum_iterate.py
	
	new             = 7
	incomplete      = 6
	invalid         = 5
	wont_fix        = 4
	in_progress     = 3
	fix_committed   = 2
	fix_released    = 1

.. {{{end}}}

Comparing Enums
===============

Because enumeration members are not ordered, they only support
comparison by identity and equality.

.. literalinclude:: enum_comparison.py
   :caption:
   :start-after: #end_pymotw_header

The greater-than and less-than comparison operators raise a
:class:`TypeError` exception.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'enum_comparison.py'))
.. }}}

::

	$ python3 enum_comparison.py
	
	Equal   : False True
	Identity: False True
	Ordered by value:
	  Cannot sort: unorderable types: BugStatus() < BugStatus()

.. {{{end}}}

Use the :class:`IntEnum` class for enumerations where the members need
to behave more like numbers, for example to support comparisons.

.. literalinclude:: enum_intenum.py
   :caption:
   :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'enum_intenum.py'))
.. }}}

::

	$ python3 enum_intenum.py
	
	Equal   : False True
	Identity: False True
	Ordered by value:
	  fix_released
	  fix_committed
	  in_progress
	  wont_fix
	  invalid
	  incomplete
	  new

.. {{{end}}}



.. comparison
.. unique values
.. functional API for creating
.. integer enums
.. non-integer values of enum members (tuple, such as planet example, or fancier)


.. seealso::

   * :pydoc:`enum`
