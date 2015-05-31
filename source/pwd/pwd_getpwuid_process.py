#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2009 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id$"
#end_pymotw_header

import pwd
import os

uid = os.getuid()
user_info = pwd.getpwuid(uid)
print('Currently running with UID=%s username=%s' %
      (uid, user_info.pw_name))
