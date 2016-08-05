Type Checking
=============

The :mod:`operator` module also includes functions for testing API
compliance for mapping, number, and sequence types. 

.. include:: operator_typechecking.py
    :literal:
    :start-after: #end_pymotw_header

The tests are not perfect, since the interfaces are not strictly
defined, but they do provide some idea of what is supported.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'operator_typechecking.py'))
.. }}}

::

	$ python operator_typechecking.py
	
	isMappingType(o): False
	isMappingType(t): True
	isNumberType(o): False
	isNumberType(t): True
	isSequenceType(o): False
	isSequenceType(t): True

.. {{{end}}}
