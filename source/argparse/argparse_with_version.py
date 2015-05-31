#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""
"""
#end_pymotw_header

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-a', action="store_true", default=False)
parser.add_argument('-b', action="store", dest="b")
parser.add_argument('-c', action="store", dest="c", type=int)
parser.add_argument('--version', '-v',
                    action='version',
                    version='%(prog)s 1.0')

print(parser.parse_args())

print('This is not printed')
