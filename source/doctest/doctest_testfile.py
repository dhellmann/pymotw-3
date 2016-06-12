#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Run the tests from an external file.
"""
#end_pymotw_header

import doctest

if __name__ == '__main__':
    doctest.testfile('doctest_in_help.rst')
    
