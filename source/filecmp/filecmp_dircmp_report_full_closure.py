#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""
#end_pymotw_header

import filecmp

comparison = filecmp.dircmp('example/dir1', 'example/dir2')
comparison.report_full_closure()
