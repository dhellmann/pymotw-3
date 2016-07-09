#!/usr/bin/env python
"""Using optparse with single-letter options.
"""
#end_pymotw_header

import getopt

opts, args = getopt.getopt(['-a', '-bval', '-c', 'val'], 'ab:c:')

for opt in opts:
    print opt
    
