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


.. create
.. access names and values
.. iterating over
.. comparison
.. unique values
.. functional API for creating
.. integer enums
.. non-integer values of enum members (tuple, such as planet example, or fancier)


.. seealso::

   * :pydoc:`enum`
