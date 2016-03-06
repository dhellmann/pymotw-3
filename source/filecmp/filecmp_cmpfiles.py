#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Compare files in two directories.
"""

__version__ = "$Id$"
#end_pymotw_header

import filecmp
import os

# Determine the items that exist in both directories
d1_contents = set(os.listdir('example/dir1'))
d2_contents = set(os.listdir('example/dir2'))
common = list(d1_contents & d2_contents)
common_files = [ f 
                 for f in common 
                 if os.path.isfile(os.path.join('example/dir1', f))
                 ]
print 'Common files:', common_files

# Compare the directories
match, mismatch, errors = filecmp.cmpfiles('example/dir1', 
                                           'example/dir2', 
                                           common_files)
print 'Match   :', match
print 'Mismatch:', mismatch
print 'Errors  :', errors
