#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2009 Doug Hellmann All rights reserved.
#
"""
"""
#end_pymotw_header

import decimal
import pprint

context = decimal.getcontext()

print 'Emax     =', context.Emax
print 'Emin     =', context.Emin
print 'capitals =', context.capitals
print 'prec     =', context.prec
print 'rounding =', context.rounding
print 'flags    ='
pprint.pprint(context.flags)
print 'traps    ='
pprint.pprint(context.traps)
