=================================================================
rlcompleter -- Adds tab-completion to the interactive interpreter
=================================================================

.. module:: rlcompleter
    :synopsis: Adds tab-completion to the interactive interpreter

:Purpose: Adds tab-completion to the interactive interpreter
:Available In: 1.5 and later

:mod:`rlcompleter` adds tab-completion for Python symbols to the
interactive interpreter.  Importing the module causes it to configure
a completer function for :mod:`readline`.  The only other step
required is to configure the tab key to trigger the completer.  All of
this can be done in a `PYTHONSTARTUP
<http://docs.python.org/using/cmdline.html#envvar-PYTHONSTARTUP>`_
file so that it runs each time the interactive interpreter starts.

For example, create a file ``~/.pythonrc`` containing:

.. include:: rlcompleter_pythonstartup.py
    :literal:
    :start-after: #end_pymotw_header

Then set ``PYTHONSTARTUP`` to ``"~/.pythonrc"``.  When you start the
interactive interpreter, tab completion for names from the contents of
modules or attributes of objects is activated.

.. seealso::

    `rlcompleter <http://docs.python.org/2.7/library/rlcompleter.html>`_
        The standard library documentation for this module.

    :mod:`readline`
        The readline module.
