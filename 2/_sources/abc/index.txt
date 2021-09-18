============================
abc -- Abstract Base Classes
============================

.. module:: abc
    :synopsis: Abstract Base Classes

:Purpose: Define and use abstract base classes for API checks in your code.
:Available In: 2.6

Why use Abstract Base Classes?
==============================

Abstract base classes are a form of interface checking more strict
than individual ``hasattr()`` checks for particular methods.  By
defining an abstract base class, you can define a common API for a set
of subclasses.  This capability is especially useful in situations
where a third-party is going to provide implementations, such as with
plugins to an application, but can also aid you when working on a
large team or with a large code-base where keeping all classes in your
head at the same time is difficult or not possible.

How ABCs Work
=============

:mod:`abc` works by marking methods of the base class as abstract, and
then registering concrete classes as implementations of the abstract
base.  If your code requires a particular API, you can use
``issubclass()`` or ``isinstance()`` to check an object against the
abstract class.

Let's start by defining an abstract base class to represent the API of
a set of plugins for saving and loading data.

.. include:: abc_base.py
    :literal:
    :start-after: #end_pymotw_header


Registering a Concrete Class
============================

There are two ways to indicate that a concrete class implements an
abstract: register the class with the abc or subclass directly from
the abc.

.. include:: abc_register.py
    :literal:
    :start-after: #end_pymotw_header

In this example the ``PluginImplementation`` is not derived from
``PluginBase``, but is registered as implementing the ``PluginBase``
API.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_register.py'))
.. }}}

::

	$ python abc_register.py
	
	Subclass: True
	Instance: True

.. {{{end}}}

Implementation Through Subclassing
==================================

By subclassing directly from the base, we can avoid the need to
register the class explicitly.

.. include:: abc_subclass.py
    :literal:
    :start-after: #end_pymotw_header

In this case the normal Python class management is used to recognize
``PluginImplementation`` as implementing the abstract ``PluginBase``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_subclass.py'))
.. }}}

::

	$ python abc_subclass.py
	
	Subclass: True
	Instance: True

.. {{{end}}}

A side-effect of using direct subclassing is it is possible to find
all of the implementations of your plugin by asking the base class for
the list of known classes derived from it (this is not an abc feature,
all classes can do this).

.. include:: abc_find_subclasses.py
    :literal:
    :start-after: #end_pymotw_header

Notice that even though ``abc_register`` is imported,
``RegisteredImplementation`` is not among the list of subclasses
because it is not actually derived from the base.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_find_subclasses.py'))
.. }}}

::

	$ python abc_find_subclasses.py
	
	SubclassImplementation

.. {{{end}}}

Dr. André Roberge `has described
<http://us.pycon.org/2009/conference/schedule/event/47/>`_ using this
capability to discover plugins by importing all of the modules in a
directory dynamically and then looking at the subclass list to find
the implementation classes.

Incomplete Implementations
--------------------------

Another benefit of subclassing directly from your abstract base class
is that the subclass cannot be instantiated unless it fully implements
the abstract portion of the API.  This can keep half-baked
implementations from triggering unexpected errors at runtime.

.. include:: abc_incomplete.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_incomplete.py', ignore_error=True))
.. }}}

::

	$ python abc_incomplete.py
	
	Subclass: True
	Instance:
	Traceback (most recent call last):
	  File "abc_incomplete.py", line 22, in <module>
	    print 'Instance:', isinstance(IncompleteImplementation(), PluginBase)
	TypeError: Can't instantiate abstract class IncompleteImplementation with abstract methods load

.. {{{end}}}


Concrete Methods in ABCs
========================

Although a concrete class must provide an implementation of an
abstract methods, the abstract base class can also provide an
implementation that can be invoked via ``super()``.  This lets you
re-use common logic by placing it in the base class, but force
subclasses to provide an overriding method with (potentially) custom
logic.

.. include:: abc_concrete_method.py
    :literal:
    :start-after: #end_pymotw_header

Since ``ABCWithConcreteImplementation`` is an abstract base class, it
isn't possible to instantiate it to use it directly.  Subclasses
*must* provide an override for ``retrieve_values()``, and in this case
the concrete class massages the data before returning it at all.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_concrete_method.py'))
.. }}}

::

	$ python abc_concrete_method.py
	
	base class reading data
	subclass sorting data
	['line one', 'line three', 'line two']
	

.. {{{end}}}

.. _abc-abstract-properties:

Abstract Properties
===================

If your API specification includes attributes in addition to methods,
you can require the attributes in concrete classes by defining them
with ``@abstractproperty``.

.. include:: abc_abstractproperty.py
    :literal:
    :start-after: #end_pymotw_header

The ``Base`` class in the example cannot be instantiated because it
has only an abstract version of the property getter method.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_abstractproperty.py'))
.. }}}

::

	$ python abc_abstractproperty.py
	
	ERROR: Can't instantiate abstract class Base with abstract methods value
	Implementation.value: concrete property

.. {{{end}}}

You can also define abstract read/write properties.

.. include:: abc_abstractproperty_rw.py
    :literal:
    :start-after: #end_pymotw_header

Notice that the concrete property must be defined the same way as the
abstract property.  Trying to override a read/write property in
``PartialImplementation`` with one that is read-only does not work.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_abstractproperty_rw.py'))
.. }}}

::

	$ python abc_abstractproperty_rw.py
	
	ERROR: Can't instantiate abstract class Base with abstract methods value
	ERROR: Can't instantiate abstract class PartialImplementation with abstract methods value
	Implementation.value: Default value
	Changed value: New value

.. {{{end}}}

To use the decorator syntax does with read/write abstract properties,
the methods to get and set the value should be named the same.

.. include:: abc_abstractproperty_rw_deco.py
    :literal:
    :start-after: #end_pymotw_header

Notice that both methods in the ``Base`` and ``Implementation``
classes are named ``value()``, although they have different
signatures.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_abstractproperty_rw_deco.py'))
.. }}}

::

	$ python abc_abstractproperty_rw_deco.py
	
	Implementation.value: Default value
	Changed value: New value

.. {{{end}}}

.. _abc-collection-types:

Collection Types
================

The :mod:`collections` module defines several abstract base classes
related to container (and containable) types.

General container classes:

- Container
- Sized

Iterator and Sequence classes:

- Iterable
- Iterator
- Sequence
- MutableSequence

Unique values:

- Hashable
- Set
- MutableSet

Mappings:

- Mapping
- MutableMapping
- MappingView
- KeysView
- ItemsView
- ValuesView

Miscelaneous:

- Callable

In addition to serving as detailed real-world examples of abstract
base classes, Python's built-in types are automatically registered to
these classes when you import :mod:`collections`. This means you can
safely use ``isinstance()`` to check parameters in your code to ensure
that they support the API you need.  The base classes can also be used
to define your own collection types, since many of them provide
concrete implementations of the internals and only need a few methods
overridden.  Refer to the standard library docs for collections for
more details.

.. seealso::

    `abc <http://docs.python.org/2.7/library/abc.html>`_
        The standard library documentation for this module.

    :pep:`3119`
        Introducing Abstract Base Classes
    
    :mod:`collections`
        The collections module includes abstract base classes for several collection types.

    `collections <http://docs.python.org/2.7/library/collections.html>`_
        The standard library documentation for collections.

    :pep:`3141`
        A Type Hierarchy for Numbers

    `Wikipedia: Strategy Pattern <http://en.wikipedia.org/wiki/Strategy_pattern>`_
        Description and examples of the strategy pattern.

    `Plugins and monkeypatching <http://us.pycon.org/2009/conference/schedule/event/47/>`_
        PyCon 2009 presentation by Dr. André Roberge
