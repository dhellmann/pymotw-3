#!/usr/bin/env python
#
# Copyright 2007 Doug Hellmann.
#
"""Context diff example
"""

__version__ = "$Id$"
#end_pymotw_header

import difflib
from difflib_data import *

diff = difflib.context_diff(text1_lines, text2_lines, lineterm='')
print '\n'.join(list(diff))
