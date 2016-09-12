#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2009 Doug Hellmann All rights reserved.
#
"""
"""
#end_pymotw_header

import json
from StringIO import StringIO

f = StringIO('[{"a": "A", "c": 3.0, "b": [2, 4]}]')
print json.load(f)
