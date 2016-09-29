===========================================
 doctest --- Testing Through Documentation
===========================================

.. module:: doctest
    :synopsis: Write automated tests as part of the documentation for a module.

:Purpose: Write automated tests as part of the documentation for a module.

:mod:`doctest` tests source code by running examples embedded in the
documentation and verifying that they produce the expected results.
It works by parsing the help text to find examples, running them, then
comparing the output text against the expected value.  Many developers
find :mod:`doctest` easier to use than :mod:`unittest` because, in its
simplest form, there is no API to learn before using it.  However, as
the examples become more complex the lack of fixture management can
make writing :mod:`doctest` tests more cumbersome than using
:mod:`unittest`.

Getting Started
===============

The first step to setting up doctests is to use the interactive
interpreter to create examples and then copy and paste them into the
docstrings in the module.  Here, :func:`my_function` has two examples
given:

.. literalinclude:: doctest_simple.py
   :caption:
   :start-after: #end_pymotw_header

To run the tests, use :mod:`doctest` as the main program via the
``-m`` option.  Usually no output is produced while the tests are
running, so the next example includes the ``-v`` option to make the
output more verbose.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m doctest -v doctest_simple.py'))
.. }}}

.. code-block:: none

	$ python3 -m doctest -v doctest_simple.py
	
	Trying:
	    my_function(2, 3)
	Expecting:
	    6
	ok
	Trying:
	    my_function('a', 3)
	Expecting:
	    'aaa'
	ok
	1 items had no tests:
	    doctest_simple
	1 items passed all tests:
	   2 tests in doctest_simple.my_function
	2 tests in 2 items.
	2 passed and 0 failed.
	Test passed.

.. {{{end}}}

Examples cannot usually stand on their own as explanations of a
function, so :mod:`doctest` also allows for surrounding text.  It
looks for lines beginning with the interpreter prompt (``>>>``) to
find the beginning of a test case, and the case is ended by a blank
line or by the next interpreter prompt.  Intervening text is ignored,
and can have any format as long as it does not look like a test case.

.. literalinclude:: doctest_simple_with_docs.py
   :caption:
   :start-after: #end_pymotw_header

The surrounding text in the updated docstring makes it more useful to
a human reader.  Because it is ignored by :mod:`doctest`, the results
are the same.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m doctest -v doctest_simple_with_docs.py'))
.. }}}

.. code-block:: none

	$ python3 -m doctest -v doctest_simple_with_docs.py
	
	Trying:
	    my_function(2, 3)
	Expecting:
	    6
	ok
	Trying:
	    my_function('a', 3)
	Expecting:
	    'aaa'
	ok
	1 items had no tests:
	    doctest_simple_with_docs
	1 items passed all tests:
	   2 tests in doctest_simple_with_docs.my_function
	2 tests in 2 items.
	2 passed and 0 failed.
	Test passed.

.. {{{end}}}

Handling Unpredictable Output
=============================

There are other cases where the exact output may not be predictable,
but should still be testable.  For example, local date and time values
and object ids change on every test run, the default precision used in
the representation of floating point values depend on compiler
options, and object string representations may not be deterministic.
Although these conditions cannot be controlled, there are techniques
for dealing with them.

For example, in CPython, object identifiers are based on the memory
address of the data structure holding the object.

.. literalinclude:: doctest_unpredictable.py
   :caption:
   :start-after: #end_pymotw_header

These id values change each time a program runs, because it is loaded
into a different part of memory.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m doctest -v doctest_unpredictable.py', ignore_error=True))
.. }}}

.. code-block:: none

	$ python3 -m doctest -v doctest_unpredictable.py
	
	Trying:
	    unpredictable(MyClass())
	Expecting:
	    [<doctest_unpredictable.MyClass object at 0x10055a2d0>]
	****************************************************************
	******
	File ".../doctest_unpredictable.py", line 18, in doctest_unpredi
	ctable.unpredictable
	Failed example:
	    unpredictable(MyClass())
	Expected:
	    [<doctest_unpredictable.MyClass object at 0x10055a2d0>]
	Got:
	    [<doctest_unpredictable.MyClass object at 0x1016889e8>]
	2 items had no tests:
	    doctest_unpredictable
	    doctest_unpredictable.MyClass
	****************************************************************
	******
	1 items had failures:
	   1 of   1 in doctest_unpredictable.unpredictable
	1 tests in 3 items.
	0 passed and 1 failed.
	***Test Failed*** 1 failures.

.. {{{end}}}

When the tests include values that are likely to change in
unpredictable ways, and where the actual value is not important to the
test results, use the :const:`ELLIPSIS` option to tell :mod:`doctest`
to ignore portions of the verification value.

.. literalinclude:: doctest_ellipsis.py
   :caption:
   :start-after: #end_pymotw_header

The "``#doctest: +ELLIPSIS``" comment after the call to
:func:`unpredictable` tells :mod:`doctest` to turn on the
:const:`ELLIPSIS` option for that test.  The ``...`` replaces the
memory address in the object id, so that portion of the expected value
is ignored and the actual output matches and the test passes.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m doctest -v doctest_ellipsis.py'))
.. }}}

.. code-block:: none

	$ python3 -m doctest -v doctest_ellipsis.py
	
	Trying:
	    unpredictable(MyClass()) #doctest: +ELLIPSIS
	Expecting:
	    [<doctest_ellipsis.MyClass object at 0x...>]
	ok
	2 items had no tests:
	    doctest_ellipsis
	    doctest_ellipsis.MyClass
	1 items passed all tests:
	   1 tests in doctest_ellipsis.unpredictable
	1 tests in 3 items.
	1 passed and 0 failed.
	Test passed.

.. {{{end}}}

There are cases where the unpredictable value cannot be ignored,
because that would make the test incomplete or inaccurate.  For
example, simple tests quickly become more complex when dealing with
data types whose string representations are inconsistent.  The string
form of a dictionary, for example, may change based on the order the
keys are added.

.. literalinclude:: doctest_hashed_values.py
   :caption:
   :start-after: #end_pymotw_header

Because of hash randomization and key collision, the internal key list
order may be different for the dictionary each time the script
runs. Sets use the same hashing algorithm, and exhibit the same
behavior.

.. NOT RUNNING -- producing different orders isn't predictable
.. cog.out(run_script(cog.inFile, 'doctest_hashed_values.py'))
.. cog.out(run_script(cog.inFile, 'doctest_hashed_values.py', include_prefix=False))

.. code-block:: none

	$ python3 doctest_hashed_values.py
	
	dict: {'aa': 2, 'a': 1, 'aaa': 3}
	set : {'aa', 'a', 'aaa'}

	$ python3 doctest_hashed_values.py
	
	dict: {'a': 1, 'aa': 2, 'aaa': 3}
	set : {'a', 'aa', 'aaa'}

The best way to deal with these potential discrepancies is to create
tests that produce values that are not likely to change.  In the case
of dictionaries and sets, that might mean looking for specific keys
individually, generating a sorted list of the contents of the data
structure, or comparing against a literal value for equality instead
of depending on the string representation.

.. literalinclude:: doctest_hashed_values_tests.py
   :caption:
   :start-after: #end_pymotw_header

The single example is actually interpreted as two separate tests, with
the first expecting no console output and the second expecting the
boolean result of the comparison operation.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m doctest -v doctest_hashed_values_tests.py',
..                    line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 -m doctest -v doctest_hashed_values_tests.py
	
	Trying:
	    grouped = group_by_length([ 'python', 'module', 'of',
	    'the', 'week' ])
	Expecting nothing
	ok
	Trying:
	    grouped == { 2:set(['of']),
	                 3:set(['the']),
	                 4:set(['week']),
	                 6:set(['python', 'module']),
	                 }
	Expecting:
	    True
	ok
	1 items had no tests:
	    doctest_hashed_values_tests
	1 items passed all tests:
	   2 tests in doctest_hashed_values_tests.group_by_length
	2 tests in 2 items.
	2 passed and 0 failed.
	Test passed.

.. {{{end}}}

Tracebacks
==========

Tracebacks are a special case of changing data.  Since the paths in a
traceback depend on the location where a module is installed on the
file system, it would be impossible to write portable tests if they
were treated the same as other output.

.. literalinclude:: doctest_tracebacks.py
   :caption:
   :start-after: #end_pymotw_header

:mod:`doctest` makes a special effort to recognize tracebacks, and
ignore the parts that might change from system to system.  

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m doctest -v doctest_tracebacks.py'))
.. }}}

.. code-block:: none

	$ python3 -m doctest -v doctest_tracebacks.py
	
	Trying:
	    this_raises()
	Expecting:
	    Traceback (most recent call last):
	      File "<stdin>", line 1, in <module>
	      File "/no/such/path/doctest_tracebacks.py", line 14, in
	      this_raises
	        raise RuntimeError('here is the error')
	    RuntimeError: here is the error
	ok
	1 items had no tests:
	    doctest_tracebacks
	1 items passed all tests:
	   1 tests in doctest_tracebacks.this_raises
	1 tests in 2 items.
	1 passed and 0 failed.
	Test passed.

.. {{{end}}}

In fact, the entire body of the traceback is ignored and can be
omitted.

.. literalinclude:: doctest_tracebacks_no_body.py
   :caption:
   :start-after: #end_pymotw_header

When :mod:`doctest` sees a traceback header line (either "``Traceback
(most recent call last):``" or "``Traceback (innermost last):``", to
support different versions of Python), it skips ahead to find the
exception type and message, ignoring the intervening lines entirely.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m doctest -v doctest_tracebacks_no_body.py'))
.. }}}

.. code-block:: none

	$ python3 -m doctest -v doctest_tracebacks_no_body.py
	
	Trying:
	    this_raises()
	Expecting:
	    Traceback (most recent call last):
	    RuntimeError: here is the error
	ok
	Trying:
	    this_raises()
	Expecting:
	    Traceback (innermost last):
	    RuntimeError: here is the error
	ok
	1 items had no tests:
	    doctest_tracebacks_no_body
	1 items passed all tests:
	   2 tests in doctest_tracebacks_no_body.this_raises
	2 tests in 2 items.
	2 passed and 0 failed.
	Test passed.

.. {{{end}}}

Working Around Whitespace
=========================

In real world applications, output usually includes whitespace such as
blank lines, tabs, and extra spacing to make it more readable.  Blank
lines, in particular, cause issues with :mod:`doctest` because they
are used to delimit tests.

.. literalinclude:: doctest_blankline_fail.py
   :caption:
   :start-after: #end_pymotw_header

:func:`double_space` takes a list of input lines, and prints them
double-spaced with blank lines between.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m doctest -v doctest_blankline_fail.py', ignore_error=True))
.. }}}

.. code-block:: none

	$ python3 -m doctest -v doctest_blankline_fail.py
	
	Trying:
	    double_space(['Line one.', 'Line two.'])
	Expecting:
	    Line one.
	****************************************************************
	******
	File ".../doctest_blankline_fail.py", line 14, in doctest_blankl
	ine_fail.double_space
	Failed example:
	    double_space(['Line one.', 'Line two.'])
	Expected:
	    Line one.
	Got:
	    Line one.
	    <BLANKLINE>
	    Line two.
	    <BLANKLINE>
	1 items had no tests:
	    doctest_blankline_fail
	****************************************************************
	******
	1 items had failures:
	   1 of   1 in doctest_blankline_fail.double_space
	1 tests in 2 items.
	0 passed and 1 failed.
	***Test Failed*** 1 failures.

.. {{{end}}}


The test fails, because it interprets the blank line after the line
containing ``Line one.`` in the docstring as the end of the sample
output.  To match the blank lines, replace them in the sample input
with the string ``<BLANKLINE>``.

.. literalinclude:: doctest_blankline.py
   :caption:
   :start-after: #end_pymotw_header

:mod:`doctest` replaces actual blank lines with the same literal
before performing the comparison, so now the actual and expected
values match and the test passes.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m doctest -v doctest_blankline.py'))
.. }}}

.. code-block:: none

	$ python3 -m doctest -v doctest_blankline.py
	
	Trying:
	    double_space(['Line one.', 'Line two.'])
	Expecting:
	    Line one.
	    <BLANKLINE>
	    Line two.
	    <BLANKLINE>
	ok
	1 items had no tests:
	    doctest_blankline
	1 items passed all tests:
	   1 tests in doctest_blankline.double_space
	1 tests in 2 items.
	1 passed and 0 failed.
	Test passed.

.. {{{end}}}

Another pitfall of using text comparisons for tests is that embedded
whitespace can also cause tricky problems with tests.  This example
has a single extra space after the ``6``.

.. literalinclude:: doctest_extra_space.py
   :caption:
   :start-after: #end_pymotw_header

Extra spaces can find their way into code via copy-and-paste
errors, but since they come at the end of the line, they can go
unnoticed in the source file and be invisible in the test failure
report as well.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m doctest -v doctest_extra_space.py', ignore_error=True))
.. }}}

.. code-block:: none

	$ python3 -m doctest -v doctest_extra_space.py
	
	Trying:
	    my_function(2, 3)
	Expecting:
	    6 
	****************************************************************
	******
	File ".../doctest_extra_space.py", line 17, in doctest_extra_spa
	ce.my_function
	Failed example:
	    my_function(2, 3)
	Expected:
	    6 
	Got:
	    6
	Trying:
	    my_function('a', 3)
	Expecting:
	    'aaa'
	ok
	1 items had no tests:
	    doctest_extra_space
	****************************************************************
	******
	1 items had failures:
	   1 of   2 in doctest_extra_space.my_function
	2 tests in 2 items.
	1 passed and 1 failed.
	***Test Failed*** 1 failures.

.. {{{end}}}

Using one of the diff-based reporting options, such as
``REPORT_NDIFF``, shows the difference between the actual and expected
values with more detail, and the extra space becomes visible.

.. literalinclude:: doctest_ndiff.py
   :caption:
   :start-after: #end_pymotw_header

Unified (``REPORT_UDIFF``) and context (``REPORT_CDIFF``) diffs are
also available, for output where those formats are more readable.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m doctest -v doctest_ndiff.py', ignore_error=True))
.. }}}

.. code-block:: none

	$ python3 -m doctest -v doctest_ndiff.py
	
	Trying:
	    my_function(2, 3) #doctest: +REPORT_NDIFF
	Expecting:
	    6 
	****************************************************************
	******
	File ".../doctest_ndiff.py", line 17, in doctest_ndiff.my_functi
	on
	Failed example:
	    my_function(2, 3) #doctest: +REPORT_NDIFF
	Differences (ndiff with -expected +actual):
	    - 6
	    ?  -
	    + 6
	Trying:
	    my_function('a', 3)
	Expecting:
	    'aaa'
	ok
	1 items had no tests:
	    doctest_ndiff
	****************************************************************
	******
	1 items had failures:
	   1 of   2 in doctest_ndiff.my_function
	2 tests in 2 items.
	1 passed and 1 failed.
	***Test Failed*** 1 failures.

.. {{{end}}}


There are cases where it is beneficial to add extra whitespace in the
sample output for the test, and have :mod:`doctest` ignore it.  For
example, data structures can be easier to read when spread across
several lines, even if their representation would fit on a single
line.

.. include:: doctest_normalize_whitespace.py
   :literal:
   :start-after: #end_pymotw_header

When ``NORMALIZE_WHITESPACE`` is turned on, any whitespace in the
actual and expected values is considered a match.  Whitespace cannot
be added to the expected value where none exists in the output, but
the length of the whitespace sequence and actual whitespace characters
do not need to match.  The first test example gets this rule correct,
and passes, even though there are extra spaces and newlines.  The
second has extra whitespace after ``[`` and before ``]``, so it fails.

.. NOT RUNNING
.. cog.out(run_script(cog.inFile, '-m doctest -v doctest_normalize_whitespace.py', ignore_error=True))

.. code-block:: none

    $ python3 -m doctest -v doctest_normalize_whitespace.py

    Trying:
        my_function(['A', 'B'], 3) #doctest: +NORMALIZE_WHITESPACE
    Expecting:
        ['A', 'B',
         'A', 'B',
         'A', 'B',]
    ***************************************************************
    File "doctest_normalize_whitespace.py", line 13, in doctest_nor
    malize_whitespace.my_function
    Failed example:
        my_function(['A', 'B'], 3) #doctest: +NORMALIZE_WHITESPACE
    Expected:
        ['A', 'B',
         'A', 'B',
         'A', 'B',]
    Got:
        ['A', 'B', 'A', 'B', 'A', 'B']
    Trying:
        my_function(['A', 'B'], 2) #doctest: +NORMALIZE_WHITESPACE
    Expecting:
        [ 'A', 'B',
          'A', 'B', ]
    ***************************************************************
    File "doctest_normalize_whitespace.py", line 21, in doctest_nor
    malize_whitespace.my_function
    Failed example:
        my_function(['A', 'B'], 2) #doctest: +NORMALIZE_WHITESPACE
    Expected:
        [ 'A', 'B',
          'A', 'B', ]
    Got:
        ['A', 'B', 'A', 'B']
    1 items had no tests:
        doctest_normalize_whitespace
    ***************************************************************
    1 items had failures:
       2 of   2 in doctest_normalize_whitespace.my_function
    2 tests in 2 items.
    0 passed and 2 failed.
    ***Test Failed*** 2 failures.


Test Locations
==============

All of the tests in the examples so far have been written in the
docstrings of the functions they are testing.  That is convenient for
users who examine the docstrings for help using the function
(especially with :mod:`pydoc`), but :mod:`doctest` looks for tests in
other places, too.  The obvious location for additional tests is in
the docstrings elsewhere in the module.

.. literalinclude:: doctest_docstrings.py
   :caption:
   :start-after: #end_pymotw_header

Docstrings at the module, class, and function levels can all contain
tests.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m doctest -v doctest_docstrings.py'))
.. }}}

.. code-block:: none

	$ python3 -m doctest -v doctest_docstrings.py
	
	Trying:
	    A('a') == B('b')
	Expecting:
	    False
	ok
	Trying:
	    A('instance_name').name
	Expecting:
	    'instance_name'
	ok
	Trying:
	    A('name').method()
	Expecting:
	    'eman'
	ok
	Trying:
	    B('different_name').name
	Expecting:
	    'different_name'
	ok
	1 items had no tests:
	    doctest_docstrings.A.__init__
	4 items passed all tests:
	   1 tests in doctest_docstrings
	   1 tests in doctest_docstrings.A
	   1 tests in doctest_docstrings.A.method
	   1 tests in doctest_docstrings.B
	4 tests in 5 items.
	4 passed and 0 failed.
	Test passed.

.. {{{end}}}

There are cases where tests exist for a module that should be included
with the source code but not in the help text for a module, so they
need to be placed somewhere other than the docstrings.  :mod:`doctest`
also looks for a module-level variable called ``__test__`` and uses it
to locate other tests.  The value of ``__test__`` should be a dictionary that maps
test set names (as strings) to strings, modules, classes, or
functions.

.. literalinclude:: doctest_private_tests.py
   :caption:
   :start-after: #end_pymotw_header

If the value associated with a key is a string, it is treated as a
docstring and scanned for tests.  If the value is a class or function,
:mod:`doctest` searches them recursively for docstrings, which are
then scanned for tests.  In this example, the module
:mod:`doctest_private_tests_external` has a single test in its
docstring.

.. literalinclude:: doctest_private_tests_external.py
   :caption:
   :start-after: #end_pymotw_header

After scanning the example file, :mod:`doctest` finds a total of five tests to run.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m doctest -v doctest_private_tests.py'))
.. }}}

.. code-block:: none

	$ python3 -m doctest -v doctest_private_tests.py
	
	Trying:
	    my_function(['A', 'B', 'C'], 2)
	Expecting:
	    ['A', 'B', 'C', 'A', 'B', 'C']
	ok
	Trying:
	    my_function(2, 3)
	Expecting:
	    6
	ok
	Trying:
	    my_function(2.0, 3)
	Expecting:
	    6.0
	ok
	Trying:
	    my_function('a', 3)
	Expecting:
	    'aaa'
	ok
	Trying:
	    my_function(3, 'a')
	Expecting:
	    'aaa'
	ok
	2 items had no tests:
	    doctest_private_tests
	    doctest_private_tests.my_function
	3 items passed all tests:
	   1 tests in doctest_private_tests.__test__.external
	   2 tests in doctest_private_tests.__test__.numbers
	   2 tests in doctest_private_tests.__test__.strings
	5 tests in 5 items.
	5 passed and 0 failed.
	Test passed.

.. {{{end}}}

External Documentation
======================

Mixing tests in with regular code is not the only way to use
:mod:`doctest`.  Examples embedded in external project documentation
files, such as reStructuredText files, can be used as well.

.. literalinclude:: doctest_in_help.py
   :caption:
   :start-after: #end_pymotw_header

The help for this sample module is saved to a separate file,
``doctest_in_help.txt``.  The examples illustrating how to use the
module are included with the help text, and :mod:`doctest` can be used
to find and run them.

.. literalinclude:: doctest_in_help.txt
   :caption:
   :language: none

The tests in the text file can be run from the command line, just as
with the Python source modules.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m doctest -v doctest_in_help.txt'))
.. }}}

.. code-block:: none

	$ python3 -m doctest -v doctest_in_help.txt
	
	Trying:
	    from doctest_in_help import my_function
	Expecting nothing
	ok
	Trying:
	    my_function(2, 3)
	Expecting:
	    6
	ok
	Trying:
	    my_function(2.0, 3)
	Expecting:
	    6.0
	ok
	Trying:
	    my_function('a', 3)
	Expecting:
	    'aaa'
	ok
	Trying:
	    my_function(['A', 'B', 'C'], 2)
	Expecting:
	    ['A', 'B', 'C', 'A', 'B', 'C']
	ok
	1 items passed all tests:
	   5 tests in doctest_in_help.txt
	5 tests in 1 items.
	5 passed and 0 failed.
	Test passed.

.. {{{end}}}

Normally :mod:`doctest` sets up the test execution environment to
include the members of the module being tested, so the tests do not
need to import the module explicitly.  In this case, however, the
tests are not defined in a Python module, and :mod:`doctest` does not
know how to set up the global namespace, so the examples need to do
the import work themselves.  All of the tests in a given file share
the same execution context, so importing the module once at the top of
the file is enough.

Running Tests
=============

The previous examples all use the command line test runner built into
:mod:`doctest`.  It is easy and convenient for a single module, but
will quickly become tedious as a package spreads out into multiple
files.  There are several alternative approaches.

By Module
---------

The instructions to run :mod:`doctest` against the source can be
included at the bottom of modules.

.. literalinclude:: doctest_testmod.py
   :caption:
   :start-after: #end_pymotw_header

Calling :func:`testmod` only if the current module name is
``__main__`` ensures that the tests are only run when the module is
invoked as a main program.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'doctest_testmod.py -v'))
.. }}}

.. code-block:: none

	$ python3 doctest_testmod.py -v
	
	Trying:
	    my_function(2, 3)
	Expecting:
	    6
	ok
	Trying:
	    my_function('a', 3)
	Expecting:
	    'aaa'
	ok
	1 items had no tests:
	    __main__
	1 items passed all tests:
	   2 tests in __main__.my_function
	2 tests in 2 items.
	2 passed and 0 failed.
	Test passed.

.. {{{end}}}

The first argument to :func:`testmod` is a module containing code to
be scanned for tests.  A separate test script can use this feature to
import the real code and run the tests in each module one after
another.

.. literalinclude:: doctest_testmod_other_module.py
   :caption:
   :start-after: #end_pymotw_header

A test suite can be constructed for the project by importing each
module and running its tests.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'doctest_testmod_other_module.py -v'))
.. }}}

.. code-block:: none

	$ python3 doctest_testmod_other_module.py -v
	
	Trying:
	    my_function(2, 3)
	Expecting:
	    6
	ok
	Trying:
	    my_function('a', 3)
	Expecting:
	    'aaa'
	ok
	1 items had no tests:
	    doctest_simple
	1 items passed all tests:
	   2 tests in doctest_simple.my_function
	2 tests in 2 items.
	2 passed and 0 failed.
	Test passed.

.. {{{end}}}

By File
-------

:func:`testfile` works in a way similar to :func:`testmod`, allowing
the tests to be invoked explicitly in an external file from within the
test program.

.. literalinclude:: doctest_testfile.py
   :caption:
   :start-after: #end_pymotw_header

Both :func:`testmod` and :func:`testfile` include optional parameters
to control the behavior of the tests through the :mod:`doctest`
options.  Refer to the standard library documentation for more details
about those features -- most of the time they are not needed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'doctest_testfile.py -v'))
.. }}}

.. code-block:: none

	$ python3 doctest_testfile.py -v
	
	Trying:
	    from doctest_in_help import my_function
	Expecting nothing
	ok
	Trying:
	    my_function(2, 3)
	Expecting:
	    6
	ok
	Trying:
	    my_function(2.0, 3)
	Expecting:
	    6.0
	ok
	Trying:
	    my_function('a', 3)
	Expecting:
	    'aaa'
	ok
	Trying:
	    my_function(['A', 'B', 'C'], 2)
	Expecting:
	    ['A', 'B', 'C', 'A', 'B', 'C']
	ok
	1 items passed all tests:
	   5 tests in doctest_in_help.txt
	5 tests in 1 items.
	5 passed and 0 failed.
	Test passed.

.. {{{end}}}

Unittest Suite
--------------

When both :mod:`unittest` and :mod:`doctest` are used for testing the
same code in different situations, the :mod:`unittest` integration in
:mod:`doctest` can be used to run the tests together.  Two classes,
:class:`DocTestSuite` and :class:`DocFileSuite` create test suites
compatible with the test-runner API of :mod:`unittest`.

.. literalinclude:: doctest_unittest.py
   :caption:
   :start-after: #end_pymotw_header

The tests from each source are collapsed into a single outcome,
instead of being reported individually.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'doctest_unittest.py'))
.. }}}

.. code-block:: none

	$ python3 doctest_unittest.py
	
	my_function (doctest_simple)
	Doctest: doctest_simple.my_function ... ok
	doctest_in_help.txt
	Doctest: doctest_in_help.txt ... ok
	
	----------------------------------------------------------------
	------
	Ran 2 tests in 0.002s
	
	OK

.. {{{end}}}

Test Context
============

The execution context created by :mod:`doctest` as it runs tests
contains a copy of the module-level globals for the test module.  Each
test source (function, class, module) has its own set of global
values to isolate the tests from each other somewhat, so they are
less likely to interfere with one another.

.. literalinclude:: doctest_test_globals.py
   :caption:
   :start-after: #end_pymotw_header

:class:`TestGlobals` has two methods: :func:`one` and :func:`two`.
The tests in the docstring for :func:`one` set a global variable, and
the test for :func:`two` looks for it (expecting not to find it).

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m doctest -v doctest_test_globals.py'))
.. }}}

.. code-block:: none

	$ python3 -m doctest -v doctest_test_globals.py
	
	Trying:
	    var = 'value'
	Expecting nothing
	ok
	Trying:
	    'var' in globals()
	Expecting:
	    True
	ok
	Trying:
	    'var' in globals()
	Expecting:
	    False
	ok
	2 items had no tests:
	    doctest_test_globals
	    doctest_test_globals.TestGlobals
	2 items passed all tests:
	   2 tests in doctest_test_globals.TestGlobals.one
	   1 tests in doctest_test_globals.TestGlobals.two
	3 tests in 4 items.
	3 passed and 0 failed.
	Test passed.

.. {{{end}}}

That does not mean the tests *cannot* interfere with each other,
though, if they change the contents of mutable variables defined in
the module.

.. literalinclude:: doctest_mutable_globals.py
   :caption:
   :start-after: #end_pymotw_header

The module variable ``_module_data`` is changed by the tests for
:func:`one`, causing the test for :func:`two` to fail.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m doctest -v doctest_mutable_globals.py', ignore_error=True))
.. }}}

.. code-block:: none

	$ python3 -m doctest -v doctest_mutable_globals.py
	
	Trying:
	    TestGlobals().one()
	Expecting nothing
	ok
	Trying:
	    'var' in _module_data
	Expecting:
	    True
	ok
	Trying:
	    'var' in _module_data
	Expecting:
	    False
	****************************************************************
	******
	File ".../doctest_mutable_globals.py", line 25, in doctest_mutab
	le_globals.TestGlobals.two
	Failed example:
	    'var' in _module_data
	Expected:
	    False
	Got:
	    True
	2 items had no tests:
	    doctest_mutable_globals
	    doctest_mutable_globals.TestGlobals
	1 items passed all tests:
	   2 tests in doctest_mutable_globals.TestGlobals.one
	****************************************************************
	******
	1 items had failures:
	   1 of   1 in doctest_mutable_globals.TestGlobals.two
	3 tests in 4 items.
	2 passed and 1 failed.
	***Test Failed*** 1 failures.

.. {{{end}}}

If global values are needed for the tests, to parameterize them for an
environment for example, values can be passed to :func:`testmod` and
:func:`testfile` to have the context set up using data controlled by
the caller.

.. seealso::

   * :pydoc:`doctest`

   * `The Mighty Dictionary <https://www.youtube.com/watch?v=C4Kc8xzcA68>`__ --
     Presentation by Brandon Rhodes at PyCon 2010 about the internal
     operations of the :class:`dict`.

   * :mod:`difflib` -- Python's sequence difference computation
     library, used to produce the ndiff output.

   * `Sphinx <http://www.sphinx-doc.org/>`_ -- As well as being the
     documentation processing tool for Python's standard library,
     Sphinx has been adopted by many third-party projects because it
     is easy to use and produces clean output in several digital and
     print formats.  Sphinx includes an extension for running doctests
     as is processes documentation source files, so the examples are
     always accurate.

   * `py.test <http://doc.pytest.org/en/latest/>`_ -- Third-party
     test runner with :mod:`doctest` support.

   * `nose2 <https://nose2.readthedocs.io/en/latest/>`_ -- Third-party
     test runner with :mod:`doctest` support.

   * `Manuel <https://pythonhosted.org/manuel/>`_ -- Third-party
     documentation-based test runner with more advanced test case
     extraction and integration with Sphinx.
