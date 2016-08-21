#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Examine the objects being managed.
"""
#end_pymotw_header

import gc

print len(gc.get_objects())
