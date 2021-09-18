=======================================
unittest -- Automated testing framework
=======================================

.. module:: unittest
    :synopsis: Automated testing framework

:Purpose: Automated testing framework
:Available In: 2.1

Python's :mod:`unittest` module, sometimes referred to as PyUnit, is
based on the XUnit framework design by Kent Beck and Erich Gamma. The
same pattern is repeated in many other languages, including C, perl,
Java, and Smalltalk. The framework implemented by :mod:`unittest`
supports fixtures, test suites, and a test runner to enable automated
testing for your code.

Basic Test Structure
====================

Tests, as defined by :mod:`unittest`, have two parts: code to manage
test "fixtures", and the test itself. Individual tests are created by
subclassing :class:`TestCase` and overriding or adding appropriate
methods. For example,

.. include:: unittest_simple.py
    :literal:
    :start-after: #end_pymotw_header

In this case, the :class:`SimplisticTest` has a single :func:`test()`
method, which would fail if True is ever False.

Running Tests
=============

The easiest way to run unittest tests is to include:

::

    if __name__ == '__main__':
        unittest.main()

at the bottom of each test file, then simply run the script directly from the
command line:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'unittest_simple.py'))
.. }}}

::

	$ python unittest_simple.py
	
	.
	----------------------------------------------------------------------
	Ran 1 test in 0.000s
	
	OK

.. {{{end}}}

This abbreviated output includes the amount of time the tests took, along with
a status indicator for each test (the "." on the first line of output means
that a test passed). For more detailed test results, include the -v option:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'unittest_simple.py -v'))
.. }}}

::

	$ python unittest_simple.py -v
	
	test (__main__.SimplisticTest) ... ok
	
	----------------------------------------------------------------------
	Ran 1 test in 0.000s
	
	OK

.. {{{end}}}

Test Outcomes
=============

Tests have 3 possible outcomes:

ok
  The test passes.
  
FAIL
  The test does not pass, and raises an AssertionError exception.

ERROR
  The test raises an exception other than AssertionError.

There is no explicit way to cause a test to "pass", so a test's status depends
on the presence (or absence) of an exception. 

.. include:: unittest_outcomes.py
    :literal:
    :start-after: #end_pymotw_header

When a test fails or generates an error, the traceback is included in the
output.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'unittest_outcomes.py', ignore_error=True))
.. }}}

::

	$ python unittest_outcomes.py
	
	EF.
	======================================================================
	ERROR: testError (__main__.OutcomesTest)
	----------------------------------------------------------------------
	Traceback (most recent call last):
	  File "unittest_outcomes.py", line 42, in testError
	    raise RuntimeError('Test error!')
	RuntimeError: Test error!
	
	======================================================================
	FAIL: testFail (__main__.OutcomesTest)
	----------------------------------------------------------------------
	Traceback (most recent call last):
	  File "unittest_outcomes.py", line 39, in testFail
	    self.failIf(True)
	AssertionError: True is not false
	
	----------------------------------------------------------------------
	Ran 3 tests in 0.000s
	
	FAILED (failures=1, errors=1)

.. {{{end}}}


In the example above, :func:`testFail()` fails and the traceback shows
the line with the failure code. It is up to the person reading the
test output to look at the code to figure out the semantic meaning of
the failed test, though. To make it easier to understand the nature of
a test failure, the :func:`fail*()` and :func:`assert*()` methods all
accept an argument *msg*, which can be used to produce a more detailed
error message.

.. include:: unittest_failwithmessage.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'unittest_failwithmessage.py -v', ignore_error=True))
.. }}}

::

	$ python unittest_failwithmessage.py -v
	
	testFail (__main__.FailureMessageTest) ... FAIL
	
	======================================================================
	FAIL: testFail (__main__.FailureMessageTest)
	----------------------------------------------------------------------
	Traceback (most recent call last):
	  File "unittest_failwithmessage.py", line 36, in testFail
	    self.failIf(True, 'failure message goes here')
	AssertionError: failure message goes here
	
	----------------------------------------------------------------------
	Ran 1 test in 0.000s
	
	FAILED (failures=1)

.. {{{end}}}


Asserting Truth
===============

Most tests assert the truth of some condition. There are a few
different ways to write truth-checking tests, depending on the
perspective of the test author and the desired outcome of the code
being tested. If the code produces a value which can be evaluated as
true, the methods :func:`failUnless()` and :func:`assertTrue()` should
be used. If the code produces a false value, the methods
:func:`failIf()` and :func:`assertFalse()` make more sense.

.. include:: unittest_truth.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'unittest_truth.py -v'))
.. }}}

::

	$ python unittest_truth.py -v
	
	testAssertFalse (__main__.TruthTest) ... ok
	testAssertTrue (__main__.TruthTest) ... ok
	testFailIf (__main__.TruthTest) ... ok
	testFailUnless (__main__.TruthTest) ... ok
	
	----------------------------------------------------------------------
	Ran 4 tests in 0.000s
	
	OK

.. {{{end}}}


Testing Equality
================

As a special case, :mod:`unittest` includes methods for testing the
equality of two values.

.. include:: unittest_equality.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'unittest_equality.py -v'))
.. }}}

::

	$ python unittest_equality.py -v
	
	testEqual (__main__.EqualityTest) ... ok
	testNotEqual (__main__.EqualityTest) ... ok
	
	----------------------------------------------------------------------
	Ran 2 tests in 0.000s
	
	OK

.. {{{end}}}


These special tests are handy, since the values being compared appear
in the failure message when a test fails.

.. include:: unittest_notequal.py
    :literal:
    :start-after: #end_pymotw_header


And when these tests are run:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'unittest_notequal.py -v', ignore_error=True))
.. }}}

::

	$ python unittest_notequal.py -v
	
	testEqual (__main__.InequalityTest) ... FAIL
	testNotEqual (__main__.InequalityTest) ... FAIL
	
	======================================================================
	FAIL: testEqual (__main__.InequalityTest)
	----------------------------------------------------------------------
	Traceback (most recent call last):
	  File "unittest_notequal.py", line 36, in testEqual
	    self.failIfEqual(1, 3-2)
	AssertionError: 1 == 1
	
	======================================================================
	FAIL: testNotEqual (__main__.InequalityTest)
	----------------------------------------------------------------------
	Traceback (most recent call last):
	  File "unittest_notequal.py", line 39, in testNotEqual
	    self.failUnlessEqual(2, 3-2)
	AssertionError: 2 != 1
	
	----------------------------------------------------------------------
	Ran 2 tests in 0.000s
	
	FAILED (failures=2)

.. {{{end}}}


Almost Equal?
=============

In addition to strict equality, it is possible to test for near
equality of floating point numbers using :func:`failIfAlmostEqual()`
and :func:`failUnlessAlmostEqual()`.

.. include:: unittest_almostequal.py
    :literal:
    :start-after: #end_pymotw_header

The arguments are the values to be compared, and the number of decimal
places to use for the test.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'unittest_almostequal.py'))
.. }}}

::

	$ python unittest_almostequal.py
	
	..
	----------------------------------------------------------------------
	Ran 2 tests in 0.000s
	
	OK

.. {{{end}}}

Testing for Exceptions
======================

As previously mentioned, if a test raises an exception other than
:ref:`AssertionError <exceptions-AssertionError>` it is treated as an
error. This is very useful for uncovering mistakes while you are
modifying code which has existing test coverage. There are
circumstances, however, in which you want the test to verify that some
code does produce an exception. For example, if an invalid value is
given to an attribute of an object. In such cases,
:func:`failUnlessRaises()` makes the code more clear than trapping the
exception yourself. Compare these two tests:

.. include:: unittest_exception.py
    :literal:
    :start-after: #end_pymotw_header

The results for both are the same, but the second test using
:func:`failUnlessRaises()` is more succinct.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'unittest_exception.py -v'))
.. }}}

::

	$ python unittest_exception.py -v
	
	testFailUnlessRaises (__main__.ExceptionTest) ... ok
	testTrapLocally (__main__.ExceptionTest) ... ok
	
	----------------------------------------------------------------------
	Ran 2 tests in 0.000s
	
	OK
	('a',) {'b': 'c'}
	('a',) {'b': 'c'}

.. {{{end}}}


Test Fixtures
=============

Fixtures are resources needed by a test. For example, if you are
writing several tests for the same class, those tests all need an
instance of that class to use for testing. Other test fixtures include
database connections and temporary files (many people would argue that
using external resources makes such tests not "unit" tests, but they
are still tests and still useful).  :class:`TestCase` includes a
special hook to configure and clean up any fixtures needed by your
tests. To configure the fixtures, override :func:`setUp()`. To clean
up, override :func:`tearDown()`.

.. include:: unittest_fixtures.py
    :literal:
    :start-after: #end_pymotw_header

When this sample test is run, you can see the order of execution of the
fixture and test methods:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'unittest_fixtures.py'))
.. }}}

::

	$ python unittest_fixtures.py
	
	.
	----------------------------------------------------------------------
	Ran 1 test in 0.000s
	
	OK
	In setUp()
	in test()
	In tearDown()

.. {{{end}}}


Test Suites
===========

The standard library documentation describes how to organize test
suites manually. I generally do not use test suites directly, because
I prefer to build the suites automatically (these are automated tests,
after all).  Automating the construction of test suites is especially
useful for large code bases, in which related tests are not all in the
same place. Tools such as nose make it easier to manage tests when
they are spread over multiple files and directories.

.. seealso::

    `unittest <https://docs.python.org/2/library/unittest.html>`_
        Standard library documentation for this module.

    :mod:`doctest`
        An alternate means of running tests embedded in docstrings or 
        external documentation files.

    `nose <http://somethingaboutorange.com/mrl/projects/nose/>`_
        A more sophisticated test manager.

    `unittest2 <http://pypi.python.org/pypi/unittest2>`_
        Ongoing improvements to :mod:`unittest`
