#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2009 Doug Hellmann All rights reserved.
#
"""
"""
#end_pymotw_header

import csv
import sys

csv.register_dialect('escaped',
                     escapechar='\\',
                     doublequote=False,
                     quoting=csv.QUOTE_NONE,
                     )
csv.register_dialect('singlequote',
                     quotechar="'",
                     quoting=csv.QUOTE_ALL,
                     )

quoting_modes = dict( (getattr(csv,n), n)
                      for n in dir(csv)
                      if n.startswith('QUOTE_')
                      )

for name in sorted(csv.list_dialects()):
    print 'Dialect: "%s"\n' % name
    dialect = csv.get_dialect(name)

    print '  delimiter   = %-6r    skipinitialspace = %r' % (
        dialect.delimiter, dialect.skipinitialspace)
    print '  doublequote = %-6r    quoting          = %s' % (
        dialect.doublequote, quoting_modes[dialect.quoting])
    print '  quotechar   = %-6r    lineterminator   = %r' % (
        dialect.quotechar, dialect.lineterminator)
    print '  escapechar  = %-6r' % dialect.escapechar
    print
    
    writer = csv.writer(sys.stdout, dialect=dialect)
    writer.writerow(
        ('col1', 1, '10/01/2010',
         'Special chars: " \' %s to parse' % dialect.delimiter)
        )
    print

