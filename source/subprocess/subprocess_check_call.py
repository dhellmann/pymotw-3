#!/usr/bin/env python
#
# Copyright 2010 Doug Hellmann.
#
"""Checking exit codes from external processes
"""
#end_pymotw_header

import subprocess

try:
    subprocess.check_call(['false'])
except subprocess.CalledProcessError as err:
    print 'ERROR:', err
