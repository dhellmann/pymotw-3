==================================
 inspect --- Inspect Live Objects
==================================

.. module:: inspect
    :synopsis: Inspect live objects

The ``inspect`` module provides functions for learning about live
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

Inspecting Modules
==================

The first kind of introspection probes live objects to learn about
them. Use ``getmembers()`` to discover the member attributes of
object.  The types of members that might be returned depend on the
type of object scanned. Modules can contain classes and functions;
classes can contain methods and attributes; and so on.

The arguments to ``getmembers()`` are an object to scan (a module,
class, or instance) and an optional predicate function that is used to
filter the objects returned. The return value is a list of tuples with
two values: the name of the member, and the type of the member. The
``inspect`` module includes several such predicate functions with
names like ``ismodule()``, ``isclass()``, etc.

.. literalinclude:: inspect_getmembers_module.py
    :caption:
    :start-after: #end_pymotw_header

This sample prints the members of the ``example`` module. Modules have
several private attributes that are used as part of the import
implementation as well as a set of ``__builtins__``.  All of these
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
	instance_of_a : <example.A object at 0x1014814a8>
	module_level_function : <function module_level_function at
	0x10148bc80>

.. {{{end}}}

The ``predicate`` argument can be used to filter the types of objects
returned.

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

Classes are scanned using ``getmembers()`` in the same way as
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
	0x101c99510>,
	                '__module__': 'example',
	                '__weakref__': <attribute '__weakref__' of 'A'
	objects>,
	                'get_name': <function A.get_name at
	0x101c99598>})),
	 ('__dir__', <method '__dir__' of 'object' objects>),
	 ('__doc__', 'The A class.'),
	 ('__eq__', <slot wrapper '__eq__' of 'object' objects>),
	 ('__format__', <method '__format__' of 'object' objects>),
	 ('__ge__', <slot wrapper '__ge__' of 'object' objects>),
	 ('__getattribute__',
	  <slot wrapper '__getattribute__' of 'object' objects>),
	 ('__gt__', <slot wrapper '__gt__' of 'object' objects>),
	 ('__hash__', <slot wrapper '__hash__' of 'object' objects>),
	 ('__init__', <function A.__init__ at 0x101c99510>),
	 ('__le__', <slot wrapper '__le__' of 'object' objects>),
	 ('__lt__', <slot wrapper '__lt__' of 'object' objects>),
	 ('__module__', 'example'),
	 ('__ne__', <slot wrapper '__ne__' of 'object' objects>),
	 ('__new__',
	  <built-in method __new__ of type object at 0x10022bb20>),
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
	0x10061fba8>),
	 ('__weakref__', <attribute '__weakref__' of 'A' objects>),
	 ('get_name', <function A.get_name at 0x101c99598>)]

.. {{{end}}}

To find the methods of a class, use the ``isfunction()``
predicate. The ``ismethod()`` predicate only recognizes bound
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
	
	[('__init__', <function A.__init__ at 0x10139d510>),
	 ('get_name', <function A.get_name at 0x10139d598>)]

.. {{{end}}}

The output for ``B`` includes the override for ``get_name()``
as well as the new method, and the inherited ``__init__()`` method
implemented in ``A``.

.. literalinclude:: inspect_getmembers_class_methods_b.py
    :caption:
    :start-after: #end_pymotw_header

Methods inherited from ``A``, such as ``__init__()``, are
identified as being methods of ``B``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getmembers_class_methods_b.py'))
.. }}}

.. code-block:: none

	$ python3 inspect_getmembers_class_methods_b.py
	
	[('__init__', <function A.__init__ at 0x10129d510>),
	 ('do_something', <function B.do_something at 0x10129d620>),
	 ('get_name', <function B.get_name at 0x10129d6a8>)]

.. {{{end}}}

Inspecting Instances
====================

Introspecting instances works in the same way as other objects.

.. literalinclude:: inspect_getmembers_instance.py
   :caption:
   :start-after: #end_pymotw_header

The predicate ``ismethod()`` recognizes two bound methods from
``A`` in the example instance.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_getmembers_instance.py'))
.. }}}

.. code-block:: none

	$ python3 inspect_getmembers_instance.py
	
	[('__init__', <bound method A.__init__ of <example.A object at 0
	x101ab1ba8>>),
	 ('get_name', <bound method A.get_name of <example.A object at 0
	x101ab1ba8>>)]

.. {{{end}}}

Documentation Strings
=====================

The docstring for an object can be retrieved with
``getdoc()``. The return value is the :attr:`__doc__` attribute
with tabs expanded to spaces and with indentation made uniform.

.. literalinclude:: inspect_getdoc.py
    :caption:
    :start-after: #end_pymotw_header

The second line of the docstring is indented when it is retrieved
through the attribute directly, but moved to the left margin by
``getdoc()``.

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
source is available. The ``getcomments()`` function looks at the
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

When a module is passed to ``getcomments()``, the return value is
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
``getsource()`` and ``getsourcelines()``.

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
to ``getsource()``.

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

Use ``getsourcelines()`` instead of ``getsource()`` to
retrieve the lines of source split into individual strings.

.. literalinclude:: inspect_getsourcelines_method.py
    :caption:
    :start-after: #end_pymotw_header

The return value from ``getsourcelines()`` is a ``tuple`` containing a
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
	 23)

.. {{{end}}}

If the source file is not available, ``getsource()`` and
``getsourcelines()`` raise an ``IOError``.

Method and Function Signatures
==============================

In addition to the documentation for a function or method, it is
possible to ask for a complete specification of the arguments the
callable takes, including default values. The ``signature()``
function returns a ``Signature`` instance containing information
about the arguments to the function.

.. literalinclude:: inspect_signature_function.py
    :caption:
    :start-after: #end_pymotw_header

The function arguments are available through the ``parameters``
attribute of the ``Signature``. ``parameters`` is an ordered
dictionary mapping the parameter names to ``Parameter`` instances
describing the argument.  In this example, the first argument to the
function, ``arg1``, does not have a default value, while ``arg2`` does.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_signature_function.py'))
.. }}}

.. code-block:: none

	$ python3 inspect_signature_function.py
	
	module_level_function(arg1, arg2='default', *args, **kwargs)
	
	Parameter details:
	  arg1
	  arg2='default'
	  *args
	  **kwargs

.. {{{end}}}

The ``Signature`` for a function can be used by decorators or
other functions to validate inputs, provide different defaults, etc.
Writing a suitably generic and reusable validation decorator has one
special challenge, though, because it can be complicated to match up
incoming arguments with their names for functions that accept a
combination of named and positional arguments. The ``bind()`` and
``bind_partial()`` methods provide the necessary logic to handle the
mapping.  They return a ``BoundArguments`` instance populated
with the arguments associated with the names of the arguments of a
specified function.

.. literalinclude:: inspect_signature_bind.py
   :caption:
   :start-after: #end_pymotw_header

The ``BoundArguments`` instance has attributes ``args`` and
``kwargs`` that can be used to call the function using the syntax to
expand the tuple and dictionary onto the stack as the arguments.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_signature_bind.py'))
.. }}}

.. code-block:: none

	$ python3 inspect_signature_bind.py
	
	Arguments:
	arg1 = 'this is arg1'
	arg2 = 'this is arg2'
	args = ('this is an extra positional argument',)
	kwargs = {'extra_named_arg': 'value'}
	
	Calling:
	this is arg1this is arg1

.. {{{end}}}

If only some arguments are available, ``bind_partial()`` will still
create a ``BoundArguments`` instance. It may not be fully usable
until the remaining arguments are added.

.. literalinclude:: inspect_signature_bind_partial.py
   :caption:
   :start-after: #end_pymotw_header

``apply_defaults()`` will add any values from the parameter
defaults.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_signature_bind_partial.py'))
.. }}}

.. code-block:: none

	$ python3 inspect_signature_bind_partial.py
	
	Without defaults:
	arg1 = 'this is arg1'
	
	With defaults:
	arg1 = 'this is arg1'
	arg2 = 'default'
	args = ()
	kwargs = {}

.. {{{end}}}

Class Hierarchies
=================

``inspect`` includes two methods for working directly with class
hierarchies. The first, ``getclasstree()``, creates a tree-like
data structure based on the classes it is given and their base
classes. Each element in the list returned is either a tuple with a
class and its base classes, or another list containing tuples for
subclasses.

.. literalinclude:: inspect_getclasstree.py
    :caption:
    :start-after: #end_pymotw_header

The output from this example is the tree of inheritance for the ``A``,
``B``, ``C``, and ``D`` classes.  ``D`` appears twice, since it
inherits from both ``C`` and ``A``.

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

If ``getclasstree()`` is called with ``unique`` set to a true value,
the output is different.

.. literalinclude:: inspect_getclasstree_unique.py
    :caption:
    :start-after: #end_pymotw_header

This time, ``D`` only appears in the output once:

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
``getmro()``, which returns a ``tuple`` of classes in the
order they should be scanned when resolving an attribute that might be
inherited from a base class using the *Method Resolution Order*
(MRO). Each class in the sequence appears only once.

.. literalinclude:: inspect_getmro.py
    :caption:
    :start-after: #end_pymotw_header

This output demonstrates the "depth-first" nature of the MRO
search. For ``B_First``, ``A`` also comes before ``C``
in the search order, because ``B`` is derived from ``A``.

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

In addition to introspection of code objects, ``inspect`` includes
functions for inspecting the runtime environment while a program is
being executed. Most of these functions work with the call stack, and
operate on *call frames*. Frame objects hold the current execution
context, including references to the code being run, the operation
being executed, as well as the values of local and global variables.
Typically such information is used to build tracebacks when exceptions
are raised. It can also be useful for logging or when debugging
programs, since the stack frames can be interrogated to discover the
argument values passed into the functions.

``currentframe()`` returns the frame at the top of the stack (for
the current function).

.. literalinclude:: inspect_currentframe.py
    :caption:
    :start-after: #end_pymotw_header

The values of the arguments to ``recurse()`` are included in the
frame's dictionary of local variables.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_currentframe.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 inspect_currentframe.py
	
	line 14 of inspect_currentframe.py
	locals:
	{'frame': <frame object at 0x1022a7b88>,
	 'keyword': 'changed value of argument',
	 'kwonly': 'must be named',
	 'limit': 2,
	 'local_variable': '..'}
	
	line 14 of inspect_currentframe.py
	locals:
	{'frame': <frame object at 0x102016b28>,
	 'keyword': 'changed value of argument',
	 'kwonly': 'must be named',
	 'limit': 1,
	 'local_variable': '.'}
	
	line 14 of inspect_currentframe.py
	locals:
	{'frame': <frame object at 0x1020176b8>,
	 'keyword': 'changed value of argument',
	 'kwonly': 'must be named',
	 'limit': 0,
	 'local_variable': ''}
	

.. {{{end}}}


Using ``stack()``, it is also possible to access all of the stack
frames from the current frame to the first caller. This example is
similar to the one shown earlier, except it waits until reaching the
end of the recursion to print the stack information.

.. literalinclude:: inspect_stack.py
    :caption:
    :start-after: #end_pymotw_header

The last part of the output represents the main program, outside of the
``recurse()`` function.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'inspect_stack.py', break_lines_at=65, line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 inspect_stack.py
	
	inspect_stack.py[11]
	  -> for level in inspect.stack():
	{'level': FrameInfo(frame=<frame object at 0x10127e5d0>,
	filename='inspect_stack.py', lineno=11, function='show_stack',
	code_context=['    for level in inspect.stack():\n'], index=0)}
	
	inspect_stack.py[24]
	  -> show_stack()
	{'limit': 0, 'local_variable': ''}
	
	inspect_stack.py[26]
	  -> recurse(limit - 1)
	{'limit': 1, 'local_variable': '.'}
	
	inspect_stack.py[26]
	  -> recurse(limit - 1)
	{'limit': 2, 'local_variable': '..'}
	
	inspect_stack.py[30]
	  -> recurse(2)
	{'__builtins__': <module 'builtins' (built-in)>,
	 '__cached__': None,
	 '__doc__': 'Inspecting the call stack.\n',
	 '__file__': 'inspect_stack.py',
	 '__loader__': <_frozen_importlib_external.SourceFileLoader
	object at 0x1007a97f0>,
	 '__name__': '__main__',
	 '__package__': None,
	 '__spec__': None,
	 'inspect': <module 'inspect' from
	'.../lib/python3.5/inspect.py'>,
	 'pprint': <module 'pprint' from '.../lib/python3.5/pprint.py'>,
	 'recurse': <function recurse at 0x1012aa400>,
	 'show_stack': <function show_stack at 0x1007a6a60>}
	

.. {{{end}}}

There are other functions for building lists of frames in different
contexts, such as when an exception is being processed. See the
documentation for ``trace()``, ``getouterframes()``, and
``getinnerframes()`` for more details.

Command Line Interface
======================

The ``inspect`` module also includes a command line interface for
getting details about objects without having to write out the calls in
a separate Python program. The input is a module name and optional
object from within the module.  The default output is the source code
for the named object. Using the ``--details`` argument causes metadata
to be printed instead of the source.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m inspect -d example'))
.. cog.out(run_script(cog.inFile, '-m inspect -d example:A', include_prefix=False))
.. cog.out(run_script(cog.inFile, '-m inspect example:A.get_name', include_prefix=False))
.. }}}

.. code-block:: none

	$ python3 -m inspect -d example
	
	Target: example
	Origin: .../example.py
	Cached: .../__pycache__/example.cpython-35.pyc
	Loader: <_frozen_importlib_external.SourceFileLoader object at 0
	x101527860>
	
	

	$ python3 -m inspect -d example:A
	
	Target: example:A
	Origin: .../example.py
	Cached: .../__pycache__/example.cpython-35.pyc
	Line: 16
	
	

	$ python3 -m inspect example:A.get_name
	
	    def get_name(self):
	        "Returns the name of the instance."
	        return self.name
	

.. {{{end}}}

.. seealso::

   * :pydoc:`inspect`

   * :ref:`Python 2 to 3 porting notes for inspect <porting-inspect>`

   * `Python 2.3 Method Resolution Order
     <http://www.python.org/download/releases/2.3/mro/>`__ --
     Documentation for the C3 Method Resolution order used by Python
     2.3 and later.

   * :mod:`pyclbr` -- The ``pyclbr`` module provides access to some of
     the same information as ``inspect`` by parsing the module without
     importing it.

   * :pep:`362` -- Function Signature Object
