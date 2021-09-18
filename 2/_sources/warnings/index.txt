============================
warnings -- Non-fatal alerts
============================

.. module:: warnings
    :synopsis: Deliver non-fatal alerts to the user about issues encountered when running a program.

:Purpose: Deliver non-fatal alerts to the user about issues encountered when running a program.
:Available In: 2.1 and later

The :mod:`warnings` module was introduced in :pep:`230` as a way to
warn programmers about changes in language or library features in
anticipation of backwards incompatible changes coming with Python
3.0. Since warnings are not fatal, a program may encounter the same
warn-able situation many times in the course of running. The
:mod:`warnings` module suppresses repeated warnings from the same
source to cut down on the annoyance of seeing the same message over
and over.  You can control the messages printed on a case-by-case
basis using the :option:`-W` option to the interpreter or by calling
functions found in :mod:`warnings` from your code.

Categories and Filtering
========================

Warnings are categorized using subclasses of the built-in exception
class :class:`Warning`. Several standard values are :ref:`described in
the documentation <exceptions-warning>`, and you can add your own by
subclassing from :class:`Warning` to create a new class.

Messages are filtered using settings controlled through the
:option:`-W` option to the interpreter. A filter consists of 5 parts,
the *action*, *message*, *category*, *module*, and *line number*. When
a warning is generated, it is compared against all of the registered
filters. The first filter that matches controls the action taken for
the warning. If no filter matches, the default action is taken.

The actions understood by the filtering mechanism are:

* error: Turn the warning into an exception.
* ignore: Discard the warning.
* always: Always emit a warning.
* default: Print the warning the first time it is generated from each location.
* module: Print the warning the first time it is generated from each module.
* once: Print the warning the first time it is generated.

The *message* portion of the filter is a regular expression that is
used to match the warning text.

The *category* is a name of an exception class, as described above.

The *module* contains a regular expression to be matched against the
module name generating the warning.

And the *line number* can be used to change the handling on specific
occurrences of a warning. Use ``0`` to have the filter apply to all
occurrences.

Generating Warnings
===================

The simplest way to emit a warning from your own code is to just call
:func:`warn()` with the message as an argument:

.. include:: warnings_warn.py
    :literal:
    :start-after: #end_pymotw_header

Then when your program runs, the message is printed:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'warnings_warn.py'))
.. }}}

::

	$ python warnings_warn.py
	
	warnings_warn.py:13: UserWarning: This is a warning message
	  warnings.warn('This is a warning message')
	Before the warning
	After the warning

.. {{{end}}}

Even though the warning is printed, the default behavior is to continue past
the warning and run the rest of the program. We can change that behavior with
a filter:

.. include:: warnings_warn_raise.py
    :literal:
    :start-after: #end_pymotw_header

This filter tells the warnings module to raise an exception when the warning
is issued.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'warnings_warn_raise.py', ignore_error=True))
.. }}}

::

	$ python warnings_warn_raise.py
	
	Before the warning
	Traceback (most recent call last):
	  File "warnings_warn_raise.py", line 15, in <module>
	    warnings.warn('This is a warning message')
	UserWarning: This is a warning message

.. {{{end}}}


We can also control the filter behavior from the command line. For
example, if we go back to ``warnings_warn.py`` and set the filter to
raise an error on :class:`UserWarning`, we see the exception:

.. {{{cog
.. cog.out(run_script(cog.inFile, '-W "error::UserWarning::0" warnings_warn.py', ignore_error=True))
.. }}}

::

	$ python -W "error::UserWarning::0" warnings_warn.py
	
	Before the warning
	Traceback (most recent call last):
	  File "warnings_warn.py", line 13, in <module>
	    warnings.warn('This is a warning message')
	UserWarning: This is a warning message

.. {{{end}}}

Since I left the fields for *message* and *module* blank, they were
interpreted as matching anything.

Filtering with Patterns
=======================

To filter on more complex rules programmatically, use
:func:`filterwarnings()`. For example, to filter based on the content
of the message text:

.. include:: warnings_filterwarnings_message.py
    :literal:
    :start-after: #end_pymotw_header

The pattern contains "``do not``", but the actual message uses "``Do
not``". The pattern matches because the regular expression is always
compiled to look for case insensitive matches.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'warnings_filterwarnings_message.py'))
.. }}}

::

	$ python warnings_filterwarnings_message.py
	
	warnings_filterwarnings_message.py:14: UserWarning: Show this message
	  warnings.warn('Show this message')

.. {{{end}}}

Running this source from the command line:

.. include:: warnings_filtering.py
    :literal:
    :start-after: #end_pymotw_header

yields:

.. {{{cog
.. cog.out(run_script(cog.inFile, '-W "ignore:do not:UserWarning::0" warnings_filtering.py'))
.. }}}

::

	$ python -W "ignore:do not:UserWarning::0" warnings_filtering.py
	
	warnings_filtering.py:12: UserWarning: Show this message
	  warnings.warn('Show this message')

.. {{{end}}}

The same pattern matching rules apply to the name of the source module
containing the warning call. To suppress all warnings from the
``warnings_filtering`` module:

.. include:: warnings_filterwarnings_module.py
    :literal:
    :start-after: #end_pymotw_header

Since the filter is in place, no warnings are emitted when
``warnings_filtering`` is imported:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'warnings_filterwarnings_module.py'))
.. }}}

::

	$ python warnings_filterwarnings_module.py
	

.. {{{end}}}

To suppress only the warning on line 14 of ``warnings_filtering``:

.. include:: warnings_filterwarnings_lineno.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'warnings_filterwarnings_lineno.py'))
.. }}}

::

	$ python warnings_filterwarnings_lineno.py
	
	/Users/dhellmann/Documents/PyMOTW/src/PyMOTW/warnings/warnings_filtering.py:12: UserWarning: Show this message
	  warnings.warn('Show this message')
	/Users/dhellmann/Documents/PyMOTW/src/PyMOTW/warnings/warnings_filtering.py:13: UserWarning: Do not show this message
	  warnings.warn('Do not show this message')

.. {{{end}}}


Repeated Warnings
=================

By default, most types of warnings are only printed the first time they occur
in a given location, where location is defined as the combination of module
and line number.

.. include:: warnings_repeated.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'warnings_repeated.py'))
.. }}}

::

	$ python warnings_repeated.py
	
	warnings_repeated.py:13: UserWarning: This is a warning!
	  warnings.warn('This is a warning!')

.. {{{end}}}


The "once" action can be used to suppress instances of the same message from
different locations.

.. include:: warnings_once.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'warnings_once.py'))
.. }}}

::

	$ python warnings_once.py
	
	warnings_once.py:14: UserWarning: This is a warning!
	  warnings.warn('This is a warning!')

.. {{{end}}}

Similarly, "module" will suppress repeated messages from the same module, no
matter what line number.

Alternate Message Delivery Functions
====================================

Normally warnings are printed to :ref:`sys.stderr
<sys-input-output>`. You can change that behavior by replacing the
:func:`showwarning()` function inside the :mod:`warnings` module. For
example, if you wanted warnings to go to a log file instead of stderr,
you could replace :func:`showwarning()` with a function like this:

.. include:: warnings_showwarning.py
    :literal:
    :start-after: #end_pymotw_header

So that when :func:`warn()` is called, the warnings are emitted with
the rest of the log messages.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'warnings_showwarning.py'))
.. }}}

::

	$ python warnings_showwarning.py
	
	WARNING:root:warnings_showwarning.py:24: UserWarning:This is a warning message

.. {{{end}}}

Formatting
==========

If it is OK for warnings to go to stderr, but you don't like the
formatting, you can replace :func:`formatwarning()` instead.

.. include:: warnings_formatwarning.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'warnings_formatwarning.py'))
.. }}}

::

	$ python warnings_formatwarning.py
	
	warnings_formatwarning.py:15: UserWarning: This is a warning message, before
	  warnings.warn('This is a warning message, before')
	 warnings_formatwarning.py:17: UserWarning:This is a warning message, after

.. {{{end}}}

Stack Level in Warnings
=======================

You'll notice that by default the warning message includes the source
line that generated it, when available. It's not all that useful to
see the line of code with the actual warning message, though. Instead,
you can tell :func:`warn()` how far up the stack it has to go to find
the line the called the function containing the warning. That way
users of a deprecated function see where the function is called,
instead of the implementation of the function.

.. include:: warnings_warn_stacklevel.py
    :literal:
    :start-after: #end_pymotw_header


Notice that in this example :func:`warn()` needs to go up the stack 2
levels, one for itself and one for :func:`old_function()`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'warnings_warn_stacklevel.py'))
.. }}}

::

	$ python warnings_warn_stacklevel.py
	
	warnings_warn_stacklevel.py:18: UserWarning: old_function() is deprecated, use new_function() instead
	  old_function()

.. {{{end}}}

.. seealso::

    `warnings <https://docs.python.org/2/library/warnings.html>`_
        Standard library documentation for this module.

    :pep:`230`
        Warning Framework

    :mod:`exceptions`
        Base classes for exceptions and warnings.
