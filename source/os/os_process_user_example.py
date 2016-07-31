#!/usr/bin/env python
"""Using the os module to find information about the user running the current process.
"""
#end_pymotw_header

import os

TEST_GID=501
TEST_UID=527

def show_user_info():
    print 'User (actual/effective)  : %d / %d' % \
        (os.getuid(), os.geteuid())
    print 'Group (actual/effective) : %d / %d' % \
        (os.getgid(), os.getegid())
    print 'Actual Groups   :', os.getgroups()
    return

print 'BEFORE CHANGE:'
show_user_info()
print

try:
    os.setegid(TEST_GID)
except OSError:
    print 'ERROR: Could not change effective group.  Rerun as root.'
else:
    print 'CHANGED GROUP:'
    show_user_info()
    print

try:
    os.seteuid(TEST_UID)
except OSError:
    print 'ERROR: Could not change effective user.  Rerun as root.'
else:
    print 'CHANGE USER:'
    show_user_info()
    print
