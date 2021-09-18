==================================================
shlex -- Lexical analysis of shell-style syntaxes.
==================================================

.. module:: shlex
    :synopsis: Lexical analysis of shell-style syntaxes.

:Purpose: Lexical analysis of shell-style syntaxes.
:Available In: 1.5.2, with additions in later versions

The shlex module implements a class for parsing simple shell-like syntaxes. It
can be used for writing your own domain specific language, or for parsing
quoted strings (a task that is more complex than it seems, at first).

Quoted Strings
==============

A common problem when working with input text is to identify a sequence of
quoted words as a single entity. Splitting the text on quotes does not always
work as expected, especially if there are nested levels of quotes. Take the
following text:

.. include:: quotes.txt
    :literal:

A naive approach might attempt to construct a regular expression to
find the parts of the text outside the quotes to separate them from
the text inside the quotes, or vice versa. Such an approach would be
unnecessarily complex and prone to errors resulting from edge cases
like apostrophes or even typos. A better solution is to use a true
parser, such as the one provided by the :mod:`shlex` module. Here is a
simple example that prints the tokens identified in the input file:

.. include:: shlex_example.py
    :literal:
    :start-after: #end_pymotw_header

When run on data with embedded quotes, the parser produces the list of tokens
we expect:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shlex_example.py quotes.txt'))
.. }}}

::

	$ python shlex_example.py quotes.txt
	
	ORIGINAL: 'This string has embedded "double quotes" and \'single quotes\' in it,\nand even "a \'nested example\'".\n'
	
	TOKENS:
	'This'
	'string'
	'has'
	'embedded'
	'"double quotes"'
	'and'
	"'single quotes'"
	'in'
	'it'
	','
	'and'
	'even'
	'"a \'nested example\'"'
	'.'

.. {{{end}}}

Isolated quotes such as apostrophes are also handled.  Given this
input file:

.. include:: apostrophe.txt
    :literal:

The token with the embedded apostrophe is no problem:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shlex_example.py apostrophe.txt'))
.. }}}

::

	$ python shlex_example.py apostrophe.txt
	
	ORIGINAL: "This string has an embedded apostrophe, doesn't it?"
	
	TOKENS:
	'This'
	'string'
	'has'
	'an'
	'embedded'
	'apostrophe'
	','
	"doesn't"
	'it'
	'?'

.. {{{end}}}

Embedded Comments
=================

Since the parser is intended to be used with command languages, it needs to
handle comments. By default, any text following a # is considered part of a
comment, and ignored. Due to the nature of the parser, only single character
comment prefixes are supported. The set of comment characters used can be
configured through the commenters property.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shlex_example.py comments.txt'))
.. }}}

::

	$ python shlex_example.py comments.txt
	
	ORIGINAL: 'This line is recognized.\n# But this line is ignored.\nAnd this line is processed.'
	
	TOKENS:
	'This'
	'line'
	'is'
	'recognized'
	'.'
	'And'
	'this'
	'line'
	'is'
	'processed'
	'.'

.. {{{end}}}

Split
=====

If you just need to split an existing string into component tokens,
the convenience function :func:`split()` is a simple wrapper around
the parser.

.. include:: shlex_split.py
    :literal:
    :start-after: #end_pymotw_header

The result is a list:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shlex_split.py'))
.. }}}

::

	$ python shlex_split.py
	
	ORIGINAL: 'This text has "quoted parts" inside it.'
	
	TOKENS:
	['This', 'text', 'has', 'quoted parts', 'inside', 'it.']

.. {{{end}}}


Including Other Sources of Tokens
=================================

The :class:`shlex` class includes several configuration properties
which allow us to control its behavior. The *source* property
enables a feature for code (or configuration) re-use by allowing one
token stream to include another. This is similar to the Bourne shell
``source`` operator, hence the name.

.. include:: shlex_source.py
    :literal:
    :start-after: #end_pymotw_header

Notice the string ``source quotes.txt`` embedded in the original
text. Since the source property of the lexer is set to "source", when
the keyword is encountered the filename appearing in the next title is
automatically included. In order to cause the filename to appear as a
single token, the ``.`` character needs to be added to the list of
characters that are included in words (otherwise "``quotes.txt``"
becomes three tokens, "``quotes``", "``.``", "``txt``"). The output
looks like:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shlex_source.py'))
.. }}}

::

	$ python shlex_source.py
	
	ORIGINAL: 'This text says to source quotes.txt before continuing.'
	
	TOKENS:
	'This'
	'text'
	'says'
	'to'
	'This'
	'string'
	'has'
	'embedded'
	'"double quotes"'
	'and'
	"'single quotes'"
	'in'
	'it'
	','
	'and'
	'even'
	'"a \'nested example\'"'
	'.'
	'before'
	'continuing.'

.. {{{end}}}

The "source" feature uses a method called :func:`sourcehook()` to load
the additional input source, so you can subclass :class:`shlex` to
provide your own implementation to load data from anywhere.

Controlling the Parser
======================

I have already given an example changing the *wordchars* value to
control which characters are included in words. It is also possible to
set the *quotes* character to use additional or alternative
quotes. Each quote must be a single character, so it is not possible
to have different open and close quotes (no parsing on parentheses,
for example).

.. include:: shlex_table.py
    :literal:
    :start-after: #end_pymotw_header

In this example, each table cell is wrapped in vertical bars:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shlex_table.py'))
.. }}}

::

	$ python shlex_table.py
	
	ORIGINAL: '|Col 1||Col 2||Col 3|'
	
	TOKENS:
	'|Col 1|'
	'|Col 2|'
	'|Col 3|'

.. {{{end}}}

It is also possible to control the whitespace characters used to split words.
If we modify the example in shlex_example.py to include period and comma, as
follows:

.. include:: shlex_whitespace.py
    :literal:
    :start-after: #end_pymotw_header

The results change to:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shlex_whitespace.py quotes.txt'))
.. }}}

::

	$ python shlex_whitespace.py quotes.txt
	
	ORIGINAL: 'This string has embedded "double quotes" and \'single quotes\' in it,\nand even "a \'nested example\'".\n'
	
	TOKENS:
	'This'
	'string'
	'has'
	'embedded'
	'"double quotes"'
	'and'
	"'single quotes'"
	'in'
	'it'
	'and'
	'even'
	'"a \'nested example\'"'

.. {{{end}}}


Error Handling
==============

When the parser encounters the end of its input before all quoted
strings are closed, it raises :ref:`ValueError
<exceptions-ValueError>`. When that happens, it is useful to examine
some of the properties of the parser maintained as it processes the
input. For example, *infile* refers to the name of the file being
processed (which might be different from the original file, if one
file sources another). The *lineno* reports the line when the error is
discovered. The *lineno* is typically the end of the file, which may
be far away from the first quote. The *token* attribute contains the
buffer of text not already included in a valid token. The
:func:`error_leader()` method produces a message prefix in a style
similar to Unix compilers, which enables editors such as emacs to
parse the error and take the user directly to the invalid line.

.. include:: shlex_errors.py
    :literal:
    :start-after: #end_pymotw_header

The example above produces this output:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shlex_errors.py', ignore_error=True))
.. }}}

::

	$ python shlex_errors.py
	
	ORIGINAL: 'This line is ok.\nThis line has an "unfinished quote.\nThis line is ok, too.\n'
	
	TOKENS:
	'This'
	'line'
	'is'
	'ok'
	'.'
	'This'
	'line'
	'has'
	'an'
	ERROR: "None", line 4:  No closing quotation following ""unfinished quote."

.. {{{end}}}


POSIX vs. Non-POSIX Parsing
===========================

The default behavior for the parser is to use a backwards-compatible style
which is not POSIX-compliant. For POSIX behavior, set the posix argument when
constructing the parser.

.. include:: shlex_posix.py
    :literal:
    :start-after: #end_pymotw_header

Here are a few examples of the differences in parsing behavior:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'shlex_posix.py'))
.. }}}

::

	$ python shlex_posix.py
	
	ORIGINAL : 'Do"Not"Separate'
	non-POSIX: ['Do"Not"Separate']
	POSIX    : ['DoNotSeparate']
	
	ORIGINAL : '"Do"Separate'
	non-POSIX: ['"Do"', 'Separate']
	POSIX    : ['DoSeparate']
	
	ORIGINAL : 'Escaped \\e Character not in quotes'
	non-POSIX: ['Escaped', '\\', 'e', 'Character', 'not', 'in', 'quotes']
	POSIX    : ['Escaped', 'e', 'Character', 'not', 'in', 'quotes']
	
	ORIGINAL : 'Escaped "\\e" Character in double quotes'
	non-POSIX: ['Escaped', '"\\e"', 'Character', 'in', 'double', 'quotes']
	POSIX    : ['Escaped', '\\e', 'Character', 'in', 'double', 'quotes']
	
	ORIGINAL : "Escaped '\\e' Character in single quotes"
	non-POSIX: ['Escaped', "'\\e'", 'Character', 'in', 'single', 'quotes']
	POSIX    : ['Escaped', '\\e', 'Character', 'in', 'single', 'quotes']
	
	ORIGINAL : 'Escaped \'\\\'\' \\"\\\'\\" single quote'
	non-POSIX: error(No closing quotation)
	POSIX    : ['Escaped', '\\ \\"\\"', 'single', 'quote']
	
	ORIGINAL : 'Escaped "\\"" \\\'\\"\\\' double quote'
	non-POSIX: error(No closing quotation)
	POSIX    : ['Escaped', '"', '\'"\'', 'double', 'quote']
	
	ORIGINAL : '"\'Strip extra layer of quotes\'"'
	non-POSIX: ['"\'Strip extra layer of quotes\'"']
	POSIX    : ["'Strip extra layer of quotes'"]
	

.. {{{end}}}


.. seealso::

    `shlex <https://docs.python.org/2/library/shlex.html>`_
        Standard library documentation for this module.

    :mod:`cmd`
        Tools for building interactive command interpreters.

    :mod:`optparse`
        Command line option parsing.

    :mod:`getopt`
        Command line option parsing.
