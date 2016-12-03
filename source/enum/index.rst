==========================
 enum -- Enumeration Type
==========================

.. module:: enum
   :synopsis: Defines enumeration type

The ``enum`` module defines an enumeration type with iteration and
comparison capabilities. It can be used to create well-defined symbols
for values, instead of using literal integers or strings.

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

.. code-block:: none

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

.. code-block:: none

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

.. code-block:: none

	$ python3 enum_comparison.py
	
	Equality: False True
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

.. code-block:: none

	$ python3 enum_intenum.py
	
	Ordered by value:
	  fix_released
	  fix_committed
	  in_progress
	  wont_fix
	  invalid
	  incomplete
	  new

.. {{{end}}}

Unique Enumeration Values
=========================

Enum members with the same value are tracked as alias references to
the same member object. Aliases do not cause repeated values to be
present in the iterator for the :class:`Enum`.

.. literalinclude:: enum_aliases.py
   :caption:
   :start-after: #end_pymotw_header

Because ``by_design`` and ``closed`` are aliases for other members,
they do not appear separately in the output when iterating over the
:class:`Enum`. The canonical name for a member is the first name
attached to the value.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'enum_aliases.py'))
.. }}}

.. code-block:: none

	$ python3 enum_aliases.py
	
	new             = 7
	incomplete      = 6
	invalid         = 5
	wont_fix        = 4
	in_progress     = 3
	fix_committed   = 2
	fix_released    = 1
	
	Same: by_design is wont_fix:  True
	Same: closed is fix_released:  True

.. {{{end}}}

To require all members to have unique values, add the ``@unique``
decorator to the :class:`Enum`.

.. literalinclude:: enum_unique_enforce.py
   :caption:
   :start-after: #end_pymotw_header

Members with repeated values trigger a :class:`ValueError` exception
when the :class:`Enum` class is being interpreted.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'enum_unique_enforce.py', ignore_error=True, 
..                    line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 enum_unique_enforce.py
	
	Traceback (most recent call last):
	  File "enum_unique_enforce.py", line 11, in <module>
	    class BugStatus(enum.Enum):
	  File ".../lib/python3.5/enum.py", line 573, in unique
	    (enumeration, alias_details))
	ValueError: duplicate values found in <enum 'BugStatus'>:
	by_design -> wont_fix, closed -> fix_released

.. {{{end}}}

Creating Enumerations Programmatically
======================================

There are cases when it is more convenient to create enumerations
programmatically, rather than hard-coding them in a class
definition. For those situations, :class:`Enum` also supports passing
the member names and values to the class constructor.

.. literalinclude:: enum_programmatic_create.py
   :caption:
   :start-after: #end_pymotw_header

The ``value`` argument is the name of the enumeration, used to build
the representation of members. The ``names`` argument lists the
members of the enumeration. When a single string is passed, it is
split on whitespace and commas and the resulting tokens are used as
names for the members, which are automatically assigned values
starting with ``1``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'enum_programmatic_create.py'))
.. }}}

.. code-block:: none

	$ python3 enum_programmatic_create.py
	
	Member: BugStatus.new
	
	All members:
	fix_released    = 1
	fix_committed   = 2
	in_progress     = 3
	wont_fix        = 4
	invalid         = 5
	incomplete      = 6
	new             = 7

.. {{{end}}}

For more control over the values associated with members, the
``names`` string can be replaced with a sequence of two-part tuples or
a dictionary mapping names to values.

.. literalinclude:: enum_programmatic_mapping.py
   :caption:
   :start-after: #end_pymotw_header

In this example a list of two-part tuples is given instead of a single
string containing only the member names. This makes it possible to
reconstruct the ``BugStatus`` enumeration with the members in the same
order as the version defined in ``enum_create.py``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'enum_programmatic_mapping.py'))
.. }}}

.. code-block:: none

	$ python3 enum_programmatic_mapping.py
	
	All members:
	new             = 7
	incomplete      = 6
	invalid         = 5
	wont_fix        = 4
	in_progress     = 3
	fix_committed   = 2
	fix_released    = 1

.. {{{end}}}

Non-integer Member Values
=========================

Enum member values are not restricted to integers. Any type of object
can be associated with a member. If the value is a tuple, the members
are passed as individual arguments to :func:`__init__`.

.. literalinclude:: enum_tuple_values.py
   :caption:
   :start-after: #end_pymotw_header

In this example, each member value is a tuple containing the numerical
id (such as might be stored in a database) and a list of valid
transitions away from the current state.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'enum_tuple_values.py'))
.. }}}

.. code-block:: none

	$ python3 enum_tuple_values.py
	
	Name: BugStatus.in_progress
	Value: (3, ['new', 'fix_committed'])
	Custom attribute: ['new', 'fix_committed']
	Using attribute: True

.. {{{end}}}

For more complex cases, tuples might become unwieldy. Since member
values can be any type of object, it is possible to use dictionaries
for cases where there are a lot of separate attributes to track for
each enum value. Complex values are passed directly to
:func:`__init__` as the only argument other than ``self``.

.. literalinclude:: enum_complex_values.py
   :caption:
   :start-after: #end_pymotw_header

This example expresses the same data as the previous example, using
dictionaries rather than tuples.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'enum_complex_values.py'))
.. }}}

.. code-block:: none

	$ python3 enum_complex_values.py
	
	Name: BugStatus.in_progress
	Value: {'transitions': ['new', 'fix_committed'], 'num': 3}
	Custom attribute: ['new', 'fix_committed']
	Using attribute: True

.. {{{end}}}

.. seealso::

   * :pydoc:`enum`

   * :pep:`435` -- Adding an Enum type to the Python standard library

   * `flufl.enum <http://pythonhosted.org/flufl.enum/>`_ -- The
     original inspiration for ``enum``, by Barry Warsaw.

