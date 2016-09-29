==============================
 heapq -- Heap Sort Algorithm
==============================

.. module:: heapq
    :synopsis: In-place heap sort algorithm

:Purpose:
    The heapq implements a min-heap sort algorithm suitable for use with
    Python's lists.

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

Example Data
============

The examples in this section use the data in ``heapq_heapdata.py``.

.. literalinclude:: heapq_heapdata.py
   :caption:
   :start-after: #end_pymotw_header

The heap output is printed using ``heapq_showtree.py``:

.. literalinclude:: heapq_showtree.py
   :caption:
   :start-after: #end_pymotw_header

Creating a Heap
===============

There are two basic ways to create a heap, :func:`heappush` and
:func:`heapify`.

.. literalinclude:: heapq_heappush.py
   :caption:
   :start-after: #end_pymotw_header

Using :func:`heappush`, the heap sort order of the elements is
maintained as new items are added from a data source.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'heapq_heappush.py'))
.. }}}

.. code-block:: none

	$ python3 heapq_heappush.py
	
	random : [19, 9, 4, 10, 11]
	
	add  19:
	
	                 19                 
	------------------------------------
	
	add   9:
	
	                 9                  
	        19        
	------------------------------------
	
	add   4:
	
	                 4                  
	        19                9         
	------------------------------------
	
	add  10:
	
	                 4                  
	        10                9         
	    19   
	------------------------------------
	
	add  11:
	
	                 4                  
	        10                9         
	    19       11   
	------------------------------------
	

.. {{{end}}}

If the data is already in memory, it is more efficient to use
:func:`heapify` to rearrange the items of the list in place.

.. literalinclude:: heapq_heapify.py
   :caption:
   :start-after: #end_pymotw_header

The result of building a list in heap order one item at a time is the
same as building it unordered and then calling :func:`heapify`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'heapq_heapify.py'))
.. }}}

.. code-block:: none

	$ python3 heapq_heapify.py
	
	random    : [19, 9, 4, 10, 11]
	heapified :
	
	                 4                  
	        9                 19        
	    10       11   
	------------------------------------
	

.. {{{end}}}


Accessing Contents of a Heap
============================

Once the heap is organized correctly, use :func:`heappop` to remove the
element with the lowest value. 

.. literalinclude:: heapq_heappop.py
   :caption:
   :start-after: #end_pymotw_header

In this example, adapted from the stdlib documentation,
:func:`heapify` and :func:`heappop` are used to sort a list of
numbers.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'heapq_heappop.py'))
.. }}}

.. code-block:: none

	$ python3 heapq_heappop.py
	
	random    : [19, 9, 4, 10, 11]
	heapified :
	
	                 4                  
	        9                 19        
	    10       11   
	------------------------------------
	
	pop      4:
	
	                 9                  
	        10                19        
	    11   
	------------------------------------
	
	pop      9:
	
	                 10                 
	        11                19        
	------------------------------------
	

.. {{{end}}}

To remove existing elements and replace them with new values in a
single operation, use :func:`heapreplace`.

.. literalinclude:: heapq_heapreplace.py
   :caption:
   :start-after: #end_pymotw_header

Replacing elements in place makes it possible to maintain a fixed size
heap, such as a queue of jobs ordered by priority.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'heapq_heapreplace.py'))
.. }}}

.. code-block:: none

	$ python3 heapq_heapreplace.py
	
	start:
	
	                 4                  
	        9                 19        
	    10       11   
	------------------------------------
	
	replace  4 with  0:
	
	                 0                  
	        9                 19        
	    10       11   
	------------------------------------
	
	replace  0 with 13:
	
	                 9                  
	        10                19        
	    13       11   
	------------------------------------
	

.. {{{end}}}

Data Extremes From a Heap
=========================

:mod:`heapq` also includes two functions to examine an iterable to find
a range of the largest or smallest values it contains. 

.. literalinclude:: heapq_extremes.py
   :caption:
   :start-after: #end_pymotw_header

Using :func:`nlargest` and :func:`nsmallest` are only efficient for
relatively small values of n > 1, but can still come in handy in a few
cases.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'heapq_extremes.py'))
.. }}}

.. code-block:: none

	$ python3 heapq_extremes.py
	
	all       : [19, 9, 4, 10, 11]
	3 largest : [19, 11, 10]
	from sort : [19, 11, 10]
	3 smallest: [4, 9, 10]
	from sort : [4, 9, 10]

.. {{{end}}}

Efficiently Merging Sorted Sequences
====================================

Combining several sorted sequences into one new sequence is easy for
small data sets.

.. code-block:: python

   list(sorted(itertools.chain(*data)))

For larger data sets, this technique can use a considerable amount of
memory. Instead of sorting the entire combined sequence, :func:`merge`
uses a heap to generate a new sequence one item at a time, and
determine the next item using a fixed amount of memory.

.. literalinclude:: heapq_merge.py
   :caption:
   :start-after: #end_pymotw_header

Because the implementation of :func:`merge` uses a heap, it consumes
memory based on the number of sequences being merged, rather than the
number of items in those sequences.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'heapq_merge.py'))
.. }}}

.. code-block:: none

	$ python3 heapq_merge.py
	
	0: [33, 58, 71, 88, 95]
	1: [10, 11, 17, 38, 91]
	2: [13, 18, 39, 61, 63]
	3: [20, 27, 31, 42, 45]
	
	Merged:
	10 11 13 17 18 20 27 31 33 38 39 42 45 58 61 63 71 88 91 95 

.. {{{end}}}

.. seealso::

   * :pydoc:`heapq`

   * `WikiPedia: Heap (data structure)
     <https://en.wikipedia.org/wiki/Heap_(data_structure)>`__ -- A
     general description of heap data structures.

   * :ref:`Queue-PriorityQueue` -- A priority queue implementation
     from :mod:`Queue` in the standard library.
