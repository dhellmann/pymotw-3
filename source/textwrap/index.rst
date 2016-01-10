========================================
 textwrap -- Formatting Text Paragraphs
========================================

.. module:: textwrap
    :synopsis: Formatting text paragraphs

:Purpose: Formatting text by adjusting where line breaks occur in a paragraph.
:Python Version: 2.5 and later

The :mod:`textwrap` module can be used to format text for output in
situations where pretty-printing is desired. It offers programmatic
functionality similar to the paragraph wrapping or filling features
found in many text editors and word processors.

Example Data
============

The examples in this section use the module ``textwrap_example.py``,
which contains a string ``sample_text``.

.. include:: textwrap_example.py
    :literal:
    :start-after: #end_pymotw_header


Filling Paragraphs
==================

The :func:`fill()` function takes text as input and produces formatted
text as output.

.. include:: textwrap_fill.py
    :literal:
    :start-after: #end_pymotw_header

The results are something less than desirable.  The text is now left
justified, but the first line retains its indent and the spaces from
the front of each subsequent line are embedded in the paragraph.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'textwrap_fill.py'))
.. }}}

::

	$ python textwrap_fill.py
	
	No dedent:
	
	     The textwrap module can be used to format
	text for output in     situations where pretty-
	printing is desired.  It offers     programmatic
	functionality similar to the paragraph wrapping
	or filling features found in many text editors.

.. {{{end}}}


Removing Existing Indentation
=============================

The previous example has embedded tabs and extra spaces mixed into the
middle of the output, so it is not formatted very cleanly. Removing
the common whitespace prefix from all of the lines in the sample text
produces better results and allows the use of docstrings or embedded
multi-line strings straight from Python code while removing the
formatting of the code itself. The sample string has an artificial
indent level introduced for illustrating this feature.

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
	
	The textwrap module can be used to format text for output in
	situations where pretty-printing is desired.  It offers
	programmatic functionality similar to the paragraph wrapping
	or filling features found in many text editors.
	

.. {{{end}}}

Since "dedent" is the opposite of "indent", the result is a block of
text with the common initial whitespace from each line removed. If one
line is already indented more than another, some of the whitespace
will not be removed.

Input like

::

  ␣Line one.
  ␣␣␣Line two.
  ␣Line three.

becomes

::

  Line one.
  ␣␣Line two.
  Line three.

Combining Dedent and Fill
=========================

Next, the dedented text can be passed through :func:`fill()` with a
few different *width* values.

.. include:: textwrap_fill_width.py
    :literal:
    :start-after: #end_pymotw_header


This produces outputs in the specified widths.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'textwrap_fill_width.py'))
.. }}}

::

	$ python textwrap_fill_width.py
	
	45 Columns:
	
	The textwrap module can be used to format
	text for output in situations where pretty-
	printing is desired.  It offers programmatic
	functionality similar to the paragraph
	wrapping or filling features found in many
	text editors.
	
	70 Columns:
	
	The textwrap module can be used to format text for output in
	situations where pretty-printing is desired.  It offers programmatic
	functionality similar to the paragraph wrapping or filling features
	found in many text editors.
	

.. {{{end}}}


Hanging Indents
===============

Besides the width of the output, the indent of the first line can be
controlled independently of subsequent lines.

.. include:: textwrap_hanging_indent.py
    :literal:
    :start-after: #end_pymotw_header

This makes it possible to produce a hanging indent, where the
first line is indented less than the other lines.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'textwrap_hanging_indent.py'))
.. }}}

::

	$ python textwrap_hanging_indent.py
	
	The textwrap module can be used to format text for
	    output in situations where pretty-printing is
	    desired.  It offers programmatic functionality
	    similar to the paragraph wrapping or filling
	    features found in many text editors.

.. {{{end}}}

The indent values can include non-whitespace characters, too, so the
hanging indent can be prefixed with ``*`` to produce bullet points,
etc. 

.. seealso::

    `textwrap <http://docs.python.org/lib/module-textwrap.html>`_
        Standard library documentation for this module.
