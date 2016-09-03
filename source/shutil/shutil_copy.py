#!/usr/bin/env python3
"""Copying a file
"""
#end_pymotw_header

from shutil import *
import os

os.mkdir('example')
print('BEFORE:', os.listdir('example'))
copy('shutil_copy.py', 'example')
print('AFTER:', os.listdir('example'))
