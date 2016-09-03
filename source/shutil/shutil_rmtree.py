#!/usr/bin/env python3
"""Remove an entire tree of files.
"""
#end_pymotw_header

from shutil import *
from commands import *

print('BEFORE:')
print(getoutput('ls -rlast /tmp/example'))
rmtree('/tmp/example')
print('AFTER:')
print(getoutput('ls -rlast /tmp/example'))
