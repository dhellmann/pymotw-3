.. _collections-namedtuple:

============
 namedtuple
============

The standard :class:`tuple` uses numerical indexes to access its
members.

.. include:: collections_tuple.py
   :literal:
   :start-after: #end_pymotw_header

This makes :class:`tuples` convenient containers for simple uses.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'collections_tuple.py'))
.. }}}

::

	$ python collections_tuple.py

	Representation: ('Bob', 30, 'male')
	
	Field by index: Jane
	
	Fields by index:
	Bob is a 30 year old male
	Jane is a 29 year old female

.. {{{end}}}

On the other hand, remembering which index should be used for each
value can lead to errors, especially if the :class:`tuple` has a lot
of fields and is constructed far from where it is used.  A
:class:`namedtuple` assigns names, as well as the numerical index, to
each member.

Defining
========

:class:`namedtuple` instances are just as memory efficient as regular
tuples because they do not have per-instance dictionaries.  Each kind
of :class:`namedtuple` is represented by its own class, created by
using the :func:`namedtuple` factory function.  The arguments are the
name of the new class and a string containing the names of the
elements.

.. include:: collections_namedtuple_person.py
    :literal:
    :start-after: #end_pymotw_header

As the example illustrates, it is possible to access the fields of the
:class:`namedtuple` by name using dotted notation (``obj.attr``) as
well as using the positional indexes of standard tuples.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'collections_namedtuple_person.py'))
.. }}}

::

	$ python collections_namedtuple_person.py

	Type of Person: <type 'type'>
	
	Representation: Person(name='Bob', age=30, gender='male')
	
	Field by name: Jane
	
	Fields by index:
	Bob is a 30 year old male
	Jane is a 29 year old female

.. {{{end}}}

Invalid Field Names
===================

Field names are invalid if they are repeated or conflict with Python
keywords.

.. include:: collections_namedtuple_bad_fields.py
   :literal:
   :start-after: #end_pymotw_header

As the field names are parsed, invalid values cause
:class:`ValueError` exceptions.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'collections_namedtuple_bad_fields.py'))
.. }}}

::

	$ python collections_namedtuple_bad_fields.py

	Type names and field names cannot be a keyword: 'class'
	Encountered duplicate field name: 'age'

.. {{{end}}}

In situations where a :class:`namedtuple` is being created based on
values outside of the control of the program (such as to represent
the rows returned by a database query, where the schema is not known
in advance), set the *rename* option to ``True`` so the invalid fields
are renamed.

.. include:: collections_namedtuple_rename.py
   :literal:
   :start-after: #end_pymotw_header

The new names for renamed fields depend on their index in the tuple,
so the field with name ``class`` becomes ``_1`` and the duplicate
``age`` field is changed to ``_3``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'collections_namedtuple_rename.py'))
.. }}}

::

	$ python collections_namedtuple_rename.py

	('name', '_1', 'age', 'gender')
	('name', 'age', 'gender', '_3')

.. {{{end}}}
