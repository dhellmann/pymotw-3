.. _article-text-processing:

#####################
Text Processing Tools
#####################

The string class is the most obvious text processing tool available to Python programmers, but there are plenty of other tools in the standard library to make text manipulation simpler.  

string module
=============

Old-style code will use functions from the :mod:`string` module, instead of methods of string objects.  There is an equivalent method for each function from the module, and use of the functions is deprecated for new code.  

Newer code may use a ``string.Template`` as a simple way to parameterize strings beyond the features of the string or unicode classes.  While not as feature-rich as templates defined by many of the web frameworks or extension modules available on PyPI, ``string.Template`` is a good middle ground for user-modifiable templates where dynamic values need to be inserted into otherwise static text.

Text Input
==========

Reading from a file is easy enough, but if you're writing a line-by-line filter the :mod:`fileinput` module is even easier.  The fileinput API calls for you to iterate over the ``input()`` generator, processing each line as it is yielded.  The generator handles parsing command line arguments for file names, or falling back to reading directly from ``sys.stdin``.  The result is a flexible tool your users can run directly on a file or as part of a pipeline.

Text Output
===========

The :mod:`textwrap` module includes tools for formatting text from paragraphs by limiting the width of output, adding indentation, and inserting line breaks to wrap lines consistently.

Comparing Values
================

The standard library includes two modules related to comparing text values beyond the built-in equality and sort comparison supported by string objects.  :mod:`re` provides a complete regular expression library, implemented largely in C for performance.  Regular expressions are well-suited for finding substrings within a larger data set, comparing strings against a pattern (rather than another fixed string), and mild parsing.  

:mod:`difflib`, on the other hand, shows you the actual differences between sequences of text in terms of the parts added, removed, or changed.  The output of the comparison functions in :mod:`difflib` can be used to provide more detailed feedback to user about where changes occur in two inputs, how a document has changed over time, etc.
