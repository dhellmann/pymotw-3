=================================================
 smtplib -- Simple Mail Transfer Protocol Client
=================================================

.. module:: smtplib
    :synopsis: Simple mail transfer protocol client.

:Purpose: Interact with SMTP servers, including sending email.
:Python Version: 1.5.2 and later

:mod:`smtplib` includes the class :class:`SMTP`, which can be used to
communicate with mail servers to send mail.

.. note::

    The email addresses, host names, and IP addresses in the following
    examples have been obscured, but otherwise the transcripts
    illustrate the sequence of commands and responses accurately.


Sending an Email Message
========================

The most common use of :class:`SMTP` is to connect to a mail server
and send a message.  The mail server host name and port can be passed
to the constructor, or :func:`connect` can be invoked explicitly.
Once connected, call :func:`sendmail` with the envelope parameters and
body of the message.  The message text should be fully formed and
comply with RFC 2882, since :mod:`smtplib` does not modify the
contents or headers at all.  That means the ``From`` and ``To``
headers need to be added by the caller.

.. include:: smtplib_sendmail.py
    :literal:
    :start-after: #end_pymotw_header

In this example, debugging is also turned on to show the communication
between client and server.  Otherwise the example would produce no
output at all.

::

    $ python smtplib_sendmail.py
            
    send: 'ehlo farnsworth.local\r\n'
    reply: '250-mail.example.com Hello [192.168.1.27], pleased to meet y
    ou\r\n'
    reply: '250-ENHANCEDSTATUSCODES\r\n'
    reply: '250-PIPELINING\r\n'
    reply: '250-8BITMIME\r\n'
    reply: '250-SIZE\r\n'
    reply: '250-DSN\r\n'
    reply: '250-ETRN\r\n'
    reply: '250-AUTH GSSAPI DIGEST-MD5 CRAM-MD5\r\n'
    reply: '250-DELIVERBY\r\n'
    reply: '250 HELP\r\n'
    reply: retcode (250); Msg: mail.example.com Hello [192.168.1.27], pl
    eased to meet you
    ENHANCEDSTATUSCODES
    PIPELINING
    8BITMIME
    SIZE
    DSN
    ETRN
    AUTH GSSAPI DIGEST-MD5 CRAM-MD5
    DELIVERBY
    HELP
    send: 'mail FROM:<author@example.com> size=229\r\n'
    reply: '250 2.1.0 <author@example.com>... Sender ok\r\n'
    reply: retcode (250); Msg: 2.1.0 <author@example.com>... Sender ok
    send: 'rcpt TO:<recipient@example.com>\r\n'
    reply: '250 2.1.5 <recipient@example.com>... Recipient ok\r\n'
    reply: retcode (250); Msg: 2.1.5 <recipient@example.com>... Recipien
    t ok
    send: 'data\r\n'
    reply: '354 Enter mail, end with "." on a line by itself\r\n'
    reply: retcode (354); Msg: Enter mail, end with "." on a line by its
    elf
    data: (354, 'Enter mail, end with "." on a line by itself')
    send: 'Content-Type: text/plain; charset="us-ascii"\r\nMIME-Version:
     1.0\r\nContent-Transfer-Encoding: 7bit\r\nTo: Recipient <recipient@
    example.com>\r\nFrom: Author <author@example.com>\r\nSubject: Simple
     test message\r\n\r\nThis is the body of the message.\r\n.\r\n'
    reply: '250 2.0.0 oAT1TiRA010200 Message accepted for delivery\r\n'
    reply: retcode (250); Msg: 2.0.0 oAT1TiRA010200 Message accepted for
     delivery
    data: (250, '2.0.0 oAT1TiRA010200 Message accepted for delivery')
    send: 'quit\r\n'
    reply: '221 2.0.0 mail.example.com closing connection\r\n'
    reply: retcode (221); Msg: 2.0.0 mail.example.com closing connection
        
The second argument to :func:`sendmail`, the recipients, is passed as
a list.  Any number of addresses can be included in the list to have
the message delivered to each of them in turn.  Since the envelope
information is separate from the message headers, it is possible to
blind carbon-copy (BCC) someone by including them in the method
argument, but not in the message header.


Authentication and Encryption
=============================

The :class:`SMTP` class also handles authentication and TLS (transport
layer security) encryption, when the server supports them.  To
determine if the server supports TLS, call :func:`ehlo` directly to
identify the client to the server and ask it what extensions are
available.  Then call :func:`has_extn` to check the results.  After TLS
is started, :func:`ehlo` must be called again before authenticating.

.. include:: smtplib_authenticated.py
    :literal:
    :start-after: #end_pymotw_header

The ``STARTTLS`` extension does not appear in the reply to ``EHLO``
after TLS is enabled.

::

    $ python smtplib_authenticated.py 
    
    Recipient: recipient@example.com
    Mail server name: smtpauth.isp.net
    Mail username: user@isp.net
    user@isp.net's password: 
    send: 'ehlo localhost.local\r\n'
    reply: '250-elasmtp-isp.net Hello localhost.local [<your IP here>]\r
    \n'
    reply: '250-SIZE 14680064\r\n'
    reply: '250-PIPELINING\r\n'
    reply: '250-AUTH PLAIN LOGIN CRAM-MD5\r\n'
    reply: '250-STARTTLS\r\n'
    reply: '250 HELP\r\n'
    reply: retcode (250); Msg: elasmtp-isp.net Hello localhost.local [<y
    our IP here>]
    SIZE 14680064
    PIPELINING
    AUTH PLAIN LOGIN CRAM-MD5
    STARTTLS
    HELP
    send: 'STARTTLS\r\n'
    reply: '220 TLS go ahead\r\n'
    reply: retcode (220); Msg: TLS go ahead
    send: 'ehlo localhost.local\r\n'
    reply: '250-elasmtp-isp.net Hello localhost.local [<your IP here>]\r
    \n'
    reply: '250-SIZE 14680064\r\n'
    reply: '250-PIPELINING\r\n'
    reply: '250-AUTH PLAIN LOGIN CRAM-MD5\r\n'
    reply: '250 HELP\r\n'
    reply: retcode (250); Msg: elasmtp-isp.net Hello farnsworth.local [<
    your 
    IP here>]
    SIZE 14680064
    PIPELINING
    AUTH PLAIN LOGIN CRAM-MD5
    HELP
    send: 'AUTH CRAM-MD5\r\n'
    reply: '334 PDExNjkyLjEyMjI2MTI1NzlAZWxhc210cC1tZWFseS5hdGwuc2EuZWFy
    dGhsa
    W5rLm5ldD4=\r\n'
    reply: retcode (334); Msg: PDExNjkyLjEyMjI2MTI1NzlAZWxhc210cC1tZWFse
    S5hdG
    wuc2EuZWFydGhsaW5rLm5ldD4=
    send: 'ZGhlbGxtYW5uQGVhcnRobGluay5uZXQgN2Q1YjAyYTRmMGQ1YzZjM2NjOTNjZ
    Dc1MD
    QxN2ViYjg=\r\n'
    reply: '235 Authentication succeeded\r\n'
    reply: retcode (235); Msg: Authentication succeeded
    send: 'mail FROM:<author@example.com> size=221\r\n'
    reply: '250 OK\r\n'
    reply: retcode (250); Msg: OK
    send: 'rcpt TO:<recipient@example.com>\r\n'
    reply: '250 Accepted\r\n'
    reply: retcode (250); Msg: Accepted
    send: 'data\r\n'
    reply: '354 Enter message, ending with "." on a line by itself\r\n'
    reply: retcode (354); Msg: Enter message, ending with "." on a line 
    by itself
    data: (354, 'Enter message, ending with "." on a line by itself')
    send: 'Content-Type: text/plain; charset="us-ascii"\r\nMIME-Version:
    1.0\r\nContent-Transfer-Encoding: 7bit\r\nTo: Recipient 
    <recipient@example.com>\r\nFrom: Author <author@example.com>\r\nSubj
    ect: Test 
    from PyMOTW\r\n\r\nTest message from PyMOTW.\r\n.\r\n'
    reply: '250 OK id=1KjxNj-00032a-Ux\r\n'
    reply: retcode (250); Msg: OK id=1KjxNj-00032a-Ux
    data: (250, 'OK id=1KjxNj-00032a-Ux')
    send: 'quit\r\n'
    reply: '221 elasmtp-isp.net closing connection\r\n'
    reply: retcode (221); Msg: elasmtp-isp.net closing connection


Verifying an Email Address
==========================

The SMTP protocol includes a command to ask a server whether an
address is valid.  Usually ``VRFY`` is disabled to prevent spammers
from finding legitimate email addresses, but if it is enabled a client
can ask the server about an address and receive a status code
indicating validity along with the user's full name, if it is
available.

.. include:: smtplib_verify.py
    :literal:
    :start-after: #end_pymotw_header

As the last two lines of output here show, the address ``dhellmann``
is valid but ``notthere`` is not.

::

    $ python smtplib_verify.py

    send: 'vrfy <dhellmann>\r\n'
    reply: '250 2.1.5 Doug Hellmann <dhellmann@mail.example.com>\r\n'
    reply: retcode (250); Msg: 2.1.5 Doug Hellmann <dhellmann@mail.examp
    le.com>
    send: 'vrfy <notthere>\r\n'
    reply: '550 5.1.1 <notthere>... User unknown\r\n'
    reply: retcode (550); Msg: 5.1.1 <notthere>... User unknown
    send: 'quit\r\n'
    reply: '221 2.0.0 mail.example.com closing connection\r\n'
    reply: retcode (221); Msg: 2.0.0 mail.example.com closing connection
    dhellmann: (250, '2.1.5 Doug Hellmann <dhellmann@mail.example.com>')
    notthere : (550, '5.1.1 <notthere>... User unknown')

.. seealso::

    `smtplib <http://docs.python.org/lib/module-smtplib.html>`_
        Standard library documentation for this module.

    :rfc:`821`
        The Simple Mail Transfer Protocol (SMTP) specification.

    :rfc:`1869`
        SMTP Service Extensions to the base protocol.

    :rfc:`822`
        "Standard for the Format of ARPA Internet Text Messages", the original email message
        format specification.

    :rfc:`2822`
        "Internet Message Format", updates to the email message format.

    :mod:`email`
        Standard library module for parsing email messages.

    :mod:`smtpd`
        Implements a simple SMTP server.
