=============================================
 fileinput --- Command-Line Filter Framework
=============================================

.. module:: fileinput
    :synopsis: Process lines from input streams.

:Purpose: Create command-line filter programs to process lines from input streams.

The :mod:`fileinput` module is a framework for creating command-line
programs for processing text files as a filter.

Converting M3U files to RSS
===========================

An example of a filter is m3utorss_, a program to convert a set of
MP3 files into an RSS feed that can be shared as a podcast.  The
inputs to the program are one or more m3u files listing the MP3 files
to be distributed. The output is an RSS feed printed to the
console. To process the input, the program needs to iterate over the
list of filenames and

* Open each file.
* Read each line of the file.
* Figure out if the line refers to an mp3 file.
* If it does, extract the information from the mp3 file needed for the RSS feed.
* Print the output.

All of this file handling could have been coded by hand. It is not
that complicated and, with some testing, even the error handling would
be right. But :mod:`fileinput` handles all of the details, so the
program is simplified.

.. literalinclude:: fileinput_example.py
   :lines: 30-39

The :func:`input` function takes as argument a list of filenames to
examine. If the list is empty, the module reads data from standard
input. The function returns an iterator that produces individual lines
from the text files being processed.  The caller just needs to loop
over each line, skipping blanks and comments, to find the references
to MP3 files.

Here is the complete program.

.. literalinclude:: fileinput_example.py
   :caption:
   :start-after: #end_pymotw_header

This sample input file contains the names of several MP3 files.

.. literalinclude:: sample_data.m3u
   :caption:

Running ``fileinput_example.py`` with the sample input produces XML
data using the RSS format.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fileinput_example.py sample_data.m3u'))
.. }}}

.. code-block:: none

	$ python3 fileinput_example.py sample_data.m3u
	
	<?xml version="1.0" ?>
	<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/">
	  <channel>
	    <title>Sample podcast feed</title>
	    <description>Generated for PyMOTW</description>
	    <pubDate>Sun Jul 10 10:45:01 2016</pubDate>
	    <generator>https://pymotw.com/</generator>
	  </channel>
	  <item>
	    <title>episode-one.mp3</title>
	    <enclosure type="audio/mpeg" url="episode-one.mp3"/>
	  </item>
	  <item>
	    <title>episode-two.mp3</title>
	    <enclosure type="audio/mpeg" url="episode-two.mp3"/>
	  </item>
	</rss>
	

.. {{{end}}}

Progress Metadata
=================

In the previous example, the filename and line number being processed were
not important. Other tools, such as grep-like searching, might need
that information. :mod:`fileinput` includes functions for accessing
all of the metadata about the current line (:func:`filename`,
:func:`filelineno`, and :func:`lineno`).

.. literalinclude:: fileinput_grep.py
   :caption:
   :start-after: #end_pymotw_header

A basic pattern matching loop can be used to find the occurrences of
the string ``"fileinput"`` in the source for these examples.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'fileinput_grep.py fileinput *.py'))
.. }}}

.. code-block:: none

	$ python3 fileinput_grep.py fileinput *.py
	
	fileinput_change_subnet.py:10:import fileinput
	fileinput_change_subnet.py:17:for line in fileinput.input(files,
	 inplace=True):
	fileinput_change_subnet_noisy.py:10:import fileinput
	fileinput_change_subnet_noisy.py:18:for line in fileinput.input(
	files, inplace=True):
	fileinput_change_subnet_noisy.py:19:    if fileinput.isfirstline
	():
	fileinput_change_subnet_noisy.py:21:            fileinput.filena
	me()))
	fileinput_example.py:6:"""Example for fileinput module.
	fileinput_example.py:10:import fileinput
	fileinput_example.py:30:for line in fileinput.input(sys.argv[1:]
	):
	fileinput_grep.py:10:import fileinput
	fileinput_grep.py:16:for line in fileinput.input(sys.argv[2:]):
	fileinput_grep.py:18:        if fileinput.isstdin():
	fileinput_grep.py:22:        print(fmt.format(filename=fileinput
	.filename(),
	fileinput_grep.py:23:                         lineno=fileinput.f
	ilelineno(),

.. {{{end}}}

Text can also be read from standard input.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'cat *.py | python fileinput_grep.py fileinput', 
..                    interpreter=None))
.. }}}

.. code-block:: none

	$ cat *.py | python fileinput_grep.py fileinput
	
	10:import fileinput
	17:for line in fileinput.input(files, inplace=True):
	29:import fileinput
	37:for line in fileinput.input(files, inplace=True):
	38:    if fileinput.isfirstline():
	40:            fileinput.filename()))
	54:"""Example for fileinput module.
	58:import fileinput
	78:for line in fileinput.input(sys.argv[1:]):
	101:import fileinput
	107:for line in fileinput.input(sys.argv[2:]):
	109:        if fileinput.isstdin():
	113:        print(fmt.format(filename=fileinput.filename(),
	114:                         lineno=fileinput.filelineno(),

.. {{{end}}}


In-place Filtering
==================

Another common file-processing operation is to modify the contents of
a file where it is, rather than making a new file.  For example, a
Unix hosts file might need to be updated if a subnet range changes.

.. literalinclude:: etc_hosts

The safe way to make the change automatically is to create a new file
based on the input and then replace the original with the edited copy.
:mod:`fileinput` supports this automatically using the *inplace*
option.

.. literalinclude:: fileinput_change_subnet.py
   :caption:
   :start-after: #end_pymotw_header

Although the script uses :func:`print`, no output is produced because
:mod:`fileinput` redirects standard output to the file being
overwritten.

.. {{{cog
.. path('source/fileinput/etc_hosts').copy('source/fileinput/etc_hosts.txt')
.. cog.out(run_script(cog.inFile, 'fileinput_change_subnet.py 10.16 10.17 etc_hosts.txt'))
.. }}}

.. code-block:: none

	$ python3 fileinput_change_subnet.py 10.16 10.17 etc_hosts.txt
	

.. {{{end}}}

The updated file has the changed IP addresses of all of the servers on
the ``10.16.0.0/16`` network.

.. literalinclude:: etc_hosts.txt

Before processing begins, a backup file is created using the original
name plus ``.bak``.  

.. literalinclude:: fileinput_change_subnet_noisy.py
   :caption:
   :start-after: #end_pymotw_header

The backup file is removed when the input is closed.

.. {{{cog
.. path('source/fileinput/etc_hosts').copy('source/fileinput/etc_hosts.txt')
.. cog.out(run_script(cog.inFile, 'fileinput_change_subnet_noisy.py 10.16. 10.17. etc_hosts.txt'))
.. }}}

.. code-block:: none

	$ python3 fileinput_change_subnet_noisy.py 10.16. 10.17. etc_h\
	osts.txt
	
	Started processing etc_hosts.txt
	Directory contains: ['etc_hosts.txt', 'etc_hosts.txt.bak']
	Finished processing
	Directory contains: ['etc_hosts.txt']

.. {{{end}}}


.. seealso::

   * :pydoc:`fileinput`

   * m3utorss_ -- Script to convert m3u files listing MP3s to an RSS
     file suitable for use as a podcast feed.

   * :mod:`xml.etree` -- More details of using ElementTree to
     produce XML.

.. _m3utorss: https://pypi.python.org/pypi/m3utorss
