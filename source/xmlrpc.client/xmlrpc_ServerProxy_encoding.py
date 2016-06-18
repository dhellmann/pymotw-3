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
                               encoding='ISO-8859-1')
print 'Ping:', server.ping()
