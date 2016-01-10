#!/usr/bin/env python3
#
# Copyright 2007 Doug Hellmann.
#

"""Using the junk filter feature.
"""
#end_pymotw_header

# This example is adapted from the source for difflib.py.

from difflib import SequenceMatcher


def show_results(s):
    i, j, k = s.find_longest_match(0, 5, 0, 9)
    print('  i = {}'.format(i))
    print('  j = {}'.format(j))
    print('  k = {}'.format(k))
    print('  A[i:i+k] = {!r}'.format(A[i:i + k]))
    print('  B[j:j+k] = {!r}'.format(B[j:j + k]))

A = " abcd"
B = "abcd abcd"

print('A = {!r}'.format(A))
print('B = {!r}'.format(B))

print('\nWithout junk detection:')
show_results(SequenceMatcher(None, A, B))

print('\nTreat spaces as junk:')
show_results(SequenceMatcher(lambda x: x == " ", A, B))
