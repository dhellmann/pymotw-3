===============================
 warnings --- Non-fatal Alerts
===============================

.. module:: warnings
    :synopsis: Non-fatal alerts

:Purpose: Deliver non-fatal alerts to the user about issues encountered when running a program.

The :mod:`warnings` module was introduced by :pep:`230` as a way to warn
programmers about changes in language or library features in
anticipation of backwards incompatible changes coming with Python 3.0.
It can also be used to report recoverable configuration errors or
feature degradation from missing libraries.  It is better to deliver
user-facing messages via the :mod:`logging` module, though, because
warnings sent to the console may be lost.

Since warnings are not fatal, a program may encounter the same
warn-able situation many times in the course of running. The
:mod:`warnings` module suppresses repeated messages from the same
source to cut down on the annoyance of seeing the same warning over
and over.  The output can be controlled on a case-by-case
basis, using the command line options to the interpreter or by calling
functions found in :mod:`warnings`.

Categories and Filtering
========================

Warnings are categorized using subclasses of the built-in exception
class :class:`Warning`. Several standard values are described in the
online documentation for the :mod:`exceptions` module, and custom warnings
can be added by subclassing from :class:`Warning`.

Warnings are processed based on *filter* settings.  A filter consists
of five parts: the *action*, *message*, *category*, *module*, and
*line number*.  The *message* portion of the filter is a regular
expression that is used to match the warning text.  The *category* is
a name of an exception class.  The *module* contains a regular
expression to be matched against the module name generating the
warning.  And the *line number* can be used to change the handling on
specific occurrences of a warning. 

When a warning is generated, it is compared against all of the
registered filters. The first filter that matches controls the action
taken for the warning. If no filter matches, the default action is
taken.  The actions understood by the filtering mechanism are listed
in :table:`Warning Filter Actions`.

.. table:: Warning Filter Actions

  =======  =======
  Action   Meaning
  =======  =======
  error    Turn the warning into an exception.
  ignore   Discard the warning.
  always   Always emit a warning.
  default  Print the warning the first time it is generated from each location.
  module   Print the warning the first time it is generated from each module.
  once     Print the warning the first time it is generated.
  =======  =======

Generating Warnings
===================

The simplest way to emit a warning is to call :func:`warn` with
the message as an argument.

.. literalinclude:: warnings_warn.py
    :caption:
    :start-after: #end_pymotw_header

Then, when the program runs, the message is printed.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u warnings_warn.py'))
.. }}}

.. code-block:: none

	$ python3 -u warnings_warn.py
	
	Before the warning
	warnings_warn.py:13: UserWarning: This is a warning message
	  warnings.warn('This is a warning message')
	After the warning

.. {{{end}}}

Even though the warning is printed, the default behavior is to
continue past that point and run the rest of the program. That
behavior can be changed with a filter.

.. literalinclude:: warnings_warn_raise.py
    :caption:
    :start-after: #end_pymotw_header

In this example, the :func:`simplefilter` function adds an entry to
the internal filter list to tell the :mod:`warnings` module to raise
an exception when a :class:`UserWarning` warning is issued.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u warnings_warn_raise.py', ignore_error=True))
.. }}}

.. code-block:: none

	$ python3 -u warnings_warn_raise.py
	
	Before the warning
	Traceback (most recent call last):
	  File "warnings_warn_raise.py", line 15, in <module>
	    warnings.warn('This is a warning message')
	UserWarning: This is a warning message

.. {{{end}}}


The filter behavior can also be controlled from the command line by
using the ``-W`` option to the interpreter.  Specify the filter
properties as a string with the five parts (action, message, category,
module, and line number) separated by colons (``:``). For example, if
``warnings_warn.py`` is run with a filter set to raise an error on
:class:`UserWarning`, an exception is produced.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u -W "error::UserWarning::0" warnings_warn.py', ignore_error=True))
.. }}}

.. code-block:: none

	$ python3 -u -W "error::UserWarning::0" warnings_warn.py
	
	Before the warning
	Traceback (most recent call last):
	  File "warnings_warn.py", line 13, in <module>
	    warnings.warn('This is a warning message')
	UserWarning: This is a warning message

.. {{{end}}}

Since the fields for *message* and *module* were left blank, they were
interpreted as matching anything.

Filtering with Patterns
=======================

To filter on more complex rules programmatically, use
:func:`filterwarnings`. For example, to filter based on the content
of the message text, give a regular expression pattern as the
*message* argument.

.. literalinclude:: warnings_filterwarnings_message.py
    :caption:
    :start-after: #end_pymotw_header

The pattern contains "``do not``", but the actual message uses "``Do
not``". The pattern matches because the regular expression is always
compiled to look for case insensitive matches.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'warnings_filterwarnings_message.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 warnings_filterwarnings_message.py
	
	warnings_filterwarnings_message.py:14: UserWarning: Show this
	message
	  warnings.warn('Show this message')

.. {{{end}}}

The example program below generates two warnings.

.. literalinclude:: warnings_filter.py
    :caption:
    :start-after: #end_pymotw_header

One of the warnings can be ignored using the filter argument on the
command line.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-W "ignore:do not:UserWarning::0" warnings_filter.py'))
.. }}}

.. code-block:: none

	$ python3 -W "ignore:do not:UserWarning::0" warnings_filter.py
	
	warnings_filter.py:12: UserWarning: Show this message
	  warnings.warn('Show this message')

.. {{{end}}}

The same pattern matching rules apply to the name of the source module
containing the call generating the warning. Suppress all messages from the
``warnings_filter`` module by passing the module name as the
pattern to the *module* argument.

.. literalinclude:: warnings_filterwarnings_module.py
    :caption:
    :start-after: #end_pymotw_header

Since the filter is in place, no warnings are emitted when
``warnings_filter`` is imported.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'warnings_filterwarnings_module.py'))
.. }}}

.. code-block:: none

	$ python3 warnings_filterwarnings_module.py
	

.. {{{end}}}

To suppress only the message on line 13 of ``warnings_filter``,
include the line number as the last argument to
:func:`filterwarnings`.  Use the actual line number from the source
file to limit the filter, or ``0`` to have the filter apply to all
occurrences of the message.

.. literalinclude:: warnings_filterwarnings_lineno.py
    :caption:
    :start-after: #end_pymotw_header

The pattern matches any message, so the important arguments are the
module name and line number.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'warnings_filterwarnings_lineno.py', break_lines_at=70))
.. }}}

.. code-block:: none

	$ python3 warnings_filterwarnings_lineno.py
	
	.../warnings_filter.py:12: UserWarning: Show this message
	  warnings.warn('Show this message')

.. {{{end}}}


Repeated Warnings
=================

By default, most types of warnings are only printed the first time
they occur in a given location, with "location" defined by the
combination of module and line number where the warning is generated.

.. literalinclude:: warnings_repeated.py
    :caption:
    :start-after: #end_pymotw_header

This example calls the same function several times, but produces a single warning.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'warnings_repeated.py'))
.. }}}

.. code-block:: none

	$ python3 warnings_repeated.py
	
	warnings_repeated.py:14: UserWarning: This is a warning!
	  warnings.warn('This is a warning!')

.. {{{end}}}


The ``"once"`` action can be used to suppress instances of the same
message from different locations.

.. literalinclude:: warnings_once.py
    :caption:
    :start-after: #end_pymotw_header

The message text for all warnings is saved and only unique messages
are printed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'warnings_once.py'))
.. }}}

.. code-block:: none

	$ python3 warnings_once.py
	
	warnings_once.py:14: UserWarning: This is a warning!
	  warnings.warn('This is a warning!')

.. {{{end}}}

Similarly, ``"module"`` will suppress repeated messages from the same
module, no matter what line number.

Alternate Message Delivery Functions
====================================

Normally warnings are printed to :data:`sys.stderr`.  Change that
behavior by replacing the :func:`showwarning` function inside the
:mod:`warnings` module. For example, to send warnings to a log file
instead of standard error, replace :func:`showwarning` with a
function that logs the warning.

.. literalinclude:: warnings_showwarning.py
    :caption:
    :start-after: #end_pymotw_header

The warnings are emitted with the rest of the log messages when
:func:`warn` is called.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'warnings_showwarning.py'))
.. }}}

.. code-block:: none

	$ python3 warnings_showwarning.py
	
	WARNING:root:warnings_showwarning.py:28: UserWarning:message

.. {{{end}}}

Formatting
==========

If warnings should go to standard error, but they need to be
reformatted, replace :func:`formatwarning`.

.. literalinclude:: warnings_formatwarning.py
    :caption:
    :start-after: #end_pymotw_header

The format function must return a single string containing the
representation of the warning to be displayed to the user.

.. {{{cog
.. cog.out(run_script(cog.inFile, '-u warnings_formatwarning.py', line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 -u warnings_formatwarning.py
	
	warnings_formatwarning.py:18: UserWarning: Warning message,
	before
	  warnings.warn('Warning message, before')
	-> warnings_formatwarning.py:20: UserWarning:Warning message,
	after

.. {{{end}}}

Stack Level in Warnings
=======================

By default, the warning message includes the source line that
generated it, when available. It is not always useful to see the line
of code with the actual warning message, though. Instead,
:func:`warn` can be told how far up the stack it has to go to find
the line that called the function containing the warning.  That way,
users of a deprecated function can see where the function is called,
instead of the implementation of the function.

.. literalinclude:: warnings_warn_stacklevel.py
   :linenos:

In this example :func:`warn` needs to go up the stack two
levels, one for itself and one for :func:`old_function`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'warnings_warn_stacklevel.py', break_lines_at=74))
.. }}}

.. code-block:: none

	$ python3 warnings_warn_stacklevel.py
	
	warnings_warn_stacklevel.py:14: UserWarning: old_function() is deprecated,
	 use new_function()
	  old_function()

.. {{{end}}}

.. seealso::

   * :pydoc:`warnings`

   * :pep:`230` -- Warning Framework

   * :mod:`exceptions` -- Base classes for exceptions and warnings.

   * :mod:`logging` -- An alternative mechanism for delivering
     warnings is to write to the log.
