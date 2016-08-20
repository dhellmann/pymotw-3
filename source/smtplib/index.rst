==================================================
 smtplib --- Simple Mail Transfer Protocol Client
==================================================

.. module:: smtplib
    :synopsis: Simple mail transfer protocol client.

:Purpose: Interact with SMTP servers, including sending email.

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

.. literalinclude:: smtplib_sendmail.py
    :caption:
    :start-after: #end_pymotw_header

In this example, debugging is also turned on to show the communication
between client and server.  Otherwise the example would produce no
output at all.

.. cog.out(run_script(cog.inFile, 'smtplib_sendmail.py'))

.. code-block:: none

	$ python3 smtplib_sendmail.py
	
	send: 'ehlo 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.
	0.0.0.0.0.0.ip6.arpa\r\n'
	reply: b'250-1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0
	.0.0.0.0.0.0.ip6.arpa\r\n'
	reply: b'250-SIZE 33554432\r\n'
	reply: b'250 HELP\r\n'
	reply: retcode (250); Msg: b'1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0
	.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa\nSIZE 33554432\nHELP'
	send: 'mail FROM:<author@example.com> size=236\r\n'
	reply: b'250 OK\r\n'
	reply: retcode (250); Msg: b'OK'
	send: 'rcpt TO:<recipient@example.com>\r\n'
	reply: b'250 OK\r\n'
	reply: retcode (250); Msg: b'OK'
	send: 'data\r\n'
	reply: b'354 End data with <CR><LF>.<CR><LF>\r\n'
	reply: retcode (354); Msg: b'End data with <CR><LF>.<CR><LF>'
	data: (354, b'End data with <CR><LF>.<CR><LF>')
	send: b'Content-Type: text/plain; charset="us-ascii"\r\nMIME-Ver
	sion: 1.0\r\nContent-Transfer-Encoding: 7bit\r\nTo: Recipient <r
	ecipient@example.com>\r\nFrom: Author <author@example.com>\r\nSu
	bject: Simple test message\r\n\r\nThis is the body of the messag
	e.\r\n.\r\n'
	reply: b'250 OK\r\n'
	reply: retcode (250); Msg: b'OK'
	data: (250, b'OK')
	send: 'quit\r\n'
	reply: b'221 Bye\r\n'
	reply: retcode (221); Msg: b'Bye'

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
available.  Then call :func:`has_extn` to check the results.  After
TLS is started, :func:`ehlo` must be called again before
authenticating. Many mail hosting providers now *only* support
TLS-based connections. For communicating with those servers, use
:class:`SMTP_SSL` to start off with an encrypted connection.

.. literalinclude:: smtplib_authenticated.py
    :caption:
    :start-after: #end_pymotw_header

The ``STARTTLS`` extension does not appear in the reply to ``EHLO``
after TLS is enabled.

.. code-block:: none

   $ python3 source/smtplib/smtplib_authenticated.py
   Recipient: doug@pymotw.com
   Mail server name: localhost
   Server port: 1025
   Use TLS? (yes/no): no
   Mail username: test
   test's password:
   starting with an insecure connection
   send: 'ehlo 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0
   .0.0.0.0.0.ip6.arpa\r\n'
   reply: b'250-1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.
   0.0.0.0.0.0.ip6.arpa\r\n'
   reply: b'250-SIZE 33554432\r\n'
   reply: b'250 HELP\r\n'
   reply: retcode (250); Msg: b'1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.
   0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa\nSIZE 33554432\nHELP'
   (no STARTTLS)
   (no AUTH)
   send: 'mail FROM:<author@example.com> size=220\r\n'
   reply: b'250 OK\r\n'
   reply: retcode (250); Msg: b'OK'
   send: 'rcpt TO:<doug@pymotw.com>\r\n'
   reply: b'250 OK\r\n'
   reply: retcode (250); Msg: b'OK'
   send: 'data\r\n'
   reply: b'354 End data with <CR><LF>.<CR><LF>\r\n'
   reply: retcode (354); Msg: b'End data with <CR><LF>.<CR><LF>'
   data: (354, b'End data with <CR><LF>.<CR><LF>')
   send: b'Content-Type: text/plain; charset="us-ascii"\r\n
   MIME-Version: 1.0\r\nContent-Transfer-Encoding: 7bit\r\nTo: 
   Recipient <doug@pymotw.com>\r\nFrom: Author <author@example.com>
   \r\nSubject: Test from PyMOTW\r\n\r\nTest message from PyMOTW.
   \r\n.\r\n'
   reply: b'250 OK\r\n'
   reply: retcode (250); Msg: b'OK'
   data: (250, b'OK')
   send: 'quit\r\n'
   reply: b'221 Bye\r\n'
   reply: retcode (221); Msg: b'Bye'

   $ python3 source/smtplib/smtplib_authenticated.py
   Recipient: doug@pymotw.com
   Mail server name: mail.isp.net
   Server port: 465
   Use TLS? (yes/no): yes
   Mail username: doughellmann@isp.net
   doughellmann@isp.net's password:
   starting with a secure connection
   send: 'ehlo 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0
   .0.0.0.0.0.ip6.arpa\r\n'
   reply: b'250-mail.isp.net\r\n'
   reply: b'250-PIPELINING\r\n'
   reply: b'250-SIZE 71000000\r\n'
   reply: b'250-ENHANCEDSTATUSCODES\r\n'
   reply: b'250-8BITMIME\r\n'
   reply: b'250-AUTH PLAIN LOGIN\r\n'
   reply: b'250 AUTH=PLAIN LOGIN\r\n'
   reply: retcode (250); Msg: b'mail.isp.net\nPIPELINING\nSIZE 
   71000000\nENHANCEDSTATUSCODES\n8BITMIME\nAUTH PLAIN LOGIN\n
   AUTH=PLAIN LOGIN'
   (no STARTTLS)
   (logging in)
   send: 'AUTH PLAIN AGRvdWdoZWxsbWFubkBmYXN0bWFpbC5mbQBUTUZ3MDBmZmF
   zdG1haWw=\r\n'
   reply: b'235 2.0.0 OK\r\n'
   reply: retcode (235); Msg: b'2.0.0 OK'
   send: 'mail FROM:<author@example.com> size=220\r\n'
   reply: b'250 2.1.0 Ok\r\n'
   reply: retcode (250); Msg: b'2.1.0 Ok'
   send: 'rcpt TO:<doug@pymotw.com>\r\n'
   reply: b'250 2.1.5 Ok\r\n'
   reply: retcode (250); Msg: b'2.1.5 Ok'
   send: 'data\r\n'
   reply: b'354 End data with <CR><LF>.<CR><LF>\r\n'
   reply: retcode (354); Msg: b'End data with <CR><LF>.<CR><LF>'
   data: (354, b'End data with <CR><LF>.<CR><LF>')
   send: b'Content-Type: text/plain; charset="us-ascii"\r\n
   MIME-Version: 1.0\r\nContent-Transfer-Encoding: 7bit\r\nTo: 
   Recipient <doug@pymotw.com>\r\nFrom: Author <author@example.com>
   \r\nSubject: Test from PyMOTW\r\n\r\nTest message from PyMOTW.
   \r\n.\r\n'
   reply: b'250 2.0.0 Ok: queued as A0EF7F2983\r\n'
   reply: retcode (250); Msg: b'2.0.0 Ok: queued as A0EF7F2983'
   data: (250, b'2.0.0 Ok: queued as A0EF7F2983')
   send: 'quit\r\n'
   reply: b'221 2.0.0 Bye\r\n'
   reply: retcode (221); Msg: b'2.0.0 Bye'

Verifying an Email Address
==========================

The SMTP protocol includes a command to ask a server whether an
address is valid.  Usually ``VRFY`` is disabled to prevent spammers
from finding legitimate email addresses, but if it is enabled a client
can ask the server about an address and receive a status code
indicating validity along with the user's full name, if it is
available.

.. literalinclude:: smtplib_verify.py
    :caption:
    :start-after: #end_pymotw_header

As the last two lines of output here show, the address ``dhellmann``
is valid but ``notthere`` is not.

.. code-block:: none

    $ python3 smtplib_verify.py

    send: 'vrfy <dhellmann>\r\n'
    reply: '250 2.1.5 Doug Hellmann <dhellmann@mail>\r\n'
    reply: retcode (250); Msg: 2.1.5 Doug Hellmann <dhellmann@mail>
    send: 'vrfy <notthere>\r\n'
    reply: '550 5.1.1 <notthere>... User unknown\r\n'
    reply: retcode (550); Msg: 5.1.1 <notthere>... User unknown
    send: 'quit\r\n'
    reply: '221 2.0.0 mail closing connection\r\n'
    reply: retcode (221); Msg: 2.0.0 mail closing connection
    dhellmann: (250, '2.1.5 Doug Hellmann <dhellmann@mail>')
    notthere : (550, '5.1.1 <notthere>... User unknown')

.. seealso::

   * :pydoc:`smtplib`

   * :rfc:`821` -- The Simple Mail Transfer Protocol (SMTP)
     specification.

   * :rfc:`1869` -- SMTP Service Extensions to the base protocol.

   * :rfc:`822` -- "Standard for the Format of ARPA Internet Text
     Messages", the original email message format specification.

   * :rfc:`2822` -- "Internet Message Format", updates to the email
     message format.

   * :mod:`email` -- Standard library module for building and parsing
     email messages.

   * :mod:`smtpd` -- Implements a simple SMTP server.
