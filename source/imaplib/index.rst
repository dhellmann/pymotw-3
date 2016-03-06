.. This module does not use cog because of the IMAP server requirements.

================================
 imaplib - IMAP4 Client Library
================================

.. module:: imaplib
    :synopsis: IMAP4 client library

:Purpose: Client library for IMAP4 communication.
:Python Version: 1.5.2 and later

:mod:`imaplib` implements a client for communicating with Internet
Message Access Protocol (IMAP) version 4 servers.  The IMAP protocol
defines a set of commands sent to the server and the responses
delivered back to the client.  Most of the commands are available as
methods of the :class:`IMAP4` object used to communicate with the
server.

These examples discuss part of the IMAP protocol, but are by no means
complete.  Refer to RFC 3501 for complete details.


Variations
==========

There are three client classes for communicating with servers using
various mechanisms.  The first, :class:`IMAP4`, uses clear text
sockets; :class:`IMAP4_SSL` uses encrypted communication over SSL
sockets; and :class:`IMAP4_stream` uses the standard input and
standard output of an external command.  All of the examples here
will use :class:`IMAP4_SSL`, but the APIs for the other classes are
similar.


Connecting to a Server
======================

There are two steps for establishing a connection with an IMAP server.
First, set up the socket connection itself.  Second, authenticate as a
user with an account on the server.  The following example code will
read server and user information from a configuration file.

.. include:: imaplib_connect.py
    :literal:
    :start-after: #end_pymotw_header

When run, :func:`open_connection()` reads the configuration
information from a file in the user's home directory, then opens the
:class:`IMAP4_SSL` connection and authenticates.

::

    $ python imaplib_connect.py

    Connecting to mail.example.com
    Logging in as example
    <imaplib.IMAP4_SSL instance at 0x928cb0>

The other examples in this section reuse this module, to avoid
duplicating the code.

Authentication Failure
----------------------

If the connection is established but authentication fails, an
exception is raised.

.. include:: imaplib_connect_fail.py
    :literal:
    :start-after: #end_pymotw_header

This example uses the wrong password on purpose to trigger the
exception.

::

    $ python imaplib_connect_fail.py

    Connecting to mail.example.com
    Logging in as example
    ERROR: Authentication failed.


Example Configuration
=====================

The example account has three mailboxes, ``INBOX``,
``Archive``, and ``2008`` (a sub-folder of ``Archive``).  The mailbox
hierarchy is:

- INBOX
- Archive

  - 2008

There is one unread message in the ``INBOX`` folder, and one read
message in ``Archive/2008``.


Listing Mailboxes
=================

To retrieve the mailboxes available for an account, use the
:func:`list()` method.

.. include:: imaplib_list.py
    :literal:
    :start-after: #end_pymotw_header

The return value is a :class:`tuple` containing a response code and
the data returned by the server.  The response code is ``OK``, unless
there has been an error.  The data for :meth:`list()` is a sequence of
strings containing *flags*, the *hierarchy delimiter*, and *mailbox
name* for each mailbox.

::

    $ python imaplib_list.py

    Response code: OK
    Response:
    ['(\\HasNoChildren) "." INBOX',
     '(\\HasChildren) "." "Archive"',
     '(\\HasNoChildren) "." "Archive.2008"']

Each response string can be split into three parts using :mod:`re` or
:mod:`csv` (see *IMAP Backup Script* in the references at the end of
this section for an example using :mod:`csv`).

.. include:: imaplib_list_parse.py
    :literal:
    :start-after: #end_pymotw_header

The server quotes the mailbox name if it includes spaces, but those
quotes need to be stripped out to use the mailbox name in other calls
back to the server later.

::

    $ python imaplib_list_parse.py

    Response code: OK
    Server response: (\HasNoChildren) "." INBOX
    Parsed response: ('\\HasNoChildren', '.', 'INBOX')
    Server response: (\HasChildren) "." "Archive"
    Parsed response: ('\\HasChildren', '.', 'Archive')
    Server response: (\HasNoChildren) "." "Archive.2008"
    Parsed response: ('\\HasNoChildren', '.', 'Archive.2008')

:meth:`list()` takes arguments to specify mailboxes in part of the
hierarchy.  For example, to list sub-folders of ``Archive``, pass
``"Archive"`` as the *directory* argument.

.. include:: imaplib_list_subfolders.py
    :literal:
    :start-after: #end_pymotw_header

Only the single subfolder is returned.

::

    $ python imaplib_list_subfolders.py

    Response code: OK
    Server response: (\HasNoChildren) "." "Archive.2008"

Alternately, to list folders matching a pattern pass the *pattern*
argument.

.. include:: imaplib_list_pattern.py
    :literal:
    :start-after: #end_pymotw_header

In this case, both ``Archive`` and ``Archive.2008`` are included in
the response.

::

    $ python imaplib_list_pattern.py

    Response code: OK
    Server response: (\HasChildren) "." "Archive"
    Server response: (\HasNoChildren) "." "Archive.2008"


Mailbox Status
==============

Use :meth:`status()` to ask for aggregated information about the
contents.  :table:`IMAP 4 Mailbox Status Conditions` lists the status
conditions defined by the standard.

.. table:: IMAP 4 Mailbox Status Conditions

    ===========  =======
    Condition    Meaning
    ===========  =======
    MESSAGES     The number of messages in the mailbox.
    RECENT       The number of messages with the ``\Recent`` flag set.
    UIDNEXT      The next unique identifier value of the mailbox.
    UIDVALIDITY  The unique identifier validity value of the mailbox.
    UNSEEN       The number of messages which do not have the ``\Seen`` flag set.
    ===========  =======

The status conditions must be formatted as a space separated string
enclosed in parentheses, the encoding for a "list" in the IMAP4
specification.

.. include:: imaplib_status.py
    :literal:
    :start-after: #end_pymotw_header

The return value is the usual :class:`tuple` containing a response
code and a list of information from the server.  In this case, the
list contains a single string formatted with the name of the mailbox
in quotes, then the status conditions and values in parentheses.

::

    $ python imaplib_status.py

    ('OK', ['"INBOX" (MESSAGES 1 RECENT 0 UIDNEXT 3 UIDVALIDITY 
    1222003700 UNSEEN 1)'])
    ('OK', ['"Archive" (MESSAGES 0 RECENT 0 UIDNEXT 1 UIDVALIDITY 
    1222003809 UNSEEN 0)'])
    ('OK', ['"Archive.2008" (MESSAGES 1 RECENT 0 UIDNEXT 2 UIDVALIDITY 
    1222003831 UNSEEN 0)'])


Selecting a Mailbox
===================

The basic mode of operation, once the client is authenticated, is to
select a mailbox, then interrogate the server regarding messages in
the mailbox.  The connection is stateful, so after a mailbox is
selected all commands operate on messages in that mailbox until a new
mailbox is selected.

.. include:: imaplib_select.py
    :literal:
    :start-after: #end_pymotw_header

The response data contains the total number of messages in the
mailbox.

::

    $ python imaplib_select.py

    OK ['1']
    There are 1 messages in INBOX

If an invalid mailbox is specified, the response code is ``NO``.

.. include:: imaplib_select_invalid.py
    :literal:
    :start-after: #end_pymotw_header

The data contains an error message describing the problem.

::

    $ python imaplib_select_invalid.py

    NO ["Mailbox doesn't exist: Does Not Exist"]


Searching for Messages
======================

After selecting the mailbox, use :meth:`search()` to retrieve the IDs
of messages in the mailbox.

.. include:: imaplib_search_all.py
    :literal:
    :start-after: #end_pymotw_header

Message IDs are assigned by the server, and are implementation
dependent.  The IMAP4 protocol makes a distinction between sequential
IDs for messages at a given point in time during a transaction and UID
identifiers for messages, but not all servers implement both.

::

    $ python imaplib_search_all.py

    INBOX OK ['1']
    Archive OK ['']
    Archive.2008 OK ['1']

In this case, ``INBOX`` and ``Archive.2008`` each have a different
message with id ``1``.  The other mailboxes are empty.


Search Criteria
===============

A variety of other search criteria can be used, including looking at
dates for the message, flags, and other headers.  Refer to section
6.4.4. of RFC 3501 for complete details.

To look for messages with ``'test message 2'`` in the subject, the
search criteria should be constructed as::

  (SUBJECT "test message 2")
  
This example finds all messages with the title "test message 2" in all
mailboxes:

.. include:: imaplib_search_subject.py
    :literal:
    :start-after: #end_pymotw_header

There is only one such message in the account, and it is in the
``INBOX``.

::

    $ python imaplib_search_subject.py

    INBOX OK ['1']
    Archive OK ['']
    Archive.2008 OK ['']

Search criteria can also be combined.

.. include:: imaplib_search_from.py
    :literal:
    :start-after: #end_pymotw_header

The criteria are combined with a logical :command:`and` operation.

::

    $ python imaplib_search_from.py

    INBOX OK ['1']
    Archive OK ['']
    Archive.2008 OK ['']


Fetching Messages
=================

The identifiers returned by :meth:`search()` are used to retrieve the
contents, or partial contents, of messages for further processing
using the :meth:`fetch()` method.  It takes two arguments, the message
IDs to fetch and the portion(s) of the message to retrieve.

The *message_ids* argument is a comma separated list of ids (e.g.,
``"1"``, ``"1,2"``) or ID ranges (e.g., ``1:2``).  The *message_parts*
argument is an IMAP list of message segment names.  As with search
criteria for :meth:`search()`, the IMAP protocol specifies named
message segments so clients can efficiently retrieve only the parts of
the message they actually need.  For example, to retrieve the headers
of the messages in a mailbox, use :meth:`fetch()` with the argument
``BODY.PEEK[HEADER]``.

.. note::

  Another way to fetch the headers is ``BODY[HEADERS]``, but that form
  has a side-effect of implicitly marking the message as read, which
  is undesirable in many cases.

.. include:: imaplib_fetch_raw.py
    :literal:
    :start-after: #end_pymotw_header

The return value of :meth:`fetch()` has been partially parsed so it is
somewhat harder to work with than the return value of :meth:`list()`.
Turning on debugging shows the complete interaction between the client
and server to understand why this is so.

::

    $ python imaplib_fetch_raw.py
    
    13:12.54 imaplib version 2.58
    13:12.54 new IMAP4 connection, tag=CFKH
    13:12.54 < * OK dovecot ready.
    13:12.54 > CFKH0 CAPABILITY
    13:12.54 < * CAPABILITY IMAP4rev1 SORT THREAD=REFERENCES MULTIAPPEND
     UNSELECT IDLE CHILDREN LISTEXT LIST-SUBSCRIBED NAMESPACE AUTH=PLAIN
    13:12.54 < CFKH0 OK Capability completed.
    13:12.54 CAPABILITIES: ('IMAP4REV1', 'SORT', 'THREAD=REFERENCES', 'M
    ULTIAPPEND', 'UNSELECT', 'IDLE', 'CHILDREN', 'LISTEXT', 'LIST-SUBSCR
    IBED', 'NAMESPACE', 'AUTH=PLAIN')
    13:12.54 > CFKH1 LOGIN example "password"
    13:13.18 < CFKH1 OK Logged in.
    13:13.18 > CFKH2 EXAMINE INBOX
    13:13.20 < * FLAGS (\Answered \Flagged \Deleted \Seen \Draft $NotJun
    k $Junk)
    13:13.20 < * OK [PERMANENTFLAGS ()] Read-only mailbox.
    13:13.20 < * 2 EXISTS
    13:13.20 < * 1 RECENT
    13:13.20 < * OK [UNSEEN 1] First unseen.
    13:13.20 < * OK [UIDVALIDITY 1222003700] UIDs valid
    13:13.20 < * OK [UIDNEXT 4] Predicted next UID
    13:13.20 < CFKH2 OK [READ-ONLY] Select completed.
    13:13.20 > CFKH3 FETCH 1 (BODY.PEEK[HEADER] FLAGS)
    13:13.20 < * 1 FETCH (FLAGS ($NotJunk) BODY[HEADER] {595}
    13:13.20 read literal size 595
    13:13.20 < )
    13:13.20 < CFKH3 OK Fetch completed.
    13:13.20 > CFKH4 CLOSE
    13:13.21 < CFKH4 OK Close completed.
    13:13.21 > CFKH5 LOGOUT
    13:13.21 < * BYE Logging out
    13:13.21 BYE response: Logging out
    13:13.21 < CFKH5 OK Logout completed.
    '1 (FLAGS ($NotJunk) BODY[HEADER] {595}',
    'Return-Path: <dhellmann@example.com>\r\nReceived: from example.com 
    (localhost [127.0.0.1])\r\n\tby example.com (8.13.4/8.13.4) with ESM
    TP id m8LDTGW4018260\r\n\tfor <example@example.com>; Sun, 21 Sep 200
    8 09:29:16 -0400\r\nReceived: (from dhellmann@localhost)\r\n\tby exa
    mple.com (8.13.4/8.13.4/Submit) id m8LDTGZ5018259\r\n\tfor example@e
    xample.com; Sun, 21 Sep 2008 09:29:16 -0400\r\nDate: Sun, 21 Sep 200
    8 09:29:16 -0400\r\nFrom: Doug Hellmann <dhellmann@example.com>\r\nM
    essage-Id: <200809211329.m8LDTGZ5018259@example.com>\r\nTo: example@
    example.com\r\nSubject: test message 2\r\n\r\n'),
    )']

The response from the ``FETCH`` command starts with the flags, then
indicates that there are 595 bytes of header data.  The client
constructs a tuple with the response for the message, and then closes
the sequence with a single string containing the right parenthesis
("``)``") the server sends at the end of the fetch response.  Because of
this formatting, it may be easier to fetch different pieces of
information separately, or to recombine the response and parse it in
the client.

.. include:: imaplib_fetch_separately.py
    :literal:
    :start-after: #end_pymotw_header

Fetching values separately has the added benefit of making it easy to
use :func:`ParseFlags()` to parse the flags from the response.

::

    $ python imaplib_fetch_separately.py

    HEADER:
    Return-Path: <dhellmann@example.com>
    Received: from example.com (localhost [127.0.0.1])
        by example.com (8.13.4/8.13.4) with ESMTP id m8LDTGW4018260
        for <example@example.com>; Sun, 21 Sep 2008 09:29:16 -0400
    Received: (from dhellmann@localhost)
        by example.com (8.13.4/8.13.4/Submit) id m8LDTGZ5018259
        for example@example.com; Sun, 21 Sep 2008 09:29:16 -0400
    Date: Sun, 21 Sep 2008 09:29:16 -0400
    From: Doug Hellmann <dhellmann@example.com>
    Message-Id: <200809211329.m8LDTGZ5018259@example.com>
    To: example@example.com
    Subject: test message 2
    
    
    BODY TEXT:
    second message


    FLAGS:
    1 (FLAGS ($NotJunk))
    ('$NotJunk',)


Whole Messages
==============

As illustrated earlier, the client can ask the server for individual
parts of the message separately.  It is also possible to retrieve the
entire message as an RFC 2822 formatted mail message and parse it
with classes from the :mod:`email` module.

.. include:: imaplib_fetch_rfc822.py
    :literal:
    :start-after: #end_pymotw_header

The parser in the :mod:`email` module make it very easy to access and
manipulate messages.  This example prints just a few of the headers
for each message.

::

    $ python imaplib_fetch_rfc822.py

    SUBJECT : test message 2
    TO      : example@example.com
    FROM    : Doug Hellmann <dhellmann@example.com>


Uploading Messages
==================

To add a new message to a mailbox, construct a :class:`Message`
instance and pass it to the :meth:`append()` method, along with the
timestamp for the message.

.. include:: imaplib_append.py
    :literal:
    :start-after: #end_pymotw_header

The *payload* used in this example is a simple plaintext email body.
:class:`Message` also supports MIME-encoded multi-part messages.

::
    
    pymotw
    Subject: subject goes here
    From: pymotw@example.com
    To: example@example.com
    
    This is the body of the message.
    
    
    1:
    Return-Path: <dhellmann@example.com>
    Received: from example.com (localhost [127.0.0.1])
        by example.com (8.13.4/8.13.4) with ESMTP id m8LDTGW4018260
        for <example@example.com>; Sun, 21 Sep 2008 09:29:16 -0400
    Received: (from dhellmann@localhost)
        by example.com (8.13.4/8.13.4/Submit) id m8LDTGZ5018259
        for example@example.com; Sun, 21 Sep 2008 09:29:16 -0400
    Date: Sun, 21 Sep 2008 09:29:16 -0400
    From: Doug Hellmann <dhellmann@example.com>
    Message-Id: <200809211329.m8LDTGZ5018259@example.com>
    To: example@example.com
    Subject: test message 2
    
    
    
    2:
    Return-Path: <doug.hellmann@example.com>
    Message-Id: <0D9C3C50-462A-4FD7-9E5A-11EE222D721D@example.com>
    From: Doug Hellmann <doug.hellmann@example.com>
    To: example@example.com
    Content-Type: text/plain; charset=US-ASCII; format=flowed; delsp=yes
    Content-Transfer-Encoding: 7bit
    Mime-Version: 1.0 (Apple Message framework v929.2)
    Subject: lorem ipsum
    Date: Sun, 21 Sep 2008 12:53:16 -0400
    X-Mailer: Apple Mail (2.929.2)
    
    
    
    3:
    pymotw
    Subject: subject goes here
    From: pymotw@example.com
    To: example@example.com


Moving and Copying Messages
===========================

Once a message is on the server, it can be moved or copied without
downloading it using :meth:`move()` or :meth:`copy()`.  These methods
operate on message id ranges, just as :meth:`fetch()` does.

.. include:: imaplib_archive_read.py
    :literal:
    :start-after: #end_pymotw_header

This example script creates a new mailbox under ``Archive`` and copies
the read messages from ``INBOX`` into it.

::

    $ python imaplib_archive_read.py

    CREATED Archive.Today: ['Create completed.']
    COPYING: 1,2
    COPIED: 1 2

Running the same script again shows the importance to checking return
codes.  Instead of raising an exception, the call to :meth:`create()`
to make the new mailbox reports that the mailbox already exists.

::

    $ python imaplib_archive_read.py

    CREATED Archive.Today: ['Mailbox exists.']
    COPYING: 1,2
    COPIED: 1 2 3 4


Deleting Messages
=================

Although many modern mail clients use a "Trash folder" model for
working with deleted messages, the messages are not usually moved into
an actual folder.  Instead, their flags are updated to add
``\Deleted``.  The operation for "emptying" the trash is implemented
through the ``EXPUNGE`` command.  This example script finds the
archived messages with "Lorem ipsum" in the subject, sets the deleted
flag, then shows that the messages are still present in the folder by
querying the server again.

.. include:: imaplib_delete_messages.py
    :literal:
    :start-after: #end_pymotw_header

Explicitly calling :meth:`expunge()` removes the messages, but calling
:meth:`close()` has the same effect.  The difference is the client is
not notified about the deletions when :meth:`close()` is called.

::

    $ python imaplib_delete_messages.py

    Starting messages: 1 2 3 4
    Matching messages: 1,3
    Flags before: ['1 (FLAGS (\\Seen $NotJunk))', '3 (FLAGS (\\Seen 
    \\Recent $NotJunk))']
    Flags after: ['1 (FLAGS (\\Deleted \\Seen $NotJunk))', 
    '3 (FLAGS (\\Deleted \\Seen \\Recent $NotJunk))']
    Expunged: ['1', '2']
    Remaining messages: 1 2



.. seealso::

    `imaplib <http://docs.python.org/library/imaplib.html>`_
        The standard library documentation for this module.

    `What is IMAP? <http://www.imap.org/about/whatisIMAP.html>`_
        imap.org description of the IMAP protocol

    `University of Washington IMAP Information Center <http://www.washington.edu/imap/>`_
        Good resource for IMAP information, along with source code.

    :rfc:`3501`
        Internet Message Access Protocol

    :rfc:`2822`
        Internet Message Format

    `IMAP Backup Script`_
        A script to backup email from an IMAP server.

        .. _IMAP Backup Script: http://snipplr.com/view/7955/imap-backup-script/

    :mod:`rfc822`
        The ``rfc822`` module includes an RFC 822 / RFC 2822 parser.

    :mod:`email`
        The ``email`` module for parsing email messages.

    :mod:`mailbox`
        Local mailbox parser.

    :mod:`ConfigParser`
        Read and write configuration files.

    `IMAPClient <http://imapclient.freshfoo.com/>`_
        A higher-level client for talking to IMAP servers, written by Menno Smits.
