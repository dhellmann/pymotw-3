#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""
#end_pymotw_header

import xmlrpclib

server = xmlrpclib.ServerProxy('http://localhost:9000',
                               allow_none=True)
print 'Allowed:', server.show_type(None)

server = xmlrpclib.ServerProxy('http://localhost:9000',
                               allow_none=False)
try:
    server.show_type(None)
except TypeError as err:
    print 'ERROR:', err
    
