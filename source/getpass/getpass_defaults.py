#!/usr/bin/env python
"""Default use of getpass.
"""
#end_pymotw_header

import getpass

try:
    p = getpass.getpass()
except Exception, err:
    print 'ERROR:', err
else:
    print 'You entered:', p
