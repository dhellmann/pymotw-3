=====================================
getopt -- Command line option parsing
=====================================

.. module:: getopt
    :synopsis: Command line option parsing

:Purpose: Command line option parsing
:Available In: 1.4

The getopt module is the *old-school* command line option parser that
supports the conventions established by the Unix function
``getopt()``. It parses an argument sequence, such as ``sys.argv`` and
returns a sequence of (option, argument) pairs and a sequence of
non-option arguments.

Supported option syntax includes:

::

    -a
    -bval
    -b val
    --noarg
    --witharg=val
    --witharg val


Function Arguments
==================

The getopt function takes three arguments:

* The first argument is the sequence of arguments to be parsed. This
  usually comes from ``sys.argv[1:]`` (ignoring the program name in
  ``sys.arg[0]``).

* The second argument is the option definition string for single character
  options. If one of the options requires an argument, its letter is followed
  by a colon. 

* The third argument, if used, should be a sequence of the long-style
  option names. Long style options can be more than a single
  character, such as ``--noarg`` or ``--witharg``. The option names in
  the sequence should not include the ``--`` prefix. If any long
  option requires an argument, its name should have a suffix of ``=``.

Short and long form options can be combined in a single call.

Short Form Options
==================

If a program wants to take 2 options, ``-a``, and ``-b`` with the b
option requiring an argument, the value should be ``"ab:"``.

.. include:: getopt_short.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'getopt_short.py'))
.. }}}

::

	$ python getopt_short.py
	
	([('-a', ''), ('-b', 'val'), ('-c', 'val')], [])

.. {{{end}}}


Long Form Options
=================

If a program wants to take 2 options, ``--noarg`` and ``--witharg``
the sequence should be ``[ 'noarg', 'witharg=' ]``.

.. include:: getopt_long.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'getopt_long.py'))
.. }}}

::

	$ python getopt_long.py
	
	([('--noarg', ''), ('--witharg', 'val'), ('--witharg2', 'another')], [])

.. {{{end}}}


Example
=======

Below is a more complete example program which takes 5 options:
``-o``, ``-v``, ``--output``, ``--verbose``, and ``--version``. The
``-o``, ``--output``, and ``--version`` options each require an
argument.

.. include:: getopt_example.py
    :literal:
    :start-after: #end_pymotw_header

The program can be called in a variety of ways.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'getopt_example.py'))
.. }}}

::

	$ python getopt_example.py
	
	ARGV      : []
	OPTIONS   : []
	VERSION   : 1.0
	VERBOSE   : False
	OUTPUT    : default.out
	REMAINING : []

.. {{{end}}}

A single letter option can be a separate from its argument:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'getopt_example.py -o foo'))
.. }}}

::

	$ python getopt_example.py -o foo
	
	ARGV      : ['-o', 'foo']
	OPTIONS   : [('-o', 'foo')]
	VERSION   : 1.0
	VERBOSE   : False
	OUTPUT    : foo
	REMAINING : []

.. {{{end}}}

or combined:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'getopt_example.py -ofoo'))
.. }}}

::

	$ python getopt_example.py -ofoo
	
	ARGV      : ['-ofoo']
	OPTIONS   : [('-o', 'foo')]
	VERSION   : 1.0
	VERBOSE   : False
	OUTPUT    : foo
	REMAINING : []

.. {{{end}}}

A long form option can similarly be separate:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'getopt_example.py --output foo'))
.. }}}

::

	$ python getopt_example.py --output foo
	
	ARGV      : ['--output', 'foo']
	OPTIONS   : [('--output', 'foo')]
	VERSION   : 1.0
	VERBOSE   : False
	OUTPUT    : foo
	REMAINING : []

.. {{{end}}}

or combined, with ``=``:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'getopt_example.py --output=foo'))
.. }}}

::

	$ python getopt_example.py --output=foo
	
	ARGV      : ['--output=foo']
	OPTIONS   : [('--output', 'foo')]
	VERSION   : 1.0
	VERBOSE   : False
	OUTPUT    : foo
	REMAINING : []

.. {{{end}}}


Abbreviating Long Form Options
==============================

The long form option does not have to be spelled out entirely, so long as a
unique prefix is provided:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'getopt_example.py --o foo'))
.. }}}

::

	$ python getopt_example.py --o foo
	
	ARGV      : ['--o', 'foo']
	OPTIONS   : [('--output', 'foo')]
	VERSION   : 1.0
	VERBOSE   : False
	OUTPUT    : foo
	REMAINING : []

.. {{{end}}}

If a unique prefix is not provided, an exception is raised.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'getopt_example.py --ver 2.0', ignore_error=True))
.. }}}

::

	$ python getopt_example.py --ver 2.0
	
	ARGV      : ['--ver', '2.0']
	Traceback (most recent call last):
	  File "getopt_example.py", line 44, in <module>
	    'version=',
	  File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/getopt.py", line 88, in getopt
	    opts, args = do_longs(opts, args[0][2:], longopts, args[1:])
	  File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/getopt.py", line 152, in do_longs
	    has_arg, opt = long_has_args(opt, longopts)
	  File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/getopt.py", line 179, in long_has_args
	    raise GetoptError('option --%s not a unique prefix' % opt, opt)
	getopt.GetoptError: option --ver not a unique prefix

.. {{{end}}}

Option processing stops as soon as the first non-option argument is
encountered.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'getopt_example.py -v not_an_option --output foo'))
.. }}}

::

	$ python getopt_example.py -v not_an_option --output foo
	
	ARGV      : ['-v', 'not_an_option', '--output', 'foo']
	OPTIONS   : [('-v', '')]
	VERSION   : 1.0
	VERBOSE   : True
	OUTPUT    : default.out
	REMAINING : ['not_an_option', '--output', 'foo']

.. {{{end}}}


GNU-style Option Parsing
========================

New in Python 2.3, an additional function ``gnu_getopt()`` was
added. It allows option and non-option arguments to be mixed on the
command line in any order.

.. include:: getopt_gnu.py
    :literal:
    :start-after: #end_pymotw_header

After changing the call in the previous example, the difference becomes clear:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'getopt_gnu.py -v not_an_option --output foo'))
.. }}}

::

	$ python getopt_gnu.py -v not_an_option --output foo
	
	ARGV      : ['-v', 'not_an_option', '--output', 'foo']
	OPTIONS   : [('-v', ''), ('--output', 'foo')]
	VERSION   : 1.0
	VERBOSE   : True
	OUTPUT    : foo
	REMAINING : ['not_an_option']

.. {{{end}}}


Special Case: ``--``
====================

If ``getopt`` encounters ``--`` in the input arguments, it stops
processing the remaining arguments as options.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'getopt_example.py -v -- --output foo'))
.. }}}

::

	$ python getopt_example.py -v -- --output foo
	
	ARGV      : ['-v', '--', '--output', 'foo']
	OPTIONS   : [('-v', '')]
	VERSION   : 1.0
	VERBOSE   : True
	OUTPUT    : default.out
	REMAINING : ['--output', 'foo']

.. {{{end}}}

.. seealso::

    `getopt <http://docs.python.org/2.7/library/getopt.html>`_
        The standard library documentation for this module.

    :mod:`optparse`
        The :mod:`optparse` module.
