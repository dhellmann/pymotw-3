======================================
pyclbr -- Python class browser support
======================================

.. module:: pyclbr
    :synopsis: Python class browser support

:Purpose: Implements an API suitable for use in a source code editor for making a class browser.
:Available In: 1.4 and later

:mod:`pyclbr` can scan Python source to find classes and stand-alone functions.  The information about class, method, and function names and line numbers is gathered using :mod:`tokenize` *without* importing the code.

The examples below use this source file as input:

.. include:: pyclbr_example.py
    :literal:
    :start-after: #end_pymotw_header


Scanning for Classes
====================

There are two public functions exposed by :mod:`pyclbr`.  ``readmodule()`` takes the name of the module as argument returns a mapping of class names to ``Class`` objects containing the meta-data about the class source.

.. include:: pyclbr_readmodule.py
    :literal:
    :start-after: #end_pymotw_header

The meta-data for the class includes the file and line number where it is defined, as well as the names of super classes.  The methods of the class are saved as a mapping between method name and line number.  The output below shows the classes and methods listed in order based on their line number in the source file.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pyclbr_readmodule.py'))
.. }}}

::

	$ python pyclbr_readmodule.py
	
	Class: Base
		File: pyclbr_example.py [10]
		Method: method1 [14]
	
	Class: Sub1
		File: pyclbr_example.py [17]
		Super classes: ['Base']
	
	Class: Sub2
		File: pyclbr_example.py [21]
		Super classes: ['Base']
	
	Class: Mixin
		File: pyclbr_example.py [25]
		Method: method2 [29]
	
	Class: MixinUser
		File: pyclbr_example.py [32]
		Super classes: ['Sub2', 'Mixin']
		Method: method1 [36]
		Method: method2 [39]
		Method: method3 [42]
	

.. {{{end}}}


Scanning for Functions
======================

The other public function in :mod:`pyclbr` is ``readmodule_ex()``.  It does everything that ``readmodule()`` does, and adds functions to the result set.

.. include:: pyclbr_readmodule_ex.py
    :literal:
    :start-after: #end_pymotw_header

Each ``Function`` object has properties much like the ``Class`` object.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pyclbr_readmodule_ex.py'))
.. }}}

::

	$ python pyclbr_readmodule_ex.py
	
	Function: my_function [45]

.. {{{end}}}



.. seealso::

    `pyclbr <http://docs.python.org/2.7/library/pyclbr.html>`_
        The standard library documentation for this module.

    :mod:`inspect`
        The inspect module can discover more meta-data about classes and functions, but requires importing the code.

    :mod:`tokenize`
        The tokenize module parses Python source code into tokens.
