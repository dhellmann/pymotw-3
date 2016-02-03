#!/usr/bin/env python3
# encoding: utf-8
"""
"""
#end_pymotw_header

import enum


class BugStatus(enum.Enum):

    new = 1
    incomplete = 2
    invalid = 3
    wont_fix = 4
    in_progress = 5
    fix_committed = 6
    fix_released = 7


print('\nMember name: {}'.format(BugStatus.wont_fix.name))
print('Member value: {}'.format(BugStatus.wont_fix.value))
