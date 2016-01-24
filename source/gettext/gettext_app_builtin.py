#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2009 Doug Hellmann All rights reserved.
#
"""
"""
#end_pymotw_header

import gettext
gettext.install('gettext_example', 'locale',
                unicode=True, names=['ngettext'])

print _('This message is in the script.')
