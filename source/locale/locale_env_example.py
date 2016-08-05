#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Example setting the locale using environment variable(s).
"""
#end_pymotw_header

import locale
import os
import pprint
import codecs
import sys

sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)

# Default settings based on the user's environment.
locale.setlocale(locale.LC_ALL, '')

print 'Environment settings:'
for env_name in [ 'LC_ALL', 'LC_CTYPE', 'LANG', 'LANGUAGE' ]:
    print '\t%s = %s' % (env_name, os.environ.get(env_name, ''))

# What is the locale?
print
print 'Locale from environment:', locale.getlocale()

template = """
Numeric formatting:

  Decimal point      : "%(decimal_point)s"
  Grouping positions : %(grouping)s
  Thousands separator: "%(thousands_sep)s"

Monetary formatting:

  International currency symbol             : "%(int_curr_symbol)r"
  Local currency symbol                     : %(currency_symbol)r
    Unicode version                           %(currency_symbol_u)s
  Symbol precedes positive value            : %(p_cs_precedes)s
  Symbol precedes negative value            : %(n_cs_precedes)s
  Decimal point                             : "%(mon_decimal_point)s"
  Digits in fractional values               : %(frac_digits)s
  Digits in fractional values, international: %(int_frac_digits)s
  Grouping positions                        : %(mon_grouping)s
  Thousands separator                       : "%(mon_thousands_sep)s"
  Positive sign                             : "%(positive_sign)s"
  Positive sign position                    : %(p_sign_posn)s
  Negative sign                             : "%(negative_sign)s"
  Negative sign position                    : %(n_sign_posn)s

"""

sign_positions = {
    0 : 'Surrounded by parentheses',
    1 : 'Before value and symbol',
    2 : 'After value and symbol',
    3 : 'Before value',
    4 : 'After value',
    locale.CHAR_MAX : 'Unspecified',
    }

info = {}
info.update(locale.localeconv())
info['p_sign_posn'] = sign_positions[info['p_sign_posn']]
info['n_sign_posn'] = sign_positions[info['n_sign_posn']]
# convert the currency symbol to unicode
info['currency_symbol_u'] = info['currency_symbol'].decode('utf-8')

print (template % info)
