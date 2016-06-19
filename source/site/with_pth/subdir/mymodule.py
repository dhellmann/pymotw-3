#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Empty module for example.
"""
#end_pymotw_header

import os
print 'Loaded', __name__, 'from', __file__[len(os.getcwd())+1:]
