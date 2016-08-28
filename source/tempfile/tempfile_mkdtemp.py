#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id$"
#end_pymotw_header

import os
import tempfile

directory_name = tempfile.mkdtemp()
print directory_name
# Clean up the directory
os.removedirs(directory_name)
