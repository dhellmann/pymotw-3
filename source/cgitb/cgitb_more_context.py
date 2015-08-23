#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2009 Doug Hellmann.  All rights reserved.
#
"""Control the amount of context by passing a number as arg on command line
"""
#end_pymotw_header

import cgitb
import sys

context_length = int(sys.argv[1])
cgitb.enable(format='text', context=context_length)

def func2(a, divisor):
    return a / divisor

def func1(a, b):
    c = b - 5
    # Really
    # long
    # comment
    # goes
    # here.
    return func2(a, c)

func1(1, 5)
