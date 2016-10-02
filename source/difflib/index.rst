===============================
 difflib --- Compare Sequences
===============================

.. module:: difflib
    :synopsis: Compare sequences, especially lines of text.

:Purpose: Compare sequences, especially lines of text.

The :mod:`difflib` module contains tools for computing and working
with differences between sequences.  It is especially useful for
comparing text, and includes functions that produce reports using
several common difference formats.

The examples in this section will all use this common test data in the
``difflib_data.py`` module:

.. literalinclude:: difflib_data.py
    :caption:
    :start-after: #end_pymotw_header

Comparing Bodies of Text
========================

The :class:`Differ` class works on sequences of text lines and
produces human-readable *deltas*, or change instructions, including
differences within individual lines.  The default output produced by
:class:`Differ` is similar to the :command:`diff` command line tool
under UNIX.  It includes the original input values from both lists,
including common values, and markup data to indicate what changes were
made.

* Lines prefixed with ``-`` indicate that they were in the first
  sequence, but not the second.
* Lines prefixed with ``+`` were in the second sequence, but not the
  first.
* If a line has an incremental difference between versions, an extra
  line prefixed with ``?`` is used to highlight the change within the
  new version.
* If a line has not changed, it is printed with an extra blank space
  on the left column so that it is aligned with the other output that
  may have differences.

Breaking the text up into a sequence of individual lines before
passing it to :func:`compare` produces more readable output than
passing in large strings.

.. literalinclude:: difflib_differ.py
    :caption:
    :start-after: #end_pymotw_header

.. {{{cog
.. run_script(cog.inFile, 'difflib_differ.py > output.diff')
.. }}}
.. {{{end}}}


The beginning of both text segments in the sample data is the same, so
the first line is printed without any extra annotation.

.. literalinclude:: output.diff
   :lines: 1-2

The third line of the data has been changed to include a comma in the
modified text. Both versions of the line are printed, with the extra
information on line five showing the column where the text was modified,
including the fact that the ``,`` character was added.

.. literalinclude:: output.diff
   :lines: 3-5
   :language: none

The next few lines of the output show that an extra space was removed.

.. literalinclude:: output.diff
   :lines: 7-10
   :language: none

Next, a more complex change was made, replacing several words in a phrase.

.. literalinclude:: output.diff
   :lines: 11-16
   :language: none

The last sentence in the paragraph was changed significantly, so the
difference is represented by removing the old version and adding the
new.

.. literalinclude:: output.diff
   :lines: 17-
   :language: none

The :func:`ndiff` function produces essentially the same output.
The processing is specifically tailored for working with text data and
eliminating "noise" in the input.

Other Output Formats
--------------------

While the :class:`Differ` class shows all of the input lines, a
*unified diff* only includes modified lines and a bit of context. The
:func:`unified_diff` function produces this sort of output.

.. literalinclude:: difflib_unified.py
    :caption:
    :start-after: #end_pymotw_header

The *lineterm* argument is used to tell :func:`unified_diff` to skip
appending newlines to the control lines it returns because the input
lines do not include them.  Newlines are added to all of the lines
when they are printed.  The output should look familiar to users of
many common version control tools.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'difflib_unified.py'))
.. }}}

.. code-block:: none

	$ python3 difflib_unified.py
	
	--- 
	+++ 
	@@ -1,11 +1,11 @@
	 Lorem ipsum dolor sit amet, consectetuer adipiscing
	 elit. Integer eu lacus accumsan arcu fermentum euismod. Donec
	-pulvinar porttitor tellus. Aliquam venenatis. Donec facilisis
	-pharetra tortor.  In nec mauris eget magna consequat
	-convalis. Nam sed sem vitae odio pellentesque interdum. Sed
	+pulvinar, porttitor tellus. Aliquam venenatis. Donec facilisis
	+pharetra tortor. In nec mauris eget magna consequat
	+convalis. Nam cras vitae mi vitae odio pellentesque interdum. S
	ed
	 consequat viverra nisl. Suspendisse arcu metus, blandit quis,
	 rhoncus ac, pharetra eget, velit. Mauris urna. Morbi nonummy
	 molestie orci. Praesent nisi elit, fringilla ac, suscipit non,
	 tristique vel, mauris. Curabitur vel lorem id nisl porta
	-adipiscing. Suspendisse eu lectus. In nunc. Duis vulputate
	-tristique enim. Donec quis lectus a justo imperdiet tempus.
	+adipiscing. Duis vulputate tristique enim. Donec quis lectus a
	+justo imperdiet tempus.  Suspendisse eu lectus. In nunc.

.. {{{end}}}

Using :func:`context_diff` produces similar readable output.

Junk Data
=========

All of the functions that produce difference sequences accept
arguments to indicate which lines should be ignored and which
characters within a line should be ignored. These parameters can be
used to skip over markup or whitespace changes in two versions of a
file, for example.

.. literalinclude:: difflib_junk.py
    :caption:
    :start-after: #end_pymotw_header

The default for :class:`Differ` is to not ignore any lines or
characters explicitly, but to rely on the ability of
:class:`SequenceMatcher` to detect noise. The default for
:func:`ndiff` is to ignore space and tab characters.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'difflib_junk.py'))
.. }}}

.. code-block:: none

	$ python3 difflib_junk.py
	
	A = ' abcd'
	B = 'abcd abcd'
	
	Without junk detection:
	  a    = 0
	  b    = 4
	  size = 5
	  A[a:a+size] = ' abcd'
	  B[b:b+size] = ' abcd'
	
	Treat spaces as junk:
	  a    = 1
	  b    = 0
	  size = 4
	  A[a:a+size] = 'abcd'
	  B[b:b+size] = 'abcd'

.. {{{end}}}


Comparing Arbitrary Types
=========================

The :class:`SequenceMatcher` class compares two sequences of any
types, as long as the values are hashable. It uses an algorithm to
identify the longest contiguous matching blocks from the sequences,
eliminating "junk" values that do not contribute to the real data.

The funct :func:`get_opcodes` returns a list of instructions for
modifying the first sequence to make it match the second. The
instructions are encoded as five-element tuples including a string
instruction (the "opcode") and two pairs of start and stop indexes
into the sequences (denoted as ``i1``, ``i2``, ``j1``, and ``j2``).

.. list-table:: get_opcodes() instructions
   :header-rows: 1

   * - Opcode
     - Definition
   * - ``'replace'``
     - Replace ``a[i1:i2]`` with ``b[j1:j2]``.
   * - ``'delete'``
     - Remove ``a[i1:i2]`` entirely.
   * - ``'insert'``
     - Insert ``b[j1:j2]`` at ``a[i1:i1]``.
   * - ``'equal'``
     - The subsequences are already equal.

.. literalinclude:: difflib_seq.py
    :caption:
    :start-after: #end_pymotw_header

This example compares two lists of integers and uses
:func:`get_opcodes` to derive the instructions for converting the
original list into the newer version.  The modifications are applied
in reverse order so that the list indexes remain accurate after items
are added and removed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'difflib_seq.py'))
.. }}}

.. code-block:: none

	$ python3 difflib_seq.py
	
	Initial data:
	s1 = [1, 2, 3, 5, 6, 4]
	s2 = [2, 3, 5, 4, 6, 1]
	s1 == s2: False
	
	Replace [4] from s1[5:6] with [1] from s2[5:6]
	  before = [1, 2, 3, 5, 6, 4]
	   after = [1, 2, 3, 5, 6, 1] 
	
	s1[4:5] and s2[4:5] are the same
	   after = [1, 2, 3, 5, 6, 1] 
	
	Insert [4] from s2[3:4] into s1 at 4
	  before = [1, 2, 3, 5, 6, 1]
	   after = [1, 2, 3, 5, 4, 6, 1] 
	
	s1[1:4] and s2[0:3] are the same
	   after = [1, 2, 3, 5, 4, 6, 1] 
	
	Remove [1] from positions [0:1]
	  before = [1, 2, 3, 5, 4, 6, 1]
	   after = [2, 3, 5, 4, 6, 1] 
	
	s1 == s2: True

.. {{{end}}}

:class:`SequenceMatcher` works with custom classes, as well as
built-in types, as long as they are hashable.

.. seealso::

   * :pydoc:`difflib`

   * `Pattern Matching: The Gestalt Approach
     <http://www.drdobbs.com/database/pattern-matching-the-gestalt-approach/184407970>`__
     -- Discussion of a similar algorithm by John W. Ratcliff
     and D. E. Metzener published in Dr. Dobb’s Journal in July, 1988.
