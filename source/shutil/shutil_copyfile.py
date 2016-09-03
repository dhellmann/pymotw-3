#!/usr/bin/env python3
"""Copying a file
"""
#end_pymotw_header

from shutil import *
from glob import glob

print('BEFORE:', glob('shutil_copyfile.*'))
copyfile('shutil_copyfile.py', 'shutil_copyfile.py.copy')
print('AFTER:', glob('shutil_copyfile.*'))
