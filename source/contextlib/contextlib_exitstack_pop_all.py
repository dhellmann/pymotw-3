#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2015 Doug Hellmann.  All rights reserved.
"""
"""
#end_pymotw_header
import contextlib


class Tracker:
    "Base class for noisy context managers."

    def __init__(self, i):
        self.i = i

    def msg(self, s):
        print('  %s(%s): %s' %
              (self.__class__.__name__, self.i, s))

    def __enter__(self):
        self.msg('entering')


class HandleError(Tracker):
    "If an exception is received, treat it as handled."

    def __exit__(self, *exc_details):
        received_exc = exc_details[1] is not None
        if received_exc:
            self.msg('handling exception %r' % exc_details[1])
        self.msg('exiting %s' % received_exc)
        # Return Boolean value indicating whether the exception
        # was handled.
        return received_exc


class PassError(Tracker):
    "If an exception is received, propagate it."

    def __exit__(self, *exc_details):
        received_exc = exc_details[1] is not None
        if received_exc:
            self.msg('passing exception %r' % exc_details[1])
        self.msg('exiting')
        # Return False, indicating any exception was not handled.
        return False


class ErrorOnEnter(Tracker):
    "Cause an exception."

    def __enter__(self):
        self.msg('throwing error on enter')
        raise RuntimeError('from %s' % self.i)

    def __exit__(self, *exc_info):
        self.msg('exiting')


def variable_stack(contexts):
    with contextlib.ExitStack() as stack:
        for c in contexts:
            stack.enter_context(c)
        # Return the close() method of a new stack as a clean-up
        # function.
        return stack.pop_all().close
    # Explicitly return None, indicating that the ExitStack could
    # not be initialized cleanly but that cleanup has already
    # occurred.
    return None


print('No errors:')
cleaner = variable_stack([
    HandleError(1),
    HandleError(2),
])
cleaner()

print('\nHandled error building context manager stack:')
try:
    cleaner = variable_stack([
        HandleError(1),
        ErrorOnEnter(2),
    ])
except RuntimeError as err:
    print('caught error %s' % err)
else:
    if cleaner is not None:
        cleaner()
    else:
        print('no cleaner returned')

print('\nUnhandled error building context manager stack:')
try:
    cleaner = variable_stack([
        PassError(1),
        ErrorOnEnter(2),
    ])
except RuntimeError as err:
    print('caught error %s' % err)
else:
    if cleaner is not None:
        cleaner()
    else:
        print('no cleaner returned')
