================================
 pickle -- Object Serialization
================================

.. module:: pickle
    :synopsis: Object serialization

.. module:: cPickle
    :synopsis: Object serialization

:Purpose: Object serialization
:Python Version: 1.4 and later for pickle, 1.5 and later for cPickle

The :mod:`pickle` module implements an algorithm for turning an
arbitrary Python object into a series of bytes.  This process is also
called *serializing* the object. The byte stream representing the
object can then be transmitted or stored, and later reconstructed to
create a new object with the same characteristics.

The :mod:`cPickle` module implements the same algorithm, in C instead
of Python. It is many times faster than the Python implementation, so
it is generally used instead of the pure-Python implementation.

.. warning::

    The documentation for :mod:`pickle` makes clear that it offers no
    security guarantees. In fact, unpickling data can execute
    arbitrary code.  Be careful using :mod:`pickle` for inter-process
    communication or data storage, and do not trust data that cannot
    be verified as secure.  See :ref:`hmac-pickle` in the :mod:`hmac`
    section for an example of a secure way to verify the source of a
    pickled data source.

Importing
=========

Because :mod:`cPickle` is faster than :mod:`pickle`, it is common to
first try to import :mod:`cPickle`, giving it an alias of "pickle",
then fall back on the native Python implementation in :mod:`pickle` if
the import fails. This means the program will use the faster
implementation, if it is available, and the portable implementation
otherwise.

::

    try:
       import cPickle as pickle
    except:
       import pickle

The API for the C and Python versions is the same, and data can be
exchanged between programs using either version of the library.

Encoding and Decoding Data in Strings
=====================================

This first example Uses :func:`dumps` to encode a data structure as a
string, then prints the string to the console. It uses a data
structure made up of entirely built-in types. Instances of any class
can be pickled, as will be illustrated in a later example.

.. include:: pickle_string.py
    :literal:
    :start-after: #end_pymotw_header

By default, the pickle will contain only ASCII characters. A more
efficient binary pickle format is also available, but all of the
examples here use the ASCII output because it is easier to understand
in print.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pickle_string.py'))
.. }}}

::

	$ python pickle_string.py
	
	DATA:[{'a': 'A', 'b': 2, 'c': 3.0}]
	PICKLE: "(lp1\n(dp2\nS'a'\nS'A'\nsS'c'\nF3\nsS'b'\nI2\nsa."

.. {{{end}}}

After the data is serialized, it can be written to a file, socket,
pipe, etc.  Later, the file can be read and the data unpickled to
construct a new object with the same values.

.. include:: pickle_unpickle.py
    :literal:
    :start-after: #end_pymotw_header

The newly constructed object is equal to, but not the same object as,
the original.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pickle_unpickle.py'))
.. }}}

::

	$ python pickle_unpickle.py
	
	BEFORE: [{'a': 'A', 'b': 2, 'c': 3.0}]
	AFTER : [{'a': 'A', 'b': 2, 'c': 3.0}]
	SAME? : False
	EQUAL?: True

.. {{{end}}}


Working with Streams
====================

In addition to :func:`dumps` and :func:`loads`, :mod:`pickle` provides
convenience functions for working with file-like streams. It is
possible to write multiple objects to a stream, and then read them
from the stream without knowing in advance how many objects are
written, or how big they are.

.. include:: pickle_stream.py
    :literal:
    :start-after: #end_pymotw_header


The example simulates streams using two :mod:`StringIO` buffers.  The
first receives the pickled objects, and its value is fed to a second
from which :func:`load` reads.  A simple database format could use
pickles to store objects, too (see :mod:`shelve`).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pickle_stream.py'))
.. }}}

::

	$ python pickle_stream.py
	
	WRITING : pickle (elkcip)
	WRITING : cPickle (elkciPc)
	WRITING : last (tsal)
	READ    : pickle (elkcip)
	READ    : cPickle (elkciPc)
	READ    : last (tsal)

.. {{{end}}}

Besides storing data, pickles are handy for inter-process
communication. For example, :func:`os.fork` and :func:`os.pipe` can be
used to establish worker processes that read job instructions from one
pipe and write the results to another pipe. The core code for managing
the worker pool and sending jobs in and receiving responses can be
reused, since the job and response objects do not have to be based on
a particular class. When using pipes or sockets, do not forget to
flush after dumping each object, to push the data through the
connection to the other end.  See the :mod:`multiprocessing` module
for a reusable worker pool manager.


Problems Reconstructing Objects
===============================

When working with custom classes, the class being pickled must appear
in the namespace of the process reading the pickle. Only the data for
the instance is pickled, not the class definition. The class name is
used to find the constructor to create the new object when
unpickling. This example writes instances of a class to a file:

.. include:: pickle_dump_to_file_1.py
    :literal:
    :start-after: #end_pymotw_header


When run, the script creates a file based on the name given as
argument on the command line:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pickle_dump_to_file_1.py test.dat'))
.. }}}

::

	$ python pickle_dump_to_file_1.py test.dat
	
	WRITING: pickle (elkcip)
	WRITING: cPickle (elkciPc)
	WRITING: last (tsal)

.. {{{end}}}

A simplistic attempt to load the resulting pickled objects fails:

.. include:: pickle_load_from_file_1.py
    :literal:
    :start-after: #end_pymotw_header

This version fails because there is no :class:`SimpleObject` class
available.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pickle_load_from_file_1.py test.dat', ignore_error=True))
.. }}}

::

	$ python pickle_load_from_file_1.py test.dat
	
	Traceback (most recent call last):
	  File "pickle_load_from_file_1.py", line 25, in <module>
	    o = pickle.load(in_s)
	AttributeError: 'module' object has no attribute 'SimpleObject'

.. {{{end}}}

The corrected version, which imports :class:`SimpleObject` from the
original script, succeeds.  Adding this import statement to the end of
the import list allows the script to find the class and construct the
object.

::

    from pickle_dump_to_file_1 import SimpleObject

Running the modified script now produces the desired results.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pickle_load_from_file_2.py test.dat'))
.. }}}

::

	$ python pickle_load_from_file_2.py test.dat
	
	READ: pickle (elkcip)
	READ: cPickle (elkciPc)
	READ: last (tsal)

.. {{{end}}}

Unpicklable Objects
===================

Not all objects can be pickled. Sockets, file handles, database
connections, and other objects with runtime state that depends on the
operating system or another process may not be able to be saved in a
meaningful way. Objects that have non-picklable attributes can define
:func:`__getstate__` and :func:`__setstate__` to return a subset of the
state of the instance to be pickled. New-style classes can also define
:func:`__getnewargs__`, which should return arguments to be passed to
the class memory allocator (:func:`C.__new__`).  Use of these features
is covered in more detail in the standard library documentation.

Circular References
===================

The pickle protocol automatically handles circular references between
objects, so complex data structures do not need any special handling.
Consider the directed graph in :figure:`pickle_example`.  It includes
several cycles, yet the correct structure can be pickled and then
reloaded.

.. digraph:: pickle_example
   :caption: Pickling a Data Structure With Cycles

     "root";
     "root" -> "a";
     "root" -> "b";
     "a" -> "b";
     "b" -> "a";
     "b" -> "c";
     "a" -> "a";

.. include:: pickle_cycle.py
    :literal:
    :start-after: #end_pymotw_header

The reloaded nodes are not the same object, but the relationship
between the nodes is maintained and only one copy of the object with
multiple references is reloaded. Both of these statements can be
verified by examining the :func:`id` values for the nodes before and
after being passed through pickle.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pickle_cycle.py'))
.. }}}

::

	$ python pickle_cycle.py
	
	ORIGINAL GRAPH:
	 root ->  a (4309376848)
	    a ->  b (4309376912)
	    b ->  a (4309376848)
	    b ->  c (4309376976)
	    a ->  a (4309376848)
	 root ->  b (4309376912)
	
	RELOADED GRAPH:
	 root ->  a (4309418128)
	    a ->  b (4309418192)
	    b ->  a (4309418128)
	    b ->  c (4309418256)
	    a ->  a (4309418128)
	 root ->  b (4309418192)

.. {{{end}}}


.. seealso::

    `pickle <http://docs.python.org/lib/module-pickle.html>`_
        Standard library documentation for this module.

    :mod:`shelve`
        The ``shelve`` module uses ``pickle`` to store data in a DBM database.

    `Pickle: An interesting stack language. <http://peadrop.com/blog/2007/06/18/pickle-an-interesting-stack-language/>`__
        by Alexandre Vassalotti

    `Why Python Pickle is Insecure <http://nadiana.com/python-pickle-insecure>`__
        A short example by Nadia Alramli demonstrating a security
        exploit using pickle.
