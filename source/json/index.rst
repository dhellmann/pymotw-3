====================================
 json -- JavaScript Object Notation
====================================

.. module:: json
    :synopsis: JavaScript Object Notation Serializer

:Purpose: Encode Python objects as JSON strings, and decode JSON strings into Python objects.
:Python Version: 2.6 and later

The :mod:`json` module provides an API similar to :mod:`pickle` for
converting in-memory Python objects to a serialized representation
known as JavaScript Object Notation (JSON).  Unlike pickle, JSON has
the benefit of having implementations in many languages (especially
JavaScript).  It is most widely used for communicating between the web
server and client in an AJAX application, but is also useful for other
inter-application communication needs.

Encoding and Decoding Simple Data Types
=======================================

The encoder understands Python's native types by default
(:class:`string`, :class:`unicode`, :class:`int`, :class:`float`,
:class:`list`, :class:`tuple`, and :class:`dict`).

.. include:: json_simple_types.py
    :literal:
    :start-after: #end_pymotw_header

Values are encoded in a manner superficially similar to Python's :func:`repr`
output.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'json_simple_types.py'))
.. }}}

::

	$ python json_simple_types.py

	DATA: [{'a': 'A', 'c': 3.0, 'b': (2, 4)}]
	JSON: [{"a": "A", "c": 3.0, "b": [2, 4]}]

.. {{{end}}}

Encoding, then re-decoding may not give exactly the same type of
object.

.. include:: json_simple_types_decode.py
    :literal:
    :start-after: #end_pymotw_header

In particular, strings are converted to unicode objects and
tuples become lists.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'json_simple_types_decode.py'))
.. }}}

::

	$ python json_simple_types_decode.py

	DATA   : [{'a': 'A', 'c': 3.0, 'b': (2, 4)}]
	ENCODED: [{"a": "A", "c": 3.0, "b": [2, 4]}]
	DECODED: [{'a': 'A', 'c': 3.0, 'b': [2, 4]}]
	ORIGINAL: <type 'tuple'>
	DECODED : <type 'list'>

.. {{{end}}}

Human-consumable vs. Compact Output
===================================

Another benefit of JSON over :mod:`pickle` is that the results are
human-readable.  The :func:`dumps` function accepts several arguments
to make the output even nicer.  For example, the *sort_keys* flag
tells the encoder to output the keys of a dictionary in sorted,
instead of random, order.

.. include:: json_sort_keys.py
    :literal:
    :start-after: #end_pymotw_header

Sorting makes it easier to scan the results by eye, and also makes it
possible to compare JSON output in tests.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'json_sort_keys.py'))
.. }}}

::

	$ python json_sort_keys.py

	DATA: [{'a': 'A', 'c': 3.0, 'b': (2, 4)}]
	JSON: [{"a": "A", "c": 3.0, "b": [2, 4]}]
	SORT: [{"a": "A", "b": [2, 4], "c": 3.0}]
	UNSORTED MATCH: False
	SORTED MATCH  : True

.. {{{end}}}

For highly-nested data structures, specify a value for *indent* so
the output is formatted nicely as well.

.. include:: json_indent.py
    :literal:
    :start-after: #end_pymotw_header

When indent is a non-negative integer, the output more closely
resembles that of :mod:`pprint`, with leading spaces for each level of
the data structure matching the indent level.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'json_indent.py'))
.. }}}

::

	$ python json_indent.py

	DATA: [{'a': 'A', 'c': 3.0, 'b': (2, 4)}]
	NORMAL: [{"a": "A", "b": [2, 4], "c": 3.0}]
	INDENT: [
	  {
	    "a": "A", 
	    "b": [
	      2, 
	      4
	    ], 
	    "c": 3.0
	  }
	]

.. {{{end}}}

Verbose output like this increases the number of bytes needed to
transmit the same amount of data, however, so it is not intended for
use in a production environment.  In fact, it is possible to adjust
the settings for separating data in the encoded output to make it even
more compact than the default.

.. include:: json_compact_encoding.py
    :literal:
    :start-after: #end_pymotw_header

The *separators* argument to :func:`dumps` should be a tuple
containing the strings to separate items in a list and keys from
values in a dictionary.  The default is ``(', ', ': ')``. By removing
the whitespace, a more compact output is produced.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'json_compact_encoding.py'))
.. }}}

::

	$ python json_compact_encoding.py

	DATA: [{'a': 'A', 'c': 3.0, 'b': (2, 4)}]
	repr(data)             : 35
	dumps(data)            : 35
	dumps(data, indent=2)  : 76
	dumps(data, separators): 29

.. {{{end}}}

Encoding Dictionaries
=====================

The JSON format expects the keys to a dictionary to be strings.
Trying to encode a dictionary with non-string types as keys produces
an exception. (The exception type depends on whether the pure-Python
version of the module is loaded, or if the C speed-ups are available,
but it will be either :class:`TypeError` or :class:`ValueError`.)  One
way to work around that limitation is to tell the encoder to skip over
non-string keys using the *skipkeys* argument:

.. include:: json_skipkeys.py
    :literal:
    :start-after: #end_pymotw_header

Rather than raising an exception, the non-string key is ignored.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'json_skipkeys.py'))
.. }}}

::

	$ python json_skipkeys.py

	First attempt
	ERROR: keys must be a string
	
	Second attempt
	[{"a": "A", "c": 3.0, "b": [2, 4]}]

.. {{{end}}}

Working with Custom Types
=========================

All of the examples so far have used Pythons built-in types because
those are supported by :mod:`json` natively.  It is common to need to
encode custom classes, as well, and there are two ways to do that.

Given this class to encode:

.. include:: json_myobj.py
    :literal:
    :start-after: #end_pymotw_header

The simple way of encoding a :class:`MyObj` instance is to define a
function to convert an unknown type to a known type.  It does not need
to do the encoding, so it should just convert one object to another.

.. include:: json_dump_default.py
    :literal:
    :start-after: #end_pymotw_header

In :func:`convert_to_builtin_type`, instances of classes not recognized
by :mod:`json` are converted to dictionaries with enough information
to re-create the object if a program has access to the Python modules
necessary.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'json_dump_default.py', 
..                    break_lines_at=68, line_break_mode='wrap'))
.. }}}

::

	$ python json_dump_default.py

	First attempt
	ERROR: <MyObj(instance value goes here)> is not JSON serializable
	
	With default
	default( <MyObj(instance value goes here)> )
	{"s": "instance value goes here", "__module__": "json_myobj",
	"__class__": "MyObj"}

.. {{{end}}}

To decode the results and create a :func:`MyObj` instance, use the
*object_hook* argument to :func:`loads` to tie in to the decoder so
the class can be imported from the module and used to create the
instance.

The *object_hook* is called for each dictionary decoded from the
incoming data stream, providing a chance to convert the dictionary to
another type of object.  The hook function should return the object
the calling application should receive instead of the dictionary.

.. include:: json_load_object_hook.py
    :literal:
    :start-after: #end_pymotw_header

Since :mod:`json` converts string values to unicode objects, they need
to be re-encoded as ASCII strings before they can be used as keyword
arguments to the class constructor.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'json_load_object_hook.py'))
.. }}}

::

	$ python json_load_object_hook.py

	MODULE: json_myobj
	CLASS: <class 'json_myobj.MyObj'>
	INSTANCE ARGS: {'s': 'instance value goes here'}
	[<MyObj(instance value goes here)>]

.. {{{end}}}

Similar hooks are available for the built-in types integers
(*parse_int*), floating point numbers (*parse_float*), and
constants (*parse_constant*).

Encoder and Decoder Classes
===========================

Besides the convenience functions already covered, the :mod:`json`
module provides classes for encoding and decoding.  Using the classes
directly gives access to extra APIs for customizing their behavior.

The :class:`JSONEncoder` uses an iterable interface for producing
"chunks" of encoded data, making it easier to write to files or
network sockets without having to represent an entire data structure
in memory.

.. include:: json_encoder_iterable.py
    :literal:
    :start-after: #end_pymotw_header

The output is generated in logical units, rather than being based on
any size value.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'json_encoder_iterable.py'))
.. }}}

::

	$ python json_encoder_iterable.py

	PART: [
	PART: {
	PART: "a"
	PART: : 
	PART: "A"
	PART: , 
	PART: "c"
	PART: : 
	PART: 3.0
	PART: , 
	PART: "b"
	PART: : 
	PART: [2
	PART: , 4
	PART: ]
	PART: }
	PART: ]

.. {{{end}}}

The :func:`encode` method is basically equivalent to
``''.join(encoder.iterencode())``, with some extra error checking up
front.

To encode arbitrary objects, override the :func:`default` method with
an implementation similar to the one used in
:func:`convert_to_builtin_type`.

.. include:: json_encoder_default.py
    :literal:
    :start-after: #end_pymotw_header

The output is the same as the previous implementation.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'json_encoder_default.py',
..                    break_lines_at=68, line_break_mode='wrap'))
.. }}}

::

	$ python json_encoder_default.py

	<MyObj(internal data)>
	default( <MyObj(internal data)> )
	{"s": "internal data", "__module__": "json_myobj", "__class__":
	"MyObj"}

.. {{{end}}}

Decoding text, then converting the dictionary into an object takes a
little more work to set up than the previous implementation, but not
much.

.. include:: json_decoder_object_hook.py
    :literal:
    :start-after: #end_pymotw_header

And the output is the same as the earlier example.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'json_decoder_object_hook.py'))
.. }}}

::

	$ python json_decoder_object_hook.py

	MODULE: json_myobj
	CLASS: <class 'json_myobj.MyObj'>
	INSTANCE ARGS: {'s': 'instance value goes here'}
	[<MyObj(instance value goes here)>]

.. {{{end}}}

Working with Streams and Files
==============================

All of the examples so far have assumed that the encoded version of
the entire data structure could be held in memory at one time.  With
large data structures, it may be preferable to write the encoding
directly to a file-like object.  The convenience functions
:func:`load` and :func:`dump` accept references to a file-like object
to use for reading or writing.

.. include:: json_dump_file.py
    :literal:
    :start-after: #end_pymotw_header

A socket or normal file handle would work the same way as the
:class:`StringIO` buffer used in this example.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'json_dump_file.py'))
.. }}}

::

	$ python json_dump_file.py

	[{"a": "A", "c": 3.0, "b": [2, 4]}]

.. {{{end}}}

Although it is not optimized to read only part of the data at a time,
the :func:`load` function still offers the benefit of encapsulating
the logic of generating objects from stream input.

.. include:: json_load_file.py
    :literal:
    :start-after: #end_pymotw_header

Just as for :func:`dump`, any file-like object can be passed to
:func:`load`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'json_load_file.py'))
.. }}}

::

	$ python json_load_file.py

	[{'a': 'A', 'c': 3.0, 'b': [2, 4]}]

.. {{{end}}}


Mixed Data Streams
==================

:class:`JSONDecoder` includes :func:`raw_decode`, a method for
decoding a data structure followed by more data, such as JSON data
with trailing text.  The return value is the object created by
decoding the input data, and an index into that data indicating where
decoding left off.

.. include:: json_mixed_data.py
    :literal:
    :start-after: #end_pymotw_header

Unfortunately, this only works if the object appears at the beginning
of the input.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'json_mixed_data.py'))
.. }}}

::

	$ python json_mixed_data.py

	JSON first:
	Object              : [{'a': 'A', 'c': 3.0, 'b': [2, 4]}]
	End of parsed input : 35
	Remaining text      : ' This text is not JSON.'
	
	JSON embedded:
	ERROR: No JSON object could be decoded

.. {{{end}}}


.. seealso::

    `json <http://docs.python.org/library/json.html>`_
        The standard library documentation for this module.

    `JavaScript Object Notation`_
        JSON home, with documentation and implementations in other languages.

    `simplejson <http://code.google.com/p/simplejson/>`_
        ``simplejson``, from Bob Ippolito, et al, is the externally
        maintained development version of the ``json`` library included
        with Python 2.6 and later. It maintains backwards
        compatibility with Python 2.4 and Python 2.5.

    `jsonpickle <http://code.google.com/p/jsonpickle/>`_
        ``jsonpickle`` allows for any Python object to be serialized into JSON. 

.. _JavaScript Object Notation: http://json.org/
