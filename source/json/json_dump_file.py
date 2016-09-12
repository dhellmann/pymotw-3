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

data = [ { 'a':'A', 'b':(2, 4), 'c':3.0 } ]

f = StringIO()
json.dump(data, f)

print f.getvalue()

