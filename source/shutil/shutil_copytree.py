#!/usr/bin/env python3
"""Copying an entire tree of files.
"""
#end_pymotw_header

from shutil import *
from commands import *

print('BEFORE:')
print(getoutput('ls -rlast /tmp/example'))
copytree('../shutil', '/tmp/example')
print('\nAFTER:')
print(getoutput('ls -rlast /tmp/example'))
