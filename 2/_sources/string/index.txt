===========================
string -- Working with text
===========================

.. module:: string
    :synopsis: Contains constants and classes for working with text.

:Purpose: Contains constants and classes for working with text.
:Available In: 2.5

The :mod:`string` module dates from the earliest versions of
Python. In version 2.0, many of the functions previously implemented
only in the module were moved to methods of :class:`str` and
:class:`unicode` objects. Legacy versions of those functions are still
available, but their use is deprecated and they will be dropped in
Python 3.0. The :mod:`string` module still contains several useful
constants and classes for working with string and unicode objects, and
this discussion will concentrate on them.

Constants
=========

The constants in the string module can be used to specify categories
of characters such as ``ascii_letters`` and ``digits``. Some of the
constants, such as ``lowercase``, are locale-dependent so the value
changes to reflect the language settings of the user. Others, such as
``hexdigits``, do not change when the locale changes.

.. include:: string_constants.py
    :literal:
    :start-after: #end_pymotw_header

Most of the names for the constants are self-explanatory.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'string_constants.py'))
.. }}}

::

	$ python string_constants.py
	
	ascii_letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	
	ascii_lowercase='abcdefghijklmnopqrstuvwxyz'
	
	ascii_uppercase='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	
	digits='0123456789'
	
	hexdigits='0123456789abcdefABCDEF'
	
	letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	
	lowercase='abcdefghijklmnopqrstuvwxyz'
	
	octdigits='01234567'
	
	printable='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
	
	punctuation='!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
	
	uppercase='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	
	whitespace='\t\n\x0b\x0c\r '
	

.. {{{end}}}


Functions
=========

There are two functions not moving from the string
module. :func:`capwords()` capitalizes all of the words in a string.

.. include:: string_capwords.py
    :literal:
    :start-after: #end_pymotw_header

The results are the same as if you called :func:`split()`, capitalized
the words in the resulting list, then called :func:`join()` to combine
the results.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'string_capwords.py'))
.. }}}

::

	$ python string_capwords.py
	
	The quick brown fox jumped over the lazy dog.
	The Quick Brown Fox Jumped Over The Lazy Dog.

.. {{{end}}}

The other function creates translation tables that can be used with
the :func:`translate()` method to change one set of characters to
another.

.. include:: string_maketrans.py
    :literal:
    :start-after: #end_pymotw_header

In this example, some letters are replaced by their `l33t
<http://en.wikipedia.org/wiki/Leet>`_ number alternatives.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'string_maketrans.py'))
.. }}}

::

	$ python string_maketrans.py
	
	The quick brown fox jumped over the lazy dog.
	Th3 qu1ck 620wn f0x jum93d 0v32 7h3 142y d06.

.. {{{end}}}

Templates
=========

String templates were added in Python 2.4 as part of :pep:`292` and
are intended as an alternative to the built-in interpolation
syntax. With :class:`string.Template` interpolation, variables are
identified by name prefixed with ``$`` (e.g., ``$var``) or, if
necessary to set them off from surrounding text, they can also be
wrapped with curly braces (e.g., ``${var}``).

This example compares a simple template with a similar string
interpolation setup.

.. include:: string_template.py
    :literal:
    :start-after: #end_pymotw_header

As you see, in both cases the trigger character (``$`` or ``%``) is
escaped by repeating it twice.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'string_template.py'))
.. }}}

::

	$ python string_template.py
	
	TEMPLATE: 
	foo
	$
	fooiable
	
	INTERPLOATION: 
	foo
	%
	fooiable
	

.. {{{end}}}

One key difference between templates and standard string interpolation
is that the type of the arguments is not taken into account. The
values are converted to strings, and the strings are inserted into the
result. No formatting options are available. For example, there is no
way to control the number of digits used to represent a floating point
value.

A benefit, though, is that by using the :func:`safe_substitute()`
method, it is possible to avoid exceptions if not all of the values
needed by the template are provided as arguments.

.. include:: string_template_missing.py
    :literal:
    :start-after: #end_pymotw_header

Since there is no value for missing in the values dictionary, a
:ref:`KeyError <exceptions-KeyError>` is raised by
:func:`substitute()`. Instead of raising the error,
:func:`safe_substitute()` catches it and leaves the variable
expression alone in the text.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'string_template_missing.py'))
.. }}}

::

	$ python string_template_missing.py
	
	TEMPLATE: ERROR: 'missing'
	TEMPLATE: foo is here but $missing is not provided

.. {{{end}}}

Advanced Templates
==================

If the default syntax for :class:`string.Template` is not to your
liking, you can change the behavior by adjusting the regular
expression patterns it uses to find the variable names in the template
body. A simple way to do that is to change the *delimiter* and
*idpattern* class attributes.

.. include:: string_template_advanced.py
    :literal:
    :start-after: #end_pymotw_header

In this example, variable ids must include an underscore somewhere in
the middle, so ``%notunderscored`` is not replaced by anything.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'string_template_advanced.py'))
.. }}}

::

	$ python string_template_advanced.py
	
	% replaced %notunderscored

.. {{{end}}}

For more complex changes, you can override the *pattern* attribute and
define an entirely new regular expression. The pattern provided must
contain four named groups for capturing the escaped delimiter, the
named variable, a braced version of the variable name, and invalid
delimiter patterns.

Let's look at the default pattern:

.. include:: string_template_defaultpattern.py
    :literal:
    :start-after: #end_pymotw_header

Since ``t.pattern`` is a compiled regular expression, we have to
access its pattern attribute to see the actual string.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'string_template_defaultpattern.py'))
.. }}}

::

	$ python string_template_defaultpattern.py
	
	
	    \$(?:
	      (?P<escaped>\$) |   # Escape sequence of two delimiters
	      (?P<named>[_a-z][_a-z0-9]*)      |   # delimiter and a Python identifier
	      {(?P<braced>[_a-z][_a-z0-9]*)}   |   # delimiter and a braced identifier
	      (?P<invalid>)              # Other ill-formed delimiter exprs
	    )
	    

.. {{{end}}}

If we wanted to create a new type of template using, for example,
``{{var}}`` as the variable syntax, we could use a pattern like this:

.. include:: string_template_newsyntax.py
    :literal:
    :start-after: #end_pymotw_header

We still have to provide both the named and braced patterns, even
though they are the same. Here's the output:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'string_template_newsyntax.py'))
.. }}}

::

	$ python string_template_newsyntax.py
	
	MATCHES: [('{{', '', '', ''), ('', 'var', '', '')]
	SUBSTITUTED: 
	{{
	replacement
	

.. {{{end}}}

Deprecated Functions
====================

For information on the deprecated functions moved to the string and
unicode classes, refer to `String Methods
<http://docs.python.org/lib/string-methods.html#string-methods>`_ in
the manual.

.. seealso::

    `string <https://docs.python.org/2/library/string.html>`_
        Standard library documentation for this module.

    :pep:`292`
        Simpler String Substitutions

    :ref:`article-text-processing`
