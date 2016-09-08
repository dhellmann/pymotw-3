.. Do not need to bother with cog for this one, since the examples are interactive.

==========================================
 cmd --- Line-oriented Command Processors
==========================================

.. module:: cmd
    :synopsis: Create line-oriented command processors.

:Purpose: Create line-oriented command processors.

The :mod:`cmd` module contains one public class, :class:`Cmd`,
designed to be used as a base class for interactive shells and other
command interpreters. By default it uses :mod:`readline` for
interactive prompt handling, command line editing, and command
completion.

Processing Commands
===================

A command interpreter created with :mod:`cmd` uses a loop to read all
lines from its input, parse them, and then dispatch the command to an
appropriate *command handler*. Input lines are parsed into two parts:
the command, and any other text on the line. If the user enters ``foo
bar``, and the interpreter class includes a method named
:func:`do_foo`, it is called with ``"bar"`` as the only argument.

The end-of-file marker is dispatched to :func:`do_EOF`. If a command
handler returns a true value, the program will exit cleanly. So to
give a clean way to exit the interpreter, make sure to implement
:func:`do_EOF` and have it return True.

This simple example program supports the "greet" command:

.. literalinclude:: cmd_simple.py
    :caption:
    :start-after: #end_pymotw_header

Running it interactively demonstrates how commands are dispatched and
shows of some of the features included in :class:`Cmd`.

.. code-block:: none

    $ python3 cmd_simple.py 

    (Cmd) 

The first thing to notice is the command prompt, ``(Cmd)``. The
prompt can be configured through the attribute *prompt*. If the prompt
changes as the result of a command handler, the new value is used to
query for the next command.

.. code-block:: none

   Documented commands (type help <topic>):
   ========================================
   help

   Undocumented commands:
   ======================
   EOF  greet

The :command:`help` command is built into :class:`Cmd`. With no
arguments, :command:`help` shows the list of commands available. If
the input includes a command name, the output is more verbose and
restricted to details of that command, when available.

If the command is :command:`greet`, :func:`do_greet` is invoked to
handle it:

.. code-block:: none

    (Cmd) greet
    hello

If the class does not include a specific handler for a command, the
method :func:`default` is called with the entire input line as an
argument. The built-in implementation of :func:`default` reports an
error.

.. code-block:: none

    (Cmd) foo
    *** Unknown syntax: foo

Since :func:`do_EOF` returns True, typing Ctrl-D causes the
interpreter to exit.

.. code-block:: none

    (Cmd) ^D$ 

No newline is printed on exit, so the results are a little messy.

Command Arguments
=================

This example includes a few enhancements to eliminate
some of the annoyances and add help for the :command:`greet` command.

.. literalinclude:: cmd_arguments.py
    :caption:
    :start-after: #end_pymotw_header

The docstring added to :func:`do_greet` becomes the help text for
the command:

.. code-block:: none

    $ python3 cmd_arguments.py 

    (Cmd) help

    Documented commands (type help <topic>):
    ========================================
    greet  help

    Undocumented commands:
    ======================
    EOF

    (Cmd) help greet
    greet [person]
            Greet the named person

The output shows one optional argument to :command:`greet`,
*person*. Although the argument is optional to the command, there is a
distinction between the command and the callback method. The method
always takes the argument, but sometimes the value is an empty
string. It is left up to the command handler to determine if an
empty argument is valid, or do any further parsing and processing of
the command. In this example, if a person's name is provided then the
greeting is personalized.

.. code-block:: none

    (Cmd) greet Alice
    hi, Alice
    (Cmd) greet
    hi

Whether an argument is given by the user or not, the value passed to
the command handler does not include the command itself. That
simplifies parsing in the command handler, especially if multiple
arguments are needed.

Live Help
=========

In the previous example, the formatting of the help text leaves
something to be desired. Since it comes from the docstring, it retains
the indentation from the source file. The source could be changed to
remove the extra white-space, but that would leave the application
code looking poorly formatted. A better solution is to implement a
help handler for the :command:`greet` command, named
:func:`help_greet`. The help handler is called to produce help text
for the named command.

.. literalinclude:: cmd_do_help.py
    :caption:
    :start-after: #end_pymotw_header

In this example, the text is static but formatted more nicely. It
would also be possible to use previous command state to tailor the
contents of the help text to the current context.

.. code-block:: none

    $ python3 cmd_do_help.py

    (Cmd) help greet
    greet [person]
    Greet the named person

It is up to the help handler to actually output the help message, and not
simply return the help text for handling elsewhere.

Auto-Completion
===============

:class:`Cmd` includes support for command completion based on the
names of the commands with handler methods. The user triggers
completion by hitting the tab key at an input prompt. When multiple
completions are possible, pressing tab twice prints a list of the
options.

.. note::

   The GNU libraries needed for :mod:`readline` are not available on
   all platforms by default. In those cases, tab completion may not
   work. See :mod:`readline` for tips on installing the necessary
   libraries if your Python installation does not have them.

.. code-block:: none

    $ python3 cmd_do_help.py 

    (Cmd) <tab><tab>
    EOF    greet  help   
    (Cmd) h<tab>
    (Cmd) help

Once the command is known, argument completion is handled by methods
with the prefix ``complete_``. This allows new completion handlers to
assemble a list of possible completions using arbitrary criteria
(i.e., querying a database or looking at a file or directory on the
file system). In this case, the program has a hard-coded set of
"friends" who receive a less formal greeting than named or anonymous
strangers. A real program would probably save the list somewhere, and
read it once then cache the contents to be scanned as needed.

.. literalinclude:: cmd_arg_completion.py
    :caption:
    :start-after: #end_pymotw_header

When there is input text, :func:`complete_greet` returns a list of
friends that match. Otherwise, the full list of friends is returned.

.. code-block:: none

    $ python3 cmd_arg_completion.py 

    (Cmd) greet <tab><tab>
    Adam     Alice    Barbara  Bob      
    (Cmd) greet A<tab><tab>
    Adam   Alice  
    (Cmd) greet Ad<tab>
    (Cmd) greet Adam
    hi, Adam!

If the name given is not in the list of friends, the formal greeting
is given.

.. code-block:: none

    (Cmd) greet Joe
    hello, Joe

Overriding Base Class Methods
=============================

:class:`Cmd` includes several methods that can be overridden as hooks
for taking actions or altering the base class behavior. This example
is not exhaustive, but contains many of the methods commonly useful.

.. literalinclude:: cmd_illustrate_methods.py
    :caption:
    :start-after: #end_pymotw_header

:func:`cmdloop` is the main processing loop of the
interpreter. Overriding it is usually not necessary, since the
:func:`preloop` and :func:`postloop` hooks are available.

Each iteration through :func:`cmdloop` calls :func:`onecmd` to
dispatch the command to its handler. The actual input line is parsed
with :func:`parseline` to create a tuple containing the command, and
the remaining portion of the line.

If the line is empty, :func:`emptyline` is called. The default
implementation runs the previous command again. If the line contains a
command, first :func:`precmd` is called then the handler is looked
up and invoked. If none is found, :func:`default` is called
instead. Finally :func:`postcmd` is called.

Here is an example session with ``print`` statements added:

.. code-block:: none

    $ python3 cmd_illustrate_methods.py 

    cmdloop(Illustrating the methods of cmd.Cmd)
    preloop()
    Illustrating the methods of cmd.Cmd
    (Cmd) greet Bob
    precmd(greet Bob)
    onecmd(greet Bob)
    parseline(greet Bob) => ('greet', 'Bob', 'greet Bob')
    hello, Bob
    postcmd(None, greet Bob)
    (Cmd) ^Dprecmd(EOF)
    onecmd(EOF)
    parseline(EOF) => ('EOF', '', 'EOF')
    postcmd(True, EOF)
    postloop()


Configuring Cmd Through Attributes
==================================

In addition to the methods described earlier, there are several
attributes for controlling command interpreters.  :attr:`prompt` can
be set to a string to be printed each time the user is asked for a new
command.  :attr:`intro` is the "welcome" message printed at the start
of the program. :func:`cmdloop` takes an argument for this value, or
it can be set on the class directly.  When printing help, the
:attr:`doc_header`, :attr:`misc_header`, :attr:`undoc_header`, and
:attr:`ruler` attributes are used to format the output.

.. literalinclude:: cmd_attributes.py
    :caption:
    :start-after: #end_pymotw_header

This example class shows a command handler to let the user control
the prompt for the interactive session.

.. code-block:: none

    $ python3 cmd_attributes.py 

    Simple command processor example.
    prompt: prompt hello
    hello: help

    doc_header
    ----------
    help  prompt

    undoc_header
    ------------
    EOF

    hello: 


Running Shell Commands
======================

To supplement the standard command processing, :class:`Cmd` includes
two special command prefixes. A question mark (``?``) is equivalent to
the built-in :command:`help` command, and can be used in the same
way. An exclamation point (``!``) maps to :func:`do_shell`, and is
intended for "shelling out" to run other commands, as in this example.

.. literalinclude:: cmd_do_shell.py
    :caption:
    :start-after: #end_pymotw_header

This :command:`echo` command implementation replaces the string
``$out`` in its argument with the output from the previous shell
command.

.. code-block:: none

    $ python3 cmd_do_shell.py 

    (Cmd) ?

    Documented commands (type help <topic>):
    ========================================
    echo  help  shell

    Undocumented commands:
    ======================
    EOF

    (Cmd) ? shell
    Run a shell command
    (Cmd) ? echo
    Print the input, replacing '$out' with 
            the output of the last shell command
    (Cmd) shell pwd
    running shell command: pwd
    .../pymotw-3/source/cmd

    (Cmd) ! pwd
    running shell command: pwd
    .../pymotw-3/source/cmd

    (Cmd) echo $out
    .../pymotw-3/source/cmd


Alternative Inputs
==================

While the default mode for :func:`Cmd` is to interact with the user
through the :mod:`readline` library, it is also possible to pass a
series of commands in to standard input using standard Unix shell
redirection.

.. code-block:: none

    $ echo help | python3 cmd_do_help.py

    (Cmd) 
    Documented commands (type help <topic>):
    ========================================
    greet  help

    Undocumented commands:
    ======================
    EOF

    (Cmd) 

To have the program read a script file directly, a few other changes
may be needed. Since :mod:`readline` interacts with the terminal/tty
device, rather than the standard input stream, it should be disabled
when the script is going to be reading from a file. Also, to avoid
printing superfluous prompts, the prompt can be set to an empty
string. This example shows how to open a file and pass it as input to
a modified version of the :class:`HelloWorld` example.

.. literalinclude:: cmd_file.py
    :caption:
    :start-after: #end_pymotw_header

With *use_rawinput* set to False and *prompt* set to an empty string,
the script can be called on this input file:

.. literalinclude:: cmd_file.txt
    :caption:

to produce this output:

.. code-block:: none

    $ python3 cmd_file.py cmd_file.txt 

    hello, 
    hello, Alice and Bob

Commands from sys.argv
======================

Command line arguments to the program can also be processed as
commands for the interpreter class, instead of reading commands from
the console or a file.  To use the command line arguments, call
:func:`onecmd` directly, as in this example.

.. literalinclude:: cmd_argv.py
    :caption:
    :start-after: #end_pymotw_header

Since :func:`onecmd` takes a single string as input, the arguments
to the program need to be joined together before being passed in.

.. code-block:: none

    $ python3 cmd_argv.py greet Command-Line User

    hello, Command-Line User

    $ python3 cmd_argv.py

    (Cmd) greet Interactive User
    hello, Interactive User
    (Cmd) 

.. seealso::

   * :pydoc:`cmd`

   * `cmd2 <http://pypi.python.org/pypi/cmd2>`__ -- Drop-in
     replacement for ``cmd`` with additional features.

   * `GNU readline`_ -- The GNU Readline library provides functions
     that allow users to edit input lines as they are typed.

   * :mod:`readline` -- The Python standard library interface to
     readline.

   * :mod:`subprocess` -- Managing other processes and their output.

.. _GNU readline: http://tiswww.case.edu/php/chet/readline/rltop.html
