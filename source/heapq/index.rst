==============================
 heapq -- Heap Sort Algorithm
==============================

.. module:: heapq
    :synopsis: In-place heap sort algorithm

:Purpose:
    The heapq implements a min-heap sort algorithm suitable for use with
    Python's lists.
:Python Version: New in 2.3 with additions in 2.5

A *heap* is a tree-like data structure where the child nodes have a
sort-order relationship with the parents. *Binary heaps* can be
represented using a list or array organized so that the children of
element N are at positions 2*N+1 and 2*N+2 (for zero-based
indexes). This layout makes it possible to rearrange heaps in place,
so it is not necessary to reallocate as much memory when adding or
removing items.

A max-heap ensures that the parent is larger than or equal to both of
its children. A min-heap requires that the parent be less than or
equal to its children. Python's :mod:`heapq` module implements a
min-heap.

.. toctree::

   normal

.. only:: bonus

   .. toctree::

      bonus

.. seealso::

    `heapq <http://docs.python.org/library/heapq.html>`_
        The standard library documentation for this module.

    `WikiPedia: Heap (data structure) <http://en.wikipedia.org/wiki/Heap_(data_structure)>`_
        A general description of heap data structures.

    :ref:`Queue-PriorityQueue`
        A priority queue implementation from :mod:`Queue` in the
        standard library.
