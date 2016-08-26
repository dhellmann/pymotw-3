#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Show the objects with references to a given object.
"""
#end_pymotw_header

import gc

flags = gc.DEBUG_COLLECTABLE | gc.DEBUG_UNCOLLECTABLE
gc.set_debug(flags)


class Graph:

    def __init__(self, name):
        self.name = name
        self.next = None
        print('Creating {} 0x{:x} ({})'.format(
            self.__class__.__name__, id(self), name))

    def set_next(self, next):
        print('Linking nodes {}.next = {}'.format(self, next))
        self.next = next

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__, self.name)


class CleanupGraph(Graph):

    def __del__(self):
        print('{}.__del__()'.format(self))


# Construct a graph cycle
one = Graph('one')
two = Graph('two')
one.set_next(two)
two.set_next(one)

# Construct another node that stands on its own
three = CleanupGraph('three')

# Construct a graph cycle with a finalizer
four = CleanupGraph('four')
five = CleanupGraph('five')
four.set_next(five)
five.set_next(four)

# Remove references to the graph nodes in this module's namespace
one = two = three = four = five = None

print()

# Force a sweep
print('Collecting')
gc.collect()
print('Done')

# Reset the debug flags before exiting to avoid dumping a lot
# of extra information and making the example output more
# confusing.
gc.set_debug(0)
