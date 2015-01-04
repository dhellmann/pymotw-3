#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2009 Doug Hellmann All rights reserved.
#
"""
"""
#end_pymotw_header

import sys

class ExpressionCounter(object):

    def __init__(self):
        self.count = 0
        self.previous_value = self

    def __call__(self, value):
        print
        print '  Previous:', self.previous_value
        print '  New     :', value
        print
        if value != self.previous_value:
            self.count += 1
            sys.ps1 = '(%3d)> ' % self.count
        self.previous_value = value
        sys.__displayhook__(value)

print 'installing'
sys.displayhook = ExpressionCounter()
