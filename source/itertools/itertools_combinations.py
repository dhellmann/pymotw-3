#!/usr/bin/env python3
# encoding: utf-8
#end_pymotw_header

from itertools import *


def show(iterable, n):
    for i, item in enumerate(iterable, 1):
        print(''.join(item), end=' ')
        if (i % n) == 0:
            print()
    print()

print('Unique pairs:\n')
show(combinations('abcd', r=2), 3)
