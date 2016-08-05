Data Extremes From a Heap
=========================

:mod:`heapq` also includes two functions to examine an iterable to find
a range of the largest or smallest values it contains. 

.. include:: heapq_extremes.py
    :literal:
    :start-after: #end_pymotw_header

Using :func:`nlargest` and :func:`nsmallest` are only efficient for
relatively small values of n > 1, but can still come in handy in a few
cases.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'heapq_extremes.py'))
.. }}}

::

	$ python heapq_extremes.py
	
	all       : [19, 9, 4, 10, 11]
	3 largest : [19, 11, 10]
	from sort : [19, 11, 10]
	3 smallest: [4, 9, 10]
	from sort : [4, 9, 10]

.. {{{end}}}
