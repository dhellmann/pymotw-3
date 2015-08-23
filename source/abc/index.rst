==============================
 abc -- Abstract Base Classes
==============================

.. spelling::

   Subclassing
   subclassing

.. module:: abc
   :synopsis: Abstract Base Classes

:Purpose: Define and use abstract base classes for interface verification.

Why use Abstract Base Classes?
==============================

Abstract base classes are a form of interface checking more strict
than individual :func:`hasattr` checks for particular methods.  By
defining an abstract base class, a common API can be established for a
set of subclasses.  This capability is especially useful in situations
where someone less familiar with the source for an application is
going to provide plug-in extensions, but can also help when working on
a large team or with a large code-base where keeping track of all of
the classes at the same time is difficult or not possible.

How ABCs Work
=============

:mod:`abc` works by marking methods of the base class as abstract, and
then registering concrete classes as implementations of the abstract
base.  If an application or library requires a particular API,
:func:`issubclass` or :func:`isinstance` can be used to check an
object against the abstract class.

To start, define an abstract base class to represent the API of a set
of plug-ins for saving and loading data.  Set the meta-class for the
new base class to :class:`ABCMeta`, and using decorators to establish
the public API for the class.  The following examples use
``abc_base.py``, which contains:

.. include:: abc_base.py
    :literal:
    :start-after: #end_pymotw_header


Registering a Concrete Class
============================

There are two ways to indicate that a concrete class implements an
abstract API: either explicitly register the class or create a new
subclass directly from the abstract base.  Use the :func:`register`
class method as a decorator on a concrete class to add it explicitly
when the class provides the required API, but is not part of the
inheritance tree of the abstract base class.

.. include:: abc_register.py
    :literal:
    :start-after: #end_pymotw_header

In this example the :class:`RegisteredImplementation` is derived from
:class:`LocalBaseClass`, but is registered as implementing the
:class:`PluginBase` API so :func:`issubclass` and :func:`isinstance`
treat it as though it is derived from :class:`PluginBase`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_register.py'))
.. }}}

::

	$ python3 abc_register.py
	
	Subclass: True
	Instance: True

.. {{{end}}}


Implementation Through Subclassing
==================================

Subclassing directly from the base avoids the need to register the
class explicitly.

.. include:: abc_subclass.py
    :literal:
    :start-after: #end_pymotw_header

In this case, normal Python class management features are used to
recognize :class:`PluginImplementation` as implementing the abstract
:class:`PluginBase`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_subclass.py'))
.. }}}

::

	$ python3 abc_subclass.py
	
	Subclass: True
	Instance: True

.. {{{end}}}

A side effect of using direct subclassing is it is possible to find
all of the implementations of a plug-in by asking the base class for
the list of known classes derived from it (this is not an :mod:`abc`
feature, all classes can do this).

.. include:: abc_find_subclasses.py
    :literal:
    :start-after: #end_pymotw_header

Even though :func:`abc_register` is imported,
:class:`RegisteredImplementation` is not among the list of subclasses
because it is not actually derived from the base.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_find_subclasses.py'))
.. }}}

::

	$ python3 abc_find_subclasses.py
	
	SubclassImplementation

.. {{{end}}}

Helper Base Class
=================

Forgetting to set the meta-class properly means the concrete
implementations do not have their APIs enforced. To make it easier to
set up the abstract class properly, a base class is provided that sets
the meta-class.

.. include:: abc_abc_base.py
   :literal:
   :start-after: #end_pymotw_header

To create a new abstract class, simply inherit from :class:`ABC`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_abc_base.py'))
.. }}}

::

	$ python3 abc_abc_base.py
	
	Subclass: True
	Instance: True

.. {{{end}}}

Incomplete Implementations
==========================

Another benefit of subclassing directly from the abstract base class
is that the subclass cannot be instantiated unless it fully implements
the abstract portion of the API.

.. include:: abc_incomplete.py
    :literal:
    :start-after: #end_pymotw_header

This keeps incomplete implementations from triggering unexpected
errors at runtime.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_incomplete.py', ignore_error=True, 
..                    break_lines_at=65, line_break_mode='wrap'))
.. }}}

::

	$ python3 abc_incomplete.py
	
	Subclass: True
	Traceback (most recent call last):
	  File "abc_incomplete.py", line 24, in <module>
	    print('Instance:', isinstance(IncompleteImplementation(),
	TypeError: Can't instantiate abstract class
	IncompleteImplementation with abstract methods load

.. {{{end}}}


Concrete Methods in ABCs
========================

Although a concrete class must provide implementations of all abstract
methods, the abstract base class can also provide implementations that
can be invoked via :func:`super`.  This allows common logic to be
reused by placing it in the base class, but forces subclasses to
provide an overriding method with (potentially) custom logic.

.. include:: abc_concrete_method.py
    :literal:
    :start-after: #end_pymotw_header

Since :func:`ABCWithConcreteImplementation` is an abstract base class,
it is not possible to instantiate it to use it directly.  Subclasses
*must* provide an override for :func:`retrieve_values`, and in this
case the concrete class sorts the data before returning it.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_concrete_method.py'))
.. }}}

::

	$ python3 abc_concrete_method.py
	
	base class reading data
	subclass sorting data
	['line one', 'line three', 'line two']
	

.. {{{end}}}

.. _abc-abstract-properties:

Abstract Properties
===================

If an API specification includes attributes in addition to methods, it
can require the attributes in concrete classes by combining
:func:`abstractmethod` with :func:`property`.

.. include:: abc_abstractproperty.py
    :literal:
    :start-after: #end_pymotw_header

The :class:`Base` class in the example cannot be instantiated because
it has only an abstract version of the property getter methods for
``value`` and ``constant``.  The ``value`` property is given a
concrete getter in :class:`Implementation` and ``constant`` is defined
using a class attribute.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_abstractproperty.py', 
..                    break_lines_at=65, line_break_mode='wrap'))
.. }}}

::

	$ python3 abc_abstractproperty.py
	
	ERROR: Can't instantiate abstract class Base with abstract
	methods constant, value
	Implementation.value   : concrete property
	Implementation.constant: set by a class attribute

.. {{{end}}}

Abstract read-write properties can also be defined.

.. include:: abc_abstractproperty_rw.py
    :literal:
    :start-after: #end_pymotw_header

The concrete property must be defined the same way as the abstract
property.  Overriding a read-write property in
:class:`PartialImplementation` with one that is read-only leaves the
property read-only.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_abstractproperty_rw.py', 
..                    break_lines_at=65, line_break_mode='wrap'))
.. }}}

::

	$ python3 abc_abstractproperty_rw.py
	
	ERROR: Can't instantiate abstract class Base with abstract
	methods value
	PartialImplementation.value: Read-only
	ERROR: can't set attribute
	Implementation.value: Default value
	Changed value: New value

.. {{{end}}}

To use the decorator syntax with read-write abstract properties,
the methods to get and set the value must be named the same.

Abstract Class and Static Methods
=================================

Class and static methods can also be marked as abstract.

.. include:: abc_class_static.py
   :literal:
   :start-after: #end_pymotw_header

Although the class method is invoked on the class rather than an
instance, it still prevents the class from being instantiated if it is
not defined.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_class_static.py'))
.. }}}

::

	$ python3 abc_class_static.py
	
	ERROR: Can't instantiate abstract class Base with abstract metho
	ds const_behavior, factory
	Implementation.const_behavior : Static behavior differs

.. {{{end}}}

.. seealso::

    * :pydoc:`abc`

    * :pep:`3119` -- Introducing Abstract Base Classes

    * :mod:`collections` -- The collections module includes abstract
      base classes for several collection types.

    * :pep:`3141` -- A Type Hierarchy for Numbers

    * `Wikipedia: Strategy Pattern
      <http://en.wikipedia.org/wiki/Strategy_pattern>`_ -- Description
      and examples of the strategy pattern, a common plug-in
      implementation pattern.

    * `Dynamic Code Patterns: Extending Your Applications With Plugins
      <http://pyvideo.org/video/1789/dynamic-code-patterns-extending-your-application>`__
      -- PyCon 2013 presentation by Doug Hellmann

    * :ref:`Porting notes for abc <porting-abc>`

..  This video appears to have been deleted, and the old PyCon 2009
    site appears to be gone.
    * `Plugins and monkeypatching
      <http://us.pycon.org/2009/conference/schedule/event/47/>`_ --
      PyCon 2009 presentation by Dr. André Roberge
