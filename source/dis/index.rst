======================================
 dis --- Python Bytecode Disassembler
======================================

.. module:: dis
    :synopsis: Python Bytecode Disassembler

The ``dis`` module includes functions for working with Python
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

The function ``dis()`` prints the disassembled representation of a
Python code source (module, class, method, function, or code object).
A module such as ``dis_simple.py`` can be disassembled by running
``dis`` from the command line.

.. cssclass:: with-linenos

   .. literalinclude:: dis_simple.py
      :linenos:
      :caption:

The output is organized into columns with the original source line
number, the instruction "address" within the code object, the opcode
name, and any arguments passed to the opcode.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m dis dis_simple.py'))
.. }}}

.. code-block:: none

	$ python3 -m dis dis_simple.py
	
	  4           0 LOAD_CONST               0 ('a')
	              3 LOAD_CONST               1 (1)
	              6 BUILD_MAP                1
	              9 STORE_NAME               0 (my_dict)
	             12 LOAD_CONST               2 (None)
	             15 RETURN_VALUE

.. {{{end}}}

In this case, the source translates to four different operations to
create and populate the dictionary, then save the results to a local
variable.  Since the Python interpreter is stack-based, the first
steps are to put the constants onto the stack in the correct order
with :const:`LOAD_CONST`, and then use :const:`BUILD_MAP` to pop off
the new key and value to be added to the dictionary.  The resulting
:class:`dict` object is bound to the name ``my_dict`` with
:const:`STORE_NAME`.


Disassembling Functions
=======================

Unfortunately, disassembling an entire module does not recurse into
functions automatically.

.. cssclass:: with-linenos

   .. literalinclude:: dis_function.py
      :linenos:
      :caption:

The results of disassembling ``dis_function.py`` show the operations
for loading the function's code object onto the stack and then turning
it into a function (:const:`LOAD_CONST`, :const:`MAKE_FUNCTION`), but
*not* the body of the function.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m dis dis_function.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 -m dis dis_function.py
	
	  5           0 LOAD_CONST               0 (<code object f at
	0x10141ba50, file "dis_function.py", line 5>)
	              3 LOAD_CONST               1 ('f')
	              6 MAKE_FUNCTION            0
	              9 STORE_NAME               0 (f)
	
	 10          12 LOAD_NAME                1 (__name__)
	             15 LOAD_CONST               2 ('__main__')
	             18 COMPARE_OP               2 (==)
	             21 POP_JUMP_IF_FALSE       49
	
	 11          24 LOAD_CONST               3 (0)
	             27 LOAD_CONST               4 (None)
	             30 IMPORT_NAME              2 (dis)
	             33 STORE_NAME               2 (dis)
	
	 12          36 LOAD_NAME                2 (dis)
	             39 LOAD_ATTR                2 (dis)
	             42 LOAD_NAME                0 (f)
	             45 CALL_FUNCTION            1 (1 positional, 0
	keyword pair)
	             48 POP_TOP
	        >>   49 LOAD_CONST               4 (None)
	             52 RETURN_VALUE

.. {{{end}}}

To see inside the function, the function itself must be passed to
``dis()``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'dis_function.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 dis_function.py
	
	  6           0 LOAD_GLOBAL              0 (len)
	              3 LOAD_FAST                0 (args)
	              6 CALL_FUNCTION            1 (1 positional, 0
	keyword pair)
	              9 STORE_FAST               1 (nargs)
	
	  7          12 LOAD_GLOBAL              1 (print)
	             15 LOAD_FAST                1 (nargs)
	             18 LOAD_FAST                0 (args)
	             21 CALL_FUNCTION            2 (2 positional, 0
	keyword pair)
	             24 POP_TOP
	             25 LOAD_CONST               0 (None)
	             28 RETURN_VALUE

.. {{{end}}}

To print a summary of the function, including information about the
arguments and names it uses, call :func:`show_code`, passing the
function as the first argument.

.. literalinclude:: dis_show_code.py

The argument to :func:`show_code` is passed to :func:`code_info`,
which returns a nicely formatted summary of the function, method, code
string, or other code object, ready to be printed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'dis_show_code.py'))
.. }}}

.. code-block:: none

	$ python3 dis_show_code.py
	
	Name:              f
	Filename:          dis_show_code.py
	Argument count:    0
	Kw-only arguments: 0
	Number of locals:  2
	Stack size:        3
	Flags:             OPTIMIZED, NEWLOCALS, VARARGS, NOFREE
	Constants:
	   0: None
	Names:
	   0: len
	   1: print
	Variable names:
	   0: args
	   1: nargs

.. {{{end}}}

Classes
=======

Classes can be passed to ``dis()``, in which case all of the methods
are disassembled in turn.

.. cssclass:: with-linenos

   .. literalinclude:: dis_class.py
      :linenos:
      :caption:

The methods are listed in alphabetical order, not the order they
appear in the file.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'dis_class.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 dis_class.py
	
	Disassembly of __init__:
	 16           0 LOAD_FAST                1 (name)
	              3 LOAD_FAST                0 (self)
	              6 STORE_ATTR               0 (name)
	              9 LOAD_CONST               0 (None)
	             12 RETURN_VALUE
	
	Disassembly of __str__:
	 13           0 LOAD_CONST               1 ('MyObject({})')
	              3 LOAD_ATTR                0 (format)
	              6 LOAD_FAST                0 (self)
	              9 LOAD_ATTR                1 (name)
	             12 CALL_FUNCTION            1 (1 positional, 0
	keyword pair)
	             15 RETURN_VALUE
	

.. {{{end}}}

Source Code
===========

It is often more convenient to work with the source code for a program
than with the code objects themselves. The functions in ``dis``
accept string arguments containing source code, and convert them to
code objects before producing the disassembly or other output.

.. literalinclude:: dis_string.py
   :caption:
   :start-after: #end_pymotw_header

Passing a string lets you save the step of compiling the code and
holding a reference to the results yourself, which is more convenient
in cases when statements outside of a function are being examined.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'dis_string.py'))
.. }}}

.. code-block:: none

	$ python3 dis_string.py
	
	Disassembly:
	
	  2           0 LOAD_CONST               0 ('a')
	              3 LOAD_CONST               1 (1)
	              6 BUILD_MAP                1
	              9 STORE_NAME               0 (my_dict)
	             12 LOAD_CONST               2 (None)
	             15 RETURN_VALUE
	
	Code details:
	
	Name:              <module>
	Filename:          <disassembly>
	Argument count:    0
	Kw-only arguments: 0
	Number of locals:  0
	Stack size:        2
	Flags:             NOFREE
	Constants:
	   0: 'a'
	   1: 1
	   2: None
	Names:
	   0: my_dict

.. {{{end}}}


Using Disassembly to Debug
==========================

Sometimes when debugging an exception it can be useful to see which
bytecode caused a problem.  There are a couple of ways to disassemble
the code around an error.  The first is by using ``dis()`` in the
interactive interpreter to report about the last exception.  If no
argument is passed to ``dis()``, then it looks for an exception and
shows the disassembly of the top of the stack that caused it.

.. code-block:: none

    $ python3
    Python 3.5.1 (v3.5.1:37a07cee5969, Dec  5 2015, 21:12:44)
    [GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import dis
    >>> j = 4
    >>> i = i + 4
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    NameError: name 'i' is not defined
    >>> dis.dis()
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
divisions it may not be clear which part is zero.

.. cssclass:: with-linenos

   .. literalinclude:: dis_traceback.py
      :linenos:
      :caption:

The bad value is easy to spot when it is loaded onto the stack in the
disassembled version.  The bad operation is highlighted with the
``-->``, and the previous line pushes the value for ``j`` onto the
stack.

.. {{{cog
.. results = run_script(cog.inFile, 'dis_traceback.py').splitlines()
.. cog.out('\n'.join(results[:26]))
.. cog.out('\n\n    ...trimmed...\n\n')
.. }}}

.. code-block:: none

	$ python3 dis_traceback.py
	
	  4           0 LOAD_CONST               0 (1)
	              3 STORE_NAME               0 (i)
	
	  5           6 LOAD_CONST               1 (0)
	              9 STORE_NAME               1 (j)
	
	  6          12 LOAD_CONST               2 (3)
	             15 STORE_NAME               2 (k)
	
	  8          18 SETUP_EXCEPT            26 (to 47)
	
	  9          21 LOAD_NAME                2 (k)
	             24 LOAD_NAME                0 (i)
	             27 LOAD_NAME                1 (j)
	    -->      30 BINARY_TRUE_DIVIDE
	             31 BINARY_MULTIPLY
	             32 LOAD_NAME                0 (i)
	             35 LOAD_NAME                2 (k)
	             38 BINARY_TRUE_DIVIDE
	             39 BINARY_ADD
	             40 STORE_NAME               3 (result)

    ...trimmed...

.. {{{end}}}


Performance Analysis of Loops
=============================

Besides debugging errors, ``dis`` can also help identify
performance issues. Examining the disassembled code is especially
useful with tight loops where the number of Python instructions is low
but they translate to an inefficient set of bytecodes.  The
helpfulness of the disassembly can be seen by examining a few
different implementations of a class, :class:`Dictionary`, that reads
a list of words and groups them by their first letter.

.. literalinclude:: dis_test_loop.py
   :caption:
   :start-after: #end_pymotw_header

The test driver application ``dis_test_loop.py`` can be used to run
each incarnation of the :class:`Dictionary` class.

A straightforward, but slow, implementation of :class:`Dictionary`
starts out like this:

.. cssclass:: with-linenos

   .. literalinclude:: dis_slow_loop.py
      :linenos:
      :caption:

Running the test program with this version shows the disassembled
program and the amount of time it takes to run.

.. timing values are sensitive to other operations, so don't cog
.. cog.out(run_script(cog.inFile, 'dis_test_loop.py dis_slow_loop', line_break_mode='wrap'))

.. code-block:: none

	$ python3 dis_test_loop.py dis_slow_loop
	
	 12           0 SETUP_LOOP              83 (to 86)
	              3 LOAD_FAST                1 (words)
	              6 GET_ITER
	        >>    7 FOR_ITER                75 (to 85)
	             10 STORE_FAST               2 (word)
	
	 13          13 SETUP_EXCEPT            28 (to 44)
	
	 14          16 LOAD_FAST                0 (self)
	             19 LOAD_ATTR                0 (by_letter)
	             22 LOAD_FAST                2 (word)
	             25 LOAD_CONST               1 (0)
	             28 BINARY_SUBSCR
	             29 BINARY_SUBSCR
	             30 LOAD_ATTR                1 (append)
	             33 LOAD_FAST                2 (word)
	             36 CALL_FUNCTION            1 (1 positional, 0
	keyword pair)
	             39 POP_TOP
	             40 POP_BLOCK
	             41 JUMP_ABSOLUTE            7
	
	 15     >>   44 DUP_TOP
	             45 LOAD_GLOBAL              2 (KeyError)
	             48 COMPARE_OP              10 (exception match)
	             51 POP_JUMP_IF_FALSE       81
	             54 POP_TOP
	             55 POP_TOP
	             56 POP_TOP
	
	 16          57 LOAD_FAST                2 (word)
	             60 BUILD_LIST               1
	             63 LOAD_FAST                0 (self)
	             66 LOAD_ATTR                0 (by_letter)
	             69 LOAD_FAST                2 (word)
	             72 LOAD_CONST               1 (0)
	             75 BINARY_SUBSCR
	             76 STORE_SUBSCR
	             77 POP_EXCEPT
	             78 JUMP_ABSOLUTE            7
	        >>   81 END_FINALLY
	             82 JUMP_ABSOLUTE            7
	        >>   85 POP_BLOCK
	        >>   86 LOAD_CONST               0 (None)
	             89 RETURN_VALUE

	TIME: 0.0568

The previous output shows ``dis_slow_loop.py`` taking 0.0568 seconds
to load the 235886 words in the copy of ``/usr/share/dict/words`` on
OS X.  That is not too bad, but the accompanying disassembly shows
that the loop is doing more work than it needs to.  As it enters the
loop in opcode 13, it sets up an exception context
(:const:`SETUP_EXCEPT`).  Then it takes six opcodes to find
``self.by_letter[word[0]]`` before appending ``word`` to the list.  If
there is an exception because ``word[0]`` is not in the dictionary
yet, the exception handler does all of the same work to determine
``word[0]`` (three opcodes) and sets ``self.by_letter[word[0]]`` to a
new list containing the word.

One technique to eliminate the exception setup is to pre-populate
``self.by_letter`` with one list for each letter of the alphabet.
That means the list for the new word should always be found, and the
value can be saved after the lookup.

.. cssclass:: with-linenos

   .. literalinclude:: dis_faster_loop.py
      :linenos:
      :caption:

The change cuts the number of opcodes in half, but only shaves the
time down to 0.0567 seconds.  Obviously the exception handling had
some overhead, but not a significant amount.

.. timing values are sensitive to other operations, so don't cog

.. cog.out(run_script(cog.inFile, 'dis_test_loop.py dis_faster_loop', line_break_mode='wrap'))

.. code-block:: none

	$ python3 dis_test_loop.py dis_faster_loop
	
	 17           0 SETUP_LOOP              38 (to 41)
	              3 LOAD_FAST                1 (words)
	              6 GET_ITER
	        >>    7 FOR_ITER                30 (to 40)
	             10 STORE_FAST               2 (word)
	
	 18          13 LOAD_FAST                0 (self)
	             16 LOAD_ATTR                0 (by_letter)
	             19 LOAD_FAST                2 (word)
	             22 LOAD_CONST               1 (0)
	             25 BINARY_SUBSCR
	             26 BINARY_SUBSCR
	             27 LOAD_ATTR                1 (append)
	             30 LOAD_FAST                2 (word)
	             33 CALL_FUNCTION            1 (1 positional, 0
	keyword pair)
	             36 POP_TOP
	             37 JUMP_ABSOLUTE            7
	        >>   40 POP_BLOCK
	        >>   41 LOAD_CONST               0 (None)
	             44 RETURN_VALUE

	TIME: 0.0567

The performance can be improved further by moving the lookup for
``self.by_letter`` outside of the loop (the value does not change,
after all).

.. cssclass:: with-linenos

   .. literalinclude:: dis_fastest_loop.py
      :linenos:
      :caption:

Opcodes 0-6 now find the value of ``self.by_letter`` and save it as a
local variable ``by_letter``.  Using a local variable only takes a
single opcode, instead of two (statement 22 uses :const:`LOAD_FAST` to
place the dictionary onto the stack).  After this change, the run time
is down to 0.0473 seconds.

.. timing values are sensitive to other operations, so don't cog

.. cog.out(run_script(cog.inFile, 'dis_test_loop.py dis_fastest_loop', line_break_mode='wrap'))

.. code-block:: none

	$ python3 dis_test_loop.py dis_fastest_loop
	
	 14           0 LOAD_FAST                0 (self)
	              3 LOAD_ATTR                0 (by_letter)
	              6 STORE_FAST               2 (by_letter)
	
	 15           9 SETUP_LOOP              35 (to 47)
	             12 LOAD_FAST                1 (words)
	             15 GET_ITER
	        >>   16 FOR_ITER                27 (to 46)
	             19 STORE_FAST               3 (word)
	
	 16          22 LOAD_FAST                2 (by_letter)
	             25 LOAD_FAST                3 (word)
	             28 LOAD_CONST               1 (0)
	             31 BINARY_SUBSCR
	             32 BINARY_SUBSCR
	             33 LOAD_ATTR                1 (append)
	             36 LOAD_FAST                3 (word)
	             39 CALL_FUNCTION            1 (1 positional, 0
	keyword pair)
	             42 POP_TOP
	             43 JUMP_ABSOLUTE           16
	        >>   46 POP_BLOCK
	        >>   47 LOAD_CONST               0 (None)
	             50 RETURN_VALUE

	TIME: 0.0473

A further optimization, suggested by Brandon Rhodes, is to eliminate
the Python version of the ``for`` loop entirely. If
:func:`itertools.groupby` is used to arrange the input, the iteration
is moved to C.  This is safe because the inputs are known to be
sorted.  If that was not the case, the program would need to sort them
first.

.. cssclass:: with-linenos

   .. literalinclude:: dis_eliminate_loop.py
      :linenos:
      :caption:

The :mod:`itertools` version takes only 0.0332 seconds to run, about
60% of the run time for the original.

.. timing values are sensitive to other operations, so don't cog

.. cog.out(run_script(cog.inFile, 'dis_test_loop.py dis_eliminate_loop', line_break_mode='wrap'))

.. code-block:: none

	$ python3 dis_test_loop.py dis_eliminate_loop
	
	 16           0 LOAD_GLOBAL              0 (itertools)
	              3 LOAD_ATTR                1 (groupby)
	
	 17           6 LOAD_FAST                1 (words)
	              9 LOAD_CONST               1 ('key')
	
	 18          12 LOAD_GLOBAL              2 (operator)
	             15 LOAD_ATTR                3 (itemgetter)
	             18 LOAD_CONST               2 (0)
	             21 CALL_FUNCTION            1 (1 positional, 0
	keyword pair)
	             24 CALL_FUNCTION          257 (1 positional, 1
	keyword pair)
	             27 STORE_FAST               2 (grouped)
	
	 21          30 LOAD_CONST               3 (<code object
	<dictcomp> at 0x101517930, file "/Users/dhellmann/Dropbox/PyMOTW
	/Python3/pymotw-3/source/dis/dis_eliminate_loop.py", line 21>)
	             33 LOAD_CONST               4
	('Dictionary.load_data.<locals>.<dictcomp>')
	             36 MAKE_FUNCTION            0
	
	 23          39 LOAD_FAST                2 (grouped)
	             42 GET_ITER
	             43 CALL_FUNCTION            1 (1 positional, 0
	keyword pair)
	             46 LOAD_FAST                0 (self)
	             49 STORE_ATTR               4 (by_letter)
	             52 LOAD_CONST               0 (None)
	             55 RETURN_VALUE

	TIME: 0.0332


Compiler Optimizations
======================

Disassembling compiled source also exposes some of the optimizations
made by the compiler.  For example, literal expressions are folded
during compilation, when possible.

.. cssclass:: with-linenos

   .. literalinclude:: dis_constant_folding.py
      :linenos:
      :caption:

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

.. code-block:: none

	$ python3 -m dis dis_constant_folding.py
	
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
	             38 BINARY_TRUE_DIVIDE
	             39 LOAD_CONST               6 (3)
	             42 BINARY_TRUE_DIVIDE
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

    * :pydoc:`dis` -- Includes the list of `bytecode instructions
      <https://docs.python.org/3.5/library/dis.html#python-bytecode-instructions>`_.

    * ``Include/opcode.h`` -- The source code for the CPython
      interpreter defines the byte codes in ``opcode.h``.

    * *Python Essential Reference*, 4th Edition, David M. Beazley --
      http://www.informit.com/store/product.aspx?isbn=0672329786

    * `thomas.apestaart.org "Python Disassembly"
      <http://thomas.apestaart.org/log/?p=927>`_ -- A short discussion
      of the difference between storing values in a dictionary between
      Python 2.5 and 2.6.

    * `Why is looping over range() in Python faster than using a while
      loop?
      <http://stackoverflow.com/questions/869229/why-is-looping-over-range-in-python-faster-than-using-a-while-loop>`_
      -- A discussion on StackOverflow.com comparing 2 looping
      examples via their disassembled bytecodes.

    * `Decorator for binding constants at compile time
      <http://code.activestate.com/recipes/277940/>`_ -- Python
      Cookbook recipe by Raymond Hettinger and Skip Montanaro with a
      function decorator that re-writes the bytecodes for a function
      to insert global constants to avoid runtime name lookups.
