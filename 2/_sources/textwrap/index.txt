======================================
textwrap -- Formatting text paragraphs
======================================

.. module:: textwrap
    :synopsis: Formatting text by adjusting where line breaks occur in a paragraph.

:Purpose: Formatting text by adjusting where line breaks occur in a paragraph.
:Available In: 2.5

The :mod:`textwrap` module can be used to format text for output in
situations where pretty-printing is desired. It offers programmatic
functionality similar to the paragraph wrapping or filling features
found in many text editors.

Example Data
============

The examples below use ``textwrap_example.py``, which contains a
string ``sample_text``:

.. include:: textwrap_example.py
    :literal:
    :start-after: #end_pymotw_header


Filling Paragraphs
==================

The :func:`fill()` convenience function takes text as input and
produces formatted text as output. Let's see what it does with the
sample_text provided.

.. include:: textwrap_fill.py
    :literal:
    :start-after: #end_pymotw_header

The results are something less than what we want:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'textwrap_fill.py'))
.. }}}

::

	$ python textwrap_fill.py
	
	No dedent:
	
	         The textwrap module can be used to format text for output in
	situations         where pretty-printing is desired.  It offers
	programmatic functionality similar         to the paragraph wrapping
	or filling features found in many text editors.

.. {{{end}}}


Removing Existing Indentation
=============================

Notice the embedded tabs and extra spaces mixed into the middle of the
output. It looks pretty rough. We can do better if we start by
removing any common whitespace prefix from all of the lines in the
sample text. This allows us to use docstrings or embedded multi-line
strings straight from our Python code while removing the formatting of
the code itself. The sample string has an artificial indent level
introduced for illustrating this feature.

.. include:: textwrap_dedent.py
    :literal:
    :start-after: #end_pymotw_header

The results are starting to look better:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'textwrap_dedent.py'))
.. }}}

::

	$ python textwrap_dedent.py
	
	Dedented:
	
	The textwrap module can be used to format text for output in situations
	where pretty-printing is desired.  It offers programmatic functionality similar
	to the paragraph wrapping or filling features found in many text editors.

.. {{{end}}}

Since "dedent" is the opposite of "indent", the result is a block of
text with the common initial whitespace from each line removed. If one
line is already indented more than another, some of the whitespace
will not be removed.

::

     One tab.
     Two tabs.
    One tab.

becomes

::

    One tab.
    Two tabs.
    One tab.


Combining Dedent and Fill
=========================

Next, let's see what happens if we take the dedented text and pass it
through :func:`fill()` with a few different *width* values.

.. include:: textwrap_fill_width.py
    :literal:
    :start-after: #end_pymotw_header


This gives several sets of output in the specified widths:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'textwrap_fill_width.py'))
.. }}}

::

	$ python textwrap_fill_width.py
	
	
	20 Columns:
	
	The textwrap module
	can be used to
	format text for
	output in situations
	where pretty-
	printing is desired.
	It offers
	programmatic
	functionality
	similar to the
	paragraph wrapping
	or filling features
	found in many text
	editors.
	
	60 Columns:
	
	The textwrap module can be used to format text for output in
	situations where pretty-printing is desired.  It offers
	programmatic functionality similar to the paragraph wrapping
	or filling features found in many text editors.
	
	80 Columns:
	
	The textwrap module can be used to format text for output in situations where
	pretty-printing is desired.  It offers programmatic functionality similar to the
	paragraph wrapping or filling features found in many text editors.

.. {{{end}}}


Hanging Indents
===============

Besides the width of the output, you can control the indent of the
first line independently of subsequent lines.

.. include:: textwrap_hanging_indent.py
    :literal:
    :start-after: #end_pymotw_header

This makes it relatively easy to produce a hanging indent, where the
first line is indented less than the other lines.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'textwrap_hanging_indent.py'))
.. }}}

::

	$ python textwrap_hanging_indent.py
	
	The textwrap module can be used to format text for output in
	    situations where pretty-printing is desired.  It offers
	    programmatic functionality similar to the paragraph wrapping or
	    filling features found in many text editors.

.. {{{end}}}

The indent values can include non-whitespace characters, too, so the
hanging indent can be prefixed with ``*`` to produce bullet points,
etc. That came in handy when I converted my old zwiki content so I
could import it into trac. I used the StructuredText package from Zope
to parse the zwiki data, then created a formatter to produce trac's
wiki markup as output. Using :mod:`textwrap`, I was able to format the
output pages so almost no manual tweaking was needed after the
conversion.

.. seealso::

    `textwrap <https://docs.python.org/2/library/textwrap.html>`_
        Standard library documentation for this module.

    :ref:`article-text-processing`
        More tools for working with text.
