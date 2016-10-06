#!/usr/bin/env python
# encoding: utf-8
"""
"""
#end_pymotw_header

import imp

f, filename, description = imp.find_module('example')
try:
    example_package = imp.load_module('example', f,
                                      filename, description)
    print 'Package:', example_package
finally:
    if f:
        f.close()

f, filename, description = imp.find_module(
    'submodule', example_package.__path__)
try:
    submodule = imp.load_module('example.submodule', f,
                                filename, description)
    print 'Submodule:', submodule
finally:
    if f:
        f.close()
