#!/usr/bin/env python3
"""Inspecting the call stack.
"""
#end_pymotw_header

import inspect


def show_stack():
    for level in inspect.stack():
        (frame, filename, line_num,
         func, src_code, src_index) = level
        print('{}[{}]\n  -> {}'.format(
            filename,
            line_num,
            src_code[src_index].strip(),
        ))
        print(inspect.getargvalues(frame))
        print()


def recurse(limit):
    local_variable = '.' * limit
    if limit <= 0:
        show_stack()
        return
    recurse(limit - 1)
    return local_variable

if __name__ == '__main__':
    recurse(2)
