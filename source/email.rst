=======
 Email
=======

Email is one of the oldest forms of digital communication,
but it is still one of the most popular.  Python's standard library includes
modules for sending, receiving, and storing email messages.

:mod:`smtplib` communicates with a mail server to deliver a message.
:mod:`smtpd` can be used to create a custom mail server, and provides
classes useful for debugging email transmission in other applications.

:mod:`imaplib` uses the IMAP protocol to manipulate messages stored on
a server.  It provides a low-level API for IMAP clients, and can
query, retrieve, move, and delete messages.

Local message archives can be created and modified with :mod:`mailbox`
using several standard formats including the popular mbox and
Maildir formats used by many email client programs.

.. toctree::
   :maxdepth: 1

   mailbox/index

..
   .. toctree::
      :maxdepth: 1

      smtplib/index
      smtpd/index
      imaplib/index
      mailbox/index

..   mhlib/index
..   email/index
..   poplib/index
