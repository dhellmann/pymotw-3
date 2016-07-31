#!/usr/bin/env python3
"""Show stat info for a file.
"""
#end_pymotw_header

import os
import sys
import time

if len(sys.argv) == 1:
    filename = __file__
else:
    filename = sys.argv[1]

stat_info = os.stat(filename)

print('os.stat({}):'.format(filename))
print('\tSize:', stat_info.st_size)
print('\tPermissions:', oct(stat_info.st_mode))
print('\tOwner:', stat_info.st_uid)
print('\tDevice:', stat_info.st_dev)
print('\tCreated      :', time.ctime(stat_info.st_ctime))
print('\tLast modified:', time.ctime(stat_info.st_mtime))
print('\tLast accessed:', time.ctime(stat_info.st_atime))
