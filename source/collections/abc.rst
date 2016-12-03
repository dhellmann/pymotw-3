==========================================================
 collections.abc --- abstract base classes for containers
==========================================================

.. module:: collections.abc
    :synopsis: Abstract base classes for container data types.

:Purpose: Abstract base classes for container data types.

The :mod:`collections.abc` module contains abstract base classes that
define the APIs for container data structures built into Python and
provided by the ``collections`` module.

.. list-table:: Abstract Base Classes
   :header-rows: 1
   :widths: 20 20 60

   - * Class
     * Base class(es)
     * API Purpose
   - * Container
     * 
     * Basic container features, such as the ``in`` operator.
   - * Hashable
     * 
     * Adds support for providing a hash value for the container instance.
   - * Iterable
     * 
     * Can create an iterator over the container contents.
   - * Iterator
     * Iterable
     * Is an iterator over the container contents.
   - * Sized
     * 
     * Adds methods for containers that know how big they are.
   - * Callable
     * 
     * For containers that can be invoked as a function.
   - * Sequence
     * Sized, Iterable, Container
     * Supports retrieving individual items, iterating, and changing
       the order of items.
   - * MutableSequence
     * Sequence
     * Supports adding and removing items to an instance after it has
       been created.
   - * Set
     * Sized, Iterable, Container
     * Supports set operations such as intersection and union.
   - * MutableSet
     * Set
     * Adds methods for manipulating the set contents after it is created.
   - * Mapping
     * Sized, Iterable, Container
     * Defines the read-only API used by :class:`dict`.
   - * MutableMapping
     * Mapping
     * Defines the methods for manipulating the contents of a mapping after it is created.
   - * MappingView
     * Sized
     * Defines the view API for accessing a mapping from an iterator.
   - * ItemsView
     * MappingView, Set
     * Part of the view API.
   - * KeysView
     * MappingView, Set
     * Part of the view API.
   - * ValuesView
     * MappingView
     * Part of the view API.

Besides clearly defining the APIs for containers with different
semantics, these abstract base classes can be used to test whether an
object supports an API before invoking it using
:func:`isinstance`. Some of the classes also provide implementations
of methods, and they can be used as mix-ins to build up custom
container types without implementing every method from scratch.
