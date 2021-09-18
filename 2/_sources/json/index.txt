=============================================
json -- JavaScript Object Notation Serializer
=============================================

.. module:: json
    :synopsis: JavaScript Object Notation Serializer

:Purpose: Encode Python objects as JSON strings, and decode JSON strings into Python objects.
:Available In: 2.6

The :mod:`json` module provides an API similar to :mod:`pickle` for
converting in-memory Python objects to a serialized representation
known as `JavaScript Object Notation`_ (JSON).  Unlike pickle, JSON
has the benefit of having implementations in many languages
(especially JavaScript), making it suitable for inter-application
communication.  JSON is probably most widely used for communicating
between the web server and client in an AJAX application, but is not
limited to that problem domain.

Encoding and Decoding Simple Data Types
=======================================

The encoder understands Python's native types by default (string,
unicode, int, float, list, tuple, dict).

.. include:: json_simple_types.py
    :literal:
    :start-after: #end_pymotw_header

Values are encoded in a manner very similar to Python's ``repr()``
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

In particular, strings are converted to unicode and tuples become
lists.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'json_simple_types_decode.py'))
.. }}}

::

	$ python json_simple_types_decode.py
	
	ENCODED: [{"a": "A", "c": 3.0, "b": [2, 4]}]
	DECODED: [{u'a': u'A', u'c': 3.0, u'b': [2, 4]}]
	ORIGINAL: <type 'tuple'>
	DECODED : <type 'list'>

.. {{{end}}}

Human-consumable vs. Compact Output
===================================

Another benefit of JSON over pickle is that the results are
human-readable.  The ``dumps()`` function accepts several arguments to
make the output even nicer.  For example, ``sort_keys`` tells the
encoder to output the keys of a dictionary in sorted, instead of
random, order.

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

For highly-nested data structures, you will want to specify a value
for ``indent``, so the output is formatted nicely as well.

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
transmit the same amount of data, however, so it isn't the sort of
thing you necessarily want to use in a production environment.  In
fact, you may want to adjust the settings for separating data in the
encoded output to make it even more compact than the default.

.. include:: json_compact_encoding.py
    :literal:
    :start-after: #end_pymotw_header

The ``separators`` argument to ``dumps()`` should be a tuple
containing the strings to separate items in a list and keys from
values in a dictionary.  The default is ``(', ', ': ')``. By removing
the whitespace, we can produce a more compact output.

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

The JSON format expects the keys to a dictionary to be strings.  If
you have other types as keys in your dictionary, trying to encode the
object will produce a :ref:`ValueError <exceptions-ValueError>`.  One way
to work around that limitation is to skip over non-string keys using
the ``skipkeys`` argument:

.. include:: json_skipkeys.py
    :literal:
    :start-after: #end_pymotw_header

Rather than raising an exception, the non-string key is simply
ignored.

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

Working with Your Own Types
===========================

All of the examples so far have used Pythons built-in types because
those are supported by :mod:`json` natively.  It isn't uncommon, of
course, to have your own types that you want to be able to encode as
well.  There are two ways to do that.

First, we'll need a class to encode:

.. include:: json_myobj.py
    :literal:
    :start-after: #end_pymotw_header

The simple way of encoding a ``MyObj`` instance is to define a
function to convert an unknown type to a known type.  You don't have
to do the encoding yourself, just convert one object to another.

.. include:: json_dump_default.py
    :literal:
    :start-after: #end_pymotw_header

In ``convert_to_builtin_type()``, instances of classes not recognized
by :mod:`json` are converted to dictionaries with enough information
to re-create the object if a program has access to the Python modules
necessary.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'json_dump_default.py'))
.. }}}

::

	$ python json_dump_default.py
	
	First attempt
	ERROR: <MyObj(instance value goes here)> is not JSON serializable
	
	With default
	default( <MyObj(instance value goes here)> )
	{"s": "instance value goes here", "__module__": "json_myobj", "__class__": "MyObj"}

.. {{{end}}}

To decode the results and create a ``MyObj`` instance, we need to tie
in to the decoder so we can import the class from the module and
create the instance.  For that, we use the ``object_hook`` argument to
``loads()``.

The ``object_hook`` is called for each dictionary decoded from the
incoming data stream, giving us a chance to convert the dictionary to
another type of object.  The hook function should return the object it
wants the calling application to receive instead of the dictionary.

.. include:: json_load_object_hook.py
    :literal:
    :start-after: #end_pymotw_header

Since :mod:`json` converts string values to unicode objects, we need
to re-encode them as ASCII strings before using them as keyword
arguments to the class constructor.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'json_load_object_hook.py'))
.. }}}

::

	$ python json_load_object_hook.py
	
	MODULE: <module 'json_myobj' from '/Users/dhellmann/Documents/PyMOTW/src/PyMOTW/json/json_myobj.pyc'>
	CLASS: <class 'json_myobj.MyObj'>
	INSTANCE ARGS: {'s': u'instance value goes here'}
	[<MyObj(instance value goes here)>]

.. {{{end}}}

Similar hooks are available for the built-in types integers
(``parse_int``), floating point numbers (``parse_float``), and
constants (``parse_constant``).

Encoder and Decoder Classes
===========================

Besides the convenience functions we have already examined, the
:mod:`json` module provides classes for encoding and decoding.  When
using the classes directly, you have access to extra APIs and can
create subclasses to customize their behavior.

The JSONEncoder provides an iterable interface for producing "chunks"
of encoded data, making it easier for you to write to files or network
sockets without having to represent an entire data structure in
memory.

.. include:: json_encoder_iterable.py
    :literal:
    :start-after: #end_pymotw_header

As you can see, the output is generated in logical units, rather than
being based on any size value.

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

The ``encode()`` method is basically equivalent to
``''.join(encoder.iterencode())``, with some extra error checking up
front.

To encode arbitrary objects, we can override the ``default()`` method
with an implementation similar to what we used above in
``convert_to_builtin_type()``.

.. include:: json_encoder_default.py
    :literal:
    :start-after: #end_pymotw_header

The output is the same as the previous implementation.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'json_encoder_default.py'))
.. }}}

::

	$ python json_encoder_default.py
	
	<MyObj(internal data)>
	default( <MyObj(internal data)> )
	{"s": "internal data", "__module__": "json_myobj", "__class__": "MyObj"}

.. {{{end}}}

Decoding text, then converting the dictionary into an object takes a
little more work to set up than our previous implementation, but not
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
	
	MODULE: <module 'json_myobj' from '/Users/dhellmann/Documents/PyMOTW/src/PyMOTW/json/json_myobj.pyc'>
	CLASS: <class 'json_myobj.MyObj'>
	INSTANCE ARGS: {'s': u'instance value goes here'}
	[<MyObj(instance value goes here)>]

.. {{{end}}}

Working with Streams and Files
==============================

In all of the examples so far, we have assumed that we could (and
should) hold the encoded version of the entire data structure in
memory at one time.  With large data structures it may be preferable
to write the encoding directly to a file-like object.  The convenience
functions ``load()`` and ``dump()`` accept references to a file-like
object to use for reading or writing.

.. include:: json_dump_file.py
    :literal:
    :start-after: #end_pymotw_header

A socket would work in much the same way as the normal file handle
used here.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'json_dump_file.py'))
.. }}}

::

	$ python json_dump_file.py
	
	[{"a": "A", "c": 3.0, "b": [2, 4]}]

.. {{{end}}}

Although it isn't optimized to read only part of the data at a time,
the ``load()`` function still offers the benefit of encapsulating the
logic of generating objects from stream input.

.. include:: json_load_file.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'json_load_file.py'))
.. }}}

::

	$ python json_load_file.py
	
	[{u'a': u'A', u'c': 3.0, u'b': [2, 4]}]

.. {{{end}}}


Mixed Data Streams
==================

The JSONDecoder includes the ``raw_decode()`` method for decoding a
data structure followed by more data, such as JSON data with trailing
text.  The return value is the object created by decoding the input
data, and an index into that data indicating where decoding left off.

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
	Object              : [{u'a': u'A', u'c': 3.0, u'b': [2, 4]}]
	End of parsed input : 35
	Remaining text      : ' This text is not JSON.'
	
	JSON embedded:
	ERROR: No JSON object could be decoded

.. {{{end}}}


.. seealso::

    `json <http://docs.python.org/2.7/library/json.html>`_
        The standard library documentation for this module.

    `JavaScript Object Notation`_
        JSON home, with documentation and implementations in other languages.

    http://code.google.com/p/simplejson/
        simplejson, from Bob Ippolito, et al, is the externally
        maintained development version of the json library included
        with Python 2.6 and Python 3.0. It maintains backwards
        compatibility with Python 2.4 and Python 2.5.

    `jsonpickle <http://code.google.com/p/jsonpickle/>`_
        jsonpickle allows for any Python object to be serialized into JSON. 

    :ref:`article-data-persistence`
        Other examples of storing data from Python programs.

.. _JavaScript Object Notation: http://json.org/
