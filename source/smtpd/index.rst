===============================
 smtpd --- Sample Mail Servers
===============================

.. module:: smtpd
    :synopsis: Includes classes for implementing SMTP servers.

The ``smtpd`` module includes classes for building Simple Mail
Transport Protocol (SMTP) servers.  It is the server-side of the
protocol used by :mod:`smtplib`.

Mail Server Base Class
======================

The base class for all of the provided example servers is
``SMTPServer``.  It handles communicating with the client,
receiving incoming data, and provides a convenient hook to override to
process the message once it is fully available.

The constructor arguments are the local address to listen for
connections and the remote address where proxied messages should be
delivered.  The method ``process_message()`` is provided as a hook
to be overridden by a derived class.  It is called when the message is
completely received, and given these arguments:

``peer``

  The client's address, a tuple containing IP and incoming port.

``mailfrom``

  The "from" information out of the message envelope, given to the
  server by the client when the message is delivered.  This does not
  necessarily match the ``From`` header in all cases.

``rcpttos``

  The list of recipients from the message envelope.  Again, this does
  not always match the ``To`` header, especially if a recipient is being
  blind carbon copied.

``data``

  The full RFC 5322 message body.

The default implementation of ``process_message()`` raises
``NotImplementedError``.  The next example defines a subclass
that overrides the method to print information about the messages it
receives.

.. literalinclude:: smtpd_custom.py
    :caption:
    :start-after: #end_pymotw_header

``SMTPServer`` uses :mod:`asyncore`, so to run the server call
``asyncore.loop()``.

A client is needed to demonstrate the server.  One of the examples
from the section on :mod:`smtplib` can be adapted to create a client
to send data to the test server running locally on port 1025.

.. literalinclude:: smtpd_senddata.py
    :caption:
    :start-after: #end_pymotw_header

To test the programs, run ``smtpd_custom.py`` in one terminal and
``smtpd_senddata.py`` in another.

.. NOT RUNNING

.. code-block:: none

    $ python3 smtpd_custom.py 

    Receiving message from: ('127.0.0.1', 58541)
    Message addressed from: author@example.com
    Message addressed to  : ['recipient@example.com']
    Message length        : 229

The debug output from ``smtpd_senddata.py`` shows all of the
communication with the server.

.. NOT RUNNING

.. cog.out(run_script(cog.inFile, 'smtpd_senddata.py'))

.. code-block:: none

	$ python3 smtpd_senddata.py
	
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

To stop the server, press ``Ctrl-C``.


Debugging Server
================

The previous example shows the arguments to ``process_message()``,
but ``smtpd`` also includes a server specifically designed for more
complete debugging, called ``DebuggingServer``.  It prints the
entire incoming message to the console and then stops processing (it
does not proxy the message to a real mail server).

.. literalinclude:: smtpd_debug.py
    :caption:
    :start-after: #end_pymotw_header

Using the ``smtpd_senddata.py`` client program from earlier, the output
of the ``DebuggingServer`` is:

.. NOT RUNNING

.. code-block:: none

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

Proxy Server
============

The ``PureProxy`` class implements a straightforward proxy
server.  Incoming messages are forwarded upstream to the server given
as argument to the constructor.

.. warning::

    The standard library documentation for ``smtpd`` says, "running
    this has a good chance to make you into an open relay, so please
    be careful."

The steps for setting up the proxy server are similar to the debug
server.

.. literalinclude:: smtpd_proxy.py
    :caption:
    :start-after: #end_pymotw_header

It prints no output, though, so to verify that it is working look at
the mail server logs.

.. NOT RUNNING

::

    Aug 20 19:16:34 homer sendmail[6785]: m9JNGXJb006785: 
    from=<author@example.com>, size=248, class=0, nrcpts=1, 
    msgid=<200810192316.m9JNGXJb006785@homer.example.com>, 
    proto=ESMTP, daemon=MTA, relay=[192.168.1.17]


.. seealso::

   * :pydoc:`smtpd`

   * :mod:`smtplib` -- Provides a client interface.

   * :mod:`email` -- Parses email messages.

   * :mod:`asyncore` -- Base module for writing asynchronous servers.

   * :rfc:`2822` -- *Internet Message Format*, defines the email
     message format.

   * :rfc:`5322` -- Replacement for RFC 2822.

