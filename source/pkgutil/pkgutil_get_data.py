#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Load package data
"""
#end_pymotw_header

import pkgutil

template = pkgutil.get_data('pkgwithdata', 'templates/base.html')
print template.encode('utf-8')
