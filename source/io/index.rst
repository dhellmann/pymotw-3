===============================================
 io --- Text, Binary, and Raw Stream I/O Tools
===============================================

.. module:: io
    :synopsis: Implements file I/O and provides classes for working
               with buffers using file-like API.

:Purpose: Implements file I/O and provides classes for working with
          buffers using file-like API.

The :mod:`io` module provides access to the built-in :func:`open`
function and the classes used to implement file-based input and output
operations. The classes are decomposed in such a way that they can be
recombined for alternate purposes, for example to enable writing
Unicode data to a network socket.

In-memory Streams
=================

:class:`StringIO` provides a convenient means of working with text in
memory using the file API (:func:`read`, :func:`write`, etc.). Using
:mod:`StringIO` to build large strings can offer performance savings
over some other string concatenation techniques in some
cases. In-memory stream buffers are also useful for testing, where
writing to a real file on disk may slow down the test suite.

Here are a few standard examples of using :class:`StringIO` buffers:

.. literalinclude:: io_stringio.py
    :caption:
    :start-after: #end_pymotw_header

This example uses :func:`read`, but the :func:`readline` and
:func:`readlines` methods are also available. The :class:`StringIO`
class also provides a :func:`seek` method for jumping
around in a buffer while reading, which can be useful for rewinding if
a look-ahead parsing algorithm is being used.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'io_stringio.py'))
.. }}}

.. code-block:: none

	$ python3 io_stringio.py
	
	This goes into the buffer. And so does this.
	
	Inital value for read buffer

.. {{{end}}}

To work with raw bytes instead of Unicode text, use :class:`BytesIO`.

.. literalinclude:: io_bytesio.py
   :caption:
   :start-after: #end_pymotw_header

The values written to the :class:`BytesIO` must be :class:`bytes`
rather than :class:`str`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'io_bytesio.py'))
.. }}}

.. code-block:: none

	$ python3 io_bytesio.py
	
	b'This goes into the buffer. \xc3\x81\xc3\x87\xc3\x8a'
	b'Inital value for read buffer'

.. {{{end}}}



.. seealso::

   * :pydoc:`io`

   * `Efficient String Concatenation in Python
     <http://www.skymind.com/%7Eocrow/python_string/>`_ -- Examines
     various methods of combining strings and their relative merits.
