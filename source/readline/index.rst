======================================
 readline -- The GNU readline Library
======================================

.. module:: readline
    :synopsis: The GNU readline library

:Purpose: Provides an interface to the GNU readline library for interacting with the user at a command prompt.

The :mod:`readline` module can be used to enhance interactive command
line programs to make them easier to use.  It is primarily used to
provide command line text completion, or "tab completion".

.. note::

    Because :mod:`readline` interacts with the console content,
    printing debug messages makes it difficult to see what it
    happening in the sample code versus what readline is doing for
    free.  The following examples use the :mod:`logging` module to
    write debug information to a separate file.  The log output is
    shown with each example.

.. note::

   The GNU libraries needed for :mod:`readline` are not available on
   all platforms by default.  If your system does not include them,
   you may need to recompile the Python interpreter to enable the
   module, after installing the dependencies.

Configuring
===========

There are two ways to configure the underlying readline library, using
a configuration file or the :func:`parse_and_bind` function.
Configuration options include the key-binding to invoke completion,
editing modes (:command:`vi` or :command:`emacs`), and many other
values.  Refer to the documentation for the GNU readline library for
details.

The easiest way to enable tab-completion is through a call to
:func:`parse_and_bind`.  Other options can be set at the same time.
This example changes the editing controls to use "vi" mode instead of
the default of "emacs".  To edit the current input line, press ``ESC``
then use normal :command:`vi` navigation keys such as ``j``, ``k``,
``l``, and ``h``.

.. literalinclude:: readline_parse_and_bind.py
    :caption:
    :start-after: #end_pymotw_header

The same configuration can be stored as instructions in a file read by
the library with a single call.  If ``myreadline.rc`` contains

.. literalinclude:: myreadline.rc
    :caption:

the file can be read with :func:`read_init_file`

.. literalinclude:: readline_read_init_file.py
    :caption:
    :start-after: #end_pymotw_header

    

Completing Text
===============

This program has a built-in set of possible commands and uses
tab-completion when the user is entering instructions.

.. literalinclude:: readline_completer.py
    :caption:
    :start-after: #end_pymotw_header

The :func:`input_loop` function reads one line after another
until the input value is ``"stop"``.  A more sophisticated program
could actually parse the input line and run the command.

The :class:`SimpleCompleter` class keeps a list of "options" that are
candidates for auto-completion.  The :func:`complete` method for an
instance is designed to be registered with :mod:`readline` as the
source of completions.  The arguments are a *text* string to complete
and a *state* value, indicating how many times the function has been
called with the same text.  The function is called repeatedly with the
state incremented each time.  It should return a string if there is a
candidate for that state value or ``None`` if there are no more
candidates.  The implementation of :func:`complete` here looks for a
set of matches when state is ``0``, and then returns all of the
candidate matches one at a time on subsequent calls.

When run, the initial output is:

::

    $ python readline_completer.py 

    Prompt ("stop" to quit): 

Pressing ``TAB`` twice causes a list of options to be printed.

::

    $ python readline_completer.py 

    Prompt ("stop" to quit): 
    list   print  start  stop
    Prompt ("stop" to quit): 

The log file shows that :func:`complete` was called with two separate
sequences of state values.

::

    $ tail -f /tmp/completer.log

    DEBUG:root:(empty input) matches: ['list', 'print', 'start', 'stop']
    DEBUG:root:complete('', 0) => 'list'
    DEBUG:root:complete('', 1) => 'print'
    DEBUG:root:complete('', 2) => 'start'
    DEBUG:root:complete('', 3) => 'stop'
    DEBUG:root:complete('', 4) => None
    DEBUG:root:(empty input) matches: ['list', 'print', 'start', 'stop']
    DEBUG:root:complete('', 0) => 'list'
    DEBUG:root:complete('', 1) => 'print'
    DEBUG:root:complete('', 2) => 'start'
    DEBUG:root:complete('', 3) => 'stop'
    DEBUG:root:complete('', 4) => None

The first sequence is from the first TAB key-press.  The completion
algorithm asks for all candidates but does not expand the empty input
line.  Then on the second TAB, the list of candidates is recalculated
so it can be printed for the user.

If the next input is "``l``" followed by another TAB, the screen
shows:

::

    Prompt ("stop" to quit): list

and the log reflects the different arguments to :func:`complete`:

::

    DEBUG:root:'l' matches: ['list']
    DEBUG:root:complete('l', 0) => 'list'
    DEBUG:root:complete('l', 1) => None

Pressing RETURN now causes :func:`raw_input` to return the value, and
the :command:`while` loop cycles.

::

    Dispatch list
    Prompt ("stop" to quit):

There are two possible completions for a command beginning with
"``s``".  Typing "``s``", then pressing TAB finds that "``start``" and
"``stop``" are candidates, but only partially completes the text on
the screen by adding a "``t``".

The log file shows:

::

    DEBUG:root:'s' matches: ['start', 'stop']
    DEBUG:root:complete('s', 0) => 'start'
    DEBUG:root:complete('s', 1) => 'stop'
    DEBUG:root:complete('s', 2) => None

and the screen:

::

    Prompt ("stop" to quit): st


.. warning::

    If a completer function raises an exception, it is ignored
    silently and :mod:`readline` assumes there are no matching
    completions.


Accessing the Completion Buffer
===============================

The completion algorithm in :class:`SimpleCompleter` is simplistic because it only looks at the
text argument passed to the function, but does not use any more of
readline's internal state.  It is also possible to use :mod:`readline`
functions to manipulate the text of the input buffer.

.. literalinclude:: readline_buffer.py
    :caption:
    :start-after: #end_pymotw_header

In this example, commands with sub-options are being completed.
The :func:`complete` method needs to look at the position of the
completion within the input buffer to determine whether it is part of
the first word or a later word.  If the target is the first word, the
keys of the options dictionary are used as candidates.  If it is not
the first word, then the first word is used to find candidates from
the options dictionary.

There are three top-level commands, two of which have sub-commands.

- list

  - files
  - directories

- print

  - byname
  - bysize

- stop


Following the same sequence of actions as before, pressing TAB twice
gives the three top-level commands:

::

    $ python readline_buffer.py 

    Prompt ("stop" to quit): 
    list   print  stop   
    Prompt ("stop" to quit):

and in the log:

::

    DEBUG:root:origline=''
    DEBUG:root:begin=0
    DEBUG:root:end=0
    DEBUG:root:being_completed=
    DEBUG:root:words=[]
    DEBUG:root:complete('', 0) => list
    DEBUG:root:complete('', 1) => print
    DEBUG:root:complete('', 2) => stop
    DEBUG:root:complete('', 3) => None
    DEBUG:root:origline=''
    DEBUG:root:begin=0
    DEBUG:root:end=0
    DEBUG:root:being_completed=
    DEBUG:root:words=[]
    DEBUG:root:complete('', 0) => list
    DEBUG:root:complete('', 1) => print
    DEBUG:root:complete('', 2) => stop
    DEBUG:root:complete('', 3) => None

If the first word is ``"list "`` (with a space after the word), the
candidates for completion are different:

::

    Prompt ("stop" to quit): list 
    directories  files

The log shows that the text being completed is *not* the full line,
but the portion after ``list``.

::

    DEBUG:root:origline='list '
    DEBUG:root:begin=5
    DEBUG:root:end=5
    DEBUG:root:being_completed=
    DEBUG:root:words=['list']
    DEBUG:root:candidates=['files', 'directories']
    DEBUG:root:complete('', 0) => files
    DEBUG:root:complete('', 1) => directories
    DEBUG:root:complete('', 2) => None
    DEBUG:root:origline='list '
    DEBUG:root:begin=5
    DEBUG:root:end=5
    DEBUG:root:being_completed=
    DEBUG:root:words=['list']
    DEBUG:root:candidates=['files', 'directories']
    DEBUG:root:complete('', 0) => files
    DEBUG:root:complete('', 1) => directories
    DEBUG:root:complete('', 2) => None



Input History
=============

:mod:`readline` tracks the input history automatically.  There are two
different sets of functions for working with the history.  The history
for the current session can be accessed with
:func:`get_current_history_length` and :func:`get_history_item`.  That
same history can be saved to a file to be reloaded later using
:func:`write_history_file` and :func:`read_history_file`.  By default
the entire history is saved but the maximum length of the file can be
set with :func:`set_history_length`.  A length of -1 means no limit.

.. literalinclude:: readline_history.py
    :caption:
    :start-after: #end_pymotw_header

The :class:`HistoryCompleter` remembers everything typed, and uses
those values when completing subsequent inputs.

::

    $ python readline_history.py 

    Max history file length: -1
    Startup history: []
    Prompt ("stop" to quit): foo
    Adding "foo" to the history
    Prompt ("stop" to quit): bar
    Adding "bar" to the history
    Prompt ("stop" to quit): blah
    Adding "blah" to the history
    Prompt ("stop" to quit): b
    bar   blah  
    Prompt ("stop" to quit): b
    Prompt ("stop" to quit): stop
    Final history: ['foo', 'bar', 'blah', 'stop']

The log shows this output when the "``b``" is followed by two TABs.

::

    DEBUG:root:history: ['foo', 'bar', 'blah']
    DEBUG:root:matches: ['bar', 'blah']
    DEBUG:root:complete('b', 0) => 'bar'
    DEBUG:root:complete('b', 1) => 'blah'
    DEBUG:root:complete('b', 2) => None
    DEBUG:root:history: ['foo', 'bar', 'blah']
    DEBUG:root:matches: ['bar', 'blah']
    DEBUG:root:complete('b', 0) => 'bar'
    DEBUG:root:complete('b', 1) => 'blah'
    DEBUG:root:complete('b', 2) => None

When the script is run the second time, all of the history is read
from the file.

::

    $ python readline_history.py 

    Max history file length: -1
    Startup history: ['foo', 'bar', 'blah', 'stop']
    Prompt ("stop" to quit): 

There are functions for removing individual history items and clearing
the entire history, as well.


Hooks
=====

There are several hooks available for triggering actions as part of
the interaction sequence.  The *startup* hook is invoked immediately
before printing the prompt, and the *pre-input* hook is run after the
prompt, but before reading text from the user.

.. literalinclude:: readline_hooks.py
    :caption:
    :start-after: #end_pymotw_header

Either hook is a potentially good place to use :func:`insert_text` to
modify the input buffer.

::

    $ python readline_hooks.py 

    Prompt ("stop" to quit): from startup_hook from pre_input_hook

If the buffer is modified inside the pre-input hook, :func:`redisplay`
must be called to update the screen.


.. seealso::

    `readline <http://docs.python.org/library/readline.html>`_
        The standard library documentation for this module.

    `GNU readline <http://tiswww.case.edu/php/chet/readline/readline.html>`_
        Documentation for the GNU readline library.
        
    `readline init file format <http://tiswww.case.edu/php/chet/readline/readline.html#SEC10>`_
        The initialization and configuration file format.
    
    `effbot: The readline module <http://sandbox.effbot.org/librarybook/readline.htm>`_
        Effbot's guide to the readline module.

    `pyreadline <https://launchpad.net/pyreadline>`_
        pyreadline, developed as a Python-based replacement for readline to be
        used in `iPython <http://ipython.scipy.org/>`_.

    :mod:`cmd`
        The ``cmd`` module uses ``readline`` extensively to implement  
        tab-completion in the command interface.  Some of the examples here
        were adapted from the code in ``cmd``.
    
    :mod:`rlcompleter`
        ``rlcompleter`` uses ``readline`` to add tab-completion to the interactive 
        Python interpreter.
