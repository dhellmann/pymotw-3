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

targets = [
    ('66.33.211.242', 443),
    ('104.130.43.121', 443),
]

try:
    for target in targets:
        info = event_loop.run_until_complete(
            event_loop.getnameinfo(target)
        )

        print('{:15}: {} {}'.format(target[0], *info))
finally:
    event_loop.close()
