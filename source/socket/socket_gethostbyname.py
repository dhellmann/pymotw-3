#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Convert hostname to IP address.
"""
#end_pymotw_header

import socket

HOSTS = [
    'pymotw.org',
    'www',
    'www.python.org',
    'nosuchname',
]

for host in HOSTS:
    try:
        print('%s : %s' % (host, socket.gethostbyname(host)))
    except socket.error as msg:
        print('%s : %s' % (host, msg))
