#!/usr/bin/env python
# encoding: utf-8

import sys

def trace_calls_and_returns(frame, event, arg):
    co = frame.f_code
    func_name = co.co_name
    if func_name == 'write':
        # Ignore write() calls from print statements
        return
    line_no = frame.f_lineno
    filename = co.co_filename
    if event == 'call':
        print 'Call to %s on line %s of %s' % (func_name,
                                               line_no,
                                               filename)
        return trace_calls_and_returns
    elif event == 'return':
        print '%s => %s' % (func_name, arg)
    return

def b():
    print 'in b()'
    return 'response_from_b '

def a():
    print 'in a()'
    val = b()
    return val * 2

sys.settrace(trace_calls_and_returns)
a()
