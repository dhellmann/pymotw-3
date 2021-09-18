===============================================
plistlib -- Manipulate OS X property list files
===============================================

.. module:: plistlib
    :synopsis: Manipulate OS X property list files

:Purpose: Read and write OS X property list files
:Available In: 2.6

:mod:`plistlib` provides an interface for working with property list
files used under OS X.  plist files are typically XML, sometimes
compressed.  They are used by the operating system and applications to
store preferences or other configuration settings.  The contents are
usually structured as a dictionary containing key value pairs of basic
built-in types (unicode strings, integers, dates, etc.).  Values can
also be nested data structures such as other dictionaries or lists.
Binary data, or strings with control characters, can be encoded using
the ``data`` type.

Reading plist Files
===================

OS X applications such as iCal use plist files to store meta-data
about objects they manage.  For example, iCal stores the definitions
of all of your calendars as a series of plist files in the Library
directory.  

.. literalinclude:: Info.plist
   :language: xml

This sample script finds the calendar defintions, reads
them, and prints the titles of any calendars being displayed by iCal
(having the property ``Checked`` set to a true value).

.. include:: plistlib_checked_calendars.py
   :literal:
   :start-after: #end_pymotw_header

The type of the ``Checked`` property is defined by the plist file, so
our script does not need to convert the string to an integer.

::

	$ python plistlib_checked_calendars.py
	Doug Hellmann
	Tasks
	Vacation Schedule
	EarthSeasons
	US Holidays
	Athens, GA Weather - By Weather Underground
	Birthdays
	Georgia Bulldogs Calendar (NCAA Football)
	Home
	Meetup: Django
	Meetup: Python

Writing plist Files
===================

If you want to use plist files to save your own settings, use
``writePlist()`` to serialize the data and write it to the filesystem.

.. include:: plistlib_write_plist.py
   :literal:
   :start-after: #end_pymotw_header

The first argument is the data structure to write out, and the second
is an open file handle or the name of a file.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'plistlib_write_plist.py'))
.. }}}

::

	$ python plistlib_write_plist.py
	
	<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
	<plist version="1.0">
	<dict>
		<key>a_bool</key>
		<false/>
		<key>an_int</key>
		<integer>2</integer>
		<key>nested_dict</key>
		<dict>
			<key>key</key>
			<string>value</string>
		</dict>
		<key>nested_list</key>
		<array>
			<string>a</string>
			<string>b</string>
			<string>c</string>
		</array>
		<key>simple_string</key>
		<string>This string has no special characters.</string>
		<key>the_float</key>
		<real>5.9</real>
		<key>timestamp</key>
		<date>2013-02-21T06:36:30Z</date>
		<key>xml_string</key>
		<string>&lt;element attr="value"&gt;This string includes XML markup &amp;nbsp;&lt;/element&gt;</string>
	</dict>
	</plist>
	

.. {{{end}}}


Binary Property Data
====================

Serializing binary data or strings that may include control characters
using a plist is not immune to the typical challenges for an XML
format.  To work around the issues, plist files can store binary data
in :mod:`base64` format if the object is wrapped with a ``Data``
instance.

.. include:: plistlib_binary_write.py
   :literal:
   :start-after: #end_pymotw_header

This example uses the ``writePlistToString()`` to create an in-memory
string, instead of writing to a file.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'plistlib_binary_write.py'))
.. }}}

::

	$ python plistlib_binary_write.py
	
	<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
	<plist version="1.0">
	<dict>
		<key>binary_data</key>
		<data>
		VGhpcyBkYXRhIGhhcyBhbiBlbWJlZGRlZCBudWxsLiAA
		</data>
	</dict>
	</plist>
	

.. {{{end}}}

Binary data is automatically converted to a ``Data`` instance when
read.

.. include:: plistlib_binary_read.py
   :literal:
   :start-after: #end_pymotw_header

The ``data`` attribute of the object contains the decoded data.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'plistlib_binary_read.py'))
.. }}}

::

	$ python plistlib_binary_read.py
	
	'This data has an embedded null. \x00'

.. {{{end}}}



.. seealso::

    `plistlib <http://docs.python.org/2.7/library/plistlib.html>`_
        The standard library documentation for this module.

    `plist manual page <http://developer.apple.com/documentation/Darwin/Reference/ManPages/man5/plist.5.html>`_
        Documentation of the plist file format.

    `Weather Underground <http://www.wunderground.com/>`_
        Free weather information, including ICS and RSS feeds.

    `Convert plist between XML and Binary formats <http://www.macosxhints.com/article.php?story=20050430105126392>`_
        Some plist files are stored in a binary format instead of XML
        because the binary format is faster to parse using Apple's
        libraries.  Python's plistlib module does not handle the
        binary format, so you may need to convert binary files to XML
        using ``plutil`` before reading them.

    `Using Python for System Administration <http://docs.google.com/present/view?id=0AW0cyKASCypUZGczODJ6YjdfMjRobW16dG5mNQ&hl=en>`_
        Presentation from Nigel Kersten and Chris Adams, including
        details of using PyObjC to load plists using the native Cocoa
        API, which transparently handles both the XML and binary
        formats.  See slice 27, especially.
