#!/usr/bin/env python3
# encoding: utf-8

import sys


def trace_calls(frame, event, arg):
    if event != 'call':
        return
    co = frame.f_code
    func_name = co.co_name
    if func_name == 'write':
        # Ignore write() calls from printing
        return
    func_line_no = frame.f_lineno
    func_filename = co.co_filename
    caller = frame.f_back
    caller_line_no = caller.f_lineno
    caller_filename = caller.f_code.co_filename
    print('* Call to', func_name)
    print('*  on line %s of %s' %
          (func_line_no, func_filename))
    print('*  from line %s of %s' %
          (caller_line_no, caller_filename))
    return


def b():
    print('inside b()\n')


def a():
    print('inside a()\n')
    b()

sys.settrace(trace_calls)
a()
