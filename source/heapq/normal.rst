Example Data
============

The examples in this section use the data in ``heapq_heapdata.py``.

.. include:: heapq_heapdata.py
    :literal:
    :start-after: #end_pymotw_header

The heap output is printed using ``heapq_showtree.py``:

.. include:: heapq_showtree.py
   :literal:
   :start-after: #end_pymotw_header



Creating a Heap
===============

There are two basic ways to create a heap: :func:`heappush` and
:func:`heapify`.

.. include:: heapq_heappush.py
    :literal:
    :start-after: #end_pymotw_header

Using :func:`heappush`, the heap sort order of the elements is
maintained as new items are added from a data source.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'heapq_heappush.py'))
.. }}}

::

	$ python heapq_heappush.py
	
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

.. include:: heapq_heapify.py
    :literal:
    :start-after: #end_pymotw_header

The result of building a list in heap order one item at a time is the
same as building it unordered and then calling :func:`heapify`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'heapq_heapify.py'))
.. }}}

::

	$ python heapq_heapify.py
	
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

.. include:: heapq_heappop.py
    :literal:
    :start-after: #end_pymotw_header

In this example, adapted from the stdlib documentation,
:func:`heapify` and :func:`heappop` are used to sort a list of
numbers.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'heapq_heappop.py'))
.. }}}

::

	$ python heapq_heappop.py
	
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
single operation, use ``heapreplace()``.

.. include:: heapq_heapreplace.py
    :literal:
    :start-after: #end_pymotw_header

Replacing elements in place makes it possible to maintain a fixed size
heap, such as a queue of jobs ordered by priority.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'heapq_heapreplace.py'))
.. }}}

::

	$ python heapq_heapreplace.py
	
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
