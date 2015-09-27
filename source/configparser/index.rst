===============================================
 configparser -- Work with Configuration Files
===============================================

.. module:: configparser
    :synopsis: Read/write configuration files similar to Windows INI files

:Purpose: Read/write configuration files similar to Windows INI files

Use the :mod:`configparser` module to manage user-editable
configuration files for an application. The contents of the
configuration files can be organized into groups and several option
value types are supported, including integers, floating point values,
and booleans.  Option values can be combined using Python formatting
strings, to build longer values such as URLs from shorter values like
host names and port numbers.

Configuration File Format
=========================

The file format used by :mod:`configparser` is similar to the format
used by older versions of Microsoft Windows.  It consists of one or
more named *sections*, each of which can contain individual *options*
with names and values.

Config file sections are identified by looking for lines starting with
``[`` and ending with ``]``.  The value between the square brackets is
the section name, and can contain any characters except square
brackets.

Options are listed one per line within a section.  The line starts
with the name of the option, which is separated from the value by a
colon (``:``) or equal sign (``=``).  Whitespace around the separator
is ignored when the file is parsed.

This sample configuration file has a section named ``bug_tracker`` with
three options, ``url``, ``username``, and ``password``.

.. literalinclude:: simple.ini

Reading Configuration Files
===========================

The most common use for a configuration file is to have a user or
system administrator edit the file with a regular text editor to set
application behavior defaults, and then have the application read the
file, parse it, and act based on its contents.  Use the :func:`read`
method of :mod:`ConfigParser` to read the configuration file.

.. include:: configparser_read.py
   :literal:
   :start-after: #end_pymotw_header

This program reads the ``simple.ini`` file from the previous section
and prints the value of the :data:`url` option from the
:data:`bug_tracker` section.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'configparser_read.py'))
.. }}}

::

	$ python3 configparser_read.py
	
	http://localhost:8080/bugs/

.. {{{end}}}

The :func:`read` method also accepts a list of filenames.  Each name
in turn is scanned, and if the file exists it is opened and read.

.. include:: configparser_read_many.py
   :literal:
   :start-after: #end_pymotw_header

:func:`read` returns a list containing the names of the files
successfully loaded, so the program can discover which configuration
files are missing and decide whether to ignore them.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'configparser_read_many.py', line_break_mode='fill'))
.. }}}

::

	$ python3 configparser_read_many.py
	
	Found config files: ['multisection.ini', 'simple.ini']
	Missing files     : ['also-does-not-exist.ini',
	'does_not_exist.ini']

.. {{{end}}}

Unicode Configuration Data
--------------------------

Configuration files containing Unicode data should be read using the
proper encoding value.  Changing the password value of the original
input to contain Unicode characters and saving the results in UTF-8
encoding gives:

.. literalinclude:: unicode.ini

The file is opened with the appropriate decoder, converting the UTF-8
data to native Unicode strings.

.. include:: configparser_unicode.py
   :literal:
   :start-after: #end_pymotw_header

The value returned by :func:`get` is a Unicode string, so in order to
print it safely it must be re-encoded as UTF-8.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'configparser_unicode.py'))
.. }}}

::

	$ python3 configparser_unicode.py
	
	Password: b'\xc3\x9f\xc3\xa9\xc3\xa7\xc2\xae\xc3\xa9\xe2\x80\xa0
	'
	Type    : <class 'str'>
	repr()  : 'ßéç®é†'

.. {{{end}}}

Accessing Configuration Settings
================================

:class:`ConfigParser` includes methods for examining the structure
of the parsed configuration, including listing the sections and
options, and getting their values.  This configuration file includes
two sections for separate web services:

.. literalinclude:: multisection.ini

And this sample program exercises some of the methods for looking at
the configuration data, including :func:`sections`, :func:`options`,
and :func:`items`.

.. include:: configparser_structure.py
   :literal:
   :start-after: #end_pymotw_header

Both :func:`sections` and :func:`options` return lists of strings,
while :func:`items` returns a list of tuples containing the name-value
pairs.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'configparser_structure.py'))
.. }}}

::

	$ python3 configparser_structure.py
	
	Section: bug_tracker
	  Options: ['url', 'username', 'password']
	  url = http://localhost:8080/bugs/
	  username = dhellmann
	  password = SECRET
	
	Section: wiki
	  Options: ['url', 'username', 'password']
	  url = http://localhost:8080/wiki/
	  username = dhellmann
	  password = SECRET
	

.. {{{end}}}

Testing Whether Values Are Present
----------------------------------

To test if a section exists, use :func:`has_section`, passing the
section name.

.. include:: configparser_has_section.py
   :literal:
   :start-after: #end_pymotw_header

Testing if a section exists before calling :func:`get` avoids
exceptions for missing data.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'configparser_has_section.py'))
.. }}}

::

	$ python3 configparser_has_section.py
	
	wiki        : True
	bug_tracker : True
	dvcs        : False

.. {{{end}}}

Use :func:`has_option` to test if an option exists within a section.

.. include:: configparser_has_option.py
   :literal:
   :start-after: #end_pymotw_header

If the section does not exist, :func:`has_option` returns ``False``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'configparser_has_option.py'))
.. }}}

::

	$ python3 configparser_has_option.py
	
	wiki section exists: True
	wiki.username      : True
	wiki.password      : True
	wiki.url           : True
	wiki.description   : False
	
	none section exists: False
	none.username      : False
	none.password      : False
	none.url           : False
	none.description   : False
	

.. {{{end}}}

Value Types
-----------

All section and option names are treated as strings, but option values
can be strings, integers, floating point numbers, or booleans.  There
are a range of possible boolean values that are converted true or
false.  This example file includes one of each:

.. literalinclude:: types.ini

:class:`ConfigParser` does not make any attempt to understand the
option type.  The application is expected to use the correct method to
fetch the value as the desired type.  :func:`get` always returns a
string.  Use :func:`getint` for integers, :func:`getfloat` for
floating point numbers, and :func:`getboolean` for boolean values.

.. include:: configparser_value_types.py
   :literal:
   :start-after: #end_pymotw_header

Running this program with the example input produces:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'configparser_value_types.py'))
.. }}}

::

	$ python3 configparser_value_types.py
	
	Integers:
	  positive     : '1'     -> 1
	  negative     : '-5'    -> -5
	
	Floats:
	  positive     : '0.2'   -> 0.20
	  negative     : '-3.14' -> -3.14
	
	Booleans:
	  number_true  : '1'     -> True
	  number_false : '0'     -> False
	  yn_true      : 'yes'   -> True
	  yn_false     : 'no'    -> False
	  tf_true      : 'true'  -> True
	  tf_false     : 'false' -> False
	  onoff_true   : 'on'    -> True
	  onoff_false  : 'false' -> False

.. {{{end}}}


Options as Flags
----------------

Usually the parser requires an explicit value for each option, but
with the :class:`ConfigParser` parameter *allow_no_value* set to
``True`` an option can appear by itself on a line in the input file,
and be used as a flag.

.. include:: configparser_allow_no_value.py
   :literal:
   :start-after: #end_pymotw_header

When an option has no explicit value, :func:`has_option` reports that
the option exists and :func:`get` returns ``None``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'configparser_allow_no_value.py'))
.. }}}

::

	$ python3 configparser_allow_no_value.py
	
	Could not parse: Source contains parsing errors: 'allow_no_value
	.ini'
		[line  2]: 'turn_feature_on\n'
	
	Trying again with allow_no_value=True
	
	 turn_feature_on
	  has_option: True
	         get: None
	
	 turn_other_feature_on
	  has_option: False

.. {{{end}}}

Modifying Settings
==================

While :class:`ConfigParser` is primarily intended to be configured
by reading settings from files, settings can also be populated by
calling :func:`add_section` to create a new section, and :func:`set`
to add or change an option.

.. include:: configparser_populate.py
   :literal:
   :start-after: #end_pymotw_header

All options must be set as strings, even if they will be retrieved as
integer, float, or boolean values.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'configparser_populate.py'))
.. }}}

::

	$ python3 configparser_populate.py
	
	bug_tracker
	  url = 'http://localhost:8080/bugs'
	  username = 'dhellmann'
	  password = 'secret'

.. {{{end}}}

Sections and options can be removed from a :class:`ConfigParser`
with :func:`remove_section` and :func:`remove_option`.

.. include:: configparser_remove.py
   :literal:
   :start-after: #end_pymotw_header

Removing a section deletes any options it contains.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'configparser_remove.py'))
.. }}}

::

	$ python3 configparser_remove.py
	
	Read values:
	
	bug_tracker
	  url = 'http://localhost:8080/bugs/'
	  username = 'dhellmann'
	  password = 'SECRET'
	wiki
	  url = 'http://localhost:8080/wiki/'
	  username = 'dhellmann'
	  password = 'SECRET'
	
	Modified values:
	
	bug_tracker
	  url = 'http://localhost:8080/bugs/'
	  username = 'dhellmann'

.. {{{end}}}


Saving Configuration Files
==========================

Once a :class:`ConfigParser` is populated with desired data, it
can be saved to a file by calling the :func:`write` method.  This
makes it possible to provide a user interface for editing the
configuration settings, without having to write any code to manage the
file.

.. include:: configparser_write.py
   :literal:
   :start-after: #end_pymotw_header

The :func:`write` method takes a file-like object as argument.  It
writes the data out in the INI format so it can be parsed again by
:class:`ConfigParser`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'configparser_write.py'))
.. }}}

::

	$ python3 configparser_write.py
	
	[bug_tracker]
	url = http://localhost:8080/bugs
	username = dhellmann
	password = secret
	

.. {{{end}}}

.. warning::

   Comments in the original configuration file are not preserved when
   reading, modifying, and re-writing a configuration file.



Option Search Path
==================

:class:`ConfigParser` uses a multi-step search process when
looking for an option.

Before starting the option search, the section name is tested.  If the
section does not exist, and the name is not the special value
``DEFAULT``, then :class:`NoSectionError` is raised.

1. If the option name appears in the *vars* dictionary passed to
   :func:`get`, the value from *vars* is returned.
2. If the option name appears in the specified section, the value from
   that section is returned.
3. If the option name appears in the ``DEFAULT`` section, that value
   is returned.
4. If the option name appears in the *defaults* dictionary passed to
   the constructor, that value is returned.

If the name is not found in any of those locations,
:class:`NoOptionError` is raised.

The search path behavior can be demonstrated using this configuration
file.

.. literalinclude:: with-defaults.ini

This test program includes default settings for options not specified
in the configuration file, and overrides some values that are defined
in the file.

.. include:: configparser_defaults.py
   :literal:
   :start-after: #end_pymotw_header

The output shows the origin for the value of each option, and
illustrates the way defaults from different sources override existing
values.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'configparser_defaults.py'))
.. }}}

::

	$ python3 configparser_defaults.py
	
	Defaults before loading file:
	  from-default    = 'value from defaults passed to init'
	  from-section    = 'value from defaults passed to init'
	  init-only       = 'value from defaults passed to init'
	  init-and-file   = 'value from defaults passed to init'
	  from-vars       = 'value from defaults passed to init'
	
	Defaults after loading file:
	  from-default    = 'value from defaults passed to init'
	  from-section    = 'value from DEFAULT section'
	  file-only       = 'value from DEFAULT section'
	  init-only       = 'value from defaults passed to init'
	  init-and-file   = 'value from DEFAULT section'
	  from-vars       = 'value from DEFAULT section'
	
	Option lookup:
	  from-default    = 'value from defaults passed to init'
	  from-section    = 'value from section in file'
	  section-only    = 'value from section in file'
	  file-only       = 'value from DEFAULT section'
	  init-only       = 'value from defaults passed to init'
	  init-and-file   = 'value from DEFAULT section'
	  from-vars       = 'value from vars'
	
	Error cases:
	No option 'no-option' in section: 'sect'
	No section: 'no-sect'

.. {{{end}}}


Combining Values with Interpolation
===================================

:class:`ConfigParser` provides a feature called *interpolation*
that can be used to combine values together.  Values containing
standard Python format strings trigger the interpolation feature when
they are retrieved with :func:`get`.  Options named within the value
being fetched are replaced with their values in turn, until no more
substitution is necessary.

The URL examples from earlier in this section can be rewritten to use
interpolation to make it easier to change only part of the value.  For
example, this configuration file separates the protocol, hostname, and
port from the URL as separate options.

.. literalinclude:: interpolation.ini

Interpolation is performed by default each time :func:`get` is called.
Pass a true value in the :data:`raw` argument to retrieve the original
value, without interpolation.

.. include:: configparser_interpolation.py
   :literal:
   :start-after: #end_pymotw_header

Because the value is computed by :func:`get`, changing one of the
settings being used by the ``url`` value changes the return value.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'configparser_interpolation.py'))
.. }}}

::

	$ python3 configparser_interpolation.py
	
	Original value       : http://localhost:8080/bugs/
	Altered port value   : http://localhost:9090/bugs/
	Without interpolation: %(protocol)s://%(server)s:%(port)s/bugs/

.. {{{end}}}

Using Defaults
--------------

Values for interpolation do not need to appear in the same section as
the original option.  Defaults can be mixed with override values.

.. literalinclude:: interpolation_defaults.ini

With this configuration, the value for ``url`` comes from the
``DEFAULT`` section, and the substitution starts by looking in
``bug_tracker`` and falling back to ``DEFAULT`` for pieces not found.

.. include:: configparser_interpolation_defaults.py
   :literal:
   :start-after: #end_pymotw_header

The ``hostname`` and ``port`` values come from the ``bug_tracker``
section, but the ``protocol`` comes from ``DEFAULT``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'configparser_interpolation_defaults.py'))
.. }}}

::

	$ python3 configparser_interpolation_defaults.py
	
	URL: http://localhost:8080/bugs/

.. {{{end}}}

Substitution Errors
-------------------

Substitution stops after :attr:`MAX_INTERPOLATION_DEPTH` steps to
avoid problems due to recursive references.

.. include:: configparser_interpolation_recursion.py
   :literal:
   :start-after: #end_pymotw_header

An :class:`InterpolationDepthError` exception is raised if there are
too many substitution steps.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'configparser_interpolation_recursion.py'))
.. }}}

::

	$ python3 configparser_interpolation_recursion.py
	
	ERROR: Value interpolation too deeply recursive:
		section: [sect]
		option : opt
		rawval : %(opt)s
	

.. {{{end}}}

Missing values result in an :class:`InterpolationMissingOptionError`
exception.

.. include:: configparser_interpolation_error.py
   :literal:
   :start-after: #end_pymotw_header

Since no ``server`` value is defined, the ``url`` cannot be
constructed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'configparser_interpolation_error.py'))
.. }}}

::

	$ python3 configparser_interpolation_error.py
	
	ERROR: Bad value substitution:
		section: [bug_tracker]
		option : url
		key    : server
		rawval : :%(port)s/bugs
	

.. {{{end}}}

Escaping Special Characters
===========================

Since ``%`` starts the interpolation instructions, a literal ``%`` in
a value must be escaped as ``%%``.

.. include:: escape.ini
   :literal:

Reading the value does not require any special consideration.

.. include:: configparser_escape.py
   :literal:
   :start-after: #end_pymotw_header

When the value is read, the ``%%`` is converted to ``%``
automatically.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'configparser_escape.py'))
.. }}}

::

	$ python3 configparser_escape.py
	
	a literal % must be escaped

.. {{{end}}}



.. seealso::

    * :pydoc:`configparser`

    * `ConfigObj
      <http://configobj.readthedocs.org/en/latest/configobj.html>`__
      -- An advanced configuration file parser with support for
      features like content validation.

    * :ref:`Porting notes for configparser <porting-configparser>`
