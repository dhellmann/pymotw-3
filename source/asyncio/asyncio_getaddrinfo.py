#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Scheduling a callback with call_later
"""
#end_pymotw_header

import asyncio
import functools
import logging
import socket
import sys


event_loop = asyncio.get_event_loop()

names = [
    'pymotw.com',
    'doughellmann.com',
    'python.org',
]

try:
    for name in names:
        info = event_loop.run_until_complete(
            event_loop.getaddrinfo(
                name, 443,
                proto=socket.IPPROTO_TCP,
            )
        )

        for host in info:
            print('{:20}: {}'.format(name, host[4][0]))
finally:
    event_loop.close()
