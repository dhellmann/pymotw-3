===========================
gettext -- Message Catalogs
===========================

.. module:: gettext
    :synopsis: Message Catalogs

:Purpose: Message catalog API for internationalization.
:Available In: 2.1.3 and later

The :mod:`gettext` module provides a pure-Python implementation
compatible with the `GNU gettext`_ library for message translation and
catalog management.  The tools available with the Python source
distribution enable you to extract messages from your source, build a
message catalog containing translations, and use that message catalog
to print an appropriate message for the user at runtime.

Message catalogs can be used to provide internationalized interfaces
for your program, showing messages in a language appropriate to the
user.  They can also be used for other message customizations,
including "skinning" an interface for different wrappers or partners.

.. note::

    Although the standard library documentation says everything you
    need is included with Python, I found that ``pygettext.py``
    refused to extract messages wrapped in the ``ungettext`` call,
    even when I used what seemed to be the appropriate command line
    options. I ended up installing the `GNU gettext`_ tools from
    source and using ``xgettext`` instead.

Translation Workflow Overview
=============================

The process for setting up and using translations includes five steps:

1. Mark up literal strings in your code that contain messages to translate.

   Start by identifying the messages within your program source that
   need to be translated, and marking the literal strings so the
   extraction program can find them.

2. Extract the messages.

   After you have identified the translatable strings in your program
   source, use ``xgettext`` to pull the strings out and create a
   ``.pot`` file, or translation template. The template is a text file
   with copies of all of the strings you identified and placeholders
   for their translations.

3. Translate the messages.

   Give a copy of the ``.pot`` file to the translator, changing the
   extension to ``.po``. The ``.po`` file is an editable source file
   used as input for the compilation step. The translator should
   update the header text in the file and provide translations for all
   of the strings.

4. "Compile" the message catalog from the translation.

   When the translator gives you back the completed ``.po`` file,
   compile the text file to the binary catalog format using
   ``msgfmt``. The binary format is used by the runtime catalog lookup
   code.

5. Load and activate the appropriate message catalog at runtime.

   The final step is to add a few lines to your application to
   configure and load the message catalog and install the translation
   function. There are a couple of ways to do that, with associated
   trade-offs, and each is covered below.

Let's go through those steps in a little more detail, starting with
the modifications you need to make to your code.

Creating Message Catalogs from Source Code
==========================================

:mod:`gettext` works by finding literal strings embedded in your
program in a database of translations, and pulling out the appropriate
translated string.  There are several variations of the functions for
accessing the catalog, depending on whether you are working with
Unicode strings or not.  The usual pattern is to bind the lookup
function you want to use to the name ``_`` so that your code is not
cluttered with lots of calls to functions with longer names.

The message extraction program, ``xgettext``, looks for messages
embedded in calls to the catalog lookup functions.  It understands
different source languages, and uses an appropriate parser for each.
If you use aliases for the lookup functions or need to add extra
functions, you can give ``xgettext`` the names of additional symbols
to consider when extracting messages.

Here's a simple script with a single message ready to be translated:

.. include:: gettext_example.py
    :literal:
    :start-after: #end_pymotw_header

In this case I am using the Unicode version of the lookup function,
``ugettext()``.  The text ``"This message is in the script."`` is the
message to be substituted from the catalog.  I've enabled fallback
mode, so if we run the script without a message catalog, the in-lined
message is printed:

.. {{{cog
.. sh('rm -f PyMOTW/gettext/locale/en_US/LC_MESSAGES/gettext_example.mo')
.. cog.out(run_script(cog.inFile, 'gettext_example.py'))
.. }}}

::

	$ python gettext_example.py
	
	This message is in the script.

.. {{{end}}}

The next step is to extract the message(s) and create the ``.pot``
file, using ``pygettext.py``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'xgettext -d gettext_example -o gettext_example.pot gettext_example.py', interpreter=None))
.. }}}

::

	$ xgettext -d gettext_example -o gettext_example.pot gettext_example.py
	

.. {{{end}}}

The output file produced looks like:

.. include:: gettext_example.pot
    :literal:

Message catalogs are installed into directories organized by *domain*
and *language*.  The domain is usually a unique value like your
application name.  In this case, I used ``gettext_example``.  The
language value is provided by the user's environment at runtime,
through one of the environment variables ``LANGUAGE``, ``LC_ALL``,
``LC_MESSAGES``, or ``LANG``, depending on their configuration and
platform.  My language is set to ``en_US`` so that's what I'll be
using in all of the examples below.

Now that we have the template, the next step is to create the required
directory structure and copy the template in to the right spot.  I'm
going to use the ``locale`` directory inside the PyMOTW source tree as
the root of my message catalog directory, but you would typically want
to use a directory accessible system-wide.  The full path to the
catalog input source is
``$localedir/$language/LC_MESSAGES/$domain.po``, and the actual
catalog has the filename extension ``.mo``.

For my configuration, I need to copy ``gettext_example.pot`` to
``locale/en_US/LC_MESSAGES/gettext_example.po`` and edit it to change
the values in the header and add my alternate messages.  The result
looks like:

.. include:: locale/en_US/LC_MESSAGES/gettext_example.po
    :literal:

The catalog is built from the ``.po`` file using ``msgformat``:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'cd locale/en_US/LC_MESSAGES/; msgfmt -o gettext_example.mo gettext_example.po', interpreter=None))
.. }}}

::

	$ cd locale/en_US/LC_MESSAGES/; msgfmt -o gettext_example.mo gettext_exa\
	mple.po
	

.. {{{end}}}

And now when we run the script, the message from the catalog is
printed instead of the in-line string:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gettext_example.py'))
.. }}}

::

	$ python gettext_example.py
	
	This message is in the en_US catalog.

.. {{{end}}}


Finding Message Catalogs at Runtime
===================================

As described above, the *locale directory* containing the message
catalogs is organized based on the language with catalogs named for
the *domain* of the program.  Different operating systems define their
own default value, but :mod:`gettext` does not know all of these
defaults.  Iut uses a default locale directory of ``sys.prefix +
'/share/locale'``, but most of the time it is safer for you to always
explicitly give a ``localedir`` value than to depend on this default
being valid.

The language portion of the path is taken from one of several
environment variables that can be used to configure localization
features (``LANGUAGE``, ``LC_ALL``, ``LC_MESSAGES``, and ``LANG``).
The first variable found to be set is used.  Multiple languages can be
selected by separating the values with a colon (``:``).  We can
illustrate how that works by creating a second message catalog and
running a few experiments.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'cd locale/en_CA/LC_MESSAGES/; msgfmt -o gettext_example.mo gettext_example.po', trailing_newlines=False, interpreter=None))
.. cog.out(run_script(cog.inFile, 'gettext_find.py', include_prefix=False, trailing_newlines=False))
.. cog.out(run_script(cog.inFile, 'LANGUAGE=en_CA python gettext_find.py', interpreter=None, include_prefix=False, trailing_newlines=False))
.. cog.out(run_script(cog.inFile, 'LANGUAGE=en_CA:en_US python gettext_find.py', interpreter=None, include_prefix=False, trailing_newlines=False))
.. cog.out(run_script(cog.inFile, 'LANGUAGE=en_US:en_CA python gettext_find.py', interpreter=None, include_prefix=False))
.. }}}

::

	$ cd locale/en_CA/LC_MESSAGES/; msgfmt -o gettext_example.mo gettext_exa\
	mple.po
	$ python gettext_find.py
	
	Catalogs: ['locale/en_US/LC_MESSAGES/gettext_example.mo']
	$ LANGUAGE=en_CA python gettext_find.py
	
	Catalogs: ['locale/en_CA/LC_MESSAGES/gettext_example.mo']
	$ LANGUAGE=en_CA:en_US python gettext_find.py
	
	Catalogs: ['locale/en_CA/LC_MESSAGES/gettext_example.mo', 'locale/en_US/LC_MESSAGES/gettext_example.mo']
	$ LANGUAGE=en_US:en_CA python gettext_find.py
	
	Catalogs: ['locale/en_US/LC_MESSAGES/gettext_example.mo', 'locale/en_CA/LC_MESSAGES/gettext_example.mo']

.. {{{end}}}

Although ``find()`` shows the complete list of catalogs, only the
first one in the sequence is actually loaded for message lookups.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'gettext_example.py', trailing_newlines=False))
.. cog.out(run_script(cog.inFile, 'LANGUAGE=en_CA python gettext_example.py', interpreter=None, include_prefix=False, trailing_newlines=False))
.. cog.out(run_script(cog.inFile, 'LANGUAGE=en_CA:en_US python gettext_example.py', interpreter=None, include_prefix=False, trailing_newlines=False))
.. cog.out(run_script(cog.inFile, 'LANGUAGE=en_US:en_CA python gettext_example.py', interpreter=None, include_prefix=False))
.. }}}

::

	$ python gettext_example.py
	
	This message is in the en_US catalog.
	$ LANGUAGE=en_CA python gettext_example.py
	
	This message is in the en_CA catalog.
	$ LANGUAGE=en_CA:en_US python gettext_example.py
	
	This message is in the en_CA catalog.
	$ LANGUAGE=en_US:en_CA python gettext_example.py
	
	This message is in the en_US catalog.

.. {{{end}}}


Plural Values
=============

While simple message substitution will handle most of your translation
needs, :mod:`gettext` treats pluralization as a special case.
Depending on the language, the difference between the singular and
plural forms of a message may vary only by the ending of a single
word, or the entire sentence structure may be different.  There may
also be `different forms depending on the level of plurality
<http://www.gnu.org/software/gettext/manual/gettext.html#Plural-forms>`_.
To make managing plurals easier (and possible), there is a separate
set of functions for asking for the plural form of a message.

.. include:: gettext_plural.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'xgettext -L Python -d gettext_plural -o gettext_plural.pot gettext_plural.py', interpreter=None))
.. }}}

::

	$ xgettext -L Python -d gettext_plural -o gettext_plural.pot gettext_plu\
	ral.py
	

.. {{{end}}}

Since there are alternate forms to be translated, the replacements are
listed in an array.  Using an array allows translations for languages
with multiple plural forms (Polish, `for example
<http://www.gnu.org/software/gettext/manual/gettext.html#Plural-forms>`_,
has different forms indicating the relative quantity).

.. include:: gettext_plural.pot
    :literal:

In addition to filling in the translation strings, you will also need
to describe the way plurals are formed so the library knows how to
index into the array for any given count value.  The line
``"Plural-Forms: nplurals=INTEGER; plural=EXPRESSION;\n"`` includes
two values to replace manually.  ``nplurals`` is an integer indicating
the size of the array (the number of translations used) and ``plural``
is a C language expression for converting the incoming quantity to an
index in the array when looking up the translation.  The literal
string ``n`` is replaced with the quantity passed to ``ungettext()``.

For example, English includes two plural forms.  A quantity of ``0``
is treated as plural ("0 bananas").  The Plural-Forms entry should
look like::

    Plural-Forms: nplurals=2; plural=n != 1;

The singular translation would then go in position 0, and the plural
translation in position 1.

.. include:: locale/en_US/LC_MESSAGES/gettext_plural.po
    :literal:

If we run the test script a few times after the catalog is compiled,
you can see how different values of N are converted to indexes for the
translation strings.
    
.. {{{cog
.. cog.out(run_script(cog.inFile, 'cd locale/en_US/LC_MESSAGES/; msgfmt -o gettext_plural.mo gettext_plural.po', trailing_newlines=False, interpreter=None))
.. cog.out(run_script(cog.inFile, 'gettext_plural.py 0', include_prefix=False, trailing_newlines=False))
.. cog.out(run_script(cog.inFile, 'gettext_plural.py 1', include_prefix=False, trailing_newlines=False))
.. cog.out(run_script(cog.inFile, 'gettext_plural.py 2', include_prefix=False))
.. }}}

::

	$ cd locale/en_US/LC_MESSAGES/; msgfmt -o gettext_plural.mo gettext_plur\
	al.po
	$ python gettext_plural.py 0
	
	In en_US, 0 is plural.
	$ python gettext_plural.py 1
	
	In en_US, 1 is singular.
	$ python gettext_plural.py 2
	
	In en_US, 2 is plural.

.. {{{end}}}

Application vs. Module Localization
===================================

The scope of your translation effort defines how you install and use
the :mod:`gettext` functions in your code.

Application Localization
------------------------

For application-wide translations, it would be acceptable to install a
function like ``ungettext()`` globally using the ``__builtins__``
namespace because you have control over the top-level of the
application's code.

.. include:: gettext_app_builtin.py
    :literal:
    :start-after: #end_pymotw_header

The ``install()`` function binds ``gettext()`` to the name ``_()`` in
the ``__builtins__`` namespace.  It also adds ``ngettext()`` and other
functions listed in *names*.  If *unicode* is true, the Unicode
versions of the functions are used instead of the default ASCII
versions.

Module Localization
-------------------

For a library, or individual module, modifying ``__builtins__`` is not
a good idea because you don't know what conflicts you might introduce
with an application global value.  You can import or re-bind the names
of translation functions by hand at the top of your module.

.. include:: gettext_module_global.py
    :literal:
    :start-after: #end_pymotw_header


.. seealso::

    `gettext <http://docs.python.org/2.7/library/gettext.html>`_
        The standard library documentation for this module.

    :mod:`locale`
        Other localization tools.

    `GNU gettext`_
        The message catalog formats, API, etc. for this module are all
        based on the original gettext package from GNU.  The catalog
        file formats are compatible, and the command line scripts have
        similar options (if not identical).  The `GNU gettext manual
        <http://www.gnu.org/software/gettext/manual/gettext.html>`_
        has a detailed description of the file formats and describes
        GNU versions of the tools for working with them.

    `Internationalizing Python <http://www.python.org/workshops/1997-10/proceedings/loewis.html>`_
        A paper by Martin von Löwis about techniques for
        internationalization of Python applications.

    `Django Internationalization <http://docs.djangoproject.com/en/dev/topics/i18n/>`_
        Another good source of information on using gettext, including
        real-life examples.

.. _GNU gettext: http://www.gnu.org/software/gettext/
