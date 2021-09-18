=====================================================
argparse -- Command line option and argument parsing.
=====================================================

.. module:: argparse
    :synopsis: Command line option and argument parsing.

:Purpose: Command line option and argument parsing.
:Available In: 2.7 and later

The :mod:`argparse` module was added to Python 2.7 as a replacement
for :mod:`optparse`.  The implementation of :mod:`argparse` supports
features that would not have been easy to add to :mod:`optparse`, and
that would have required backwards-incompatible API changes, so a new
module was brought into the library instead.  :mod:`optparse` is still
supported, but is not likely to receive new features.

Comparing with optparse
=======================

The API for :mod:`argparse` is similar to the one provided by
:mod:`optparse`, and in many cases :mod:`argparse` can be used as a
straightforward replacement by updating the names of the classes and
methods used.  There are a few places where direct compatibility could
not be preserved as new features were added, however.

You will have to decide whether to upgrade existing programs on a
case-by-case basis.  If you have written extra code to work around
limitations of :mod:`optparse`, you may want to upgrade to reduce the
amount of code you need to maintain.  New programs should probably use
argparse, if it is available on all deployment platforms.

Setting up a Parser
===================

The first step when using :mod:`argparse` is to create a parser object
and tell it what arguments to expect.  The parser can then be used to
process the command line arguments when your program runs.

The parser class is :class:`ArgumentParser`.  The constructor takes
several arguments to set up the description used in the help text for
the program and other global behaviors or settings.

::

    import argparse
    parser = argparse.ArgumentParser(description='This is a PyMOTW sample program')


Defining Arguments
==================

:mod:`argparse` is a complete argument *processing* library. Arguments
can trigger different actions, specified by the *action* argument to
:func:`add_argument()`. Supported actions include storing the argument
(singly, or as part of a list), storing a constant value when the
argument is encountered (including special handling for true/false
values for boolean switches), counting the number of times an argument
is seen, and calling a callback.

The default action is to store the argument value. In this case, if a
type is provided, the value is converted to that type before it is
stored. If the *dest* argument is provided, the value is saved to an
attribute of that name on the Namespace object returned when the
command line arguments are parsed.

Parsing a Command Line
======================

Once all of the arguments are defined, you can parse the command line
by passing a sequence of argument strings to :func:`parse_args()`. By
default, the arguments are taken from ``sys.argv[1:]``, but you can
also pass your own list. The options are processed using the GNU/POSIX
syntax, so option and argument values can be mixed in the sequence.

The return value from :func:`parse_args()` is a :class:`Namespace`
containing the arguments to the command. The object holds the argument
values as attributes, so if your argument ``dest`` is ``"myoption"``,
you access the value as ``args.myoption``.

Simple Examples
===============

Here is a simple example with 3 different options: a boolean option
(``-a``), a simple string option (``-b``), and an integer option
(``-c``).

.. include:: argparse_short.py
    :literal:
    :start-after: #end_pymotw_header

There are a few ways to pass values to single character options. The
example above uses two different forms, ``-bval`` and ``-c val``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_short.py'))
.. }}}

::

	$ python argparse_short.py
	
	Namespace(a=True, b='val', c=3)

.. {{{end}}}

The type of the value associated with ``'c'`` in the output is an
integer, since the :class:`ArgumentParser` was told to convert the
argument before storing it.

"Long" option names, with more than a single character in their name,
are handled in the same way.

.. include:: argparse_long.py
    :literal:
    :start-after: #end_pymotw_header

And the results are similar:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_long.py'))
.. }}}

::

	$ python argparse_long.py
	
	Namespace(noarg=True, witharg='val', witharg2=3)

.. {{{end}}}

One area in which :mod:`argparse` differs from :mod:`optparse` is the
treatment of non-optional argument values.  While :mod:`optparse`
sticks to option parsing, :mod:`argparse` is a full command-line
argument parser tool, and handles non-optional arguments as well.

.. include:: argparse_arguments.py
   :literal:
   :start-after: #end_pymotw_header

In this example, the "count" argument is an integer and the "units"
argument is saved as a string.  If either is not provided on the
command line, or the value given cannot be converted to the right
type, an error is reported.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_arguments.py 3 inches'))
.. cog.out(run_script(cog.inFile, 'argparse_arguments.py some inches', ignore_error=True, include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_arguments.py', ignore_error=True, include_prefix=False))
.. }}}

::

	$ python argparse_arguments.py 3 inches
	
	Namespace(count=3, units='inches')

	$ python argparse_arguments.py some inches
	
	usage: argparse_arguments.py [-h] count units
	argparse_arguments.py: error: argument count: invalid int value: 'some'

	$ python argparse_arguments.py
	
	usage: argparse_arguments.py [-h] count units
	argparse_arguments.py: error: too few arguments

.. {{{end}}}

Argument Actions
----------------

There are six built-in actions that can be triggered when an argument
is encountered:

``store``
  Save the value, after optionally converting it to a different type.
  This is the default action taken if none is specified expliclity.

``store_const``
  Save a value defined as part of the argument specification, rather
  than a value that comes from the arguments being parsed.  This is
  typically used to implement command line flags that aren't booleans.

``store_true`` / ``store_false``
  Save the appropriate boolean value.  These actions are used to
  implement boolean switches.

``append``
  Save the value to a list.  Multiple values are saved if the argument
  is repeated.

``append_const``
  Save a value defined in the argument specification to a list.

``version``
  Prints version details about the program and then exits.

.. include:: argparse_action.py
   :literal:
   :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_action.py -h'))
.. cog.out(run_script(cog.inFile, 'argparse_action.py -s value', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_action.py -c', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_action.py -t', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_action.py -f', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_action.py -a one -a two -a three', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_action.py -B -A', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_action.py --version', include_prefix=False))
.. }}}

::

	$ python argparse_action.py -h
	
	usage: argparse_action.py [-h] [-s SIMPLE_VALUE] [-c] [-t] [-f]
	                          [-a COLLECTION] [-A] [-B] [--version]
	
	optional arguments:
	  -h, --help       show this help message and exit
	  -s SIMPLE_VALUE  Store a simple value
	  -c               Store a constant value
	  -t               Set a switch to true
	  -f               Set a switch to false
	  -a COLLECTION    Add repeated values to a list
	  -A               Add different values to list
	  -B               Add different values to list
	  --version        show program's version number and exit

	$ python argparse_action.py -s value
	
	simple_value     = value
	constant_value   = None
	boolean_switch   = False
	collection       = []
	const_collection = []

	$ python argparse_action.py -c
	
	simple_value     = None
	constant_value   = value-to-store
	boolean_switch   = False
	collection       = []
	const_collection = []

	$ python argparse_action.py -t
	
	simple_value     = None
	constant_value   = None
	boolean_switch   = True
	collection       = []
	const_collection = []

	$ python argparse_action.py -f
	
	simple_value     = None
	constant_value   = None
	boolean_switch   = False
	collection       = []
	const_collection = []

	$ python argparse_action.py -a one -a two -a three
	
	simple_value     = None
	constant_value   = None
	boolean_switch   = False
	collection       = ['one', 'two', 'three']
	const_collection = []

	$ python argparse_action.py -B -A
	
	simple_value     = None
	constant_value   = None
	boolean_switch   = False
	collection       = []
	const_collection = ['value-2-to-append', 'value-1-to-append']

	$ python argparse_action.py --version
	
	argparse_action.py 1.0

.. {{{end}}}



Option Prefixes
---------------

The default syntax for options is based on the Unix convention of
signifying command line switches using a prefix of "-".
:mod:`argparse` supports other prefixes, so you can make your program
conform to the local platform default (i.e., use "/" on Windows)
or follow a different convention.

.. include:: argparse_prefix_chars.py
   :literal:
   :start-after: #end_pymotw_header

Set the *prefix_chars* parameter for the :class:`ArgumentParser` to a
string containing all of the characters that should be allowed to
signify options.  It is important to understand that although
*prefix_chars* establishes the allowed switch characters, the
individual argument definitions specify the syntax for a given switch.
This gives you explicit control over whether options using different
prefixes are aliases (such as might be the case for
platform-independent command line syntax) or alternatives (e.g., using
"``+``" to indicate turning a switch on and "``-``" to turn it off).
In the example above, ``+a`` and ``-a`` are separate arguments, and
``//noarg`` can also be given as ``++noarg``, but not ``--noarg``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_prefix_chars.py -h'))
.. cog.out(run_script(cog.inFile, 'argparse_prefix_chars.py +a', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_prefix_chars.py -a', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_prefix_chars.py //noarg', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_prefix_chars.py ++noarg', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_prefix_chars.py --noarg', ignore_error=True, include_prefix=False))
.. }}}

::

	$ python argparse_prefix_chars.py -h
	
	usage: argparse_prefix_chars.py [-h] [-a] [+a] [//noarg]
	
	Change the option prefix characters
	
	optional arguments:
	  -h, --help        show this help message and exit
	  -a                Turn A off
	  +a                Turn A on
	  //noarg, ++noarg

	$ python argparse_prefix_chars.py +a
	
	Namespace(a=True, noarg=False)

	$ python argparse_prefix_chars.py -a
	
	Namespace(a=False, noarg=False)

	$ python argparse_prefix_chars.py //noarg
	
	Namespace(a=None, noarg=True)

	$ python argparse_prefix_chars.py ++noarg
	
	Namespace(a=None, noarg=True)

	$ python argparse_prefix_chars.py --noarg
	
	usage: argparse_prefix_chars.py [-h] [-a] [+a] [//noarg]
	argparse_prefix_chars.py: error: unrecognized arguments: --noarg

.. {{{end}}}


Sources of Arguments
--------------------

In the examples so far, the list of arguments given to the parser have
come from a list passed in explicitly, or were taken implicitly from
:ref:`sys.argv <sys-argv>`.  Passing the list explicitly is useful
when you are using :mod:`argparse` to process command line-like
instructions that do not come from the command line (such as in a
configuration file).

.. include:: argparse_with_shlex.py
   :literal:
   :start-after: #end_pymotw_header

:mod:`shlex` makes it easy to split the string stored in the
configuration file.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_with_shlex.py'))
.. }}}

::

	$ python argparse_with_shlex.py
	
	Config  : -a -b 2
	Arg List: ['-a', '-b', '2']
	Results : Namespace(a=True, b='2', c=None)

.. {{{end}}}

An alternative to processing the configuration file yourself is to
tell :mod:`argparse` how to recognize an argument that specifies an
input file containing a set of arguments to be processed using
*fromfile_prefix_chars*.

.. include:: argparse_fromfile_prefix_chars.py
   :literal:
   :start-after: #end_pymotw_header

This example stops when it finds an argument prefixed with ``@``, then
reads the named file to find more arguments.  For example, an input
file ``argparse_fromfile_prefix_chars.txt`` contains a series of
arguments, one per line:

.. include:: argparse_fromfile_prefix_chars.txt
   :literal:

The output produced when processing the file is:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_fromfile_prefix_chars.py'))
.. }}}

::

	$ python argparse_fromfile_prefix_chars.py
	
	Namespace(a=True, b='2', c=None)

.. {{{end}}}

Automatically Generated Options
===============================

:mod:`argparse` will automatically add options to generate help and
show the version information for your application, if configured to do
so.

The *add_help* argument to :class:`ArgumentParser` controls the
help-related options.

.. include:: argparse_with_help.py
   :literal:
   :start-after: #end_pymotw_header

The help options (``-h`` and ``--help``) are added by default, but can
be disabled by setting *add_help* to false.

.. include:: argparse_without_help.py
   :literal:
   :start-after: #end_pymotw_header

Although ``-h`` and ``--help`` are defacto standard option names for
requesting help, some applications or uses of :mod:`argparse` either
don't need to provide help or need to use those option names for other
purposes.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_with_help.py -h'))
.. cog.out(run_script(cog.inFile, 'argparse_without_help.py -h', ignore_error=True, include_prefix=False))
.. }}}

::

	$ python argparse_with_help.py -h
	
	usage: argparse_with_help.py [-h] [-a] [-b B] [-c C]
	
	optional arguments:
	  -h, --help  show this help message and exit
	  -a
	  -b B
	  -c C

	$ python argparse_without_help.py -h
	
	usage: argparse_without_help.py [-a] [-b B] [-c C]
	argparse_without_help.py: error: unrecognized arguments: -h

.. {{{end}}}

The version options (``-v`` and ``--version``) are added when
*version* is set in the :class:`ArgumentParser` constructor.

.. include:: argparse_with_version.py
   :literal:
   :start-after: #end_pymotw_header

Both forms of the option print the program's version string, then
cause it to exit immediately.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_with_version.py -h'))
.. cog.out(run_script(cog.inFile, 'argparse_with_version.py -v', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_with_version.py --version', include_prefix=False))
.. }}}

::

	$ python argparse_with_version.py -h
	
	usage: argparse_with_version.py [-h] [-v] [-a] [-b B] [-c C]
	
	optional arguments:
	  -h, --help     show this help message and exit
	  -v, --version  show program's version number and exit
	  -a
	  -b B
	  -c C

	$ python argparse_with_version.py -v
	
	1.0

	$ python argparse_with_version.py --version
	
	1.0

.. {{{end}}}

Parser Organization
===================

:mod:`argparse` includes several features for organizing your argument
parsers, to make implementation easier or to improve the usability of
the help output.

Sharing Parser Rules
--------------------

It is common to need to implement a suite of command line programs
that all take a set of arguments, and then specialize in some way.
For example, if the programs all need to authenticate the user before
taking any real action, they would all need to support ``--user`` and
``--password`` options.  Rather than add the options explicitly to
every :class:`ArgumentParser`, you can define a "parent" parser with
the shared options, and then have the parsers for the individual
programs inherit from its options.

The first step is to set up the parser with the shared argument
definitions.  Since each subsequent user of the parent parser is going
to try to add the same help options, causing an exception, we turn off
automatic help generation in the base parser.

.. include:: argparse_parent_base.py
   :literal:
   :start-after: #end_pymotw_header

Next, create another parser with *parents* set:

.. include:: argparse_uses_parent.py
   :literal:
   :start-after: #end_pymotw_header

And the resulting program takes all three options:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_uses_parent.py -h'))
.. }}}

::

	$ python argparse_uses_parent.py -h
	
	usage: argparse_uses_parent.py [-h] [--user USER] [--password PASSWORD]
	                               [--local-arg]
	
	optional arguments:
	  -h, --help           show this help message and exit
	  --user USER
	  --password PASSWORD
	  --local-arg

.. {{{end}}}


Conflicting Options
-------------------

The previous example pointed out that adding two argument handlers to
a parser using the same argument name causes an exception.  Change the
conflict resolution behavior by passing a *conflict_handler*.  The two
built-in handlers are ``error`` (the default), and ``resolve``, which
picks a handler based on the order they are added.

.. include:: argparse_conflict_handler_resolve.py
   :literal:
   :start-after: #end_pymotw_header

Since the last handler with a given argument name is used, in this
example the stand-alone option ``-b`` is masked by the alias for
``--long-b``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_conflict_handler_resolve.py'))
.. }}}

::

	$ python argparse_conflict_handler_resolve.py
	
	usage: argparse_conflict_handler_resolve.py [-h] [-a A] [--long-b LONG_B]
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -a A
	  --long-b LONG_B, -b LONG_B
	                        Long and short together

.. {{{end}}}

Switching the order of the calls to :func:`add_argument` unmasks the
stand-alone option:

.. include:: argparse_conflict_handler_resolve2.py
   :literal:
   :start-after: #end_pymotw_header

Now both options can be used together.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_conflict_handler_resolve2.py'))
.. }}}

::

	$ python argparse_conflict_handler_resolve2.py
	
	usage: argparse_conflict_handler_resolve2.py [-h] [-a A] [--long-b LONG_B]
	                                             [-b B]
	
	optional arguments:
	  -h, --help       show this help message and exit
	  -a A
	  --long-b LONG_B  Long and short together
	  -b B             Short alone

.. {{{end}}}

Argument Groups
---------------

:mod:`argparse` combines the argument definitions into "groups."  By
default, it uses two groups, with one for options and another for
required position-based arguments.

.. include:: argparse_default_grouping.py
   :literal:
   :start-after: #end_pymotw_header

The grouping is reflected in the separate "positional arguments" and
"optional arguments" section of the help output:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_default_grouping.py -h'))
.. }}}

::

	$ python argparse_default_grouping.py -h
	
	usage: argparse_default_grouping.py [-h] [--optional] positional
	
	Short sample app
	
	positional arguments:
	  positional
	
	optional arguments:
	  -h, --help  show this help message and exit
	  --optional

.. {{{end}}}

You can adjust the grouping to make it more logical in the help, so
that related options or values are documented together.  The
shared-option example from earlier could be written using custom
grouping so that the authentication options are shown together in the
help.

Create the "authentication" group with :func:`add_argument_group` and
then add each of the authentication-related options to the group,
instead of the base parser.

.. include:: argparse_parent_with_group.py
   :literal:
   :start-after: #end_pymotw_header

The program using the group-based parent lists it in the *parents*
value, just as before.

.. include:: argparse_uses_parent_with_group.py
   :literal:
   :start-after: #end_pymotw_header

The help output now shows the authentication options together.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_uses_parent_with_group.py -h'))
.. }}}

::

	$ python argparse_uses_parent_with_group.py -h
	
	usage: argparse_uses_parent_with_group.py [-h] [--user USER]
	                                          [--password PASSWORD] [--local-arg]
	
	optional arguments:
	  -h, --help           show this help message and exit
	  --local-arg
	
	authentication:
	  --user USER
	  --password PASSWORD

.. {{{end}}}

Mutually Exclusive Options
--------------------------

Defining mutually exclusive options is a special case of the option
grouping feature, and uses :func:`add_mutually_exclusive_group`
instead of :func:`add_argument_group`.

.. include:: argparse_mutually_exclusive.py
   :literal:
   :start-after: #end_pymotw_header

:mod:`argparse` enforces the mutal exclusivity for you, so that only
one of the options from the group can be given.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_mutually_exclusive.py -h'))
.. cog.out(run_script(cog.inFile, 'argparse_mutually_exclusive.py -a', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_mutually_exclusive.py -b', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_mutually_exclusive.py -a -b', ignore_error=True, include_prefix=False))
.. }}}

::

	$ python argparse_mutually_exclusive.py -h
	
	usage: argparse_mutually_exclusive.py [-h] [-a | -b]
	
	optional arguments:
	  -h, --help  show this help message and exit
	  -a
	  -b

	$ python argparse_mutually_exclusive.py -a
	
	Namespace(a=True, b=False)

	$ python argparse_mutually_exclusive.py -b
	
	Namespace(a=False, b=True)

	$ python argparse_mutually_exclusive.py -a -b
	
	usage: argparse_mutually_exclusive.py [-h] [-a | -b]
	argparse_mutually_exclusive.py: error: argument -b: not allowed with argument -a

.. {{{end}}}

Nesting Parsers
---------------

The parent parser approach described above is one way to share options
between related commands.  An alternate approach is to combine the
commands into a single program, and use subparsers to handle each
portion of the command line.  The result works in the way ``svn``,
``hg``, and other programs with multiple command line actions, or
sub-commands, does.

A program to work with directories on the filesystem might define
commands for creating, deleting, and listing the contents of a
directory like this:

.. include:: argparse_subparsers.py
   :literal:
   :start-after: #end_pymotw_header

The help output shows the named subparsers as "commands" that can be
specified on the command line as positional arguments.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_subparsers.py -h'))
.. }}}

::

	$ python argparse_subparsers.py -h
	
	usage: argparse_subparsers.py [-h] {list,create,delete} ...
	
	positional arguments:
	  {list,create,delete}  commands
	    list                List contents
	    create              Create a directory
	    delete              Remove a directory
	
	optional arguments:
	  -h, --help            show this help message and exit

.. {{{end}}}

Each subparser also has its own help, describing the arguments and
options for that command.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_subparsers.py create -h'))
.. }}}

::

	$ python argparse_subparsers.py create -h
	
	usage: argparse_subparsers.py create [-h] [--read-only] dirname
	
	positional arguments:
	  dirname      New directory to create
	
	optional arguments:
	  -h, --help   show this help message and exit
	  --read-only  Set permissions to prevent writing to the directory

.. {{{end}}}

And when the arguments are parsed, the :class:`Namespace` object
returned by :func:`parse_args` includes only the values related to the
command specified.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_subparsers.py delete -r foo'))
.. }}}

::

	$ python argparse_subparsers.py delete -r foo
	
	Namespace(dirname='foo', recursive=True)

.. {{{end}}}


Advanced Argument Processing
============================

The examples so far have shown simple boolean flags, options with
string or numerical arguments, and positional arguments.
:mod:`argparse` supports sophisticated argument specification for
variable-length argument list, enumerations, and constant values as
well.

Variable Argument Lists
-----------------------

You can configure a single argument defintion to consume multiple
arguments on the command line being parsed.  Set *nargs* to one of
these flag values, based on the number of required or expected
arguments:

=======  =======
Value    Meaning
=======  =======
 ``N``    The absolute number of arguments (e.g., ``3``).
 ``?``    0 or 1 arguments
 ``*``    0 or all arguments
 ``+``    All, and at least one, argument
=======  =======

.. include:: argparse_nargs.py
   :literal:
   :start-after: #end_pymotw_header

The parser enforces the argument count instructions, and generates an
accurate syntax diagram as part of the command help text.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_nargs.py -h'))
.. cog.out(run_script(cog.inFile, 'argparse_nargs.py', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_nargs.py --three', include_prefix=False, ignore_error=True))
.. cog.out(run_script(cog.inFile, 'argparse_nargs.py --three a b c', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_nargs.py --optional', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_nargs.py --optional with_value', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_nargs.py --all with multiple values', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_nargs.py --one-or-more with_value', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_nargs.py --one-or-more with multiple values', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_nargs.py --one-or-more', ignore_error=True, include_prefix=False))
.. }}}

::

	$ python argparse_nargs.py -h
	
	usage: argparse_nargs.py [-h] [--three THREE THREE THREE]
	                         [--optional [OPTIONAL]] [--all [ALL [ALL ...]]]
	                         [--one-or-more ONE_OR_MORE [ONE_OR_MORE ...]]
	
	optional arguments:
	  -h, --help            show this help message and exit
	  --three THREE THREE THREE
	  --optional [OPTIONAL]
	  --all [ALL [ALL ...]]
	  --one-or-more ONE_OR_MORE [ONE_OR_MORE ...]

	$ python argparse_nargs.py
	
	Namespace(all=None, one_or_more=None, optional=None, three=None)

	$ python argparse_nargs.py --three
	
	usage: argparse_nargs.py [-h] [--three THREE THREE THREE]
	                         [--optional [OPTIONAL]] [--all [ALL [ALL ...]]]
	                         [--one-or-more ONE_OR_MORE [ONE_OR_MORE ...]]
	argparse_nargs.py: error: argument --three: expected 3 argument(s)

	$ python argparse_nargs.py --three a b c
	
	Namespace(all=None, one_or_more=None, optional=None, three=['a', 'b', 'c'])

	$ python argparse_nargs.py --optional
	
	Namespace(all=None, one_or_more=None, optional=None, three=None)

	$ python argparse_nargs.py --optional with_value
	
	Namespace(all=None, one_or_more=None, optional='with_value', three=None)

	$ python argparse_nargs.py --all with multiple values
	
	Namespace(all=['with', 'multiple', 'values'], one_or_more=None, optional=None, three=None)

	$ python argparse_nargs.py --one-or-more with_value
	
	Namespace(all=None, one_or_more=['with_value'], optional=None, three=None)

	$ python argparse_nargs.py --one-or-more with multiple values
	
	Namespace(all=None, one_or_more=['with', 'multiple', 'values'], optional=None, three=None)

	$ python argparse_nargs.py --one-or-more
	
	usage: argparse_nargs.py [-h] [--three THREE THREE THREE]
	                         [--optional [OPTIONAL]] [--all [ALL [ALL ...]]]
	                         [--one-or-more ONE_OR_MORE [ONE_OR_MORE ...]]
	argparse_nargs.py: error: argument --one-or-more: expected at least one argument

.. {{{end}}}

Argument Types
--------------

:mod:`argparse` treats all argument values as strings, unless you tell
it to convert the string to another type.  The *type* parameter to
:func:`add_argument` expects a converter function used by the
:class:`ArgumentParser` to transform the argument value from a string
to some other type.

.. include:: argparse_type.py
   :literal:
   :start-after: #end_pymotw_header

Any callable that takes a single string argument can be passed as
*type*, including built-in types like :func:`int`, :func:`float`, and
:func:`file`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_type.py -i 1'))
.. cog.out(run_script(cog.inFile, 'argparse_type.py -f 3.14', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_type.py --file argparse_type.py', include_prefix=False))
.. }}}

::

	$ python argparse_type.py -i 1
	
	Namespace(f=None, file=None, i=1)

	$ python argparse_type.py -f 3.14
	
	Namespace(f=3.14, file=None, i=None)

	$ python argparse_type.py --file argparse_type.py
	
	Namespace(f=None, file=<open file 'argparse_type.py', mode 'r' at 0x1004de270>, i=None)

.. {{{end}}}

If the type conversion fails, :mod:`argparse` raises an exception.
:ref:`TypeError <exceptions-TypeError>` and :ref:`ValueError
<exceptions-ValueError>` exceptions are trapped automatically and
converted to a simple error message for the user.  Other exceptions,
such as the :ref:`IOError <exceptions-IOError>` in the example below
where the input file does not exist, must be handled by the caller.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_type.py -i a', ignore_error=True))
.. cog.out(run_script(cog.inFile, 'argparse_type.py -f 3.14.15', ignore_error=True, include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_type.py --file does_not_exist.txt', ignore_error=True, include_prefix=False))
.. }}}

::

	$ python argparse_type.py -i a
	
	usage: argparse_type.py [-h] [-i I] [-f F] [--file FILE]
	argparse_type.py: error: argument -i: invalid int value: 'a'

	$ python argparse_type.py -f 3.14.15
	
	usage: argparse_type.py [-h] [-i I] [-f F] [--file FILE]
	argparse_type.py: error: argument -f: invalid float value: '3.14.15'

	$ python argparse_type.py --file does_not_exist.txt
	
	usage: argparse_type.py [-h] [-i I] [-f F] [--file FILE]
	argparse_type.py: error: [Errno 2] No such file or directory: 'does_not_exist.txt'

.. {{{end}}}

To limit an input argument to a value within a pre-defined set, use
the *choices* parameter.

.. include:: argparse_choices.py
   :literal:
   :start-after: #end_pymotw_header

If the argument to ``--mode`` is not one of the allowed values, an
error is generated and processing stops.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_choices.py -h'))
.. cog.out(run_script(cog.inFile, 'argparse_choices.py --mode read-only', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_choices.py --mode invalid', include_prefix=False, ignore_error=True, break_lines_at=71))
.. }}}

::

	$ python argparse_choices.py -h
	
	usage: argparse_choices.py [-h] [--mode {read-only,read-write}]
	
	optional arguments:
	  -h, --help            show this help message and exit
	  --mode {read-only,read-write}

	$ python argparse_choices.py --mode read-only
	
	Namespace(mode='read-only')

	$ python argparse_choices.py --mode invalid
	
	usage: argparse_choices.py [-h] [--mode {read-only,read-write}]
	argparse_choices.py: error: argument --mode: invalid choice: 'invalid' 
	(choose from 'read-only', 'read-write')

.. {{{end}}}

File Arguments
--------------

Although :class:`file` objects can instantiated with a single string
argument, that does not allow you to specify the access mode.
:class:`FileType` gives you a more flexible way of specifying that an
argument should be a file, including the mode and buffer size.

.. include:: argparse_FileType.py
   :literal:
   :start-after: #end_pymotw_header

The value associated with the argument name is the open file handle.
You are responsible for closing the file yourself when you are done
with it.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_FileType.py -h'))
.. cog.out(run_script(cog.inFile, 'argparse_FileType.py -i argparse_FileType.py -o temporary_file.txt', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'argparse_FileType.py -i no_such_file.txt', include_prefix=False, ignore_error=True))
.. }}}

::

	$ python argparse_FileType.py -h
	
	usage: argparse_FileType.py [-h] [-i in-file] [-o out-file]
	
	optional arguments:
	  -h, --help   show this help message and exit
	  -i in-file
	  -o out-file

	$ python argparse_FileType.py -i argparse_FileType.py -o temporary_file.\
	txt
	
	Input file: <open file 'argparse_FileType.py', mode 'rt' at 0x1004de270>
	Output file: <open file 'temporary_file.txt', mode 'wt' at 0x1004de300>

	$ python argparse_FileType.py -i no_such_file.txt
	
	usage: argparse_FileType.py [-h] [-i in-file] [-o out-file]
	argparse_FileType.py: error: argument -i: can't open 'no_such_file.txt': [Errno 2] No such file or directory: 'no_such_file.txt'

.. {{{end}}}


Custom Actions
--------------

In addition to the built-in actions described earlier, you can define
custom actions by providing an object that implements the Action API.
The object passed to :func:`add_argument` as *action* should take
parameters describing the argument being defined (all of the same
arguments given to :func:`add_argument`) and return a callable object
that takes as parameters the *parser* processing the arguments, the
*namespace* holding the parse results, the *value* of the argument
being acted on, and the *option_string* that triggered the action.

A class :class:`Action` is provided as a convenient starting point for
defining new actions.  The constructor handles the argument
definitions, so you only need to override :func:`__call__` in the
subclass.

.. include:: argparse_custom_action.py
   :literal:
   :start-after: #end_pymotw_header

The type of *values* depends on the value of *nargs*.  If the argument
allows multiple values, *values* will be a list even if it only
contains one item.

The value of *option_string* also depends on the original argument
specifiation.  For positional, required, arguments, *option_string* is
always ``None``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'argparse_custom_action.py'))
.. }}}

::

	$ python argparse_custom_action.py
	
	
	Initializing CustomAction
	  dest = 'a'
	  option_strings = ['-a']
	  required = False
	
	Initializing CustomAction
	  dest = 'm'
	  nargs = '*'
	  option_strings = ['-m']
	  required = False
	
	Initializing CustomAction
	  dest = 'positional'
	  option_strings = []
	  required = True
	
	Processing CustomAction for "a"
	  parser = 4299616464
	  values = 'value'
	  option_string = '-a'
	
	Processing CustomAction for "m"
	  parser = 4299616464
	  values = ['multi-value']
	  option_string = '-m'
	
	Processing CustomAction for "positional"
	  parser = 4299616464
	  values = 'positional-value'
	  option_string = None
	
	Namespace(a='VALUE', m=['MULTI-VALUE'], positional='POSITIONAL-VALUE')

.. {{{end}}}




.. more direct comparison with optparse?

.. seealso::

    `argparse <http://docs.python.org/2.7/library/argparse.html>`_
        The standard library documentation for this module.

    `original argparse <http://pypi.python.org/pypi/argparse>`__
        The PyPI page for the version of argparse from outside of the
        standard libary.  This version is compatible with older
        versions of Python, and can be installed separately.

    :mod:`ConfigParser`
        Read and write configuration files.
