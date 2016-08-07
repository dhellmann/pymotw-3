#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id$"
#end_pymotw_header

import string

values = { 'var':'foo' }

t = string.Template("""
Variable        : $var
Escape          : $$
Variable in text: ${var}iable
""")

print 'TEMPLATE:', t.substitute(values)

s = """
Variable        : %(var)s
Escape          : %%
Variable in text: %(var)siable
"""

print 'INTERPOLATION:', s % values
