#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2009 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id$"
#end_pymotw_header

import compileall
import re

compileall.compile_dir('examples', 
    rx=re.compile(r'/subdir'))
