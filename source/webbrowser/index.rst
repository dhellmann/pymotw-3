===================================
 webbrowser --- Displays web pages
===================================

.. module:: webbrowser
    :synopsis: Displays web pages

:Purpose: Use the `webbrowser` module to display web pages to your users.

The :mod:`webbrowser` module includes functions to open URLs in interactive
browser applications. The module includes a registry of available
browsers, in case multiple options are available on the system. It can
also be controlled with the ``BROWSER`` environment variable.

Simple Example
==============

To open a page in the browser, use the :func:`open()` function.

.. literalinclude:: webbrowser_open.py
   :caption:
   :start-after: #end_pymotw_header

The URL is opened in a browser window, and that window is raised to
the top of the window stack. The documentation says that an existing
window will be reused, if possible, but the actual behavior may depend
on your browser's settings. Using Firefox on my Mac, a new window was
always created.

Windows vs. Tabs
================

If you always want a new window used, use :func:`open_new()`.

.. literalinclude:: webbrowser_open_new.py
   :caption:
   :start-after: #end_pymotw_header

If you would rather create a new tab, use :func:`open_new_tab()` instead.

Using a specific browser
========================

If for some reason your application needs to use a specific browser,
you can access the set of registered browser controllers using the
:func:`get()` function. The browser controller has methods to
:func:`open()`, :func:`open_new()`, and :func:`open_new_tab()`. This
example forces the use of the lynx browser:

.. literalinclude:: webbrowser_get.py
   :caption:
   :start-after: #end_pymotw_header

Refer to the module documentation for a list of available browser
types.

``BROWSER`` variable
====================

Users can control the module from outside your application by setting
the environment variable ``BROWSER`` to the browser names or commands
to try. The value should consist of a series of browser names
separated by ``os.pathsep``. If the name includes ``%s``, the name is
interpreted as a literal command and executed directly with the ``%s``
replaced by the URL. Otherwise, the name is passed to :func:`get()` to
obtain a controller object from the registry.

For example, this command opens the web page in lynx, assuming it is
available, no matter what other browsers are registered.

::

    $ BROWSER=lynx python3 webbrowser_open.py 

If none of the names in ``BROWSER`` work, :mod:`webbrowser` falls back
to its default behavior.


Command Line Interface
======================

All of the features of the :mod:`webbrowser` module are available via
the command line as well as from within your Python program.

::

    $ python -m webbrowser   
    Usage: /Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/webbrowser.py [-n | -t] url
        -n: open new window
        -t: open new tab


.. seealso::

    `webbrowser <http://docs.python.org/lib/module-webbrowser.html>`_
        Standard library documentation for this module.
