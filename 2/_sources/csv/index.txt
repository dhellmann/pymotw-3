==================================
csv -- Comma-separated value files
==================================

.. module:: csv
    :synopsis: Read and write comma separated value files.

:Purpose: Read and write comma separated value files.
:Available In: 2.3 and later

The :mod:`csv` module is useful for working with data exported from
spreadsheets and databases into text files formatted with fields and
records, commonly referred to as *comma-separated value* (CSV) format
because commas are often used to separate the fields in a record.

.. note::

  The Python 2.5 version of :mod:`csv` does not support Unicode
  data. There are also "issues with ASCII NUL characters". Using UTF-8
  or printable ASCII is recommended.

Reading
=======

Use :func:`reader` to create a an object for reading data from a CSV
file.  The reader can be used as an iterator to process the rows of
the file in order. For example:

.. include:: csv_reader.py
    :literal:
    :start-after: #end_pymotw_header

The first argument to :func:`reader` is the source of text lines. In
this case, it is a file, but any iterable is accepted (:mod:`StringIO`
instances, lists, etc.).  Other optional arguments can be given to
control how the input data is parsed.

This example file was exported from NeoOffice_.

.. include:: testdata.csv
    :literal:

As it is read, each row of the input data is parsed and converted to a
list of strings.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'csv_reader.py testdata.csv'))
.. }}}

::

	$ python csv_reader.py testdata.csv
	
	['Title 1', 'Title 2', 'Title 3']
	['1', 'a', '08/18/07']
	['2', 'b', '08/19/07']
	['3', 'c', '08/20/07']
	['4', 'd', '08/21/07']
	['5', 'e', '08/22/07']
	['6', 'f', '08/23/07']
	['7', 'g', '08/24/07']
	['8', 'h', '08/25/07']
	['9', 'i', '08/26/07']

.. {{{end}}}


The parser handles line breaks embedded within strings in a row, which
is why a "row" is not always the same as a "line" of input from the
file.

.. include:: testlinebreak.csv
    :literal:

Values with line breaks in the input retain the internal line breaks
when returned by the parser.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'csv_reader.py testlinebreak.csv'))
.. }}}

::

	$ python csv_reader.py testlinebreak.csv
	
	['Title 1', 'Title 2', 'Title 3']
	['1', 'first line\nsecond line', '08/18/07']

.. {{{end}}}

Writing
=======

Writing CSV files is just as easy as reading them. Use :func:`writer`
to create an object for writing, then iterate over the rows, using
:func:`writerow` to print them.

.. include:: csv_writer.py
    :literal:
    :start-after: #end_pymotw_header

The output does not look exactly like the exported data used in the reader
example:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'csv_writer.py testout.csv'))
.. }}}

::

	$ python csv_writer.py testout.csv
	
	Title 1,Title 2,Title 3
	1,a,08/01/07
	2,b,08/02/07
	3,c,08/03/07
	4,d,08/04/07
	5,e,08/05/07
	6,f,08/06/07
	7,g,08/07/07
	8,h,08/08/07
	9,i,08/09/07
	10,j,08/10/07
	

.. {{{end}}}

The default quoting behavior is different for the writer, so the string column
is not quoted. That is easy to change by adding a quoting argument to quote
non-numeric values:

::

    writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)

And now the strings are quoted:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'csv_writer_quoted.py testout_quoted.csv'))
.. }}}

::

	$ python csv_writer_quoted.py testout_quoted.csv
	
	"Title 1","Title 2","Title 3"
	1,"a","08/01/07"
	2,"b","08/02/07"
	3,"c","08/03/07"
	4,"d","08/04/07"
	5,"e","08/05/07"
	6,"f","08/06/07"
	7,"g","08/07/07"
	8,"h","08/08/07"
	9,"i","08/09/07"
	10,"j","08/10/07"
	

.. {{{end}}}

.. _csv-quoting:

Quoting
-------

There are four different quoting options, defined as constants in the csv
module.

QUOTE_ALL
  Quote everything, regardless of type.

QUOTE_MINIMAL
  Quote fields with special characters (anything that would confuse a parser
  configured with the same dialect and options). This is the default

QUOTE_NONNUMERIC
  Quote all fields that are not integers or floats. When used with the reader,
  input fields that are not quoted are converted to floats.

QUOTE_NONE
  Do not quote anything on output. When used with the reader, quote characters
  are included in the field values (normally, they are treated as delimiters and
  stripped).


Dialects
========

There is no well-defined standard for comma-separated value files, so
the parser needs to be flexible.  This flexibility means there are
many parameters to control how :mod:`csv` parses or writes data.
Rather than passing each of these parameters to the reader and writer
separately, they are grouped together conveniently into a *dialect*
object. 

Dialect classes can be registered by name, so that callers of the csv
module do not need to know the parameter settings in advance.  The
complete list of registered dialects can be retrieved with
:func:`list_dialects`.

.. include:: csv_list_dialects.py
   :literal:
   :start-after: #end_pymotw_header

The standard library includes two dialects: ``excel``, and
``excel-tabs``. The ``excel`` dialect is for working with data in the
default export format for Microsoft Excel, and also works with
OpenOffice or NeoOffice.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'csv_list_dialects.py'))
.. }}}

::

	$ python csv_list_dialects.py
	
	['excel-tab', 'excel']

.. {{{end}}}

Creating a Dialect
------------------

Suppose instead of using commas to delimit fields, the input file uses
``|``, like this:

.. include:: testdata.pipes
    :literal:

A new dialect can be registered using the appropriate delimiter:

.. include:: csv_dialect.py
    :literal:
    :start-after: #end_pymotw_header

and the file can be read just as with the comma-delimited file:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'csv_dialect.py'))
.. }}}

::

	$ python csv_dialect.py
	
	['Title 1', 'Title 2', 'Title 3']
	['1', 'first line\nsecond line', '08/18/07']

.. {{{end}}}

Dialect Parameters
------------------

A dialect specifies all of the tokens used when parsing or writing a
data file.  Every aspect of the file format can be specified, from the
way columns are delimited to the character used to escape a token.

================  ======================  =======
Attribute         Default                 Meaning
================  ======================  =======
delimiter         ``,``                   Field separator (one character)
doublequote       True                    Flag controlling whether quotechar instances are doubled
escapechar        None                    Character used to indicate an escape sequence
lineterminator    ``\r\n``                String used by writer to terminate a line
quotechar         ``"``                   String to surround fields containing special values (one character)
quoting           :const:`QUOTE_MINIMAL`  Controls quoting behavior described above
skipinitialspace  False                   Ignore whitespace after the field delimiter
================  ======================  =======

.. include:: csv_dialect_variations.py
   :literal:
   :start-after: #end_pymotw_header

This program shows how the same data appears in several different dialects.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'csv_dialect_variations.py'))
.. }}}

::

	$ python csv_dialect_variations.py
	
	
	Dialect: "escaped"
	
	  delimiter   = ','       skipinitialspace = 0
	  doublequote = 0         quoting          = QUOTE_NONE
	  quotechar   = '"'       lineterminator   = '\r\n'
	  escapechar  = '\\'  
	
	col1,0,10/00/2010,Contains special chars: \" ' \, to be parsed
	col1,1,10/01/2010,Contains special chars: \" ' \, to be parsed
	col1,2,10/02/2010,Contains special chars: \" ' \, to be parsed
	
	
	Dialect: "excel"
	
	  delimiter   = ','       skipinitialspace = 0
	  doublequote = 1         quoting          = QUOTE_MINIMAL
	  quotechar   = '"'       lineterminator   = '\r\n'
	  escapechar  = None  
	
	col1,0,10/00/2010,"Contains special chars: "" ' , to be parsed"
	col1,1,10/01/2010,"Contains special chars: "" ' , to be parsed"
	col1,2,10/02/2010,"Contains special chars: "" ' , to be parsed"
	
	
	Dialect: "excel-tab"
	
	  delimiter   = '\t'      skipinitialspace = 0
	  doublequote = 1         quoting          = QUOTE_MINIMAL
	  quotechar   = '"'       lineterminator   = '\r\n'
	  escapechar  = None  
	
	col1	0	10/00/2010	"Contains special chars: "" ' 	 to be parsed"
	col1	1	10/01/2010	"Contains special chars: "" ' 	 to be parsed"
	col1	2	10/02/2010	"Contains special chars: "" ' 	 to be parsed"
	
	
	Dialect: "singlequote"
	
	  delimiter   = ','       skipinitialspace = 0
	  doublequote = 1         quoting          = QUOTE_ALL
	  quotechar   = "'"       lineterminator   = '\r\n'
	  escapechar  = None  
	
	'col1','0','10/00/2010','Contains special chars: " '' , to be parsed'
	'col1','1','10/01/2010','Contains special chars: " '' , to be parsed'
	'col1','2','10/02/2010','Contains special chars: " '' , to be parsed'
	

.. {{{end}}}

Automatically Detecting Dialects
--------------------------------

The best way to configure a dialect for parsing an input file is to
know the right settings in advance.  For data where the dialect
parameters are unknown, the :class:`Sniffer` class can be used to make
an educated guess.  The :func:`sniff` method takes a sample of the
input data and an optional argument giving the possible delimiter
characters.

.. include:: csv_dialect_sniffer.py
   :literal:
   :start-after: #end_pymotw_header

:func:`sniff` returns a :class:`Dialect` instance with the settings to
be used for parsing the data.  The results are not always perfect, as
demonstrated by the "escaped" dialect in the example.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'csv_dialect_sniffer.py'))
.. }}}

::

	$ python csv_dialect_sniffer.py
	
	
	Dialect: "escaped"
	
	['col1', '0', '10/00/2010', 'Contains special chars: \\" \' \\', ' to be parsed']
	['col1', '1', '10/01/2010', 'Contains special chars: \\" \' \\', ' to be parsed']
	['col1', '2', '10/02/2010', 'Contains special chars: \\" \' \\', ' to be parsed']
	
	Dialect: "excel"
	
	['col1', '0', '10/00/2010', 'Contains special chars: " \' , to be parsed']
	['col1', '1', '10/01/2010', 'Contains special chars: " \' , to be parsed']
	['col1', '2', '10/02/2010', 'Contains special chars: " \' , to be parsed']
	
	Dialect: "excel-tab"
	
	['col1', '0', '10/00/2010', 'Contains special chars: " \' \t to be parsed']
	['col1', '1', '10/01/2010', 'Contains special chars: " \' \t to be parsed']
	['col1', '2', '10/02/2010', 'Contains special chars: " \' \t to be parsed']
	
	Dialect: "singlequote"
	
	['col1', '0', '10/00/2010', 'Contains special chars: " \' , to be parsed']
	['col1', '1', '10/01/2010', 'Contains special chars: " \' , to be parsed']
	['col1', '2', '10/02/2010', 'Contains special chars: " \' , to be parsed']

.. {{{end}}}


Using Field Names
=================

In addition to working with sequences of data, the :mod:`csv` module
includes classes for working with rows as dictionaries so that the
fields can be named. The :class:`DictReader` and :class:`DictWriter`
classes translate rows to dictionaries instead of lists. Keys for the
dictionary can be passed in, or inferred from the first row in the
input (when the row contains headers).

.. include:: csv_dictreader.py
    :literal:
    :start-after: #end_pymotw_header

The dictionary-based reader and writer are implemented as wrappers
around the sequence-based classes, and use the same methods and
arguments. The only difference in the reader API is that rows are
returned as dictionaries instead of lists or tuples.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'csv_dictreader.py testdata.csv'))
.. }}}

::

	$ python csv_dictreader.py testdata.csv
	
	{'Title 1': '1', 'Title 3': '08/18/07', 'Title 2': 'a'}
	{'Title 1': '2', 'Title 3': '08/19/07', 'Title 2': 'b'}
	{'Title 1': '3', 'Title 3': '08/20/07', 'Title 2': 'c'}
	{'Title 1': '4', 'Title 3': '08/21/07', 'Title 2': 'd'}
	{'Title 1': '5', 'Title 3': '08/22/07', 'Title 2': 'e'}
	{'Title 1': '6', 'Title 3': '08/23/07', 'Title 2': 'f'}
	{'Title 1': '7', 'Title 3': '08/24/07', 'Title 2': 'g'}
	{'Title 1': '8', 'Title 3': '08/25/07', 'Title 2': 'h'}
	{'Title 1': '9', 'Title 3': '08/26/07', 'Title 2': 'i'}

.. {{{end}}}

The :class:`DictWriter` must be given a list of field names so it
knows how to order the columns in the output.

.. include:: csv_dictwriter.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'csv_dictwriter.py testout.csv'))
.. }}}

::

	$ python csv_dictwriter.py testout.csv
	
	Title 1,Title 2,Title 3
	1,a,08/01/07
	2,b,08/02/07
	3,c,08/03/07
	4,d,08/04/07
	5,e,08/05/07
	6,f,08/06/07
	7,g,08/07/07
	8,h,08/08/07
	9,i,08/09/07
	10,j,08/10/07
	

.. {{{end}}}

.. seealso::

    `csv <http://docs.python.org/2.7/library/csv.html>`_
        The standard library documentation for this module.

    :pep:`305`
        CSV File API

.. _NeoOffice: http://www.neooffice.org/
