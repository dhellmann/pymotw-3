=====================================
heapq -- In-place heap sort algorithm
=====================================

.. module:: heapq
    :synopsis: In-place heap sort algorithm

:Purpose:
    The heapq implements a min-heap sort algorithm suitable for use with
    Python's lists.
:Available In: New in 2.3 with additions in 2.5

A *heap* is a tree-like data structure where the child nodes have a
sort-order relationship with the parents. *Binary heaps* can be
represented using a list or array organized so that the children of
element N are at positions 2*N+1 and 2*N+2 (for zero-based
indexes). This layout makes it possible to rearrange heaps in place,
so it is not necessary to reallocate as much memory when adding or
removing items.

A max-heap ensures that the parent is larger than or equal to both of
its children. A min-heap requires that the parent be less than or
equal to its children. Python's heapq module implements a min-heap.

Example Data
============

The examples below use this sample data:

.. include:: heapq_heapdata.py
    :literal:
    :start-after: #end_pymotw_header

The heap output is printed using ``heapq_showtree.py``:

.. include:: heapq_showtree.py
   :literal:
   :start-after: #end_pymotw_header



Creating a Heap
===============

There are 2 basic ways to create a heap, ``heappush()`` and
``heapify()``.

Using ``heappush()``, the heap sort order of the elements is
maintained as new items are added from a data source.

.. include:: heapq_heappush.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'heapq_heappush.py'))
.. }}}

::

	$ python heapq_heappush.py
	
	random : [19, 9, 4, 10, 11, 8, 2]
	
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
	
	add   8:
	
	                 4                  
	        10                8         
	    19       11       9    
	------------------------------------
	
	add   2:
	
	                 2                  
	        10                4         
	    19       11       9        8    
	------------------------------------
	

.. {{{end}}}


If the data is already in memory, it is more efficient to use
``heapify()`` to rearrange the items of the list in place.

.. include:: heapq_heapify.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'heapq_heapify.py'))
.. }}}

::

	$ python heapq_heapify.py
	
	random    : [19, 9, 4, 10, 11, 8, 2]
	heapified :
	
	                 2                  
	        9                 4         
	    10       11       8        19   
	------------------------------------
	

.. {{{end}}}


Accessing Contents of a Heap
============================

Once the heap is organized correctly, use ``heappop()`` to remove the
element with the lowest value. In this example, adapted from the
stdlib documentation, ``heapify()`` and ``heappop()`` are used to sort
a list of numbers.

.. include:: heapq_heappop.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'heapq_heappop.py'))
.. }}}

::

	$ python heapq_heappop.py
	
	random    : [19, 9, 4, 10, 11, 8, 2]
	heapified :
	
	                 2                  
	        9                 4         
	    10       11       8        19   
	------------------------------------
	
	
	pop      2:
	
	                 4                  
	        9                 8         
	    10       11       19   
	------------------------------------
	
	pop      4:
	
	                 8                  
	        9                 19        
	    10       11   
	------------------------------------
	
	pop      8:
	
	                 9                  
	        10                19        
	    11   
	------------------------------------
	
	pop      9:
	
	                 10                 
	        11                19        
	------------------------------------
	
	pop     10:
	
	                 11                 
	        19        
	------------------------------------
	
	pop     11:
	
	                 19                 
	------------------------------------
	
	pop     19:
	
	------------------------------------
	
	inorder   : [2, 4, 8, 9, 10, 11, 19]

.. {{{end}}}


To remove existing elements and replace them with new values in a
single operation, use ``heapreplace()``.

.. include:: heapq_heapreplace.py
    :literal:
    :start-after: #end_pymotw_header

Replacing elements in place lets you maintain a fixed size heap, such
as a queue of jobs ordered by priority.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'heapq_heapreplace.py'))
.. }}}

::

	$ python heapq_heapreplace.py
	
	start:
	
	                 2                  
	        9                 4         
	    10       11       8        19   
	------------------------------------
	
	replace  2 with  0:
	
	                 0                  
	        9                 4         
	    10       11       8        19   
	------------------------------------
	
	replace  0 with  7:
	
	                 4                  
	        9                 7         
	    10       11       8        19   
	------------------------------------
	
	replace  4 with 13:
	
	                 7                  
	        9                 8         
	    10       11       13       19   
	------------------------------------
	
	replace  7 with  9:
	
	                 8                  
	        9                 9         
	    10       11       13       19   
	------------------------------------
	
	replace  8 with  5:
	
	                 5                  
	        9                 9         
	    10       11       13       19   
	------------------------------------
	

.. {{{end}}}

Data Extremes
=============

:mod:`heapq` also includes 2 functions to examine an iterable to find
a range of the largest or smallest values it contains. Using
``nlargest()`` and ``nsmallest()`` are really only efficient for
relatively small values of n > 1, but can still come in handy in a few
cases.

.. include:: heapq_extremes.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'heapq_extremes.py'))
.. }}}

::

	$ python heapq_extremes.py
	
	all       : [19, 9, 4, 10, 11, 8, 2]
	3 largest : [19, 11, 10]
	from sort : [19, 11, 10]
	3 smallest: [2, 4, 8]
	from sort : [2, 4, 8]

.. {{{end}}}

.. seealso::

    `heapq <http://docs.python.org/2.7/library/heapq.html>`_
        The standard library documentation for this module.

    `WikiPedia: Heap (data structure) <http://en.wikipedia.org/wiki/Heap_(data_structure)>`_
        A general description of heap data structures.

    :ref:`article-data-structures`
        Other Python data structures.

    :ref:`Queue-PriorityQueue`
        A priority queue implementation from :mod:`Queue` in the
        standard library.
