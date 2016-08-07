Compressing Network Data
========================
 
The server in the next listing uses the stream compressor to respond
to requests consisting of filenames by writing a compressed version of
the file to the socket used to communicate with the client.  It has
some artificial chunking in place to illustrate the buffering that
occurs when the data passed to :func:`compress()` or
:func:`decompress()` does not result in a complete block of compressed
or uncompressed output.

.. literalinclude:: zlib_server.py
   :lines: 11-72
 
It has some artificial chunking in place to illustrate the buffering
behavior that happens when the data passed to :func:`compress()` or
:func:`decompress()` does not result in a complete block of compressed
or uncompressed output.

.. literalinclude:: zlib_server.py
   :lines: 74-

The client connects to the socket and requests a file.  Then it loops,
receiving blocks of compressed data.  Since a block may not contain
enough information to decompress it entirely, the remainder of any
data received earlier is combined with the new data and passed to the
decompressor.  As the data is decompressed, it is appended to a
buffer, which is compared against the file contents at the end of the
processing loop.

.. warning::

    This server has obvious security implications.  Do not run it on a
    system on the open Internet or in any environment where security
    might be an issue.
 
.. {{{cog
.. cog.out(run_script(cog.inFile, 'zlib_server.py', break_lines_at=69))
.. }}}

::

    $ python zlib_server.py
    
    Client: Contacting server on 127.0.0.1:55085
    Client: sending filename: "lorem.txt"
    Server: client asked for: "lorem.txt"
    Server: RAW "Lorem ipsum dolor sit amet, consectetuer adipiscing elit
    . Donec
    "
    Server: SENDING "7801"
    Server: RAW "egestas, enim et consectetuer ullamcorper, lectus ligula
     rutrum "
    Server: BUFFERING
    Server: RAW "leo, a
    elementum elit tortor eu quam. Duis tincidunt nisi ut ant"
    Server: BUFFERING
    Server: RAW "e. Nulla
    facilisi. Sed tristique eros eu libero. Pellentesque ve"
    Server: BUFFERING
    Server: RAW "l arcu. Vivamus
    purus orci, iaculis ac, suscipit sit amet, pulvi"
    Server: BUFFERING
    Server: RAW "nar eu,
    lacus.
    "
    Server: BUFFERING
    Server: FLUSHING "55904b6ac4400c44f73e451da0f129b20c2110c85e696b8c40d
    dedd167ce1f7915025a087daa9ef4be8c07e4f21c38962e834b800647435fd3b90747
    b2810eb9"
    Server: FLUSHING "c4bbcc13ac123bded6e4bef1c91ee40d3c6580e3ff52aad2e8c
    b2eb6062dad74a89ca904cbb0f2545e0db4b1f2e01955b8c511cb2ac08967d228af14
    47c8ec72"
    Server: FLUSHING "e40c4c714116e60cdef171bb6c0feaa255dff1c507c2c4439ec
    9605b7e0ba9fc54bae39355cb89fd6ebe5841d673c7b7bc68a46f575a312eebd220d4
    b32441bd"
    Server: FLUSHING "c1b36ebf0aedef3d57ea4b26dd986dd39af57dfb05d32279de"
    Client: READ "780155904b6ac4400c44f73e451da0f129b20c2110c85e696b8c40d
    dedd167ce1f7915025a087daa9ef4be8c07e4f21c38962e834b800647435fd3b90747
    b281"
    Client: DECOMPRESSED "Lorem ipsum dolor sit amet, consectetuer "
    Client: READ "0eb9c4bbcc13ac123bded6e4bef1c91ee40d3c6580e3ff52aad2e8c
    b2eb6062dad74a89ca904cbb0f2545e0db4b1f2e01955b8c511cb2ac08967d228af14
    47c8"
    Client: DECOMPRESSED "adipiscing elit. Donec
    egestas, enim et consectetuer ullamcorper, lectus ligula rutrum leo, 
    a
    elementum elit tortor eu quam. Duis ti"
    Client: READ "ec72e40c4c714116e60cdef171bb6c0feaa255dff1c507c2c4439ec
    9605b7e0ba9fc54bae39355cb89fd6ebe5841d673c7b7bc68a46f575a312eebd220d4
    b324"
    Client: DECOMPRESSED "ncidunt nisi ut ante. Nulla
    facilisi. Sed tristique eros eu libero. Pellentesque vel arcu. Vivamu
    s
    purus orci, iacu"
    Client: READ "41bdc1b36ebf0aedef3d57ea4b26dd986dd39af57dfb05d32279de"
    Client: DECOMPRESSED "lis ac, suscipit sit amet, pulvinar eu,
    lacus.
    "
    Client: response matches file contents: True

.. {{{end}}}
