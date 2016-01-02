#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Converting hostnames to IP addresses
"""
#end_pymotw_header

import asyncio
import functools
import logging
import socket
import sys


targets = [
    ('pymotw.com', 'https'),
    ('doughellmann.com', 'https'),
    ('python.org', 'https'),
]

event_loop = asyncio.get_event_loop()
try:
    for target in targets:
        info = event_loop.run_until_complete(
            event_loop.getaddrinfo(
                *target,
                proto=socket.IPPROTO_TCP,
            )
        )

        for host in info:
            print('{:20}: {}'.format(target[0], host[4][0]))
finally:
    event_loop.close()
