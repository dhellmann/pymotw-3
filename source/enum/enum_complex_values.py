#!/usr/bin/env python3
# encoding: utf-8
"""
"""
#end_pymotw_header

import enum


class BugStatus(enum.Enum):

    new = {
        'value': 7,
        'transitions': ['incomplete',
                        'invalid',
                        'wont_fix',
                        'in_progress',
                        ],
    }
    incomplete = {
        'value': 6,
        'transitions': ['new', 'wont_fix'],
    }
    invalid = {
        'value': 5,
        'transitions': ['new'],
    }
    wont_fix = {
        'value': 4,
        'transitions': ['new'],
    }
    in_progress = {
        'value': 3,
        'transitions': ['new', 'fix_committed'],
    }
    fix_committed = {
        'value': 2,
        'transitions': ['in_progress', 'fix_released'],
    }
    fix_released = {
        'value': 1,
        'transitions': ['new'],
    }

    def __init__(self, vals):
        self.num = vals['value']
        self.transitions = vals['transitions']

    def can_transition(self, new_state):
        return new_state.name in self.transitions


print('Name:', BugStatus.in_progress)
print('Value:', BugStatus.in_progress.value)
print('Custom attribute:', BugStatus.in_progress.transitions)
print('Using attribute:',
      BugStatus.in_progress.can_transition(BugStatus.new))
