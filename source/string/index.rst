========================================
 string -- Text Constants and Templates
========================================

.. module:: string
    :synopsis: Contains constants and classes for working with text.

:Purpose: Contains constants and classes for working with text.
:Python Version: 1.4 and later

The :mod:`string` module dates from the earliest versions of
Python. In version 2.0, many of the functions previously implemented
only in the module were moved to methods of :class:`str` and
:class:`unicode` objects. Legacy versions of those functions are still
available, but their use is deprecated and they will be dropped in
Python 3.0. The :mod:`string` module retains several useful constants
and classes for working with :class:`string` and :class:`unicode`
objects, and this discussion will concentrate on them.

Functions
=========

The two functions :func:`capwords` and :func:`maketrans` are not
moving from the string module.  :func:`capwords()` capitalizes all of
the words in a string.

.. include:: string_capwords.py
    :literal:
    :start-after: #end_pymotw_header

The results are the same as calling :func:`split()`, capitalizing the
words in the resulting list, then called :func:`join()` to combine the
results.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'string_capwords.py'))
.. }}}

::

	$ python string_capwords.py

	The quick brown fox jumped over the lazy dog.
	The Quick Brown Fox Jumped Over The Lazy Dog.

.. {{{end}}}

The :func:`maketrans` function creates translation tables that can be
used with the :func:`translate()` method to change one set of
characters to another more efficiently than with repeated calls to
:func:`replace`.

.. include:: string_maketrans.py
    :literal:
    :start-after: #end_pymotw_header

In this example, some letters are replaced by their "l33t"
number alternatives.

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

String templates were added in Python 2.4 as part of PEP 292 and
are intended as an alternative to the built-in interpolation
syntax. With :class:`string.Template` interpolation, variables are
identified by prefixing the name with ``$`` (e.g., ``$var``) or, if
necessary to set them off from surrounding text, they can also be
wrapped with curly braces (e.g., ``${var}``).

This example compares a simple template with a similar string
interpolation using the ``%`` operator.

.. include:: string_template.py
    :literal:
    :start-after: #end_pymotw_header

In both cases, the trigger character (``$`` or ``%``) is escaped by
repeating it twice.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'string_template.py'))
.. }}}

::

	$ python string_template.py

	TEMPLATE: 
	Variable        : foo
	Escape          : $
	Variable in text: fooiable
	
	INTERPLOATION: 
	Variable        : foo
	Escape          : %
	Variable in text: fooiable
	

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

Since there is no value for *missing* in the values dictionary, a
:class:`KeyError` is raised by :func:`substitute()`. Instead of
raising the error, :func:`safe_substitute()` catches it and leaves the
variable expression alone in the text.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'string_template_missing.py'))
.. }}}

::

	$ python string_template_missing.py

	substitute()     : ERROR: 'missing'
	safe_substitute(): foo is here but $missing is not provided

.. {{{end}}}

Advanced Templates
==================

The default syntax for :class:`string.Template` can be changed by
adjusting the regular expression patterns it uses to find the variable
names in the template body. A simple way to do that is to change the
:attr:`delimiter` and :attr:`idpattern` class attributes.

.. include:: string_template_advanced.py
    :literal:
    :start-after: #end_pymotw_header

In this example, the substitution rules are changed so that the
delimiter is ``%`` instead of ``$`` and variable names must include an
underscore somewhere in the middle.  The pattern ``%notunderscored``
is not replaced by anything, because it does not include an underscore
character.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'string_template_advanced.py'))
.. }}}

::

	$ python string_template_advanced.py

	Modified ID pattern:
	
	  Delimiter : %
	  Replaced  : replaced
	  Ignored   : %notunderscored
	

.. {{{end}}}

For more complex changes, override the :attr:`pattern` attribute and
define an entirely new regular expression. The pattern provided must
contain four named groups for capturing the escaped delimiter, the
named variable, a braced version of the variable name, and invalid
delimiter patterns.

.. include:: string_template_defaultpattern.py
    :literal:
    :start-after: #end_pymotw_header

The value of ``t.pattern`` is a compiled regular expression, but the
original string is available via its :attr:`pattern` attribute.

.. this output was edited for clarity and to make it fit on the page

::

	\$(?:
	  (?P<escaped>\$) |                # two delimiters
	  (?P<named>[_a-z][_a-z0-9]*)    | # identifier
	  {(?P<braced>[_a-z][_a-z0-9]*)} | # braced identifier
	  (?P<invalid>)                    # ill-formed delimiter exprs
	)

This example defines a new pattern to create a new type of template,
using ``{{var}}`` as the variable syntax.

.. include:: string_template_newsyntax.py
    :literal:
    :start-after: #end_pymotw_header

Both the :attr:`named` and :attr:`braced` patterns must be provided
separately, even though they are the same.  Running the sample program
generates:

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

.. seealso::

    `string <http://docs.python.org/lib/module-string.html>`_
        Standard library documentation for this module.

    `String Methods <http://docs.python.org/lib/string-methods.html#string-methods>`_ 
        Methods of :class:`str` objects that replace the deprecated
        functions in :mod:`string`.

    :pep:`292`
        Simpler String Substitutions

    `l33t <http://en.wikipedia.org/wiki/Leet>`_
        "Leetspeak" alternative alphabet
