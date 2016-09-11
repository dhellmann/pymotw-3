#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id$"
#end_pymotw_header

import subprocess

print 'popen4:'
proc = subprocess.Popen('cat -; echo "to stderr" 1>&2',
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        )
msg = 'through stdin to stdout\n'
stdout_value, stderr_value = proc.communicate(msg)
print '\tcombined output:', repr(stdout_value)
print '\tstderr value   :', repr(stderr_value)
