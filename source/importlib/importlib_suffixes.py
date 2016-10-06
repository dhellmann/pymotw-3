#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

#end_pymotw_header

import importlib.machinery

SUFFIXES = [
    ('Source:', importlib.machinery.SOURCE_SUFFIXES),
    ('Debug bytecode:',
     importlib.machinery.DEBUG_BYTECODE_SUFFIXES),
    ('Optimized bytecode:',
     importlib.machinery.OPTIMIZED_BYTECODE_SUFFIXES),
    ('Bytecode:', importlib.machinery.BYTECODE_SUFFIXES),
    ('Extension:', importlib.machinery.EXTENSION_SUFFIXES),
]


def main():
    tmpl = '{:<20}  {}'
    for name, value in SUFFIXES:
        print(tmpl.format(name, value))

if __name__ == '__main__':
    main()
