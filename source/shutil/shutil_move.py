#!/usr/bin/env python3
"""Copying a file
"""
#end_pymotw_header

from shutil import *
from glob import glob

with open('example.txt', 'wt') as f:
    f.write('contents')

print('BEFORE: ', glob('example*'))
move('example.txt', 'example.out')
print('AFTER : ', glob('example*'))
