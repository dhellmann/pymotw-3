==========================
 pyclbr --- Class Browser
==========================

.. module:: pyclbr
    :synopsis: Class browser

:Purpose: Implements an API suitable for use in a source code editor
          for making a class browser.

:mod:`pyclbr` can scan Python source to find classes and stand-alone
functions.  The information about class, method, and function names
and line numbers is gathered using :mod:`tokenize` *without* importing
the code.

The examples in this section use this source file as input:

.. literalinclude:: pyclbr_example.py
    :caption:
    :start-after: #end_pymotw_header


Scanning for Classes
====================

There are two public functions exposed by :mod:`pyclbr`.
The first, :func:`readmodule`, takes the name of the module as argument returns a
mapping of class names to :class:`Class` objects containing the metadata
about the class source.

.. literalinclude:: pyclbr_readmodule.py
    :caption:
    :start-after: #end_pymotw_header

The metadata for the class includes the file and line number where it
is defined, as well as the names of super classes.  The methods of the
class are saved as a mapping between method name and line number.  The
output shows the classes and methods listed in order based on
their line number in the source file.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pyclbr_readmodule.py'))
.. }}}

.. code-block:: none

	$ python3 pyclbr_readmodule.py
	
	Class: Base
		File: pyclbr_example.py [11]
		Method: method1 [15]
	
	Class: Sub1
		File: pyclbr_example.py [19]
		Super classes: ['Base']
	
	Class: Sub2
		File: pyclbr_example.py [24]
		Super classes: ['Base']
	
	Class: Mixin
		File: pyclbr_example.py [29]
		Method: method2 [33]
	
	Class: MixinUser
		File: pyclbr_example.py [37]
		Super classes: ['Sub2', 'Mixin']
		Method: method1 [41]
		Method: method2 [44]
		Method: method3 [47]
	

.. {{{end}}}


Scanning for Functions
======================

The other public function in :mod:`pyclbr` is :func:`readmodule_ex`.
It does everything that :func:`readmodule` does, and adds functions to
the result set.

.. literalinclude:: pyclbr_readmodule_ex.py
    :caption:
    :start-after: #end_pymotw_header

Each :class:`Function` object has properties much like the
:class:`Class` object.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pyclbr_readmodule_ex.py'))
.. }}}

.. code-block:: none

	$ python3 pyclbr_readmodule_ex.py
	
	Function: my_function [51]

.. {{{end}}}



.. seealso::

   * :pydoc:`pyclbr`

   * :mod:`inspect` -- The ``inspect`` module can discover more
     metadata about classes and functions, but requires importing the
     code.

   * :mod:`tokenize` -- The ``tokenize`` module parses Python source
     code into tokens.
