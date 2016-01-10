======
 Text
======

The :class:`string` class is the most obvious text processing tool
available to Python programmers, but there are plenty of other tools
in the standard library to make advanced text manipulation simple.  

Older code, written before Python 2.0, uses functions from the
:mod:`string` module, instead of methods of :class:`string` objects.
There is an equivalent method for each function from the module, and
use of the functions is deprecated for new code.

Programs using Python 2.4 or later may use :class:`string.Template`
as a simple way to parameterize strings beyond the features of the
:class:`string` or :class:`unicode` classes.  While not as
feature-rich as templates defined by many of the web frameworks or
extension modules available from the Python Package Index,
:class:`string.Template` is a good middle ground for user-modifiable
templates where dynamic values need to be inserted into otherwise
static text.

The :mod:`textwrap` module includes tools for formatting text from
paragraphs by limiting the width of output, adding indentation, and
inserting line breaks to wrap lines consistently.

The standard library includes two modules related to comparing text
values beyond the built-in equality and sort comparison supported by
string objects.  :mod:`re` provides a complete regular expression
library, implemented in C for speed.  Regular expressions are
well-suited for finding substrings within a larger data set, comparing
strings against a pattern more complex than another fixed string, and
mild parsing.

:mod:`difflib`, on the other hand, computes the actual differences
between sequences of text in terms of the parts added, removed, or
changed.  The output of the comparison functions in :mod:`difflib` can
be used to provide more detailed feedback to user about where changes
occur in two inputs, how a document has changed over time, etc.

.. toctree::
   :maxdepth: 1

   textwrap/index
   difflib/index

..
   string/index
   re/index
   difflib/index
