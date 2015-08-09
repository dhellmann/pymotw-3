Compressing Network Data
========================

The code in the next example responds to requests consisting of
filenames by writing a compressed version of the file to the socket
used to communicate with the client.  It has some artificial chunking
in place to illustrate the buffering that occurs when the data passed
to :func:`compress()` or :func:`decompress()` does not result in a
complete block of compressed or uncompressed output.

.. literalinclude:: bz2_server.py
   :lines: 11-52

The main program starts a server in a thread, combining
:mod:`SocketServer` and :class:`Bz2RequestHandler`.  

.. literalinclude:: bz2_server.py
   :lines: 55-

It then opens a socket to communicate with the server as a client, and
requests the file (defaulting to ``lorem.txt``) which contains:

.. include:: lorem.txt
   :literal:

.. warning::

    This implementation has obvious security implications.  Do not run
    it on a server on the open Internet or in any environment where
    security might be an issue.

Running ``bz2_server.py`` produces:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'bz2_server.py', break_lines_at=68))
.. }}}

::

	$ python bz2_server.py
	
	Client: Contacting server on 127.0.0.1:55091
	Client: sending filename: "lorem.txt"
	Server: client asked for: "lorem.txt"
	Server: RAW "Lorem ipsum dolor sit amet, cons"
	Server: BUFFERING
	Server: RAW "ectetuer adipiscing elit. Donec
	"
	Server: BUFFERING
	Server: RAW "egestas, enim et consectetuer ul"
	Server: BUFFERING
	Server: RAW "lamcorper, lectus ligula rutrum "
	Server: BUFFERING
	Server: RAW "leo,
	a elementum elit tortor eu "
	Server: BUFFERING
	Server: RAW "quam. Duis tincidunt nisi ut ant"
	Server: BUFFERING
	Server: RAW "e. Nulla
	facilisi.
	"
	Server: BUFFERING
	Server: FLUSHING "425a6839314159265359ba83a48c000014d580001040050405
	2fa7fe003000ba"
	Server: FLUSHING "9112793d4ca789068698a0d1a341901a0d53f4d1119a8d4c9e
	812d755a67c107"
	Server: FLUSHING "98387682c7ca7b5a3bb75da77755eb81c1cb1ca94c4b6faf20
	9c52a90aaa4d16"
	Server: FLUSHING "a4a1b9c167a01c8d9ef32589d831e77df7a5753a398b11660e
	392126fc18a72a"
	Server: FLUSHING "1088716cc8dedda5d489da410748531278043d70a8a131c2b8
	adcd6a221bdb8c"
	Server: FLUSHING "7ff76b88c1d5342ee48a70a12175074918"
	Client: READ "425a6839314159265359ba83a48c000014d5800010400504052fa7
	fe003000ba"
	Client: BUFFERING
	Client: READ "9112793d4ca789068698a0d1a341901a0d53f4d1119a8d4c9e812d
	755a67c107"
	Client: BUFFERING
	Client: READ "98387682c7ca7b5a3bb75da77755eb81c1cb1ca94c4b6faf209c52
	a90aaa4d16"
	Client: BUFFERING
	Client: READ "a4a1b9c167a01c8d9ef32589d831e77df7a5753a398b11660e3921
	26fc18a72a"
	Client: BUFFERING
	Client: READ "1088716cc8dedda5d489da410748531278043d70a8a131c2b8adcd
	6a221bdb8c"
	Client: BUFFERING
	Client: READ "7ff76b88c1d5342ee48a70a12175074918"
	Client: DECOMPRESSED "Lorem ipsum dolor sit amet, consectetuer adipi
	scing elit. Donec
	egestas, enim et consectetuer ullamcorper, lectus ligula rutrum leo,
	a elementum elit tortor eu quam. Duis tincidunt nisi ut ante. Nulla
	facilisi.
	"
	Client: response matches file contents: True

.. {{{end}}}
