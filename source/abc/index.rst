===============================
 abc --- Abstract Base Classes
===============================

.. module:: abc
   :synopsis: Abstract Base Classes

:Purpose: Define and use abstract base classes for interface verification.

Why use Abstract Base Classes?
==============================

Abstract base classes are a form of interface checking more strict
than individual ``hasattr()`` checks for particular methods.  By
defining an abstract base class, a common API can be established for a
set of subclasses.  This capability is especially useful in situations
where someone less familiar with the source for an application is
going to provide plug-in extensions, but can also help when working on
a large team or with a large code-base where keeping track of all of
the classes at the same time is difficult or not possible.

How ABCs Work
=============

``abc`` works by marking methods of the base class as abstract, and
then registering concrete classes as implementations of the abstract
base.  If an application or library requires a particular API,
``issubclass()`` or ``isinstance()`` can be used to check an
object against the abstract class.

To start, define an abstract base class to represent the API of a set
of plug-ins for saving and loading data.  Set the metaclass for the
new base class to ``ABCMeta``, and use decorators to establish
the public API for the class.  The following examples use
``abc_base.py``, which contains:

.. literalinclude:: abc_base.py
    :caption:
    :start-after: #end_pymotw_header


Registering a Concrete Class
============================

There are two ways to indicate that a concrete class implements an
abstract API: either explicitly register the class or create a new
subclass directly from the abstract base.  Use the ``register()``
class method as a decorator on a concrete class to add it explicitly
when the class provides the required API, but is not part of the
inheritance tree of the abstract base class.

.. literalinclude:: abc_register.py
    :caption:
    :start-after: #end_pymotw_header

In this example the ``RegisteredImplementation`` is derived from
``LocalBaseClass``, but is registered as implementing the
``PluginBase`` API so ``issubclass()`` and ``isinstance()``
treat it as though it is derived from ``PluginBase``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_register.py'))
.. }}}

.. code-block:: none

	$ python3 abc_register.py
	
	Subclass: True
	Instance: True

.. {{{end}}}


Implementation Through Subclassing
==================================

Subclassing directly from the base avoids the need to register the
class explicitly.

.. literalinclude:: abc_subclass.py
    :caption:
    :start-after: #end_pymotw_header

In this case, normal Python class management features are used to
recognize ``SubclassImplementation`` as implementing the abstract
``PluginBase``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_subclass.py'))
.. }}}

.. code-block:: none

	$ python3 abc_subclass.py
	
	Subclass: True
	Instance: True

.. {{{end}}}

A side effect of using direct subclassing is it is possible to find
all of the implementations of a plug-in by asking the base class for
the list of known classes derived from it (this is not an ``abc``
feature, all classes can do this).

.. literalinclude:: abc_find_subclasses.py
    :caption:
    :start-after: #end_pymotw_header

Even though ``abc_register()`` is imported,
``RegisteredImplementation`` is not among the list of subclasses
because it is not actually derived from the base.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_find_subclasses.py'))
.. }}}

.. code-block:: none

	$ python3 abc_find_subclasses.py
	
	SubclassImplementation

.. {{{end}}}

Helper Base Class
=================

Forgetting to set the metaclass properly means the concrete
implementations do not have their APIs enforced. To make it easier to
set up the abstract class properly, a base class is provided that sets
the metaclass automatically.

.. literalinclude:: abc_abc_base.py
   :caption:
   :start-after: #end_pymotw_header

To create a new abstract class, simply inherit from ``ABC``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_abc_base.py'))
.. }}}

.. code-block:: none

	$ python3 abc_abc_base.py
	
	Subclass: True
	Instance: True

.. {{{end}}}

Incomplete Implementations
==========================

Another benefit of subclassing directly from the abstract base class
is that the subclass cannot be instantiated unless it fully implements
the abstract portion of the API.

.. literalinclude:: abc_incomplete.py
    :caption:
    :start-after: #end_pymotw_header

This keeps incomplete implementations from triggering unexpected
errors at runtime.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_incomplete.py', ignore_error=True, 
..                    break_lines_at=65, line_break_mode='wrap'))
.. }}}

.. code-block:: none

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
can be invoked via ``super()``.  This allows common logic to be
reused by placing it in the base class, but forces subclasses to
provide an overriding method with (potentially) custom logic.

.. literalinclude:: abc_concrete_method.py
    :caption:
    :start-after: #end_pymotw_header

Since ``ABCWithConcreteImplementation()`` is an abstract base class,
it is not possible to instantiate it to use it directly.  Subclasses
*must* provide an override for ``retrieve_values()``, and in this
case the concrete class sorts the data before returning it.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_concrete_method.py'))
.. }}}

.. code-block:: none

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
``abstractmethod()`` with ``property()``.

.. literalinclude:: abc_abstractproperty.py
    :caption:
    :start-after: #end_pymotw_header

The ``Base`` class in the example cannot be instantiated because
it has only an abstract version of the property getter methods for
``value`` and ``constant``.  The ``value`` property is given a
concrete getter in ``Implementation`` and ``constant`` is defined
using a class attribute.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_abstractproperty.py', 
..                    break_lines_at=65, line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 abc_abstractproperty.py
	
	ERROR: Can't instantiate abstract class Base with abstract
	methods constant, value
	Implementation.value   : concrete property
	Implementation.constant: set by a class attribute

.. {{{end}}}

Abstract read-write properties can also be defined.

.. literalinclude:: abc_abstractproperty_rw.py
    :caption:
    :start-after: #end_pymotw_header

The concrete property must be defined the same way as the abstract
property, as either read-write or read-only.  Overriding a read-write
property in ``PartialImplementation`` with one that is read-only
leaves the property read-only -- the property's setter method from the
base class is not reused.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_abstractproperty_rw.py', 
..                    break_lines_at=65, line_break_mode='wrap'))
.. }}}

.. code-block:: none

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

.. literalinclude:: abc_class_static.py
   :caption:
   :start-after: #end_pymotw_header

Although the class method is invoked on the class rather than an
instance, it still prevents the class from being instantiated if it is
not defined.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'abc_class_static.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 abc_class_static.py
	
	ERROR: Can't instantiate abstract class Base with abstract
	methods const_behavior, factory
	Implementation.const_behavior : Static behavior differs

.. {{{end}}}

.. seealso::

    * :pydoc:`abc`

    * :pep:`3119` -- Introducing Abstract Base Classes

    * :mod:`collections` -- The collections module includes abstract
      base classes for several collection types.

    * :pep:`3141` -- A Type Hierarchy for Numbers

    * `Wikipedia: Strategy Pattern
      <https://en.wikipedia.org/wiki/Strategy_pattern>`_ -- Description
      and examples of the strategy pattern, a common plug-in
      implementation pattern.

    * `Dynamic Code Patterns: Extending Your Applications With Plugins
      <http://pyvideo.org/pycon-us-2013/dynamic-code-patterns-extending-your-application.html>`__
      -- PyCon 2013 presentation by Doug Hellmann

    * :ref:`Python 2 to 3 porting notes for abc <porting-abc>`

..  This video appears to have been deleted, and the old PyCon 2009
    site appears to be gone.
    * `Plugins and monkeypatching
      <http://us.pycon.org/2009/conference/schedule/event/47/>`_ --
      PyCon 2009 presentation by Dr. André Roberge
