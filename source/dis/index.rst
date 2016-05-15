=====================================
 dis -- Python Bytecode Disassembler
=====================================

.. module:: dis
    :synopsis: Python Bytecode Disassembler

:Purpose: Convert code objects to a human-readable representation of the bytecodes for analysis.
:Python Version: 1.4 and later

The :mod:`dis` module includes functions for working with Python
bytecode by "disassembling" it into a more human-readable form.
Reviewing the bytecodes being executed by the interpreter is a good
way to hand-tune tight loops and perform other kinds of optimizations.
It is also useful for finding race conditions in multi-threaded
applications, since it can be used to estimate the point in the code
where thread control may switch.

.. warning::

   The use of bytecodes is a version-specific implementation detail of
   the CPython interpreter.  Refer to ``Include/opcode.h`` in the
   source code for the version of the interpreter you are using to
   find the canonical list of bytecodes.

Basic Disassembly
=================

The function :func:`dis` prints the disassembled representation of a
Python code source (module, class, method, function, or code object).
A module such as ``dis_simple.py`` can be disassembled by running
:mod:`dis` from the command line.

.. literalinclude:: dis_simple.py
    :linenos:

The output is organized into columns with the original source line
number, the instruction "address" within the code object, the opcode
name, and any arguments passed to the opcode.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m dis dis_simple.py'))
.. }}}

::

	$ python -m dis dis_simple.py
	
	  4           0 BUILD_MAP                1
	              3 LOAD_CONST               0 (1)
	              6 LOAD_CONST               1 ('a')
	              9 STORE_MAP           
	             10 STORE_NAME               0 (my_dict)
	             13 LOAD_CONST               2 (None)
	             16 RETURN_VALUE        

.. {{{end}}}

In this case, the source translates to five different operations to
create and populate the dictionary, then save the results to a local
variable.  Since the Python interpreter is stack-based, the first
steps are to put the constants onto the stack in the correct order
with :const:`LOAD_CONST`, and then use :const:`STORE_MAP` to pop off
the new key and value to be added to the dictionary.  The resulting
object is bound to the name "my_dict" with :const:`STORE_NAME`.


Disassembling Functions
=======================

Unfortunately, disassembling an entire module does not recurse into
functions automatically.

.. literalinclude:: dis_function.py
    :linenos:

The results of disassembling ``dis_function.py`` show the operations
for loading the function's code object onto the stack and then turning
it into a function (:const:`LOAD_CONST`, :const:`MAKE_FUNCTION`), but
*not* the body of the function.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m dis dis_function.py', break_lines_at=65))
.. }}}

::

	$ python -m dis dis_function.py
	
	  4           0 LOAD_CONST               0 (<code object f at 0x1
	00479030, file "dis_function.py", line 4>)
	              3 MAKE_FUNCTION            0
	              6 STORE_NAME               0 (f)
	
	  8           9 LOAD_NAME                1 (__name__)
	             12 LOAD_CONST               1 ('__main__')
	             15 COMPARE_OP               2 (==)
	             18 POP_JUMP_IF_FALSE       49
	
	  9          21 LOAD_CONST               2 (-1)
	             24 LOAD_CONST               3 (None)
	             27 IMPORT_NAME              2 (dis)
	             30 STORE_NAME               2 (dis)
	
	 10          33 LOAD_NAME                2 (dis)
	             36 LOAD_ATTR                2 (dis)
	             39 LOAD_NAME                0 (f)
	             42 CALL_FUNCTION            1
	             45 POP_TOP             
	             46 JUMP_FORWARD             0 (to 49)
	        >>   49 LOAD_CONST               3 (None)
	             52 RETURN_VALUE        

.. {{{end}}}

To see inside the function, it must be passed to :func:`dis`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'dis_function.py'))
.. }}}

::

	$ python dis_function.py
	
	  5           0 LOAD_GLOBAL              0 (len)
	              3 LOAD_FAST                0 (args)
	              6 CALL_FUNCTION            1
	              9 STORE_FAST               1 (nargs)
	
	  6          12 LOAD_FAST                1 (nargs)
	             15 PRINT_ITEM          
	             16 LOAD_FAST                0 (args)
	             19 PRINT_ITEM          
	             20 PRINT_NEWLINE       
	             21 LOAD_CONST               0 (None)
	             24 RETURN_VALUE        

.. {{{end}}}


Classes
=======

Classes can be passed to :func:`dis`, in which case all of the methods
are disassembled in turn.

.. literalinclude:: dis_class.py
    :linenos:

The methods are listed in alphabetical order, not the order they
appear in the file.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'dis_class.py'))
.. }}}

::

	$ python dis_class.py
	
	Disassembly of __init__:
	 15           0 LOAD_FAST                1 (name)
	              3 LOAD_FAST                0 (self)
	              6 STORE_ATTR               0 (name)
	              9 LOAD_CONST               0 (None)
	             12 RETURN_VALUE        
	
	Disassembly of __str__:
	 12           0 LOAD_CONST               1 ('MyObject(%s)')
	              3 LOAD_FAST                0 (self)
	              6 LOAD_ATTR                0 (name)
	              9 BINARY_MODULO       
	             10 RETURN_VALUE        
	

.. {{{end}}}


Using Disassembly to Debug
==========================

Sometimes when debugging an exception it can be useful to see which
bytecode caused a problem.  There are a couple of ways to disassemble
the code around an error.  The first is by using :func:`dis` in the
interactive interpreter to report about the last exception.  If no
argument is passed to :func:`dis`, then it looks for an exception and
shows the disassembly of the top of the stack that caused it.

::

    $ python

    Python 2.6.2 (r262:71600, Apr 16 2009, 09:17:39) 
    [GCC 4.0.1 (Apple Computer, Inc. build 5250)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import dis
    >>> j = 4
    >>> i = i + 4
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    NameError: name 'i' is not defined
    >>> dis.distb()
      1 -->       0 LOAD_NAME                0 (i)
                  3 LOAD_CONST               0 (4)
                  6 BINARY_ADD          
                  7 STORE_NAME               0 (i)
                 10 LOAD_CONST               1 (None)
                 13 RETURN_VALUE        
    >>>

The ``-->`` after the line number indicates the opcode that caused the
error.  There is no ``i`` variable defined, so the value associated
with the name cannot be loaded onto the stack.

A program can also print the information about an active traceback by
passing it to :func:`distb` directly.  In this example, there is a
:class:`DivideByZero` exception, but since the formula has two
divisions it is not clear which part is zero.

.. literalinclude:: dis_traceback.py
    :linenos:

The bad value is easy to spot when it is loaded onto the stack in the
disassembled version.  The bad operation is highlighted with the
``-->``, and the previous line pushes the value for ``j`` onto the
stack.

.. {{{cog
.. results = run_script(cog.inFile, 'dis_traceback.py').splitlines()
.. cog.out('\n'.join(results[:26]))
.. cog.out('\n\n    ...trimmed...\n\n')
.. }}}

::

	$ python dis_traceback.py
	
	  4           0 LOAD_CONST               0 (1)
	              3 STORE_NAME               0 (i)
	
	  5           6 LOAD_CONST               1 (0)
	              9 STORE_NAME               1 (j)
	
	  6          12 LOAD_CONST               2 (3)
	             15 STORE_NAME               2 (k)
	
	 10          18 SETUP_EXCEPT            26 (to 47)
	
	 11          21 LOAD_NAME                2 (k)
	             24 LOAD_NAME                0 (i)
	             27 LOAD_NAME                1 (j)
	    -->      30 BINARY_DIVIDE       
	             31 BINARY_MULTIPLY     
	             32 LOAD_NAME                0 (i)
	             35 LOAD_NAME                2 (k)
	             38 BINARY_DIVIDE       
	             39 BINARY_ADD          
	             40 STORE_NAME               3 (result)

    ...trimmed...

.. {{{end}}}


Performance Analysis of Loops
=============================

Besides debugging errors, :mod:`dis` can also help identify
performance issues. Examining the disassembled code is especially
useful with tight loops where the number of Python instructions is low
but they translate to an inefficient set of bytecodes.  The
helpfulness of the disassembly can be seen by examining a few
different implementations of a class, :class:`Dictionary`, that reads
a list of words and groups them by their first letter.

.. include:: dis_test_loop.py
    :literal:
    :start-after: #end_pymotw_header

The test driver application ``dis_test_loop.py`` can be used to run
each incarnation of the :class:`Dictionary` class.

A straightforward, but slow, implementation of :class:`Dictionary`
starts out like this:

.. literalinclude:: dis_slow_loop.py
    :linenos:

Running the test program with this version shows the disassembled
program and the amount of time it takes to run.

.. timing values are sensitive to other operations, so don't cog

::

	$ python dis_test_loop.py dis_slow_loop

	 11           0 SETUP_LOOP              84 (to 87)
	              3 LOAD_FAST                1 (words)
	              6 GET_ITER            
	        >>    7 FOR_ITER                76 (to 86)
	             10 STORE_FAST               2 (word)
	
	 12          13 SETUP_EXCEPT            28 (to 44)
	
	 13          16 LOAD_FAST                0 (self)
	             19 LOAD_ATTR                0 (by_letter)
	             22 LOAD_FAST                2 (word)
	             25 LOAD_CONST               1 (0)
	             28 BINARY_SUBSCR       
	             29 BINARY_SUBSCR       
	             30 LOAD_ATTR                1 (append)
	             33 LOAD_FAST                2 (word)
	             36 CALL_FUNCTION            1
	             39 POP_TOP             
	             40 POP_BLOCK           
	             41 JUMP_ABSOLUTE            7
	
	 14     >>   44 DUP_TOP             
	             45 LOAD_GLOBAL              2 (KeyError)
	             48 COMPARE_OP              10 (exception match)
	             51 JUMP_IF_FALSE           27 (to 81)
	             54 POP_TOP             
	             55 POP_TOP             
	             56 POP_TOP             
	             57 POP_TOP             
	
	 15          58 LOAD_FAST                2 (word)
	             61 BUILD_LIST               1
	             64 LOAD_FAST                0 (self)
	             67 LOAD_ATTR                0 (by_letter)
	             70 LOAD_FAST                2 (word)
	             73 LOAD_CONST               1 (0)
	             76 BINARY_SUBSCR       
	             77 STORE_SUBSCR        
	             78 JUMP_ABSOLUTE            7
	        >>   81 POP_TOP             
	             82 END_FINALLY         
	             83 JUMP_ABSOLUTE            7
	        >>   86 POP_BLOCK           
	        >>   87 LOAD_CONST               0 (None)
	             90 RETURN_VALUE        
	
	TIME: 0.1074

The previous output shows ``dis_slow_loop.py`` taking 0.1074 seconds
to load the 234936 words in the copy of ``/usr/share/dict/words`` on
OS X.  That is not too bad, but the accompanying disassembly shows that
the loop is doing more work than it needs to.  As it enters the loop
in opcode 13, it sets up an exception context (:const:`SETUP_EXCEPT`).
Then it takes six opcodes to find ``self.by_letter[word[0]]`` before
appending ``word`` to the list.  If there is an exception because
``word[0]`` is not in the dictionary yet, the exception handler does
all of the same work to determine ``word[0]`` (three opcodes) and sets
``self.by_letter[word[0]]`` to a new list containing the word.

One technique to eliminate the exception setup is to pre-populate
``self.by_letter`` with one list for each letter of the alphabet.
That means the list for the new word should always be found, and the
value can be saved after the lookup.


.. literalinclude:: dis_faster_loop.py
    :linenos:

The change cuts the number of opcodes in half, but only shaves the
time down to 0.0984 seconds.  Obviously the exception handling had
some overhead, but not a huge amount.

.. timing values are sensitive to other operations, so don't cog

::

	$ python dis_test_loop.py dis_faster_loop

	 14           0 SETUP_LOOP              38 (to 41)
	              3 LOAD_FAST                1 (words)
	              6 GET_ITER            
	        >>    7 FOR_ITER                30 (to 40)
	             10 STORE_FAST               2 (word)
	
	 15          13 LOAD_FAST                0 (self)
	             16 LOAD_ATTR                0 (by_letter)
	             19 LOAD_FAST                2 (word)
	             22 LOAD_CONST               1 (0)
	             25 BINARY_SUBSCR       
	             26 BINARY_SUBSCR       
	             27 LOAD_ATTR                1 (append)
	             30 LOAD_FAST                2 (word)
	             33 CALL_FUNCTION            1
	             36 POP_TOP             
	             37 JUMP_ABSOLUTE            7
	        >>   40 POP_BLOCK           
	        >>   41 LOAD_CONST               0 (None)
	             44 RETURN_VALUE        
	
	TIME: 0.0984

The performance can be improved further by moving the lookup for
``self.by_letter`` outside of the loop (the value does not change,
after all).

.. literalinclude:: dis_fastest_loop.py
    :linenos:

Opcodes 0-6 now find the value of ``self.by_letter`` and save it as a
local variable ``by_letter``.  Using a local variable only takes a
single opcode, instead of two (statement 22 uses :const:`LOAD_FAST` to
place the dictionary onto the stack).  After this change, the run time
is down to 0.0842 seconds.

.. timing values are sensitive to other operations, so don't cog

::

	$ python dis_test_loop.py dis_fastest_loop

	 13           0 LOAD_FAST                0 (self)
	              3 LOAD_ATTR                0 (by_letter)
	              6 STORE_FAST               2 (by_letter)
	
	 14           9 SETUP_LOOP              35 (to 47)
	             12 LOAD_FAST                1 (words)
	             15 GET_ITER            
	        >>   16 FOR_ITER                27 (to 46)
	             19 STORE_FAST               3 (word)
	
	 15          22 LOAD_FAST                2 (by_letter)
	             25 LOAD_FAST                3 (word)
	             28 LOAD_CONST               1 (0)
	             31 BINARY_SUBSCR       
	             32 BINARY_SUBSCR       
	             33 LOAD_ATTR                1 (append)
	             36 LOAD_FAST                3 (word)
	             39 CALL_FUNCTION            1
	             42 POP_TOP             
	             43 JUMP_ABSOLUTE           16
	        >>   46 POP_BLOCK           
	        >>   47 LOAD_CONST               0 (None)
	             50 RETURN_VALUE        
	
	TIME: 0.0842

A further optimization, suggested by Brandon Rhodes, is to eliminate
the Python version of the ``for`` loop entirely. If
:func:`itertools.groupby` is used to arrange the input, the iteration
is moved to C.  This is safe because the inputs are known to be
sorted.  If that was not the case, the program would need to sort them
first.

.. literalinclude:: dis_eliminate_loop.py
    :linenos:

The :mod:`itertools` version takes only 0.0543 seconds to run, just
over half of the original time.

.. timing values are sensitive to other operations, so don't cog

::

	$ python dis_test_loop.py dis_eliminate_loop

	 15           0 LOAD_GLOBAL              0 (itertools)
	              3 LOAD_ATTR                1 (groupby)
	              6 LOAD_FAST                1 (words)
	              9 LOAD_CONST               1 ('key')
	             12 LOAD_GLOBAL              2 (operator)
	             15 LOAD_ATTR                3 (itemgetter)
	             18 LOAD_CONST               2 (0)
	             21 CALL_FUNCTION            1
	             24 CALL_FUNCTION          257
	             27 STORE_FAST               2 (grouped)
	
	 17          30 LOAD_GLOBAL              4 (dict)
	             33 LOAD_CONST               3 (<code object 
    <genexpr> at 0x7e7b8, file "dis_eliminate_loop.py", line 17>)
	             36 MAKE_FUNCTION            0
	             39 LOAD_FAST                2 (grouped)
	             42 GET_ITER            
	             43 CALL_FUNCTION            1
	             46 CALL_FUNCTION            1
	             49 LOAD_FAST                0 (self)
	             52 STORE_ATTR               5 (by_letter)
	             55 LOAD_CONST               0 (None)
	             58 RETURN_VALUE        
	
	TIME: 0.0543


Compiler Optimizations
======================

Disassembling compiled source also exposes some of the optimizations
made by the compiler.  For example, literal expressions are folded
during compilation, when possible.

.. literalinclude:: dis_constant_folding.py
    :linenos:

None of the values in the expressions on lines 5-7 can change the way
the operation is performed, so the result of the expressions can be
computed at compilation time and collapsed into single
:const:`LOAD_CONST` instructions.  That is not true about lines
10-12. Because a variable is involved in those expressions, and the
variable might refer to an object that overloads the operator
involved, the evaluation has to be delayed to runtime.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m dis dis_constant_folding.py'))
.. }}}

::

	$ python -m dis dis_constant_folding.py
	
	  5           0 LOAD_CONST              11 (3)
	              3 STORE_NAME               0 (i)
	
	  6           6 LOAD_CONST              12 (19.04)
	              9 STORE_NAME               1 (f)
	
	  7          12 LOAD_CONST              13 ('Hello, World!')
	             15 STORE_NAME               2 (s)
	
	 10          18 LOAD_NAME                0 (i)
	             21 LOAD_CONST               6 (3)
	             24 BINARY_MULTIPLY     
	             25 LOAD_CONST               7 (4)
	             28 BINARY_MULTIPLY     
	             29 STORE_NAME               3 (I)
	
	 11          32 LOAD_NAME                1 (f)
	             35 LOAD_CONST               1 (2)
	             38 BINARY_DIVIDE       
	             39 LOAD_CONST               6 (3)
	             42 BINARY_DIVIDE       
	             43 STORE_NAME               4 (F)
	
	 12          46 LOAD_NAME                2 (s)
	             49 LOAD_CONST               8 ('\n')
	             52 BINARY_ADD          
	             53 LOAD_CONST               9 ('Fantastic!')
	             56 BINARY_ADD          
	             57 STORE_NAME               5 (S)
	             60 LOAD_CONST              10 (None)
	             63 RETURN_VALUE        

.. {{{end}}}


.. seealso::

    `dis <http://docs.python.org/library/dis.html>`_
        The standard library documentation for this module, including
        the list of `bytecode instructions
        <http://docs.python.org/library/dis.html#python-bytecode-instructions>`_.

    ``Include/opcode.h``
        The source code for the CPython interpreter defines the byte
        codes in ``opcode.h``.

    *Python Essential Reference*, 4th Edition, David M. Beazley
        http://www.informit.com/store/product.aspx?isbn=0672329786

    `thomas.apestaart.org "Python Disassembly" <http://thomas.apestaart.org/log/?p=927>`_
        A short discussion of the difference between storing values in
        a dictionary between Python 2.5 and 2.6.

    `Why is looping over range() in Python faster than using a while loop? <http://stackoverflow.com/questions/869229/why-is-looping-over-range-in-python-faster-than-using-a-while-loop>`_
        A discussion on StackOverflow.com comparing 2 looping examples
        via their disassembled bytecodes.

    `Decorator for binding constants at compile time <http://code.activestate.com/recipes/277940/>`_
        Python Cookbook recipe by Raymond Hettinger and Skip Montanaro
        with a function decorator that re-writes the bytecodes for a
        function to insert global constants to avoid runtime name
        lookups.
