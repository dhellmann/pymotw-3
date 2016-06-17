.. Not using cog because these examples are interactive.

====================================
 getpass --- Secure Password Prompt
====================================

.. module:: getpass
    :synopsis: Prompt for a password securely

:Purpose: Prompt the user for a value, usually a password, without echoing what they type to the console.

Many programs that interact with the user via the terminal need to ask
the user for password values without showing what the user types on
the screen.  The :mod:`getpass` module provides a portable way to
handle such password prompts securely.

Example
=======

The :func:`getpass()` function prints a prompt, then reads input from
the user until they press return. The input is returned as a string to
the caller.

.. literalinclude:: getpass_defaults.py
   :caption:
   :start-after: #end_pymotw_header

The default prompt, if none is specified by the caller, is
"``Password:``".

::

    $ python3 getpass_defaults.py

    Password:
    You entered: sekret

The prompt can be changed to any value needed.

.. literalinclude:: getpass_prompt.py
   :caption:
   :start-after: #end_pymotw_header

Some programs ask for a "pass phrase" instead of a simple password, to
give better security.

::

    $ python3 getpass_prompt.py

    What is your favorite color?
    Right.  Off you go.

    $ python3 getpass_prompt.py

    What is your favorite color?
    Auuuuugh!

By default, :func:`getpass()` uses :data:`sys.stdout` to print the
prompt string. For a program that may produce useful output on
``sys.stdout``, it is frequently better to send the prompt to another
stream such as :data:`sys.stderr`.

.. literalinclude:: getpass_stream.py
   :caption:
   :start-after: #end_pymotw_header

Using :data:`sys.stderr` for the prompt means standard output can be
redirected (to a pipe or file) without seeing the password prompt. The
value entered by the user is still not echoed back to the screen.

::

    $ python3 getpass_stream.py >/dev/null

    Password:

Using getpass Without a Terminal
================================

Under Unix, :func:`getpass()` always requires a tty it can control via
:mod:`termios`, so input echoing can be disabled. This means values
will not be read from a non-terminal stream redirected to standard
input. Instead, :mod:`getpass` tries to get to the tty for a process,
and no error is raised if they can access it.

::

    $ echo "not sekret" | python3 getpass_defaults.py

    Password: 
    You entered: sekret

It is up to the caller to detect when the input stream is not a tty,
and use an alternate method for reading in that case.

.. literalinclude:: getpass_noterminal.py
   :caption:
   :start-after: #end_pymotw_header

With a tty:

::

    $ python3 ./getpass_noterminal.py

    Using getpass:
    Read:  sekret

Without a tty:

::

    $ echo "sekret" | python3 ./getpass_noterminal.py

    Using readline
    Read:  sekret

.. seealso::

   * :pydoc:`getpass`

   * :mod:`readline` -- Interactive prompt library.
