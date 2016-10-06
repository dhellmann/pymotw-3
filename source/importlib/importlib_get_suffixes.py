#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id$"
#end_pymotw_header

import imp

module_types = { imp.PY_SOURCE:   'source',
                 imp.PY_COMPILED: 'compiled',
                 imp.C_EXTENSION: 'extension',
                 imp.PY_RESOURCE: 'resource',
                 imp.PKG_DIRECTORY: 'package',
                 }

def main():
    fmt = '%10s %10s %10s'
    print fmt % ('Extension', 'Mode', 'Type')
    print '-' * 32
    for extension, mode, module_type in imp.get_suffixes():
        print fmt % (extension, mode, module_types[module_type])

if __name__ == '__main__':
    main()
