======================================
 mailbox --- Manipulate Email Archives
======================================

.. module:: mailbox
    :synopsis: Access and manipulate email archives.

:Purpose: Work with email messages in various local file formats.

The ``mailbox`` module defines a common API for accessing email
messages stored in local disk formats, including:

- Maildir
- mbox
- MH
- Babyl
- MMDF

There are base classes for ``Mailbox`` and ``Message``, and
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

Instantiate the ``mbox`` class by passing the filename to the
constructor.  If the file does not exist, it is created when
``add()`` is used to append messages.

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

.. code-block:: none

	$ python3 mailbox_mbox_create.py
	
	From MAILER-DAEMON Sun Jul 10 14:45:06 2016
	From: Author <author@example.com>
	To: Recipient <recipient@example.com>
	Subject: Sample message 1
	
	This is the body.
	>From (will not be escaped).
	There are 3 lines.
	
	From MAILER-DAEMON Sun Jul 10 14:45:06 2016
	From: Author <author@example.com>
	To: Recipient <recipient@example.com>
	Subject: Sample message 2
	
	This is the second body.
	
	

.. {{{end}}}

Reading an mbox Mailbox
-----------------------

To read an existing mailbox, open it and treat the ``mbox``
object like a dictionary.  The keys are arbitrary values defined by
the mailbox instance and are not necessary meaningful other than as
internal identifiers for message objects.

.. literalinclude:: mailbox_mbox_read.py
    :caption:
    :start-after: #end_pymotw_header

The open mailbox supports the iterator protocol, but unlike true
dictionary objects the default iterator for a mailbox works on the
*values* instead of the *keys*.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'mailbox_mbox_read.py'))
.. }}}

.. code-block:: none

	$ python3 mailbox_mbox_read.py
	
	Sample message 1
	Sample message 2

.. {{{end}}}

Removing Messages from an mbox Mailbox
--------------------------------------

To remove an existing message from an mbox file, either use its key with
:meth:`remove` or use ``del``.

.. literalinclude:: mailbox_mbox_remove.py
    :caption:
    :start-after: #end_pymotw_header

The :meth:`lock` and :meth:`unlock` methods are used to prevent issues
from simultaneous access to the file, and :meth:`flush` forces the
changes to be written to disk.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'mailbox_mbox_remove.py'))
.. }}}

.. code-block:: none

	$ python3 mailbox_mbox_remove.py
	
	Removing: 1
	From MAILER-DAEMON Sun Jul 10 14:45:06 2016
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

The only real difference between creating a ``Maildir`` and
``mbox`` is that the argument to the constructor is a directory
name instead of a file name.  As before, if the mailbox does not
exist, it is created when messages are added.

.. literalinclude:: mailbox_maildir_create.py
    :caption:
    :start-after: #end_pymotw_header

When messages are added to the mailbox, they go to the ``new``
subdirectory.

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

.. code-block:: none

	$ python3 mailbox_maildir_create.py
	
	Example
		Directories: ['cur', 'new', 'tmp']
	Example/cur
		Directories: []
	Example/new
		Directories: []
	
	*** Example/new/1468161907.M47549P22409Q1.lrrr.local
	From: Author <author@example.com>
	To: Recipient <recipient@example.com>
	Subject: Sample message 1
	
	This is the body.
	From (will not be escaped).
	There are 3 lines.
	
	********************
	
	*** Example/new/1468161907.M52295P22409Q2.lrrr.local
	From: Author <author@example.com>
	To: Recipient <recipient@example.com>
	Subject: Sample message 2
	
	This is the second body.
	
	********************
	Example/tmp
		Directories: []

.. {{{end}}}

After they are read, a client could move them to the ``cur``
subdirectory using the ``set_subdir()`` method of the
``MaildirMessage``.

.. literalinclude:: mailbox_maildir_set_subdir.py
   :caption:
   :start-after: #end_pymotw_header

Although a maildir includes a "``tmp``" directory, the only valid
arguments for ``set_subdir()`` are "``cur``" and "``new``".

.. {{{cog
.. cog.out(run_script(cog.inFile, 'mailbox_maildir_set_subdir.py'))
.. }}}

.. code-block:: none

	$ python3 mailbox_maildir_set_subdir.py
	
	Before:
	new    "Sample message 2"
	new    "Sample message 1"
	
	After:
	cur    "Sample message 2"
	cur    "Sample message 1"
	
	Example
		Directories: ['cur', 'new', 'tmp']
	Example/cur
		Directories: []
	Example/cur/1468161907.M47549P22409Q1.lrrr.local
	Example/cur/1468161907.M52295P22409Q2.lrrr.local
	Example/new
		Directories: []
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

.. code-block:: none

	$ python3 mailbox_maildir_read.py
	
	Sample message 2
	Sample message 1

.. {{{end}}}


Removing Messages from a Maildir Mailbox
----------------------------------------

To remove an existing message from a Maildir mailbox, either pass its
key to :meth:`remove` or use ``del``.

.. literalinclude:: mailbox_maildir_remove.py
    :caption:
    :start-after: #end_pymotw_header

There is no way to compute the key for a message, so use :meth:`items`
or :meth:`iteritems` to retrieve the key and message object from the
mailbox at the same time.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'mailbox_maildir_remove.py'))
.. }}}

.. code-block:: none

	$ python3 mailbox_maildir_remove.py
	
	Removing: 1468161907.M52295P22409Q2.lrrr.local
	Example
		Directories: ['cur', 'new', 'tmp']
	Example/cur
		Directories: []
	
	*** Example/cur/1468161907.M47549P22409Q1.lrrr.local
	From: Author <author@example.com>
	To: Recipient <recipient@example.com>
	Subject: Sample message 1
	
	This is the body.
	From (will not be escaped).
	There are 3 lines.
	
	********************
	Example/new
		Directories: []
	Example/tmp
		Directories: []

.. {{{end}}}


Maildir folders
---------------

Subdirectories or *folders* of a Maildir mailbox can be managed
directly through the methods of the ``Maildir`` class.  Callers
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

.. code-block:: none

	$ python3 mailbox_maildir_folders.py
	
	Example
	Example/cur
	Example/cur/1468161907.M47549P22409Q1.lrrr.local
	Example/new
	Example/tmp
	Example
	Example/.subfolder
	Example/.subfolder/cur
	Example/.subfolder/maildirfolder
	Example/.subfolder/new
	Example/.subfolder/tmp
	Example/cur
	Example/cur/1468161907.M47549P22409Q1.lrrr.local
	Example/new
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
	Example/cur/1468161907.M47549P22409Q1.lrrr.local
	Example/new
	Example/tmp
	Example
	Example/.subfolder
	Example/.subfolder/cur
	Example/.subfolder/maildirfolder
	Example/.subfolder/new
	Example/.subfolder/tmp
	Example/cur
	Example/cur/1468161907.M47549P22409Q1.lrrr.local
	Example/new
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

Message Flags
=============

Messages in mailboxes have flags for tracking aspects such as whether
or not the message has been read, flagged as important by the reader,
or marked for deletion later. Flags are stored as a sequence of
format-specific letter codes and the ``Message`` classes have
methods to retrieve and change the values of the flags. This example
shows the flags on the messages in the ``Example`` maildir before
adding the flag to indicate that the message is considered important.

.. literalinclude:: mailbox_maildir_add_flag.py
   :caption:
   :start-after: #end_pymotw_header

By default messages have no flags. Adding a flag changes the message
in memory, but does not update the message on disk. To update the
message on disk store the message object in the mailbox using its
existing identifier.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'mailbox_maildir_add_flag.py'))
.. }}}

.. code-block:: none

	$ python3 mailbox_maildir_add_flag.py
	
	Before:
	       "Sample message 1"
	
	After:
	F      "Sample message 1"

.. {{{end}}}

Adding flags with ``add_flag()`` preserves any existing flags. Using
``set_flags()`` writes over any existing set of flags, replacing it
with the new values passed to the method.

.. literalinclude:: mailbox_maildir_set_flags.py
   :caption:
   :start-after: #end_pymotw_header

The ``F`` flag added by the previous example is lost when
``set_flags()`` replaces the flags with ``S`` in this example.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'mailbox_maildir_set_flags.py'))
.. }}}

.. code-block:: none

	$ python3 mailbox_maildir_set_flags.py
	
	Before:
	F      "Sample message 1"
	
	After:
	S      "Sample message 1"

.. {{{end}}}

Other Formats
=============

``mailbox`` supports a few other formats, but none are as
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
