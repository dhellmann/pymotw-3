#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

#__version__ = "$Id$"
#end_pymotw_header
import bz2
import logging
import SocketServer
import binascii

BLOCK_SIZE = 32

class Bz2RequestHandler(SocketServer.BaseRequestHandler):

    logger = logging.getLogger('Server')
    
    def handle(self):
        compressor = bz2.BZ2Compressor()
        
        # Find out what file the client wants
        filename = self.request.recv(1024)
        self.logger.debug('client asked for: "%s"', filename)
        
        # Send chunks of the file as they are compressed
        with open(filename, 'rb') as input:
            while True:            
                block = input.read(BLOCK_SIZE)
                if not block:
                    break
                self.logger.debug('RAW "%s"', block)
                compressed = compressor.compress(block)
                if compressed:
                    self.logger.debug('SENDING "%s"',
                                      binascii.hexlify(compressed))
                    self.request.send(compressed)
                else:
                    self.logger.debug('BUFFERING')
        
        # Send any data being buffered by the compressor
        remaining = compressor.flush()
        while remaining:
            to_send = remaining[:BLOCK_SIZE]
            remaining = remaining[BLOCK_SIZE:]
            self.logger.debug('FLUSHING "%s"',
                              binascii.hexlify(to_send))
            self.request.send(to_send)
        return


if __name__ == '__main__':
    import socket
    import sys
    from cStringIO import StringIO
    import threading

    logging.basicConfig(level=logging.DEBUG,
                        format='%(name)s: %(message)s',
                        )

    # Set up a server, running in a separate thread
    address = ('localhost', 0) # let the kernel assign a port
    server = SocketServer.TCPServer(address, Bz2RequestHandler)
    ip, port = server.server_address # what port was assigned?

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)
    t.start()

    logger = logging.getLogger('Client')

    # Connect to the server
    logger.info('Contacting server on %s:%s', ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    # Ask for a file
    requested_file = (sys.argv[0]
                      if len(sys.argv) > 1
                      else 'lorem.txt')
    logger.debug('sending filename: "%s"', requested_file)
    len_sent = s.send(requested_file)

    # Receive a response
    buffer = StringIO()
    decompressor = bz2.BZ2Decompressor()
    while True:
        response = s.recv(BLOCK_SIZE)
        if not response:
            break
        logger.debug('READ "%s"', binascii.hexlify(response))

        # Include any unconsumed data when feeding the decompressor.
        decompressed = decompressor.decompress(response)
        if decompressed:
            logger.debug('DECOMPRESSED "%s"', decompressed)
            buffer.write(decompressed)
        else:
            logger.debug('BUFFERING')

    full_response = buffer.getvalue()
    lorem = open(requested_file, 'rt').read()
    logger.debug('response matches file contents: %s',
                 full_response == lorem)

    # Clean up
    server.shutdown()
    server.socket.close()
    s.close()
