======================================
 mailbox --- Manipulate Email Archives
======================================

.. module:: mailbox
    :synopsis: Access and manipulate email archives.

:Purpose: Work with email messages in various local file formats.

The :mod:`mailbox` module defines a common API for accessing email
messages stored in local disk formats, including:

- Maildir
- mbox
- MH
- Babyl
- MMDF

There are base classes for :class:`Mailbox` and :class:`Message`, and
each mailbox format includes a corresponding pair of subclasses to
implement the details for that format.

mbox
====

The mbox format is the simplest to show in documentation, since it is
entirely plain text.  Each mailbox is stored as a single file, with
all of the messages concatenated together.  Each time a line starting
with ``"From "`` ("From" followed by a single space) is encountered it
is treated as the beginning of a new message.  Any time those
characters appear at the beginning of a line in the message body, they
are escaped by prefixing the line with ``">"``.

Creating an mbox Mailbox
------------------------

Instantiate the :class:`mbox` class by passing the filename to the
constructor.  If the file does not exist, it is created when
:func:`add` is used to append messages.

.. literalinclude:: mailbox_mbox_create.py
    :caption:
    :start-after: #end_pymotw_header

The result of this script is a new mailbox file with two email
messages.

.. {{{cog
.. import os
.. os.system('rm -f source/mailbox/example.mbox')
.. os.system('rm -f example.mbox')
.. cog.out(run_script(cog.inFile, 'mailbox_mbox_create.py'))
.. }}}

::

	$ python3 mailbox_mbox_create.py
	
	From MAILER-DAEMON Sun Jan 31 16:39:25 2016
	From: Author <author@example.com>
	To: Recipient <recipient@example.com>
	Subject: Sample message 1
	
	This is the body.
	>From (will not be escaped).
	There are 3 lines.
	
	From MAILER-DAEMON Sun Jan 31 16:39:25 2016
	From: Author <author@example.com>
	To: Recipient <recipient@example.com>
	Subject: Sample message 2
	
	This is the second body.
	
	

.. {{{end}}}

Reading an mbox Mailbox
-----------------------

To read an existing mailbox, open it and treat the :class:`mbox`
object like a dictionary.  The keys are arbitrary values defined by
the mailbox instance and are not necessary meaningful other than as
internal identifiers for message objects.

.. literalinclude:: mailbox_mbox_read.py
    :caption:
    :start-after: #end_pymotw_header

The open mailbox supports the iterator protocol, but unlike true
dictionary objects, the default iterator for a mailbox works on the *values*
instead of the *keys*.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'mailbox_mbox_read.py'))
.. }}}

::

	$ python3 mailbox_mbox_read.py
	
	Sample message 1
	Sample message 2

.. {{{end}}}

Removing Messages from an mbox Mailbox
--------------------------------------

To remove an existing message from an mbox file, either use its key with
:meth:`remove` or use :command:`del`.

.. literalinclude:: mailbox_mbox_remove.py
    :caption:
    :start-after: #end_pymotw_header

The :meth:`lock` and :meth:`unlock` methods are used to prevent issues
from simultaneous access to the file, and :meth:`flush` forces the
changes to be written to disk.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'mailbox_mbox_remove.py'))
.. }}}

::

	$ python3 mailbox_mbox_remove.py
	
	Removing: 1
	From MAILER-DAEMON Sun Jan 31 16:39:25 2016
	From: Author <author@example.com>
	To: Recipient <recipient@example.com>
	Subject: Sample message 1
	
	This is the body.
	>From (will not be escaped).
	There are 3 lines.
	
	

.. {{{end}}}

Maildir
=======

The Maildir format was created to eliminate the problem of concurrent
modification to an mbox file.  Instead of using a single file, the
mailbox is organized as directory where each message is contained in
its own file.  This also allows mailboxes to be nested, so the API
for a Maildir mailbox is extended with methods to work with
sub-folders.

Creating a Maildir Mailbox
--------------------------

The only real difference between creating a :class:`Maildir` and
:class:`mbox` is that the argument to the constructor is a directory
name instead of a file name.  As before, if the mailbox does not
exist, it is created when messages are added.

.. literalinclude:: mailbox_maildir_create.py
    :caption:
    :start-after: #end_pymotw_header

When messages are added to the mailbox, they go to the ``new``
subdirectory.  After they are read, a client could move them to the
``cur`` subdirectory.

.. warning::

    Although it is safe to write to the same maildir from multiple
    processes, :meth:`add` is not thread-safe.  Use a semaphore or
    other locking device to prevent simultaneous modifications to the
    mailbox from multiple threads of the same process.

.. {{{cog
.. from paver.path import path
.. (path(cog.inFile).dirname() / 'Example').rmtree()
.. cog.out(run_script(cog.inFile, 'mailbox_maildir_create.py'))
.. }}}

::

	$ python3 mailbox_maildir_create.py
	
	Example
		Directories: ['cur', 'new', 'tmp']
	Example/cur
		Directories: []
	Example/new
		Directories: []
	
	*** Example/new/1454258365.M762908P48861Q1.hubert.local
	From: Author <author@example.com>
	To: Recipient <recipient@example.com>
	Subject: Sample message 1
	
	This is the body.
	From (will not be escaped).
	There are 3 lines.
	
	********************
	
	*** Example/new/1454258365.M766115P48861Q2.hubert.local
	From: Author <author@example.com>
	To: Recipient <recipient@example.com>
	Subject: Sample message 2
	
	This is the second body.
	
	********************
	Example/tmp
		Directories: []

.. {{{end}}}


Reading a Maildir Mailbox
-------------------------

Reading from an existing Maildir mailbox works just like an mbox
mailbox.

.. literalinclude:: mailbox_maildir_read.py
    :caption:
    :start-after: #end_pymotw_header

The messages are not guaranteed to be read in any particular order.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'mailbox_maildir_read.py'))
.. }}}

::

	$ python3 mailbox_maildir_read.py
	
	Sample message 1
	Sample message 2

.. {{{end}}}


Removing Messages from a Maildir Mailbox
----------------------------------------

To remove an existing message from a Maildir mailbox, either pass its
key to :meth:`remove` or use :command:`del`.

.. literalinclude:: mailbox_maildir_remove.py
    :caption:
    :start-after: #end_pymotw_header

There is no way to compute the key for a message, so use :meth:`items`
or :meth:`iteritems` to retrieve the key and message object from the
mailbox at the same time.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'mailbox_maildir_remove.py'))
.. }}}

::

	$ python3 mailbox_maildir_remove.py
	
	Removing: 1454258365.M766115P48861Q2.hubert.local
	Example
		Directories: ['cur', 'new', 'tmp']
	Example/cur
		Directories: []
	Example/new
		Directories: []
	
	*** Example/new/1454258365.M762908P48861Q1.hubert.local
	From: Author <author@example.com>
	To: Recipient <recipient@example.com>
	Subject: Sample message 1
	
	This is the body.
	From (will not be escaped).
	There are 3 lines.
	
	********************
	Example/tmp
		Directories: []

.. {{{end}}}


Maildir folders
---------------

Subdirectories or *folders* of a Maildir mailbox can be managed
directly through the methods of the :class:`Maildir` class.  Callers
can list, retrieve, create, and remove sub-folders for a given
mailbox.

.. literalinclude:: mailbox_maildir_folders.py
    :caption:
    :start-after: #end_pymotw_header

The directory name for the folder is constructed by prefixing the
folder name with a period (``.``).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'mailbox_maildir_folders.py'))
.. }}}

::

	$ python3 mailbox_maildir_folders.py
	
	Example
	Example/cur
	Example/new
	Example/new/1454258365.M762908P48861Q1.hubert.local
	Example/tmp
	Example
	Example/.subfolder
	Example/.subfolder/cur
	Example/.subfolder/maildirfolder
	Example/.subfolder/new
	Example/.subfolder/tmp
	Example/cur
	Example/new
	Example/new/1454258365.M762908P48861Q1.hubert.local
	Example/tmp
	Example
	Example/.subfolder
	Example/.subfolder/.second_level
	Example/.subfolder/.second_level/cur
	Example/.subfolder/.second_level/maildirfolder
	Example/.subfolder/.second_level/new
	Example/.subfolder/.second_level/tmp
	Example/.subfolder/cur
	Example/.subfolder/maildirfolder
	Example/.subfolder/new
	Example/.subfolder/tmp
	Example/cur
	Example/new
	Example/new/1454258365.M762908P48861Q1.hubert.local
	Example/tmp
	Example
	Example/.subfolder
	Example/.subfolder/cur
	Example/.subfolder/maildirfolder
	Example/.subfolder/new
	Example/.subfolder/tmp
	Example/cur
	Example/new
	Example/new/1454258365.M762908P48861Q1.hubert.local
	Example/tmp
	Before: []
	
	##############################
	
	subfolder created: ['subfolder']
	subfolder contents: []
	
	##############################
	
	second_level created: ['second_level']
	
	##############################
	
	second_level removed: []

.. {{{end}}}


Other Formats
=============

:mod:`mailbox` supports a few other formats, but none are as
popular as mbox or Maildir.  MH is another multi-file mailbox format
used by some mail handlers.  Babyl and MMDF are single-file formats
with different message separators than mbox.  The single-file formats
support the same API as mbox, and MH includes the folder-related
methods found in the Maildir class.

.. seealso::

   * :pydoc:`mailbox`

   * :ref:`Porting notes for mailbox <porting-mailbox>`

   * `mbox manpage from qmail
     <http://www.qmail.org/man/man5/mbox.html>`_ -- Documentation for
     the mbox format.

   * `Maildir manpage from qmail
     <http://www.qmail.org/man/man5/maildir.html>`_ -- Documentation
     for the Maildir format.

   * :mod:`email` -- The ``email`` module.

   * :mod:`imaplib` -- The ``imaplib`` module can work with saved
     email messages on an IMAP server.
