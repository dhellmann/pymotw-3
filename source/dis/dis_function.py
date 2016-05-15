#!/usr/bin/env python
# encoding: utf-8

def f(*args):
    nargs = len(args)
    print nargs, args

if __name__ == '__main__':
    import dis
    dis.dis(f)
