Implementing MapReduce
======================

The :class:`Pool` class can be used to create a simple single-server
MapReduce implementation.  Although it does not give the full benefits
of distributed processing, it does illustrate how easy it is to break
some problems down into distributable units of work.

In a MapReduce-based system, input data is broken down into chunks for
processing by different worker instances.  Each chunk of input data is
*mapped* to an intermediate state using a simple transformation.  The
intermediate data is then collected together and partitioned based on
a key value so that all of the related values are together.  Finally,
the partitioned data is *reduced* to a result set.

.. literalinclude:: multiprocessing_mapreduce.py
    :caption:
    :start-after: #end_pymotw_header

The following example script uses SimpleMapReduce to counts the
"words" in the reStructuredText source for this article, ignoring some
of the markup.

.. literalinclude:: multiprocessing_wordcount.py
    :caption:
    :start-after: #end_pymotw_header

The :func:`file_to_words` function converts each input file to a
sequence of tuples containing the word and the number ``1`` (representing
a single occurrence) .The data is divided up by :func:`partition`
using the word as the key, so the resulting structure consists of a key
and a sequence of ``1`` values representing each occurrence of the word.
The partitioned data is converted to a set of tuples containing a word
and the count for that word by :func:`count_words` during the
reduction phase.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_wordcount.py'))
.. }}}

::

	$ python multiprocessing_wordcount.py

	PoolWorker-1 reading basics.rst
	PoolWorker-1 reading index.rst
	PoolWorker-2 reading communication.rst
	PoolWorker-2 reading mapreduce.rst
	
	TOP 20 WORDS BY FREQUENCY
	
	process         :    81
	multiprocessing :    43
	worker          :    38
	after           :    34
	starting        :    33
	running         :    32
	processes       :    32
	python          :    31
	start           :    29
	class           :    28
	literal         :    27
	header          :    27
	pymotw          :    27
	end             :    27
	daemon          :    23
	now             :    22
	func            :    21
	can             :    21
	consumer        :    20
	mod             :    19

.. {{{end}}}
