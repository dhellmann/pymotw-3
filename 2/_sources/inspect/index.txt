===============================
inspect -- Inspect live objects
===============================

.. module:: inspect
    :synopsis: Inspect live objects

:Purpose:
    The inspect module provides functions for introspecting on live
    objects and their source code.
:Available In: added in 2.1, with updates in 2.3 and 2.5

The :mod:`inspect` module provides functions for learning about live
objects, including modules, classes, instances, functions, and
methods. You can use functions in this module to retrieve the original
source code for a function, look at the arguments to a method on the
stack, and extract the sort of information useful for producing
library documentation for your source code.  My own `CommandLineApp`_
module uses inspect to determine the valid options to a command line
program, as well as any arguments and their names so command line
programs are self-documenting and the help text is generated
automatically.

Module Information
==================

The first kind of introspection supported lets you probe live objects
to learn about them. For example, it is possible to discover the
classes and functions in a module, the methods of a class, etc. Let's
start with the module-level details and work our way down to the
function level.

To determine how the interpreter will treat and load a file as a
module, use :func:`getmoduleinfo()`. Pass a filename as the only
argument, and the return value is a tuple including the module base
name, the suffix of the file, the mode that will be used for reading
the file, and the module type as defined in the :mod:`imp` module. It
is important to note that the function looks only at the file's name,
and does not actually check if the file exists or try to read the
file.

.. include:: inspect_getmoduleinfo.py
    :literal:
    :start-after: #end_pymotw_header

Here are a few sample runs:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getmoduleinfo.py example.py'))
.. cog.out(run_script(cog.inFile, 'inspect_getmoduleinfo.py readme.txt', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'inspect_getmoduleinfo.py notthere.pyc', include_prefix=False))
.. }}}

::

	$ python inspect_getmoduleinfo.py example.py
	
	NAME   : example
	SUFFIX : .py
	MODE   : U (universal newline)
	MTYPE  : source

	$ python inspect_getmoduleinfo.py readme.txt
	
	Could not determine module type of readme.txt

	$ python inspect_getmoduleinfo.py notthere.pyc
	
	NAME   : notthere
	SUFFIX : .pyc
	MODE   : rb (read-binary)
	MTYPE  : compiled

.. {{{end}}}


Example Module
==============

The rest of the examples for this tutorial use a single example file
source file, found in ``PyMOTW/inspect/example.py`` and which is
included below.  The file is also available as part of the source
distribution associated with this series of articles.

.. include:: example.py
    :literal:
    :start-after: #end_pymotw_header

Modules
=======

It is possible to probe live objects to determine their components
using :func:`getmembers()`. The arguments to :func:`getmembers()` are
an object to scan (a module, class, or instance) and an optional
predicate function that is used to filter the objects returned. The
return value is a list of tuples with 2 values: the name of the
member, and the type of the member. The inspect module includes
several such predicate functions with names like :func:`ismodule()`,
:func:`isclass()`, etc.  You can provide your own predicate function
as well.

The types of members that might be returned depend on the type of
object scanned. Modules can contain classes and functions; classes can
contain methods and attributes; and so on.

.. include:: inspect_getmembers_module.py
    :literal:
    :start-after: #end_pymotw_header

This sample prints the members of the example module. Modules have a
set of ``__builtins__``, which are ignored in the output for this
example because they are not actually part of the module and the list
is long.

.. No cog, the memory addresses and paths change.

::

    $ python inspect_getmembers_module.py
    A : <class 'example.A'>
    B : <class 'example.B'>
    __doc__ : 'Sample file to serve as the basis for inspect examples.\n'
    __file__ : '/Users/dhellmann/Documents/PyMOTW/branches/inspect/example.pyc'
    __name__ : 'example'
    instance_of_a : <example.A object at 0xbb810>
    module_level_function : <function module_level_function at 0xc8230>


The predicate argument can be used to filter the types of objects returned.

.. include:: inspect_getmembers_module_class.py
    :literal:
    :start-after: #end_pymotw_header

Notice that only classes are included in the output, now:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getmembers_module_class.py'))
.. }}}

::

	$ python inspect_getmembers_module_class.py
	
	A : <class 'example.A'>
	B : <class 'example.B'>

.. {{{end}}}


Classes
=======

Classes are scanned using :func:`getmembers()` in the same way as
modules, though the types of members are different.

.. include:: inspect_getmembers_class.py
    :literal:
    :start-after: #end_pymotw_header

Since no filtering is applied, the output shows the attributes, methods,
slots, and other members of the class:

.. No cog, memory locations change.

::

    $ python inspect_getmembers_class.py
    [('__class__', <type 'type'>),
     ('__delattr__', <slot wrapper '__delattr__' of 'object' objects>),
     ('__dict__', <dictproxy object at 0xca090>),
     ('__doc__', 'The A class.'),
     ('__getattribute__', <slot wrapper '__getattribute__' of 'object' objects>),
     ('__hash__', <slot wrapper '__hash__' of 'object' objects>),
     ('__init__', <unbound method A.__init__>),
     ('__module__', 'example'),
     ('__new__', <built-in method __new__ of type object at 0x32ff38>),
     ('__reduce__', <method '__reduce__' of 'object' objects>),
     ('__reduce_ex__', <method '__reduce_ex__' of 'object' objects>),
     ('__repr__', <slot wrapper '__repr__' of 'object' objects>),
     ('__setattr__', <slot wrapper '__setattr__' of 'object' objects>),
     ('__str__', <slot wrapper '__str__' of 'object' objects>),
     ('__weakref__', <attribute '__weakref__' of 'A' objects>),
     ('get_name', <unbound method A.get_name>)]

To find the methods of a class, use the :func:`ismethod()` predicate:

.. include:: inspect_getmembers_class_methods.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getmembers_class_methods.py'))
.. }}}

::

	$ python inspect_getmembers_class_methods.py
	
	[('__init__', <unbound method A.__init__>),
	 ('get_name', <unbound method A.get_name>)]

.. {{{end}}}


If we look at class B, we see the over-ride for :func:`get_name()` as
well as the new method, and the inherited :func:`__init__()` method
implented in A.

.. include:: inspect_getmembers_class_methods_b.py
    :literal:
    :start-after: #end_pymotw_header

Notice that even though :func:`__init__()` is inherited from
:class:`A`, it is identified as a method of :class:`B`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getmembers_class_methods_b.py'))
.. }}}

::

	$ python inspect_getmembers_class_methods_b.py
	
	[('__init__', <unbound method B.__init__>),
	 ('do_something', <unbound method B.do_something>),
	 ('get_name', <unbound method B.get_name>)]

.. {{{end}}}


Documentation Strings
=====================

The docstring for an object can be retrieved with
:func:`getdoc()`. The return value is the ``__doc__`` attribute with
tabs expanded to spaces and with indentation made uniform.

.. include:: inspect_getdoc.py
    :literal:
    :start-after: #end_pymotw_header

Notice the difference in indentation on the second line of the
doctring:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getdoc.py'))
.. }}}

::

	$ python inspect_getdoc.py
	
	B.__doc__:
	This is the B class.
	    It is derived from A.
	    
	
	getdoc(B):
	This is the B class.
	It is derived from A.

.. {{{end}}}

In addition to the actual docstring, it is possible to retrieve the
comments from the source file where an object is implemented, if the
source is available. The :func:`getcomments()` function looks at the
source of the object and finds comments on lines preceding the
implementation.

.. include:: inspect_getcomments_method.py
    :literal:
    :start-after: #end_pymotw_header

The lines returned include the comment prefix, but any whitespace
prefix is stripped off.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getcomments_method.py'))
.. }}}

::

	$ python inspect_getcomments_method.py
	
	# This method is not part of A.
	

.. {{{end}}}

When a module is passed to :func:`getcomments()`, the return value is
always the first comment in the module.

.. include:: inspect_getcomments_module.py
    :literal:
    :start-after: #end_pymotw_header

Notice that contiguous lines from the example file are included as a single
comment, but as soon as a blank line appears the comment is stopped.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getcomments_module.py'))
.. }}}

::

	$ python inspect_getcomments_module.py
	
	# This comment appears first
	# and spans 2 lines.
	

.. {{{end}}}

Retrieving Source
=================

If the ``.py`` file is available for a module, the original source
code for the class or method can be retrieved using
:func:`getsource()` and :func:`getsourcelines()`.

.. include:: inspect_getsource_method.py
    :literal:
    :start-after: #end_pymotw_header

The original indent level is retained in this case.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getsource_method.py'))
.. }}}

::

	$ python inspect_getsource_method.py
	
	    def get_name(self):
	        "Returns the name of the instance."
	        return self.name
	

.. {{{end}}}

When a class is passed in, all of the methods for the class are included in
the output.

.. include:: inspect_getsource_class.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getsource_class.py'))
.. }}}

::

	$ python inspect_getsource_class.py
	
	class A(object):
	    """The A class."""
	    def __init__(self, name):
	        self.name = name
	
	    def get_name(self):
	        "Returns the name of the instance."
	        return self.name
	

.. {{{end}}}

If you need the lines of source split up, it can be easier to use
:func:`getsourcelines()` instead of :func:`getsource()`. The return
value from :func:`getsourcelines()` is a tuple containing a list of
strings (the lines from the source file), and a starting line number
in the file where the source appears.

.. include:: inspect_getsourcelines_method.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getsourcelines_method.py'))
.. }}}

::

	$ python inspect_getsourcelines_method.py
	
	(['    def get_name(self):\n',
	  '        "Returns the name of the instance."\n',
	  '        return self.name\n'],
	 48)

.. {{{end}}}

If the source file is not available, :func:`getsource()` and
:func:`getsourcelines()` raise an :ref:`IOError <exceptions-IOError>`.

Method and Function Arguments
=============================

In addition to the documentation for a function or method, it is
possible to ask for a complete specification of the arguments the
callable takes, including default values. The :func:`getargspec()`
function returns a tuple containing the list of positional argument
names, the name of any variable positional arguments (e.g.,
``*args``), the names of any variable named arguments (e.g.,
``**kwds``), and default values for the arguments. If there are
default values, they match up with the end of the positional argument
list.

.. include:: inspect_getargspec_function.py
    :literal:
    :start-after: #end_pymotw_header

Note that the first argument, *arg1*, does not have a default
value. The single default therefore is matched up with *arg2*.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getargspec_function.py'))
.. }}}

::

	$ python inspect_getargspec_function.py
	
	NAMES   : ['arg1', 'arg2']
	*       : args
	**      : kwargs
	defaults: ('default',)
	args & defaults: [('arg2', 'default')]

.. {{{end}}}


Class Hierarchies
=================

:mod:`inspect` includes two methods for working directly with class
hierarchies. The first, :func:`getclasstree()`, creates a tree-like
data structure using nested lists and tuples based on the classes it
is given and their base classes. Each element in the list returned is
either a tuple with a class and its base classes, or another list
containing tuples for subclasses.

.. .. digraph:: class_hierarchy

..    "A";
..    "B" -> "A";
..    "C" -> "B";
..    "D" -> "C";
..    "D" -> "A";

.. include:: inspect_getclasstree.py
    :literal:
    :start-after: #end_pymotw_header

The output from this example is the "tree" of inheritance for the A, B, C, and
D classes. Note that D appears twice, since it inherits from both C and A.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getclasstree.py'))
.. }}}

::

	$ python inspect_getclasstree.py
	
	A, B, C, D:
	 object
	   A
	     D
	     B
	       C
	         D

.. {{{end}}}

If we call :func:`getclasstree()` with ``unique=True``, the output is
different.

.. include:: inspect_getclasstree_unique.py
    :literal:
    :start-after: #end_pymotw_header

This time, D only appears in the output once:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getclasstree_unique.py'))
.. }}}

::

	$ python inspect_getclasstree_unique.py
	
	 object
	   A
	     B
	       C
	         D

.. {{{end}}}


Method Resolution Order
=======================

The other function for working with class hierarchies is
:func:`getmro()`, which returns a tuple of classes in the order they
should be scanned when resolving an attribute that might be inherited
from a base class. Each class in the sequence appears only once.

.. include:: inspect_getmro.py
    :literal:
    :start-after: #end_pymotw_header

This output demonstrates the "depth-first" nature of the MRO_
search. For B_First, A also comes before C in the search order,
because B is derived from A.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getmro.py'))
.. }}}

::

	$ python inspect_getmro.py
	
	B_First:
		B_First
		B
		A
		C
		object
	
	C_First:
		C_First
		C
		B
		A
		object

.. {{{end}}}


The Stack and Frames
====================

In addition to introspection of code objects, :mod:`inspect` includes
functions for inspecting the runtime environment while a program is
running. Most of these functions work with the call stack, and operate
on "call frames". Each frame record in the stack is a 6 element tuple
containing the frame object, the filename where the code exists, the
line number in that file for the current line being run, the function
name being called, a list of lines of context from the source file,
and the index into that list of the current line. Typically such
information is used to build tracebacks when exceptions are raised. It
can also be useful when debugging programs, since the stack frames can
be interrogated to discover the argument values passed into the
functions.

:func:`currentframe()` returns the frame at the top of the stack (for
the current function). :func:`getargvalues()` returns a tuple with
argument names, the names of the variable arguments, and a dictionary
with local values from the frame. By combining them, we can see the
arguments to functions and local variables at different points in the
call stack.

.. include:: inspect_getargvalues.py
    :literal:
    :start-after: #end_pymotw_header

The value for ``local_variable`` is included in the frame's local
variables even though it is not an argument to the function.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getargvalues.py'))
.. }}}

::

	$ python inspect_getargvalues.py
	
	3 ArgInfo(args=['limit'], varargs=None, keywords=None, locals={'local_variable': '...', 'limit': 3})
	2 ArgInfo(args=['limit'], varargs=None, keywords=None, locals={'local_variable': '..', 'limit': 2})
	1 ArgInfo(args=['limit'], varargs=None, keywords=None, locals={'local_variable': '.', 'limit': 1})
	0 ArgInfo(args=['limit'], varargs=None, keywords=None, locals={'local_variable': '', 'limit': 0})

.. {{{end}}}


Using :func:`stack()`, it is also possible to access all of the stack
frames from the current frame to the first caller. This example is
similar to the one above, except it waits until reaching the end of
the recursion to print the stack information.

.. include:: inspect_stack.py
    :literal:
    :start-after: #end_pymotw_header

The last part of the output represents the main program, outside of the
recurse function.

.. Frame locations change, no cog.

::

    $ python inspect_stack.py
    inspect_stack.py[37]
      -> for frame, filename, line_num, func, source_code, source_index in inspect.stack():
    (['limit'], None, None, {'local_variable': '', 'line_num': 37, 'frame': <frame object at 0x61ba30>, 
    'filename': 'inspect_stack.py', 'limit': 0, 'func': 'recurse', 'source_index': 0, 
    'source_code': ['        for frame, filename, line_num, func, source_code, source_index in inspect.stack():\n']})

    inspect_stack.py[42]
      -> recurse(limit - 1)
    (['limit'], None, None, {'local_variable': '.', 'limit': 1})

    inspect_stack.py[42]
      -> recurse(limit - 1)
    (['limit'], None, None, {'local_variable': '..', 'limit': 2})

    inspect_stack.py[42]
      -> recurse(limit - 1)
    (['limit'], None, None, {'local_variable': '...', 'limit': 3})

    inspect_stack.py[46]
      -> recurse(3)
    ([], None, None, {'__builtins__': <module '__builtin__' (built-in)>, 
    '__file__': 'inspect_stack.py', 
    'inspect': <module 'inspect' from '/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/inspect.pyc'>, 
    'recurse': <function recurse at 0xc81b0>, '__name__': '__main__', 
    '__doc__': 'Inspecting the call stack.\n\n'})

There are other functions for building lists of frames in different
contexts, such as when an exception is being processed. See the
documentation for :func:`trace()`, :func:`getouterframes()`, and
:func:`getinnerframes()` for more details.


.. seealso::

    `inspect <http://docs.python.org/2.7/library/inspect.html>`_
        The standard library documentation for this module.

    `CommandLineApp`_
        Base class for object-oriented command line applications

        .. _CommandLineApp: http://www.doughellmann.com/projects/CommandLineApp/

    `Python 2.3 Method Resolution Order <http://www.python.org/download/releases/2.3/mro/>`__
        Documentation for the C3 Method Resolution order used by
        Python 2.3 and later.

.. _MRO: http://www.python.org/download/releases/2.3/mro/
