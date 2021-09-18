.. _article-data-structures:

#########################
In-Memory Data Structures
#########################

Python includes several standard programming data structures as `built-in types <http://docs.python.org/2.7/library/stdtypes.html>`_ (list, tuple, dictionary, and set).  Most applications won't need any other structures, but when they do the standard library delivers.

array
=====

For large amounts of data, it may be more efficient to use an :mod:`array` instead of a ``list``.  Since the array is limited to a single data type, it can use a more compact memory representation than a general purpose list.  As an added benefit, arrays can be manipulated using many of the same methods as a list, so it may be possible to replaces lists with arrays in to your application without a lot of other changes.

Sorting
=======

If you need to maintain a sorted list as you add and remove values, check out :mod:`heapq`.  By using the functions in :mod:`heapq` to add or remove items from a list, you can maintain the sort order of the list with low overhead.  

Another option for building sorted lists or arrays is :mod:`bisect`.  bisect uses a binary search to find the insertion point for new items, and is an alternative to repeatedly sorting a list that changes frequently.

Queue
=====

Although the built-in list can simulate a queue using the ``insert()`` and ``pop()`` methods, it isn't thread-safe.  For true ordered communication between threads you should use a :mod:`Queue`.  :mod:`multiprocessing` includes a version of a Queue that works between processes, making it easier to port between the modules.

collections
===========

:mod:`collections` includes implementations of several data structures that extend those found in other modules.  For example, Deque is a double-ended queue, and allows you to add or remove items from either end.  The ``defaultdict`` is a dictionary that responds with a default value if a key is missing.  And ``namedtuple`` extends the normal tuple to give each member item an attribute name in addition to a numerical index.

Decoding Data
=============

If you are working with data from another application, perhaps coming from a binary file or stream of data, you will find :mod:`struct` useful for decoding the data into Python's native types for easier manipulation.

Custom Variations
=================

And finally, if the available types don't give you what you need, you may want to subclass one of the native types and customize it.  You can also start from scratch by using the abstract base classes defined in :mod:`collections`.
