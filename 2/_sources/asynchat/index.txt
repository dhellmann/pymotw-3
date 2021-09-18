=========================================
asynchat -- Asynchronous protocol handler
=========================================

.. module:: asynchat
    :synopsis: Asynchronous protocol handler

:Purpose: Asynchronous network communication protocol handler
:Available In: 1.5.2 and later

The :mod:`asynchat` module builds on :mod:`asyncore` to make it easier
to implement protocols based on passing messages back and forth
between server and client. The :class:`async_chat` class is an
:class:`asyncore.dispatcher` subclass that receives data and looks for
a message terminator. Your subclass only needs to specify what to do
when data comes in and how to respond once the terminator is
found. Outgoing data is queued for transmission via FIFO objects
managed by :class:`async_chat`.

Message Terminators
===================

Incoming messages are broken up based on *terminators*, controlled for
each instance via :func:`set_terminator()`. There are three possible
configurations:

1. If a string argument is passed to :func:`set_terminator()`, the
   message is considered complete when that string appears in the
   input data.
2. If a numeric argument is passed, the message is considered complete
   when that many bytes have been read.
3. If ``None`` is passed, message termination is not managed by
   :class:`async_chat`.

The :class:`EchoServer` example below uses both a simple string
terminator and a message length terminator, depending on the context
of the incoming data. The HTTP request handler example in the standard
library documentation offers another example of how to change the
terminator based on the context to differentiate between HTTP headers
and the HTTP POST request body.

Server and Handler
==================

To make it easier to understand how :mod:`asynchat` is different from
:mod:`asyncore`, the examples here duplicate the functionality of the
:class:`EchoServer` example from the :mod:`asyncore` discussion. The
same pieces are needed: a server object to accept connections, handler
objects to deal with communication with each client, and client
objects to initiate the conversation.

The :class:`EchoServer` needed to work with :mod:`asynchat` is
essentially the same as the one created for the :mod:`asyncore`
example, with fewer :mod:`logging` calls because they are less
interesting this time around:

.. include:: asynchat_echo_server.py
    :literal:
    :start-after: #end_pymotw_header

The :class:`EchoHandler` is based on ``asynchat.async_chat`` instead
of the :class:`asyncore.dispatcher` this time around. It operates at a
slightly higher level of abstraction, so reading and writing are
handled automatically. The buffer needs to know four things:

- what to do with incoming data (by overriding
  :func:`handle_incoming_data()`)
- how to recognize the end of an incoming message (via
  :func:`set_terminator()`)
- what to do when a complete message is received (in
  :func:`found_terminator()`)
- what data to send (using :func:`push()`)

The example application has two operating modes. It is either waiting
for a command of the form ``ECHO length\n``, or waiting for the data
to be echoed. The mode is toggled back and forth by setting an
instance variable *process_data* to the method to be invoked when the
terminator is found and then changing the terminator as appropriate.

.. include:: asynchat_echo_handler.py
    :literal:
    :start-after: #end_pymotw_header

Once the complete command is found, the handler switches to
message-processing mode and waits for the complete set of text to be
received. When all of the data is available, it is pushed onto the
outgoing channel and set up the handler to be closed once the data is
sent.

Client
======

The client works in much the same way as the handler. As with the
:mod:`asyncore` implementation, the message to be sent is an argument
to the client's constructor. When the socket connection is
established, :func:`handle_connect()` is called so the client can send
the command and message data.

The command is pushed directly, but a special "producer" class is used
for the message text. The producer is polled for chunks of data to
send out over the network. When the producer returns an empty string,
it is assumed to be empty and writing stops.

The client expects just the message data in response, so it sets an
integer terminator and collects data in a list until the entire
message has been received.

.. include:: asynchat_echo_client.py
    :literal:
    :start-after: #end_pymotw_header


Putting It All Together
=======================

The main program for this example sets up the client and server in the
same :mod:`asyncore` main loop.

.. include:: asynchat_echo_main.py
    :literal:
    :start-after: #end_pymotw_header

Normally you would have them in separate processes, but this makes it
easier to show the combined output.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asynchat_echo_main.py'))
.. }}}

::

	$ python asynchat_echo_main.py
	
	EchoClient: connecting to ('127.0.0.1', 56193)
	EchoClient: handle_connect()
	EchoProducer: more() -> (64 bytes)
	"""Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec
	"""
	EchoHandler: collect_incoming_data() -> (8 bytes)
	"""ECHO 166"""
	EchoHandler: found_terminator()
	EchoHandler: _process_command() "ECHO 166"
	EchoHandler: collect_incoming_data() -> (55 bytes)
	"""Lorem ipsum dolor sit amet, consectetuer adipiscing eli"""
	EchoProducer: more() -> (64 bytes)
	"""egestas, enim et consectetuer ullamcorper, lectus ligula rutrum """
	EchoHandler: collect_incoming_data() -> (64 bytes)
	"""t. Donec
	egestas, enim et consectetuer ullamcorper, lectus ligul"""
	EchoProducer: more() -> (38 bytes)
	"""leo, a
	elementum elit tortor eu quam.
	"""
	EchoHandler: collect_incoming_data() -> (47 bytes)
	"""a rutrum leo, a
	elementum elit tortor eu quam.
	"""
	EchoHandler: found_terminator()
	EchoHandler: _process_message() echoing
	"""Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec
	egestas, enim et consectetuer ullamcorper, lectus ligula rutrum leo, a
	elementum elit tortor eu quam.
	"""
	EchoProducer: more() -> (0 bytes)
	""""""
	EchoClient: collect_incoming_data() -> (64)
	"""Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec
	"""
	EchoClient: collect_incoming_data() -> (64)
	"""egestas, enim et consectetuer ullamcorper, lectus ligula rutrum """
	EchoClient: collect_incoming_data() -> (38)
	"""leo, a
	elementum elit tortor eu quam.
	"""
	EchoClient: found_terminator()
	EchoClient: RECEIVED COPY OF MESSAGE

.. {{{end}}}


.. seealso::

    `asynchat <http://docs.python.org/2.7/library/asynchat.html>`_
        The standard library documentation for this module.

    :mod:`asyncore`
        The asyncore module implements an lower-level asynchronous I/O
        event loop.
