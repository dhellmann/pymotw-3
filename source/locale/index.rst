======================================
 locale --- Cultural Localization API
======================================

.. module:: locale
    :synopsis: POSIX cultural localization API

:Purpose: Format and parse values that depend on location or language.

The ``locale`` module is part of Python's internationalization and
localization support library. It provides a standard way to handle
operations that may depend on the language or location of a user. For
example, it handles formatting numbers as currency, comparing strings
for sorting, and working with dates. It does not cover translation
(see the :mod:`gettext` module) or Unicode encoding (see the
:mod:`codecs` module).

.. note::

  Changing the locale can have application-wide ramifications, so the
  recommended practice is to avoid changing the value in a library and
  to let the application set it one time. In the examples in this
  section, the locale is changed several times within a short program
  to highlight the differences in the settings of various locales. It
  is far more likely that an application will set the locale once as
  it starts up or when a web request is received and not change it.

This section covers some of the high-level functions in the
``locale`` module. There are others which are lower level
(``format_string()``) or which relate to managing the locale for an
application (``resetlocale()``).

Probing the Current Locale
==========================

The most common way to let the user change the locale settings for an
application is through an environment variable (``LC_ALL``,
``LC_CTYPE``, ``LANG``, or ``LANGUAGE``, depending on the
platform). The application then calls ``setlocale()`` without a
hard-coded value, and the environment value is used.

.. literalinclude:: locale_env.py
   :caption:
   :start-after: #end_pymotw_header

The ``localeconv()`` method returns a dictionary containing the
locale's conventions.  The full list of value names and definitions is
covered in the standard library documentation.

A Mac running OS X 10.11.6 with all of the variables unset produces
this output:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'LANG= LC_CTYPE= PYTHONCOERCECLOCALE=0 python3 locale_env.py', interpreter=None))
.. }}}

.. code-block:: none

	$ LANG= LC_CTYPE= PYTHONCOERCECLOCALE=0 python3 locale_env.py
	
	Environment settings:
	  LC_ALL = 
	  LC_CTYPE = 
	  LANG = 
	  LANGUAGE = 
	
	Locale from environment: (None, None)
	
	Numeric formatting:
	
	  Decimal point      : "."
	  Grouping positions : []
	  Thousands separator: ""
	
	Monetary formatting:
	
	  International currency symbol   : "''"
	  Local currency symbol           : ''
	  Symbol precedes positive value  : 127
	  Symbol precedes negative value  : 127
	  Decimal point                   : ""
	  Digits in fractional values     : 127
	  Digits in fractional values,
	                   international  : 127
	  Grouping positions              : []
	  Thousands separator             : ""
	  Positive sign                   : ""
	  Positive sign position          : Unspecified
	  Negative sign                   : ""
	  Negative sign position          : Unspecified
	
	

.. {{{end}}}

Running the same script with the ``LANG`` variable set shows how
the locale and default encoding change.

The United States (``en_US``):

.. {{{cog
.. cog.out(run_script(cog.inFile, 'LANG=en_US LC_CTYPE=en_US LC_ALL=en_US python3 locale_env.py', interpreter=None))
.. }}}

.. code-block:: none

	$ LANG=en_US LC_CTYPE=en_US LC_ALL=en_US python3 locale_env.py
	
	Environment settings:
	  LC_ALL = en_US
	  LC_CTYPE = en_US
	  LANG = en_US
	  LANGUAGE = 
	
	Locale from environment: ('en_US', 'ISO8859-1')
	
	Numeric formatting:
	
	  Decimal point      : "."
	  Grouping positions : [3, 3, 0]
	  Thousands separator: ","
	
	Monetary formatting:
	
	  International currency symbol   : "'USD '"
	  Local currency symbol           : '$'
	  Symbol precedes positive value  : 1
	  Symbol precedes negative value  : 1
	  Decimal point                   : "."
	  Digits in fractional values     : 2
	  Digits in fractional values,
	                   international  : 2
	  Grouping positions              : [3, 3, 0]
	  Thousands separator             : ","
	  Positive sign                   : ""
	  Positive sign position          : Before value and symbol
	  Negative sign                   : "-"
	  Negative sign position          : Before value and symbol
	
	

.. {{{end}}}

France (``fr_FR``):

.. {{{cog
.. cog.out(run_script(cog.inFile, 'LANG=fr_FR LC_CTYPE=fr_FR LC_ALL=fr_FR python3 locale_env.py', interpreter=None))
.. }}}

.. code-block:: none

	$ LANG=fr_FR LC_CTYPE=fr_FR LC_ALL=fr_FR python3 locale_env.py
	
	Environment settings:
	  LC_ALL = fr_FR
	  LC_CTYPE = fr_FR
	  LANG = fr_FR
	  LANGUAGE = 
	
	Locale from environment: ('fr_FR', 'ISO8859-1')
	
	Numeric formatting:
	
	  Decimal point      : ","
	  Grouping positions : [127]
	  Thousands separator: ""
	
	Monetary formatting:
	
	  International currency symbol   : "'EUR '"
	  Local currency symbol           : 'Eu'
	  Symbol precedes positive value  : 0
	  Symbol precedes negative value  : 0
	  Decimal point                   : ","
	  Digits in fractional values     : 2
	  Digits in fractional values,
	                   international  : 2
	  Grouping positions              : [3, 3, 0]
	  Thousands separator             : " "
	  Positive sign                   : ""
	  Positive sign position          : Before value and symbol
	  Negative sign                   : "-"
	  Negative sign position          : After value and symbol
	
	

.. {{{end}}}


Spain (``es_ES``):


.. {{{cog
.. cog.out(run_script(cog.inFile, 'LANG=es_ES LC_CTYPE=es_ES LC_ALL=es_ES python3 locale_env.py', interpreter=None))
.. }}}

.. code-block:: none

	$ LANG=es_ES LC_CTYPE=es_ES LC_ALL=es_ES python3 locale_env.py
	
	Environment settings:
	  LC_ALL = es_ES
	  LC_CTYPE = es_ES
	  LANG = es_ES
	  LANGUAGE = 
	
	Locale from environment: ('es_ES', 'ISO8859-1')
	
	Numeric formatting:
	
	  Decimal point      : ","
	  Grouping positions : [127]
	  Thousands separator: ""
	
	Monetary formatting:
	
	  International currency symbol   : "'EUR '"
	  Local currency symbol           : 'Eu'
	  Symbol precedes positive value  : 0
	  Symbol precedes negative value  : 0
	  Decimal point                   : ","
	  Digits in fractional values     : 2
	  Digits in fractional values,
	                   international  : 2
	  Grouping positions              : [3, 3, 0]
	  Thousands separator             : "."
	  Positive sign                   : ""
	  Positive sign position          : Before value and symbol
	  Negative sign                   : "-"
	  Negative sign position          : Before value and symbol
	
	

.. {{{end}}}

Portugal (``pt_PT``):


.. {{{cog
.. cog.out(run_script(cog.inFile, 'LANG=pt_PT LC_CTYPE=pt_PT LC_ALL=pt_PT python3 locale_env.py', interpreter=None))
.. }}}

.. code-block:: none

	$ LANG=pt_PT LC_CTYPE=pt_PT LC_ALL=pt_PT python3 locale_env.py
	
	Environment settings:
	  LC_ALL = pt_PT
	  LC_CTYPE = pt_PT
	  LANG = pt_PT
	  LANGUAGE = 
	
	Locale from environment: ('pt_PT', 'ISO8859-1')
	
	Numeric formatting:
	
	  Decimal point      : ","
	  Grouping positions : []
	  Thousands separator: " "
	
	Monetary formatting:
	
	  International currency symbol   : "'EUR '"
	  Local currency symbol           : 'Eu'
	  Symbol precedes positive value  : 0
	  Symbol precedes negative value  : 0
	  Decimal point                   : "."
	  Digits in fractional values     : 2
	  Digits in fractional values,
	                   international  : 2
	  Grouping positions              : [3, 3, 0]
	  Thousands separator             : "."
	  Positive sign                   : ""
	  Positive sign position          : Before value and symbol
	  Negative sign                   : "-"
	  Negative sign position          : Before value and symbol
	
	

.. {{{end}}}


Poland (``pl_PL``):


.. {{{cog
.. cog.out(run_script(cog.inFile, 'LANG=pl_PL LC_CTYPE=pl_PL LC_ALL=pl_PL python3 locale_env.py', interpreter=None))
.. }}}

.. code-block:: none

	$ LANG=pl_PL LC_CTYPE=pl_PL LC_ALL=pl_PL python3 locale_env.py
	
	Environment settings:
	  LC_ALL = pl_PL
	  LC_CTYPE = pl_PL
	  LANG = pl_PL
	  LANGUAGE = 
	
	Locale from environment: ('pl_PL', 'ISO8859-2')
	
	Numeric formatting:
	
	  Decimal point      : ","
	  Grouping positions : [3, 3, 0]
	  Thousands separator: " "
	
	Monetary formatting:
	
	  International currency symbol   : "'PLN '"
	  Local currency symbol           : 'zł'
	  Symbol precedes positive value  : 1
	  Symbol precedes negative value  : 1
	  Decimal point                   : ","
	  Digits in fractional values     : 2
	  Digits in fractional values,
	                   international  : 2
	  Grouping positions              : [3, 3, 0]
	  Thousands separator             : " "
	  Positive sign                   : ""
	  Positive sign position          : After value
	  Negative sign                   : "-"
	  Negative sign position          : After value
	
	

.. {{{end}}}


Currency
========

The earlier example output shows that changing the locale updates the
currency symbol setting and the character to separate whole numbers
from decimal fractions.  This example loops through several different
locales to print a positive and negative currency value formatted for
each locale.

.. literalinclude:: locale_currency.py
   :caption:
   :start-after: #end_pymotw_header

The output is this small table:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'locale_currency.py'))
.. }}}

.. code-block:: none

	$ python3 locale_currency.py
	
	       USA:   $1234.56   -$1234.56
	    France: 1234,56 Eu  1234,56 Eu-
	     Spain: 1234,56 Eu  -1234,56 Eu
	  Portugal: 1234.56 Eu  -1234.56 Eu
	    Poland: zł 1234,56  zł 1234,56-

.. {{{end}}}

Formatting Numbers
==================

Numbers not related to currency are also formatted differently
depending on the locale.  In particular, the ``grouping`` character
used to separate large numbers into readable chunks changes.

.. literalinclude:: locale_grouping.py
   :caption:
   :start-after: #end_pymotw_header

To format numbers without the currency symbol, use ``format()``
instead of ``currency()``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'locale_grouping.py'))
.. }}}

.. code-block:: none

	$ python3 locale_grouping.py
	
	    Locale    Integer           Float
	       USA    123,456      123,456.78
	    France     123456       123456,78
	     Spain     123456       123456,78
	  Portugal     123456       123456,78
	    Poland    123 456      123 456,78

.. {{{end}}}

To convert locale-formatted numbers to a normalized locale-agnostic
format, use ``delocalize()``.

.. literalinclude:: locale_delocalize.py
   :caption:
   :start-after: #end_pymotw_header

Grouping punctuation is removed and the decimal separator is converted
to always be a ``.``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'locale_delocalize.py'))
.. }}}

.. code-block:: none

	$ python3 locale_delocalize.py
	
	       USA: 123,456.78   123456.78
	    France:  123456,78   123456.78
	     Spain:  123456,78   123456.78
	  Portugal:  123456,78   123456.78
	    Poland: 123 456,78   123456.78

.. {{{end}}}



Parsing Numbers
===============

Besides generating output in different formats, the ``locale``
module helps with parsing input. It includes ``atoi()`` and
``atof()`` functions for converting the strings to integer and
floating point values based on the locale's numerical formatting
conventions.

.. literalinclude:: locale_atof.py
   :caption:
   :start-after: #end_pymotw_header

The grouping and decimal separator values of the locale are recognized
by the parser.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'locale_atof.py'))
.. }}}

.. code-block:: none

	$ python3 locale_atof.py
	
	       USA:  1,234.56 => 1234.560000
	    France:   1234,56 => 1234.560000
	     Spain:   1234,56 => 1234.560000
	  Portugal:   1234.56 => 1234.560000
	    Poland:  1 234,56 => 1234.560000

.. {{{end}}}


Dates and Times
===============

Another important aspect of localization is date and time formatting.

.. literalinclude:: locale_date.py
   :caption:
   :start-after: #end_pymotw_header

This example uses the date formatting string for the locale to print
the current date and time.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'locale_date.py'))
.. }}}

.. code-block:: none

	$ python3 locale_date.py
	
	       USA: Sun Mar 18 16:20:59 2018
	    France: Dim 18 mar 16:20:59 2018
	     Spain: dom 18 mar 16:20:59 2018
	  Portugal: Dom 18 Mar 16:20:59 2018
	    Poland: ndz 18 mar 16:20:59 2018

.. {{{end}}}

.. seealso::

   * :pydoc:`locale`

   * :ref:`Python 2 to 3 porting notes for locale <porting-locale>`

   * :mod:`gettext` -- Message catalogs for translations.
