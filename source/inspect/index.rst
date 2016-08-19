==================================
 inspect --- Inspect Live Objects
==================================

.. module:: inspect
    :synopsis: Inspect live objects

:Purpose:
    The inspect module provides functions for introspecting on live
    objects and their source code.

The :mod:`inspect` module provides functions for learning about live
objects, including modules, classes, instances, functions, and
methods. The functions in this module can be used to retrieve the
original source code for a function, look at the arguments to a method
on the stack, and extract the sort of information useful for producing
library documentation for source code.

Example Module
==============

The rest of the examples for this section use this example file,
``example.py``.

.. literalinclude:: example.py
    :caption:
    :start-after: #!/usr/bin/env python3

Module Information
==================

The first kind of introspection probes live objects to learn about
them. For example, it is possible to discover the classes and
functions in a module, the methods of a class, etc.

To determine how the interpreter will treat and load a file as a
module, use :func:`getmoduleinfo`. Pass a filename as the only
argument, and the return value is a :class:`tuple` including the
module base name, the suffix of the file, the mode that will be used
for reading the file, and the module type as defined in the :mod:`imp`
module. It is important to note that the function looks only at the
file's name, and does not actually check if the file exists or try to
read the file.

.. literalinclude:: inspect_getmoduleinfo.py
    :caption:
    :start-after: #end_pymotw_header

Here are a few sample runs:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getmoduleinfo.py example.py'))
.. cog.out(run_script(cog.inFile, 'inspect_getmoduleinfo.py readme.txt', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'inspect_getmoduleinfo.py notthere.pyc', include_prefix=False))
.. }}}

.. code-block:: none

	$ python3 inspect_getmoduleinfo.py example.py
	
	NAME   : example
	SUFFIX : .py
	MODE   : r 
	MTYPE  : source

	$ python3 inspect_getmoduleinfo.py readme.txt
	
	Could not determine module type of readme.txt

	$ python3 inspect_getmoduleinfo.py notthere.pyc
	
	NAME   : notthere
	SUFFIX : .pyc
	MODE   : rb (read-binary)
	MTYPE  : compiled

.. {{{end}}}

Inspecting Modules
==================

It is possible to probe live objects to determine their components
using :func:`getmembers`. The arguments are an object to scan (a
module, class, or instance) and an optional predicate function that is
used to filter the objects returned. The return value is a list of
tuples with two values: the name of the member, and the type of the
member. The :mod:`inspect` module includes several such predicate
functions with names like :func:`ismodule`, :func:`isclass`, etc.

The types of members that might be returned depend on the type of
object scanned. Modules can contain classes and functions; classes can
contain methods and attributes; and so on.

.. literalinclude:: inspect_getmembers_module.py
    :caption:
    :start-after: #end_pymotw_header

This sample prints the members of the ``example`` module. Modules have
several private attributes that are used as part of the import
implementation as well as a set of :data:`__builtins__`.  All of these
are ignored in the output for this example because they are not
actually part of the module and the list is long.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getmembers_module.py',
..         line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 inspect_getmembers_module.py
	
	A : <class 'example.A'>
	B : <class 'example.B'>
	instance_of_a : <example.A object at 0x10148b390>
	module_level_function : <function module_level_function at
	0x101487620>

.. {{{end}}}

The *predicate* argument can be used to filter the types of objects returned.

.. literalinclude:: inspect_getmembers_module_class.py
    :caption:
    :start-after: #end_pymotw_header

Only classes are included in the output, now.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getmembers_module_class.py'))
.. }}}

.. code-block:: none

	$ python3 inspect_getmembers_module_class.py
	
	A : <class 'example.A'>
	B : <class 'example.B'>

.. {{{end}}}


Inspecting Classes
==================

Classes are scanned using :func:`getmembers` in the same way as
modules, though the types of members are different.

.. literalinclude:: inspect_getmembers_class.py
    :caption:
    :start-after: #end_pymotw_header

Because no filtering is applied, the output shows the attributes,
methods, slots, and other members of the class.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getmembers_class.py',
..         line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 inspect_getmembers_class.py
	
	[('__class__', <class 'type'>),
	 ('__delattr__',
	  <slot wrapper '__delattr__' of 'object' objects>),
	 ('__dict__',
	  mappingproxy({'__dict__': <attribute '__dict__' of 'A'
	objects>,
	                '__doc__': 'The A class.',
	                '__init__': <function A.__init__ at
	0x101c8ae18>,
	                '__module__': 'example',
	                '__weakref__': <attribute '__weakref__' of 'A'
	objects>,
	                'get_name': <function A.get_name at
	0x101c8aea0>})),
	 ('__dir__', <method '__dir__' of 'object' objects>),
	 ('__doc__', 'The A class.'),
	 ('__eq__', <slot wrapper '__eq__' of 'object' objects>),
	 ('__format__', <method '__format__' of 'object' objects>),
	 ('__ge__', <slot wrapper '__ge__' of 'object' objects>),
	 ('__getattribute__',
	  <slot wrapper '__getattribute__' of 'object' objects>),
	 ('__gt__', <slot wrapper '__gt__' of 'object' objects>),
	 ('__hash__', <slot wrapper '__hash__' of 'object' objects>),
	 ('__init__', <function A.__init__ at 0x101c8ae18>),
	 ('__le__', <slot wrapper '__le__' of 'object' objects>),
	 ('__lt__', <slot wrapper '__lt__' of 'object' objects>),
	 ('__module__', 'example'),
	 ('__ne__', <slot wrapper '__ne__' of 'object' objects>),
	 ('__new__',
	  <built-in method __new__ of type object at 0x100229960>),
	 ('__reduce__', <method '__reduce__' of 'object' objects>),
	 ('__reduce_ex__', <method '__reduce_ex__' of 'object'
	objects>),
	 ('__repr__', <slot wrapper '__repr__' of 'object' objects>),
	 ('__setattr__',
	  <slot wrapper '__setattr__' of 'object' objects>),
	 ('__sizeof__', <method '__sizeof__' of 'object' objects>),
	 ('__str__', <slot wrapper '__str__' of 'object' objects>),
	 ('__subclasshook__',
	  <built-in method __subclasshook__ of type object at
	0x100512658>),
	 ('__weakref__', <attribute '__weakref__' of 'A' objects>),
	 ('get_name', <function A.get_name at 0x101c8aea0>)]

.. {{{end}}}

To find the methods of a class, use the :func:`isfunction`
predicate. The :func:`ismethod` predicate only recognizes bound
methods of instances.

.. literalinclude:: inspect_getmembers_class_methods.py
    :caption:
    :start-after: #end_pymotw_header

Only unbound methods are returned now.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getmembers_class_methods.py'))
.. }}}

.. code-block:: none

	$ python3 inspect_getmembers_class_methods.py
	
	[('__init__', <function A.__init__ at 0x101ca6e18>),
	 ('get_name', <function A.get_name at 0x101ca6ea0>)]

.. {{{end}}}

The output for :class:`B` includes the override for :func:`get_name`
as well as the new method, and the inherited :func:`__init__` method
implemented in :class:`A`.

.. literalinclude:: inspect_getmembers_class_methods_b.py
    :caption:
    :start-after: #end_pymotw_header

Methods inherited from :class:`A`, such as :func:`__init__`, are
identified as being methods of :class:`B`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getmembers_class_methods_b.py'))
.. }}}

.. code-block:: none

	$ python3 inspect_getmembers_class_methods_b.py
	
	[('__init__', <function A.__init__ at 0x101497e18>),
	 ('do_something', <function B.do_something at 0x101497f28>),
	 ('get_name', <function B.get_name at 0x101498048>)]

.. {{{end}}}

Inspecting Instances
====================

Introspecting instances works in the same way as other objects.

.. literalinclude:: inspect_getmembers_instance.py
   :caption:
   :start-after: #end_pymotw_header

The predicate :func:`ismethod` recognizes two bound methods from
:class:`A` in the example instance.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getmembers_instance.py'))
.. }}}

.. code-block:: none

	$ python3 inspect_getmembers_instance.py
	
	[('__init__', <bound method A.__init__ of <example.A object at 0
	x1018b21d0>>),
	 ('get_name', <bound method A.get_name of <example.A object at 0
	x1018b21d0>>)]

.. {{{end}}}

Documentation Strings
=====================

The docstring for an object can be retrieved with
:func:`getdoc`. The return value is the :attr:`__doc__` attribute
with tabs expanded to spaces and with indentation made uniform.

.. literalinclude:: inspect_getdoc.py
    :caption:
    :start-after: #end_pymotw_header

The second line of the docstring is indented when it is retrieved
through the attribute directly, but moved to the left margin by
:func:`getdoc`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getdoc.py'))
.. }}}

.. code-block:: none

	$ python3 inspect_getdoc.py
	
	B.__doc__:
	This is the B class.
	    It is derived from A.
	    
	
	getdoc(B):
	This is the B class.
	It is derived from A.

.. {{{end}}}

In addition to the actual docstring, it is possible to retrieve the
comments from the source file where an object is implemented, if the
source is available. The :func:`getcomments` function looks at the
source of the object and finds comments on lines preceding the
implementation.

.. literalinclude:: inspect_getcomments_method.py
    :caption:
    :start-after: #end_pymotw_header

The lines returned include the comment prefix with any whitespace
prefix stripped off.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getcomments_method.py'))
.. }}}

.. code-block:: none

	$ python3 inspect_getcomments_method.py
	
	# This method is not part of A.
	

.. {{{end}}}

When a module is passed to :func:`getcomments`, the return value is
always the first comment in the module.

.. literalinclude:: inspect_getcomments_module.py
    :caption:
    :start-after: #end_pymotw_header

Contiguous lines from the example file are included as a single
comment, but as soon as a blank line appears the comment is stopped.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getcomments_module.py'))
.. }}}

.. code-block:: none

	$ python3 inspect_getcomments_module.py
	
	# This comment appears first
	# and spans 2 lines.
	

.. {{{end}}}

Retrieving Source
=================

If the ``.py`` file is available for a module, the original source
code for the class or method can be retrieved using
:func:`getsource` and :func:`getsourcelines`.

.. literalinclude:: inspect_getsource_class.py
    :caption:
    :start-after: #end_pymotw_header

When a class is passed in, all of the methods for the class are included in
the output.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getsource_class.py'))
.. }}}

.. code-block:: none

	$ python3 inspect_getsource_class.py
	
	class A(object):
	    """The A class."""
	
	    def __init__(self, name):
	        self.name = name
	
	    def get_name(self):
	        "Returns the name of the instance."
	        return self.name
	

.. {{{end}}}

To retrieve the source for a single method, pass the method reference
to :func:`getsource`.

.. literalinclude:: inspect_getsource_method.py
    :caption:
    :start-after: #end_pymotw_header

The original indent level is retained in this case.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getsource_method.py'))
.. }}}

.. code-block:: none

	$ python3 inspect_getsource_method.py
	
	    def get_name(self):
	        "Returns the name of the instance."
	        return self.name
	

.. {{{end}}}

Use :func:`getsourcelines` instead of :func:`getsource` to
retrieve the lines of source split into individual strings.

.. literalinclude:: inspect_getsourcelines_method.py
    :caption:
    :start-after: #end_pymotw_header

The return value from :func:`getsourcelines` is a :class:`tuple` containing a
list of strings (the lines from the source file), and a starting line
number in the file where the source appears.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getsourcelines_method.py'))
.. }}}

.. code-block:: none

	$ python3 inspect_getsourcelines_method.py
	
	(['    def get_name(self):\n',
	  '        "Returns the name of the instance."\n',
	  '        return self.name\n'],
	 24)

.. {{{end}}}

If the source file is not available, :func:`getsource` and
:func:`getsourcelines` raise an :class:`IOError`.

Method and Function Arguments
=============================

In addition to the documentation for a function or method, it is
possible to ask for a complete specification of the arguments the
callable takes, including default values. The :func:`getargspec`
function returns a tuple containing the list of positional argument
names, the name of any variable positional arguments (e.g.,
``*args``), the names of any variable named arguments (e.g.,
``**kwds``), and default values for the arguments. If there are
default values, they match up with the end of the positional argument
list.

.. literalinclude:: inspect_getargspec_function.py
    :caption:
    :start-after: #end_pymotw_header

In this example, the first argument to the function, *arg1*, does not
have a default value. The single default therefore is matched up with
*arg2*.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getargspec_function.py'))
.. }}}

.. code-block:: none

	$ python3 inspect_getargspec_function.py
	
	NAMES   : ['arg1', 'arg2']
	*       : args
	**      : kwargs
	defaults: ('default',)
	args & defaults: [('arg2', 'default')]

.. {{{end}}}

The argspec for a function can be used by decorators or other
functions to validate inputs, provide different defaults, etc.
Writing a suitably generic and reusable validation decorator has one
special challenge, though, because it can be complicated to match up
incoming arguments with their names for functions that accept a
combination of named and positional arguments.  :func:`getcallargs`
provides the necessary logic to handle the mapping.  It returns a
dictionary populated with its arguments associated with the names of
the arguments of a specified function.

.. literalinclude:: inspect_getcallargs.py
   :caption:
   :start-after: #end_pymotw_header

The keys of the dictionary are the argument names of the function, so
the function can be called using the ``**`` syntax to expand the
dictionary onto the stack as the arguments.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getcallargs.py'))
.. }}}

.. code-block:: none

	$ python3 inspect_getcallargs.py
	
	('a',) {'unknown_name': 'value'}
	{'arg1': 'a',
	 'arg2': 'default',
	 'args': (),
	 'kwargs': {'unknown_name': 'value'}}
	
	('a',) {'arg2': 'value'}
	{'arg1': 'a', 'arg2': 'value', 'args': (), 'kwargs': {}}
	
	('a', 'b', 'c', 'd') {}
	{'arg1': 'a', 'arg2': 'b', 'args': ('c', 'd'), 'kwargs': {}}
	
	() {'arg1': 'a'}
	{'arg1': 'a', 'arg2': 'default', 'args': (), 'kwargs': {}}
	

.. {{{end}}}

Class Hierarchies
=================

:mod:`inspect` includes two methods for working directly with class
hierarchies. The first, :func:`getclasstree`, creates a tree-like
data structure based on the classes it is given and their base
classes. Each element in the list returned is either a tuple with a
class and its base classes, or another list containing tuples for
subclasses.

.. literalinclude:: inspect_getclasstree.py
    :caption:
    :start-after: #end_pymotw_header

The output from this example is the "tree" of inheritance for the
:class:`A`, :class:`B`, :class:`C`, and :class:`D` classes. 
:class:`D` appears twice, since it inherits from both :class:`C` and
:class:`A`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getclasstree.py'))
.. }}}

.. code-block:: none

	$ python3 inspect_getclasstree.py
	
	A, B, C, D:
	 object
	   A
	     D
	     B
	       C
	         D

.. {{{end}}}

If :func:`getclasstree` is called with *unique* set to a true value,
the output is different.

.. literalinclude:: inspect_getclasstree_unique.py
    :caption:
    :start-after: #end_pymotw_header

This time, :class:`D` only appears in the output once:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getclasstree_unique.py'))
.. }}}

.. code-block:: none

	$ python3 inspect_getclasstree_unique.py
	
	 object
	   A
	     B
	       C
	         D

.. {{{end}}}


Method Resolution Order
=======================

The other function for working with class hierarchies is
:func:`getmro`, which returns a :class:`tuple` of classes in the
order they should be scanned when resolving an attribute that might be
inherited from a base class using the *Method Resolution Order*
(MRO). Each class in the sequence appears only once.

.. literalinclude:: inspect_getmro.py
    :caption:
    :start-after: #end_pymotw_header

This output demonstrates the "depth-first" nature of the MRO
search. For :class:`B_First`, :class:`A` also comes before :class:`C`
in the search order, because :class:`B` is derived from :class:`A`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getmro.py'))
.. }}}

.. code-block:: none

	$ python3 inspect_getmro.py
	
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
being executed. Most of these functions work with the call stack, and operate
on "call frames." Each frame record in the stack is a six element
tuple containing the frame object, the filename where the code exists,
the line number in that file for the current line being run, the
function name being called, a list of lines of context from the source
file, and the index into that list of the current line. Typically such
information is used to build tracebacks when exceptions are raised. It
can also be useful for logging or when debugging programs, since the
stack frames can be interrogated to discover the argument values
passed into the functions.

:func:`currentframe` returns the frame at the top of the stack (for
the current function). :func:`getargvalues` returns a tuple with
argument names, the names of the variable arguments, and a dictionary
with local values from the frame. Combining them shows the arguments
to functions and local variables at different points in the call
stack.

.. literalinclude:: inspect_getargvalues.py
    :caption:
    :start-after: #end_pymotw_header

The value for :data:`local_variable` is included in the frame's local
variables even though it is not an argument to the function.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getargvalues.py', break_lines_at=55))
.. }}}

.. code-block:: none

	$ python3 inspect_getargvalues.py
	
	2 ArgInfo(args=['limit'], varargs=None, keywords=None, 
	locals={'local_variable': '..', 'limit': 2})
	1 ArgInfo(args=['limit'], varargs=None, keywords=None, 
	locals={'local_variable': '.', 'limit': 1})
	0 ArgInfo(args=['limit'], varargs=None, keywords=None, 
	locals={'local_variable': '', 'limit': 0})

.. {{{end}}}


Using :func:`stack`, it is also possible to access all of the stack
frames from the current frame to the first caller. This example is
similar to the one shown earlier, except it waits until reaching the
end of the recursion to print the stack information.

.. literalinclude:: inspect_stack.py
    :caption:
    :start-after: #end_pymotw_header

The last part of the output represents the main program, outside of the
:func:`recurse` function.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_stack.py', break_lines_at=65, line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 inspect_stack.py
	
	inspect_stack.py[10]
	  -> for level in inspect.stack():
	ArgInfo(args=[], varargs=None, keywords=None,
	locals={'src_index': 0, 'frame': <frame object at 0x10042ef88>,
	'line_num': 10, 'func': 'show_stack', 'level':
	FrameInfo(frame=<frame object at 0x10042ef88>,
	filename='inspect_stack.py', lineno=10, function='show_stack',
	code_context=['    for level in inspect.stack():\n'], index=0),
	'src_code': ['    for level in inspect.stack():\n'], 'filename':
	'inspect_stack.py'})
	
	inspect_stack.py[25]
	  -> show_stack()
	ArgInfo(args=['limit'], varargs=None, keywords=None,
	locals={'local_variable': '', 'limit': 0})
	
	inspect_stack.py[27]
	  -> recurse(limit - 1)
	ArgInfo(args=['limit'], varargs=None, keywords=None,
	locals={'local_variable': '.', 'limit': 1})
	
	inspect_stack.py[27]
	  -> recurse(limit - 1)
	ArgInfo(args=['limit'], varargs=None, keywords=None,
	locals={'local_variable': '..', 'limit': 2})
	
	inspect_stack.py[31]
	  -> recurse(2)
	ArgInfo(args=[], varargs=None, keywords=None,
	locals={'__cached__': None, '__package__': None, '__builtins__':
	<module 'builtins' (built-in)>, 'show_stack': <function
	show_stack at 0x101857f28>, 'recurse': <function recurse at
	0x101c8a620>, '__name__': '__main__', '__loader__':
	<_frozen_importlib_external.SourceFileLoader object at
	0x1018aa828>, '__file__': 'inspect_stack.py', 'inspect': <module
	'inspect' from '.../lib/python3.5/inspect.py'>, '__doc__':
	'Inspecting the call stack.\n', '__spec__': None})
	

.. {{{end}}}

There are other functions for building lists of frames in different
contexts, such as when an exception is being processed. See the
documentation for :func:`trace`, :func:`getouterframes`, and
:func:`getinnerframes` for more details.


.. seealso::

   * :pydoc:`inspect`

   * `Python 2.3 Method Resolution Order
     <http://www.python.org/download/releases/2.3/mro/>`__ --
     Documentation for the C3 Method Resolution order used by Python
     2.3 and later.

   * :mod:`pyclbr` -- The ``pyclbr`` module provides access to some of
     the same information as ``inspect`` by parsing the module without
     importing it.
