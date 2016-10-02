==========================================
 unittest --- Automated Testing Framework
==========================================

.. module:: unittest
    :synopsis: Automated testing framework

:Purpose: Automated testing framework

Python's :mod:`unittest` module is based on the XUnit framework design
by Kent Beck and Erich Gamma. The same pattern is repeated in many
other languages, including C, Perl, Java, and Smalltalk. The framework
implemented by :mod:`unittest` supports fixtures, test suites, and a
test runner to enable automated testing.

Basic Test Structure
====================

Tests, as defined by :mod:`unittest`, have two parts: code to manage
test dependencies (called "fixtures"), and the test itself. Individual
tests are created by subclassing :class:`TestCase` and overriding or
adding appropriate methods. For example,

.. literalinclude:: unittest_simple.py
    :caption:
    :start-after: #end_pymotw_header

In this case, the :class:`SimplisticTest` has a single :func:`test`
method, which would fail if ``a`` is ever different from ``b``.

Running Tests
=============

The easiest way to run unittest tests is use the automatic discovery
available through the command line interface.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m unittest unittest_simple.py'))
.. }}}

.. code-block:: none

	$ python3 -m unittest unittest_simple.py
	
	.
	----------------------------------------------------------------
	Ran 1 test in 0.000s
	
	OK

.. {{{end}}}

This abbreviated output includes the amount of time the tests took,
along with a status indicator for each test (the "." on the first line
of output means that a test passed). For more detailed test results,
include the ``-v`` option.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m unittest -v unittest_simple.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 -m unittest -v unittest_simple.py
	
	test (unittest_simple.SimplisticTest) ... ok
	
	----------------------------------------------------------------
	Ran 1 test in 0.000s
	
	OK

.. {{{end}}}

Test Outcomes
=============

Tests have 3 possible outcomes, described in :table:`Test Case Outcomes`.

.. table:: Test Case Outcomes

  =======  ===========
  Outcome  Description
  =======  ===========
  ok       The test passes.
  FAIL     The test does not pass, and raises an AssertionError exception.
  ERROR    The test raises any exception other than AssertionError.
  =======  ===========

There is no explicit way to cause a test to "pass", so a test's status
depends on the presence (or absence) of an exception.

.. literalinclude:: unittest_outcomes.py
    :caption:
    :start-after: #end_pymotw_header

When a test fails or generates an error, the traceback is included in the
output.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m unittest unittest_outcomes.py', ignore_error=True,
..         line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 -m unittest unittest_outcomes.py
	
	EF.
	================================================================
	ERROR: testError (unittest_outcomes.OutcomesTest)
	----------------------------------------------------------------
	Traceback (most recent call last):
	  File ".../unittest_outcomes.py", line 18, in testError
	    raise RuntimeError('Test error!')
	RuntimeError: Test error!
	
	================================================================
	FAIL: testFail (unittest_outcomes.OutcomesTest)
	----------------------------------------------------------------
	Traceback (most recent call last):
	  File ".../unittest_outcomes.py", line 15, in testFail
	    self.assertFalse(True)
	AssertionError: True is not false
	
	----------------------------------------------------------------
	Ran 3 tests in 0.001s
	
	FAILED (failures=1, errors=1)

.. {{{end}}}

In the previous example, :func:`testFail` fails and the traceback
shows the line with the failure code. It is up to the person reading
the test output to look at the code to figure out the meaning of the
failed test, though.

.. literalinclude:: unittest_failwithmessage.py
    :caption:
    :start-after: #end_pymotw_header

To make it easier to understand the nature of a test failure, the
:func:`fail*` and :func:`assert*` methods all accept an argument
*msg*, which can be used to produce a more detailed error message.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m unittest -v unittest_failwithmessage.py',
..         line_break_mode='wrap', ignore_error=True))
.. }}}

.. code-block:: none

	$ python3 -m unittest -v unittest_failwithmessage.py
	
	testFail (unittest_failwithmessage.FailureMessageTest) ... FAIL
	
	================================================================
	FAIL: testFail (unittest_failwithmessage.FailureMessageTest)
	----------------------------------------------------------------
	Traceback (most recent call last):
	  File ".../unittest_failwithmessage.py", line 12, in testFail
	    self.assertFalse(True, 'failure message goes here')
	AssertionError: True is not false : failure message goes here
	
	----------------------------------------------------------------
	Ran 1 test in 0.000s
	
	FAILED (failures=1)

.. {{{end}}}


Asserting Truth
===============

Most tests assert the truth of some condition. There are two different
ways to write truth-checking tests, depending on the perspective of
the test author and the desired outcome of the code being tested.

.. literalinclude:: unittest_truth.py
    :caption:
    :start-after: #end_pymotw_header

If the code produces a value which can be evaluated as true, the
method :func:`assertTrue` should be used. If the code produces a false
value, the method :func:`assertFalse` make more sense.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m unittest -v unittest_truth.py'))
.. }}}

.. code-block:: none

	$ python3 -m unittest -v unittest_truth.py
	
	testAssertFalse (unittest_truth.TruthTest) ... ok
	testAssertTrue (unittest_truth.TruthTest) ... ok
	
	----------------------------------------------------------------
	Ran 2 tests in 0.000s
	
	OK

.. {{{end}}}


Testing Equality
================

As a special case, :mod:`unittest` includes methods for testing the
equality of two values.

.. literalinclude:: unittest_equality.py
    :caption:
    :start-after: #end_pymotw_header

When they fail, these special test methods produce error messages
including the values being compared.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m unittest -v unittest_equality.py', ignore_error=True,
..         line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 -m unittest -v unittest_equality.py
	
	testExpectEqual (unittest_equality.EqualityTest) ... ok
	testExpectEqualFails (unittest_equality.EqualityTest) ... FAIL
	testExpectNotEqual (unittest_equality.EqualityTest) ... ok
	testExpectNotEqualFails (unittest_equality.EqualityTest) ...
	FAIL
	
	================================================================
	FAIL: testExpectEqualFails (unittest_equality.EqualityTest)
	----------------------------------------------------------------
	Traceback (most recent call last):
	  File ".../unittest_equality.py", line 15, in
	testExpectEqualFails
	    self.assertEqual(2, 3 - 2)
	AssertionError: 2 != 1
	
	================================================================
	FAIL: testExpectNotEqualFails (unittest_equality.EqualityTest)
	----------------------------------------------------------------
	Traceback (most recent call last):
	  File ".../unittest_equality.py", line 21, in
	testExpectNotEqualFails
	    self.assertNotEqual(1, 3 - 2)
	AssertionError: 1 == 1
	
	----------------------------------------------------------------
	Ran 4 tests in 0.001s
	
	FAILED (failures=2)

.. {{{end}}}

Almost Equal?
=============

In addition to strict equality, it is possible to test for near
equality of floating point numbers using :func:`failIfAlmostEqual`
and :func:`failUnlessAlmostEqual`.

.. literalinclude:: unittest_almostequal.py
    :caption:
    :start-after: #end_pymotw_header

The arguments are the values to be compared, and the number of decimal
places to use for the test.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m unittest unittest_almostequal.py',
..                    ignore_error=True))
.. }}}

.. code-block:: none

	$ python3 -m unittest unittest_almostequal.py
	
	.F.
	================================================================
	FAIL: testEqual (unittest_almostequal.AlmostEqualTest)
	----------------------------------------------------------------
	Traceback (most recent call last):
	  File ".../unittest_almostequal.py", line 12, in testEqual
	    self.assertEqual(1.1, 3.3 - 2.2)
	AssertionError: 1.1 != 1.0999999999999996
	
	----------------------------------------------------------------
	Ran 3 tests in 0.001s
	
	FAILED (failures=1)

.. {{{end}}}

Containers
==========


In addition to the generic :func:`assertEqual` and
:func:`assertNotEqual`, there are special methods for comparing
containers like :class:`list`, :class:`dict:`, and :class:`set`
objects.

.. literalinclude:: unittest_equality_container.py
   :caption:
   :start-after: #end_pymotw_header

Each method reports inequality using a format that is meaningful for
the input type, making test failures easier to understand and correct.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m unittest unittest_equality_container.py',
..         line_break_mode='wrap', ignore_error=True))
.. }}}

.. code-block:: none

	$ python3 -m unittest unittest_equality_container.py
	
	FFFFFFF
	================================================================
	FAIL: testCount
	(unittest_equality_container.ContainerEqualityTest)
	----------------------------------------------------------------
	Traceback (most recent call last):
	  File ".../unittest_equality_container.py", line 15, in
	testCount
	    [1, 3, 2, 3],
	AssertionError: Element counts were not equal:
	First has 2, Second has 1:  2
	First has 1, Second has 2:  3
	
	================================================================
	FAIL: testDict
	(unittest_equality_container.ContainerEqualityTest)
	----------------------------------------------------------------
	Traceback (most recent call last):
	  File ".../unittest_equality_container.py", line 21, in
	testDict
	    {'a': 1, 'b': 3},
	AssertionError: {'b': 2, 'a': 1} != {'b': 3, 'a': 1}
	- {'a': 1, 'b': 2}
	?               ^
	
	+ {'a': 1, 'b': 3}
	?               ^
	
	
	================================================================
	FAIL: testList
	(unittest_equality_container.ContainerEqualityTest)
	----------------------------------------------------------------
	Traceback (most recent call last):
	  File ".../unittest_equality_container.py", line 27, in
	testList
	    [1, 3, 2],
	AssertionError: Lists differ: [1, 2, 3] != [1, 3, 2]
	
	First differing element 1:
	2
	3
	
	- [1, 2, 3]
	+ [1, 3, 2]
	
	================================================================
	FAIL: testMultiLineString
	(unittest_equality_container.ContainerEqualityTest)
	----------------------------------------------------------------
	Traceback (most recent call last):
	  File ".../unittest_equality_container.py", line 41, in
	testMultiLineString
	    """),
	AssertionError: '\nThis string\nhas more than one\nline.\n' !=
	'\nThis string has\nmore than two\nlines.\n'
	  
	- This string
	+ This string has
	?            ++++
	- has more than one
	? ----           --
	+ more than two
	?           ++
	- line.
	+ lines.
	?     +
	
	
	================================================================
	FAIL: testSequence
	(unittest_equality_container.ContainerEqualityTest)
	----------------------------------------------------------------
	Traceback (most recent call last):
	  File ".../unittest_equality_container.py", line 47, in
	testSequence
	    [1, 3, 2],
	AssertionError: Sequences differ: [1, 2, 3] != [1, 3, 2]
	
	First differing element 1:
	2
	3
	
	- [1, 2, 3]
	+ [1, 3, 2]
	
	================================================================
	FAIL: testSet
	(unittest_equality_container.ContainerEqualityTest)
	----------------------------------------------------------------
	Traceback (most recent call last):
	  File ".../unittest_equality_container.py", line 53, in testSet
	    set([1, 3, 2, 4]),
	AssertionError: Items in the second set but not the first:
	4
	
	================================================================
	FAIL: testTuple
	(unittest_equality_container.ContainerEqualityTest)
	----------------------------------------------------------------
	Traceback (most recent call last):
	  File ".../unittest_equality_container.py", line 59, in
	testTuple
	    (1, 'b'),
	AssertionError: Tuples differ: (1, 'a') != (1, 'b')
	
	First differing element 1:
	'a'
	'b'
	
	- (1, 'a')
	?      ^
	
	+ (1, 'b')
	?      ^
	
	
	----------------------------------------------------------------
	Ran 7 tests in 0.003s
	
	FAILED (failures=7)

.. {{{end}}}

Use :func:`assertIn` to test container membership.

.. literalinclude:: unittest_in.py
   :caption:
   :start-after: #end_pymotw_header

Any object that supports the ``in`` operator or the container API can
be used with :func:`assertIn`.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m unittest unittest_in.py', ignore_error=True))
.. }}}

.. code-block:: none

	$ python3 -m unittest unittest_in.py
	
	FFF
	================================================================
	FAIL: testDict (unittest_in.ContainerMembershipTest)
	----------------------------------------------------------------
	Traceback (most recent call last):
	  File ".../unittest_in.py", line 12, in testDict
	    self.assertIn(4, {1: 'a', 2: 'b', 3: 'c'})
	AssertionError: 4 not found in {1: 'a', 2: 'b', 3: 'c'}
	
	================================================================
	FAIL: testList (unittest_in.ContainerMembershipTest)
	----------------------------------------------------------------
	Traceback (most recent call last):
	  File ".../unittest_in.py", line 15, in testList
	    self.assertIn(4, [1, 2, 3])
	AssertionError: 4 not found in [1, 2, 3]
	
	================================================================
	FAIL: testSet (unittest_in.ContainerMembershipTest)
	----------------------------------------------------------------
	Traceback (most recent call last):
	  File ".../unittest_in.py", line 18, in testSet
	    self.assertIn(4, set([1, 2, 3]))
	AssertionError: 4 not found in {1, 2, 3}
	
	----------------------------------------------------------------
	Ran 3 tests in 0.001s
	
	FAILED (failures=3)

.. {{{end}}}


Testing for Exceptions
======================

As previously mentioned, if a test raises an exception other than
:class:`AssertionError` it is treated as an error. This is very useful
for uncovering mistakes while modifying code that has existing test
coverage. There are circumstances, however, in which the test should
verify that some code does produce an exception. For example, if an
invalid value is given to an attribute of an object. In such cases,
:func:`assertRaises` makes the code more clear than trapping the
exception in the test. Compare these two tests:

.. literalinclude:: unittest_exception.py
    :caption:
    :start-after: #end_pymotw_header

The results for both are the same, but the second test using
:func:`failUnlessRaises` is more succinct.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-m unittest -v unittest_exception.py'))
.. }}}

.. code-block:: none

	$ python3 -m unittest -v unittest_exception.py
	
	testAssertRaises (unittest_exception.ExceptionTest) ... ok
	testTrapLocally (unittest_exception.ExceptionTest) ... ok
	
	----------------------------------------------------------------
	Ran 2 tests in 0.000s
	
	OK

.. {{{end}}}


Test Fixtures
=============

Fixtures are outside resources needed by a test. For example, tests
for one class may all need an instance of another class that provides
configuration settings or another shared resource. Other test fixtures
include database connections and temporary files (many people would
argue that using external resources makes such tests not "unit" tests,
but they are still tests and still useful).

:mod:`unittest` includes special hooks to configure and clean up any
fixtures needed by tests. To establish fixtures for each individual
test case, override :func:`setUp` on the :class:`TestCase`. To clean
them up, override :func:`tearDown`. To manage one set of fixtures for
all instances of a test class, override the class methods
:func:`setUpClass` and :func:`tearDownClass` for the
:class:`TestCase`. And to handle especially expensive setup operations
for all of the tests within a module, use the module-level functions
:func:`setUpModule` and :func:`tearDownModule`.

.. literalinclude:: unittest_fixtures.py
    :caption:
    :start-after: #end_pymotw_header

When this sample test is run, the order of execution of the fixture
and test methods is apparent.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u -m unittest -v unittest_fixtures.py'))
.. }}}

.. code-block:: none

	$ python3 -u -m unittest -v unittest_fixtures.py
	
	In setUpModule()
	In setUpClass()
	test1 (unittest_fixtures.FixturesTest) ... In setUp()
	In test1()
	In tearDown()
	ok
	test2 (unittest_fixtures.FixturesTest) ... In setUp()
	In test2()
	In tearDown()
	ok
	In tearDownClass()
	In tearDownModule()
	
	----------------------------------------------------------------
	Ran 2 tests in 0.000s
	
	OK

.. {{{end}}}


Test Suites
===========

The standard library documentation describes how to organize test
suites manually.  Automated test discovery is more manageable for
large code bases, in which related tests are not all in the same
place. Tools such as :command:`nose` and :command:`py.test` make it
easier to manage tests when they are spread over multiple files and
directories.

.. seealso::

   * :pydoc:`unittest`

   * :mod:`doctest` -- An alternate means of running tests embedded in
     docstrings or external documentation files.

   * `nose <https://nose.readthedocs.io/en/latest/>`_ -- Third-party
     test runner with sophisticated discovery features.

   * `py.test <http://codespeak.net/py/dist/test/>`_ -- A popular
     third-party test runner with support for distributed execution
     and an alternate fixture management system.

   * `testrepository
     <http://testrepository.readthedocs.io/en/latest/>`_ --
     Third-party test runner used by the OpenStack project, with
     support for parallel execution andtracking failures.
