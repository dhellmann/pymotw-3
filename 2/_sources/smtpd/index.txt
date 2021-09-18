============================
smtpd -- Sample SMTP Servers
============================

.. module:: smtpd
    :synopsis: Includes classes for implementing SMTP servers.

:Purpose: Includes classes for implementing SMTP servers.
:Available In: 2.1 and later

The :mod:`smtpd` module includes classes for building simple mail
transport protocol servers.  It is the server-side of the protocol
used by :mod:`smtplib`.


SMTPServer
==========

The base class for all of the provided example servers is
:class:`SMTPServer`.  It handles communicating with the client,
receiving the data, and provides a convenient hook to override to
handle the message once it is fully available.

The constructor arguments are the local address to listen for
connections and the remote address for proxying.  The method
:func:`process_message()` is provided as a hook to be overridden by
your derived class.  It is called when the message is completely
received, and given these arguments:

peer

  The client's address, a tuple containing IP and incoming port.

mailfrom

  The "from" information out of the message envelope, given to the
  server by the client when the message is delivered.  This does not
  necessarily match the ``From`` header in all cases.
  
rcpttos

  The list of recipients from the message envelope.  Again, this does
  not always match the ``To`` header, especially if someone is blind
  carbon copied.

data

  The full :rfc:`2822` message body.

Since the default implementation of :func:`process_message()` raises
:ref:`NotImplementedError <exceptions-NotImplementedError>`, to
demonstrate using :class:`SMTPServer` we need to create a subclass and
provide a useful implementation.  This first example defines a server
that prints information about the messages it receives.

.. include:: smtpd_custom.py
    :literal:
    :start-after: #end_pymotw_header

:class:`SMTPServer` uses :mod:`asyncore`, so to run the server we call
``asyncore.loop()``.

Now, we need a client to send data.  By adapting one of the examples
from the :mod:`smtplib` page, we can set up a client to send data to
our test server running locally on port 1025.

.. include:: smtpd_senddata.py
    :literal:
    :start-after: #end_pymotw_header

Now if we run ``smtpd_custom.py`` in one terminal, and
``smtpd_senddata.py`` in another, we should see:

::

    $ python smtpd_senddata.py 
    send: 'ehlo farnsworth.local\r\n'
    reply: '502 Error: command "EHLO" not implemented\r\n'
    reply: retcode (502); Msg: Error: command "EHLO" not implemented
    send: 'helo farnsworth.local\r\n'
    reply: '250 farnsworth.local\r\n'
    reply: retcode (250); Msg: farnsworth.local
    send: 'mail FROM:<author@example.com>\r\n'
    reply: '250 Ok\r\n'
    reply: retcode (250); Msg: Ok
    send: 'rcpt TO:<recipient@example.com>\r\n'
    reply: '250 Ok\r\n'
    reply: retcode (250); Msg: Ok
    send: 'data\r\n'
    reply: '354 End data with <CR><LF>.<CR><LF>\r\n'
    reply: retcode (354); Msg: End data with <CR><LF>.<CR><LF>
    data: (354, 'End data with <CR><LF>.<CR><LF>')
    send: 'Content-Type: text/plain; charset="us-ascii"\r\nMIME-Version: 1.0\r\nContent-Transfer-Encoding: 7bit\r\nTo: Recipient <recipient@example.com>\r\nFrom: Author <author@example.com>\r\nSubject: Simple test message\r\n\r\nThis is the body of the message.\r\n.\r\n'
    reply: '250 Ok\r\n'
    reply: retcode (250); Msg: Ok
    data: (250, 'Ok')
    send: 'quit\r\n'
    reply: '221 Bye\r\n'
    reply: retcode (221); Msg: Bye

and

::

    $ python smtpd_custom.py 
    Receiving message from: ('127.0.0.1', 58541)
    Message addressed from: author@example.com
    Message addressed to  : ['recipient@example.com']
    Message length        : 229

The port number for the incoming message will vary each time.  Notice
that the *rcpttos* argument is a list of values and *mailfrom* is a
single string.

.. note::

    To stop the server, press ``Ctrl-C``.


DebuggingServer
===============

The example above shows the arguments to :func:`process_message()`,
but :mod:`smtpd` also includes a server specifically designed for more
complete debugging, called :class:`DebuggingServer`.  It prints the
entire incoming message to stdout and then stops processing (it does
not proxy the message to a real mail server).

.. include:: smtpd_debug.py
    :literal:
    :start-after: #end_pymotw_header

Using the ``smtpd_senddata.py`` client program from above, the output
of the :class:`DebuggingServer` is:

::

    $ python smtpd_debug.py
    ---------- MESSAGE FOLLOWS ----------
    Content-Type: text/plain; charset="us-ascii"
    MIME-Version: 1.0
    Content-Transfer-Encoding: 7bit
    To: Recipient <recipient@example.com>
    From: Author <author@example.com>
    Subject: Simple test message
    X-Peer: 127.0.0.1

    This is the body of the message.
    ------------ END MESSAGE ------------

PureProxy
=========

The :class:`PureProxy` class implements a straightforward proxy
server.  Incoming messages are forwarded upstream to the server given
as argument to the constructor.

.. warning::

    The stdlib docs say, "running this has a good chance to make you
    into an open relay, so please be careful."

Setting up the proxy server is just as easy as the debug server:

.. include:: smtpd_proxy.py
    :literal:
    :start-after: #end_pymotw_header

It prints no output, though, so to verify that it is working we need
to look at the mail server logs.

::

    Oct 19 19:16:34 homer sendmail[6785]: m9JNGXJb006785: from=<author@example.com>, size=248, class=0, nrcpts=1, msgid=<200810192316.m9JNGXJb006785@homer.example.com>, proto=ESMTP, daemon=MTA, relay=[192.168.1.17]


MailmanProxy
============

:mod:`smtpd` also includes a special proxy that acts as a front-end
for Mailman_.  If the local Mailman configuration recognizes the
address, it is handled directly.  Otherwise the message is delivered
to the proxy.


.. seealso::

    `smtpd <https://docs.python.org/2/library/smtpd.html>`_
        Standard library documentation for this module.

    :mod:`smtplib`
        Provides a client interface.

    :mod:`email`
        Parses email messages.

    :mod:`asyncore`
        Base module for writing asynchronous servers.

    :rfc:`2822`
        Defines the email message format.

    `GNU Mailman mailing list software <http://www.gnu.org/software/mailman/index.html>`_
        An excellent example of Python software that works with email messages.

.. _Mailman: http://www.gnu.org/software/mailman/index.html

