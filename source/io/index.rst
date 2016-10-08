===============================================
 StringIO -- Text Buffers with a File-like API
===============================================

.. module:: StringIO
    :synopsis: Work with text buffers using file-like API

.. module:: cStringIO
    :synopsis: Work with text buffers using file-like API

:Purpose: Work with text buffers using file-like API
:Python Version: 1.4 and later

:class:`StringIO` provides a convenient means of working with text in
memory using the file API (:func:`read`, :func:`write`, etc.). There
are two separate implementations. The :mod:`cStringIO` version is
written in C for speed, while :mod:`StringIO` is written in Python for
portability. Using :mod:`cStringIO` to build large strings can offer
performance savings over some other string concatenation techniques.

Examples
========

Here are a few standard examples of using :class:`StringIO` buffers:

.. include:: stringio_examples.py
    :literal:
    :start-after: #end_pymotw_header

This example uses :func:`read()`, but the :func:`readline()` and
:func:`readlines()` methods are also available. The :class:`StringIO`
class also provides a :func:`seek()` method for jumping
around in a buffer while reading, which can be useful for rewinding if
a look-ahead parsing algorithm is being used.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'stringio_examples.py'))
.. }}}

::

	$ python stringio_examples.py

	This goes into the buffer. And so does this.
	
	Inital value for read buffer

.. {{{end}}}


.. seealso::

    `StringIO <http://docs.python.org/lib/module-StringIO.html>`_
        Standard library documentation for this module.

    `The StringIO module ::: www.effbot.org <http://effbot.org/librarybook/stringio.htm>`_
        effbot's examples with StringIO

    `Efficient String Concatenation in Python <http://www.skymind.com/%7Eocrow/python_string/>`_
        Examines various methods of combining strings and their relative merits.
