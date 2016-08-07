#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id$"
#end_pymotw_header

import gzip

with gzip.open('example.txt.gz', 'rb') as input_file:
    print 'Entire file:'
    all_data = input_file.read()
    print all_data
    
    expected = all_data[5:15]
    
    # rewind to beginning
    input_file.seek(0)
    
    # move ahead 5 bytes
    input_file.seek(5)
    print 'Starting at position 5 for 10 bytes:'
    partial = input_file.read(10)
    print partial
    
    print
    print expected == partial
