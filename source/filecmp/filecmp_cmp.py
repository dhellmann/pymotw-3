#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Compare two files.
"""

__version__ = "$Id$"
#end_pymotw_header

import filecmp

print 'common_file:', 
print filecmp.cmp('example/dir1/common_file', 
                  'example/dir2/common_file'),
print filecmp.cmp('example/dir1/common_file', 
                  'example/dir2/common_file',
                  shallow=False)

print 'not_the_same:', 
print filecmp.cmp('example/dir1/not_the_same', 
                  'example/dir2/not_the_same'),
print filecmp.cmp('example/dir1/not_the_same', 
                  'example/dir2/not_the_same',
                  shallow=False)

print 'identical:',
print filecmp.cmp('example/dir1/file_only_in_dir1', 
                  'example/dir1/file_only_in_dir1'),
print filecmp.cmp('example/dir1/file_only_in_dir1', 
                  'example/dir1/file_only_in_dir1',
                  shallow=False)

