#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2009 Doug Hellmann All rights reserved.
#
"""
"""

#end_pymotw_header

import tarfile

for filename in [ 'README.txt', 'example.tar', 
                  'bad_example.tar', 'notthere.tar' ]:
    try:
        print '%15s  %s' % (filename, tarfile.is_tarfile(filename))
    except IOError, err:
        print '%15s  %s' % (filename, err)
