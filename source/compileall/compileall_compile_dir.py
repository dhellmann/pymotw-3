#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2009 Doug Hellmann All rights reserved.
#
"""
"""

#end_pymotw_header
import compileall
import glob

print('Before:', glob.glob('examples/__pycache__/*'))
print()

compileall.compile_dir('examples')

print('\nAfter:', glob.glob('examples/__pycache__/*'))
