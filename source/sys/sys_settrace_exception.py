#!/usr/bin/env python
# encoding: utf-8

import sys

def trace_exceptions(frame, event, arg):
    if event != 'exception':
        return
    co = frame.f_code
    func_name = co.co_name
    line_no = frame.f_lineno
    filename = co.co_filename
    exc_type, exc_value, exc_traceback = arg
    print 'Tracing exception:\n%s "%s"\non line %s of %s\n' % \
        (exc_type.__name__, exc_value, line_no, func_name)

def trace_calls(frame, event, arg):
    if event != 'call':
        return
    co = frame.f_code
    func_name = co.co_name
    if func_name in TRACE_INTO:
        return trace_exceptions

def c():
    raise RuntimeError('generating exception in c()')

def b():
    c()
    print 'Leaving b()'

def a():
    b()
    print 'Leaving a()'
    
TRACE_INTO = ['a', 'b', 'c']

sys.settrace(trace_calls)
try:
    a()
except Exception, e:
    print 'Exception handler:', e
